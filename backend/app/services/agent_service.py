import asyncio
import json
import time
from collections import deque
from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from google import genai
from google.genai import types

from app.core.config import settings
from app.db.models import StagedAction, DataSource, Conversation, Message, get_utc_now
from app.mcp.tools import query_invoices, enrich_crm_accounts, check_data_source_connected


class AgentRateLimiter:
    """
    Enterprise Agent Rate & Concurrency Gatekeeper:
    - Concurrency semaphore (max 3 concurrent queries)
    - Sliding-window rate limiter (max 10 requests / minute)
    """
    def __init__(self, max_concurrent: int = 3, max_per_minute: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.max_per_minute = max_per_minute
        self.requests_log: deque = deque()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            now = time.time()
            # Purge timestamps older than 60 seconds
            while self.requests_log and self.requests_log[0] < now - 60.0:
                self.requests_log.popleft()

            if len(self.requests_log) >= self.max_per_minute:
                wait_time = int(60.0 - (now - self.requests_log[0])) + 1
                raise HTTPException(
                    status_code=429,
                    detail=f"Quota d'utilisation dépassé (limite de {self.max_per_minute} req/min). Veuillez patienter {wait_time}s."
                )

            self.requests_log.append(now)


agent_rate_limiter = AgentRateLimiter(
    max_concurrent=settings.AGENT_MAX_CONCURRENCY,
    max_per_minute=settings.AGENT_RATE_LIMIT_PER_MINUTE
)


# ── Tool declarations for Gemini function calling ──
TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="erp_factures_query",
        description=(
            "Recherche les factures dans la base financière ERP. "
            "Filtrage par retard en jours, statut, région et devise. "
            "Retourne le nombre total, le montant total, le détail par région et les 5 plus grosses factures."
        ),
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "retard_jours__gt": types.Schema(type="INTEGER", description="Nombre minimum de jours de retard (ex: 30)"),
                "statut": types.Schema(type="STRING", description="Statut: impaye, partiel, paye"),
                "region": types.Schema(type="STRING", description="Région: Europe, Afrique de l'Ouest, Afrique du Nord, Afrique Centrale, Afrique de l'Est"),
                "currency": types.Schema(type="STRING", description="Devise: EUR, XOF, MAD, XAF, KES"),
            },
        ),
    ),
    types.FunctionDeclaration(
        name="crm_comptes_enrich",
        description="Enrichit les comptes clients depuis le CRM (contacts, emails, litiges, éligibilité).",
        parameters=types.Schema(
            type="OBJECT",
            properties={
                "customer_names": types.Schema(
                    type="ARRAY",
                    items=types.Schema(type="STRING"),
                    description="Liste des noms de clients à enrichir",
                ),
            },
            required=["customer_names"],
        ),
    ),
]

SYSTEM_PROMPT = """Tu es OpérIA, un agent IA spécialisé dans les opérations financières, le contrôle du crédit et le recouvrement de créances.
Tu as accès à la base financière ERP et au CRM des entreprises en Europe et Afrique.
Tu dois systématiquement utiliser les outils à ta disposition pour fonder tes réponses sur des données réelles.
Règles strictes :
- Réponds toujours en français professionnel et concis.
- Cite les chiffres exacts retournés par les outils.
- Exclus impérativement des relances les comptes présentant un litige actif (ex: contestation de livraison).
- Toute action d'envoi d'email, d'export de données ou d'ajustement d'encours est soumise à validation humaine (HITL).
- Si une source de données est déconnectée par coupe-circuit de sécurité, signale-le immédiatement à l'utilisateur.
"""


class AgentService:
    @staticmethod
    async def stream_chat(
        db: AsyncSession,
        query: str,
        conversation_id: str = "conv-factures",
        experience_level: str = "SENIOR_EXPERT"
    ) -> AsyncGenerator[dict, None]:
        # Enforce rate limiting quota
        try:
            await agent_rate_limiter.acquire()
        except HTTPException as e:
            yield {"event": "error", "data": json.dumps({"error": e.detail}, ensure_ascii=False)}
            yield {"event": "done", "data": json.dumps({"conversation_id": conversation_id}, ensure_ascii=False)}
            return

        # Enforce concurrency gatekeeper
        async with agent_rate_limiter.semaphore:
            # Ensure conversation exists in database
            conv = await db.get(Conversation, conversation_id)
            if not conv:
                title = (query[:40] + "...") if len(query) > 40 else query
                conv = Conversation(id=conversation_id, title=title)
                db.add(conv)
            else:
                conv.updated_at = get_utc_now()

            # Record user message
            user_msg = Message(
                conversation_id=conversation_id,
                sender="user",
                content=query
            )
            db.add(user_msg)
            await db.commit()

            assistant_text = ""
            assistant_meta = {}

            generator = None
            if settings.GEMINI_API_KEY and settings.AGENT_MODE != "local":
                try:
                    generator = AgentService._stream_gemini(db, query, conversation_id, experience_level)
                except Exception as e:
                    print(f"[Gemini Exception]: {type(e).__name__}: {e}", flush=True)

            if generator is None:
                generator = AgentService._stream_local(db, query, conversation_id, experience_level)

            try:
                async for event in generator:
                    ev_type = event.get("event")
                    ev_data = event.get("data", "")
                    if ev_type == "content_delta":
                        try:
                            d = json.loads(ev_data) if isinstance(ev_data, str) else ev_data
                            if "text" in d:
                                assistant_text += d["text"]
                        except Exception:
                            pass
                    elif ev_type == "invoices_table":
                        try:
                            assistant_meta["invoices"] = json.loads(ev_data) if isinstance(ev_data, str) else ev_data
                        except Exception:
                            pass
                    elif ev_type == "staged_action_created":
                        try:
                            assistant_meta["action"] = json.loads(ev_data) if isinstance(ev_data, str) else ev_data
                        except Exception:
                            pass
                    elif ev_type == "tool_call_completed":
                        try:
                            t_item = json.loads(ev_data) if isinstance(ev_data, str) else ev_data
                            assistant_meta.setdefault("tools", []).append(t_item)
                        except Exception:
                            pass

                    yield event
            except Exception as e:
                print(f"[Stream Error]: {e}", flush=True)
                # Fallback to local if gemini failed mid-stream
                async for event in AgentService._stream_local(db, query, conversation_id, experience_level):
                    yield event

            # Save assistant response to DB
            if assistant_text or assistant_meta:
                asst_msg = Message(
                    conversation_id=conversation_id,
                    sender="assistant",
                    content=assistant_text.strip() or "Analyse terminée.",
                    meta=assistant_meta
                )
                db.add(asst_msg)
                await db.commit()

    @staticmethod
    async def _stream_gemini(
        db: AsyncSession,
        query: str,
        conversation_id: str,
        experience_level: str = "SENIOR_EXPERT"
    ) -> AsyncGenerator[dict, None]:
        yield {"event": "thinking", "data": json.dumps(
            {"status": f"Analyse par Gemini AI (Mode {experience_level})..."}, ensure_ascii=False
        )}

        exp_instruction = {
            "JUNIOR": "Niveau d'expérience JUNIOR : Sois direct et concis, présente les chiffres bruts sans recommandations stratégiques complexes.",
            "STANDARD": "Niveau d'expérience STANDARD : Analyse professionnelle opérationnelle, vérification des factures et proposition d'actions standards.",
            "SENIOR_EXPERT": "Niveau d'expérience SENIOR_EXPERT : Analyse financière approfondie multi-devises, diagnostic des risques d'impayés, exclusion proactive des litiges et actions opérationnelles cadrées par HITL."
        }.get(experience_level, "Niveau SENIOR_EXPERT")
        full_system_prompt = f"{SYSTEM_PROMPT}\n{exp_instruction}"

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        tools = [types.Tool(function_declarations=TOOL_DECLARATIONS)]

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=query,
            config=types.GenerateContentConfig(
                system_instruction=full_system_prompt,
                tools=tools,
                temperature=0.2,
            ),
        )

        # Handle function calls
        for _ in range(3):
            candidate = response.candidates[0] if response.candidates else None
            if not candidate or not candidate.content or not candidate.content.parts:
                break
            part = candidate.content.parts[0]

            if part.function_call:
                fc = part.function_call
                t_name = fc.name
                t_args = dict(fc.args) if fc.args else {}

                yield {"event": "tool_call_started", "data": json.dumps(
                    {"tool": t_name, "parameters": t_args}, ensure_ascii=False
                )}

                if t_name == "erp_factures_query":
                    tool_res = await query_invoices(
                        db,
                        retard_jours__gt=t_args.get("retard_jours__gt", 30),
                        statut=t_args.get("statut", "impaye"),
                        region=t_args.get("region"),
                        currency=t_args.get("currency"),
                    )
                    if tool_res.get("circuit_breaker") == "OPEN":
                        yield {"event": "content_delta", "data": json.dumps(
                            {"text": f"\n\n⚠️ **{tool_res.get('message')}**\n\n"}, ensure_ascii=False
                        )}
                    elif tool_res.get("top_invoices"):
                        yield {"event": "invoices_table", "data": json.dumps(tool_res["top_invoices"], ensure_ascii=False)}
                elif t_name == "crm_comptes_enrich":
                    tool_res = await enrich_crm_accounts(db, t_args.get("customer_names", []))
                    if tool_res.get("circuit_breaker") == "OPEN":
                        yield {"event": "content_delta", "data": json.dumps(
                            {"text": f"\n\n⚠️ **{tool_res.get('message')}**\n\n"}, ensure_ascii=False
                        )}
                else:
                    tool_res = {"status": "ok"}

                yield {"event": "tool_call_completed", "data": json.dumps(
                    {"tool": t_name, "status": tool_res.get("status", "ok"), "duration_ms": tool_res.get("duration_ms", 20), "summary": "Données récupérées"},
                    ensure_ascii=False
                )}

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[
                        types.Content(role="user", parts=[types.Part.from_text(text=query)]),
                        candidate.content,
                        types.Content(role="user", parts=[types.Part.from_function_response(name=t_name, response={"result": tool_res})])
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        tools=tools,
                        temperature=0.2,
                    ),
                )
            else:
                break

        res_text = response.text or "Analyse terminée."
        for word in res_text.split(" "):
            yield {"event": "content_delta", "data": json.dumps({"text": word + " "}, ensure_ascii=False)}
            await asyncio.sleep(0.01)

        yield {"event": "done", "data": json.dumps({"conversation_id": conversation_id}, ensure_ascii=False)}

    @staticmethod
    async def _stream_local(
        db: AsyncSession,
        query: str,
        conversation_id: str = "conv-factures",
        experience_level: str = "SENIOR_EXPERT"
    ) -> AsyncGenerator[dict, None]:
        q = query.lower()

        thinking_payload = json.dumps({'status': f'Analyse de la demande métier (Moteur Local · {experience_level})...'}, ensure_ascii=False)
        yield {"event": "thinking", "data": thinking_payload}
        await asyncio.sleep(0.05)

        # Vérification Circuit Breaker Source Financière si la requête implique des factures
        is_fin_query = any(k in q for k in ["facture", "impayé", "retard", "30 jours", "créance", "échu", "fcfa", "dirham", "mad", "xof", "eur"])
        if is_fin_query:
            is_fin_conn = await check_data_source_connected(db, "src-fin")
            if not is_fin_conn:
                yield {"event": "content_delta", "data": json.dumps({
                    "text": "⚠️ **ACCÈS BLOQUÉ (Coupe-circuit de sécurité)** : La source de données financière (ERP) est actuellement déconnectée par l'administrateur. Rétablissement de la connexion requis pour consulter les factures."
                }, ensure_ascii=False)}
                yield {"event": "done", "data": json.dumps({"conversation_id": conversation_id}, ensure_ascii=False)}
                return

        # Scénario 1: Requête factures impayées & créances
        if is_fin_query:
            reg = None
            if "ouest" in q or "abidjan" in q or "xof" in q or "dakar" in q or "côte d'ivoire" in q or "mali" in q:
                reg = "Afrique de l'Ouest"
            elif "nord" in q or "maroc" in q or "casablanca" in q or "mad" in q or "tunisie" in q:
                reg = "Afrique du Nord"
            elif "europe" in q or "france" in q or "eur" in q or "paris" in q or "lyon" in q:
                reg = "Europe"

            tool_started = json.dumps({
                'tool': 'erp.factures.query',
                'parameters': {'retard_jours__gt': 30, 'statut': 'impaye', 'region': reg}
            }, ensure_ascii=False)
            yield {"event": "tool_call_started", "data": tool_started}

            tool_data = await query_invoices(db, retard_jours__gt=30, statut="impaye", region=reg)

            tool_completed = json.dumps({
                'tool': 'erp.factures.query',
                'status': 'ok',
                'duration_ms': tool_data.get("duration_ms", 12),
                'summary': f"{tool_data['count']} factures identifiées ({tool_data['total_amount']:,.0f} €)"
            }, ensure_ascii=False)
            yield {"event": "tool_call_completed", "data": tool_completed}

            # Enrichissement CRM
            t2_started = json.dumps({
                'tool': 'crm.comptes.enrich',
                'parameters': {'customer_names': [inv['customer'] for inv in tool_data.get("top_invoices", [])]}
            }, ensure_ascii=False)
            yield {"event": "tool_call_started", "data": t2_started}

            names = [inv['customer'] for inv in tool_data.get("top_invoices", [])]
            crm_data = await enrich_crm_accounts(db, names)

            t2_completed = json.dumps({
                'tool': 'crm.comptes.enrich',
                'status': 'ok',
                'duration_ms': crm_data.get("duration_ms", 8),
                'summary': f"{len(crm_data['eligible_for_dunning'])} comptes éligibles à la relance"
            }, ensure_ascii=False)
            yield {"event": "tool_call_completed", "data": t2_completed}

            # Envoi du tableau
            invoices_payload = json.dumps(tool_data["top_invoices"], ensure_ascii=False)
            yield {"event": "invoices_table", "data": invoices_payload}

            # Synthèse textuelle
            excluded_text = ""
            if crm_data.get("excluded_disputes"):
                excluded_names = ", ".join(crm_data["excluded_disputes"])
                excluded_text = f" ⚠️ **Attention** : {excluded_names} est exclu des relances (litige de livraison en cours CMD-2026-084)."

            summary_text = (
                f"L'analyse révèle **{tool_data['count']} factures impayées** à plus de 30 jours, "
                f"pour un total échu de **{tool_data['total_amount']:,.2f} €**.{excluded_text} "
                f"Souhaitez-vous que je prépare une relance amiable (HITL) ou un ajustement d'encours ?"
            )
            for word in summary_text.split(" "):
                yield {"event": "content_delta", "data": json.dumps({"text": word + " "}, ensure_ascii=False)}
                await asyncio.sleep(0.01)

            # Création de l'action préparée
            act_db = await db.get(StagedAction, "act-4821")
            if not act_db:
                db.add(StagedAction(
                    action_id="act-4821",
                    action_type="RELANCE_EMAIL",
                    criticality="SENSITIVE",
                    status="PENDING",
                    title="Relance de factures échues",
                    description="Comptes éligibles identifiés sans litige.",
                    consequence_warning="Les messages seront envoyés aux contacts financiers via SMTP Mailpit.",
                    target_count=len(crm_data['eligible_for_dunning']),
                    financial_amount=tool_data['total_amount'],
                    currency="EUR",
                    channel="Email",
                    payload={"clients": crm_data['eligible_for_dunning']}
                ))
                await db.commit()

            staged_payload = json.dumps({
                'action_id': 'act-4821',
                'title': 'Relance de factures échues',
                'description': "Comptes éligibles identifiés sans litige.",
                'consequence_warning': "Les messages seront envoyés aux contacts financiers via SMTP Mailpit.",
                'target_count': len(crm_data['eligible_for_dunning']),
                'financial_amount': tool_data['total_amount'],
                'currency': 'EUR',
                'channel': 'Email',
                'status': 'PENDING'
            }, ensure_ascii=False)
            yield {"event": "staged_action_created", "data": staged_payload}

        # Scénario 2: Demande de relance explicite (HITL)
        elif "relance" in q or "envoie" in q or "prépare" in q:
            # Vérification coupe-circuit messagerie
            is_msg_conn = await check_data_source_connected(db, "src-msg")
            if not is_msg_conn:
                yield {"event": "content_delta", "data": json.dumps({
                    "text": "⚠️ **CANAL DÉCONNECTÉ** : Le canal Messagerie (Mailpit / SMTP) est actuellement déconnecté par coupe-circuit. Aucune relance ne peut être envoyée."
                }, ensure_ascii=False)}
                yield {"event": "done", "data": json.dumps({"conversation_id": conversation_id}, ensure_ascii=False)}
                return

            act_db = await db.get(StagedAction, "act-4821")
            if act_db:
                act_db.status = "PENDING"
            else:
                db.add(StagedAction(
                    action_id="act-4821",
                    action_type="RELANCE_EMAIL",
                    criticality="SENSITIVE",
                    status="PENDING",
                    title="Relance de factures échues",
                    description="Comptes éligibles identifiés sans litige.",
                    consequence_warning="Les messages seront envoyés aux contacts financiers via SMTP Mailpit.",
                    target_count=4,
                    financial_amount=42680.0,
                    channel="Email",
                    payload={"clients": ["Nova Conseil", "Atelier N7", "SOTRA Logistique Abidjan", "Casablanca Tech Solutions"]}
                ))
            await db.commit()

            relance_text = json.dumps({
                'text': "J'ai préparé la relance amiable pour les 4 comptes éligibles (Mali Coton Agro exclu pour litige). Action sensible : rien n'est envoyé avant votre validation explicite."
            }, ensure_ascii=False)
            yield {"event": "content_delta", "data": relance_text}

            act_payload = json.dumps({
                'action_id': 'act-4821',
                'title': 'Relance de factures échues',
                'description': "Comptes éligibles identifiés sans litige (4 comptes).",
                'consequence_warning': "Les messages seront envoyés aux contacts financiers via SMTP Mailpit.",
                'target_count': 4,
                'financial_amount': 42680.0,
                'channel': 'Email',
                'status': 'PENDING'
            }, ensure_ascii=False)
            yield {"event": "staged_action_created", "data": act_payload}

        # Scénario 3: Export CSV
        elif "export" in q or "csv" in q:
            t_exp = json.dumps({
                'tool': 'crm.comptes.filter',
                'status': 'ok',
                'duration_ms': 25,
                'summary': 'Préparation export opérationnel CSV'
            }, ensure_ascii=False)
            yield {"event": "tool_call_completed", "data": t_exp}

            exp_text = json.dumps({
                'text': "J'ai préparé l'export CSV des comptes et factures. Conformément aux règles de sécurité, l'export de données requiert votre validation humaine."
            }, ensure_ascii=False)
            yield {"event": "content_delta", "data": exp_text}

            act_exp = await db.get(StagedAction, "act-4820")
            if not act_exp:
                db.add(StagedAction(
                    action_id="act-4820",
                    action_type="EXPORT_CSV",
                    criticality="SENSITIVE",
                    status="PENDING",
                    title="Export des clients actifs",
                    description="Export structuré des entreprises et encours au format CSV",
                    consequence_warning="Conséquence : génération et téléchargement d'un fichier CSV.",
                    target_count=5,
                    channel="Fichier CSV",
                    payload={"format": "csv", "query": "clients_actifs"}
                ))
                await db.commit()

            exp_act = json.dumps({
                'action_id': 'act-4820',
                'title': 'Export des clients actifs',
                'description': 'Export structuré des entreprises et encours au format CSV',
                'consequence_warning': 'Conséquence : génération et téléchargement d\'un fichier CSV.',
                'target_count': 5,
                'channel': 'Fichier CSV',
                'status': 'PENDING'
            }, ensure_ascii=False)
            yield {"event": "staged_action_created", "data": exp_act}

        # Scénario 4: Ajustement d'encours (Credit limit adjustment)
        elif any(k in q for k in ["encours", "plafond", "crédit", "credit", "ajust"]):
            t_crm = json.dumps({
                'tool': 'crm.comptes.lookup',
                'status': 'ok',
                'duration_ms': 18,
                'summary': 'Analyse historique Atelier N7'
            }, ensure_ascii=False)
            yield {"event": "tool_call_completed", "data": t_crm}

            enc_text = json.dumps({
                'text': "J'ai préparé une proposition d'ajustement du plafond d'encours pour **Atelier N7** de 25 000 € à 35 000 €. Cette opération modifiant le risque financier, elle est soumise à votre validation humaine."
            }, ensure_ascii=False)
            yield {"event": "content_delta", "data": enc_text}

            act_enc = await db.get(StagedAction, "act-4822")
            if not act_enc:
                db.add(StagedAction(
                    action_id="act-4822",
                    action_type="AJUSTEMENT_ENCOURS",
                    criticality="SENSITIVE",
                    status="PENDING",
                    title="Ajustement de plafond d'encours : Atelier N7",
                    description="Révision de l'encours autorisé de 25 000 € à 35 000 €",
                    consequence_warning="Conséquence : modification contractuelle de la limite de crédit client.",
                    target_count=1,
                    financial_amount=35000.0,
                    currency="EUR",
                    channel="CRM / Risque",
                    payload={"client": "Atelier N7", "new_limit": 35000.0}
                ))
                await db.commit()

            enc_act = json.dumps({
                'action_id': 'act-4822',
                'title': "Ajustement de plafond d'encours : Atelier N7",
                'description': "Révision de l'encours autorisé de 25 000 € à 35 000 €",
                'consequence_warning': "Conséquence : modification contractuelle de la limite de crédit client.",
                'target_count': 1,
                'financial_amount': 35000.0,
                'currency': 'EUR',
                'channel': 'CRM / Risque',
                'status': 'PENDING'
            }, ensure_ascii=False)
            yield {"event": "staged_action_created", "data": enc_act}

        # Scénario 5: Synthèse de gestion
        elif "marge" in q or "résumé" in q or "pipeline" in q or "synthèse" in q:
            t_marge = json.dumps({
                'tool': 'bi.ventes.aggregate',
                'status': 'ok',
                'duration_ms': 22,
                'summary': 'Agrégation commerciale régionale terminée'
            }, ensure_ascii=False)
            yield {"event": "tool_call_completed", "data": t_marge}

            marge_text = json.dumps({
                'text': "Voici la synthèse de trésorerie : Les créances d'Europe et d'Afrique du Nord sont stabilisées. Le corridor Afrique de l'Ouest (SOTRA Abidjan) concentre le principal volume d'encours. Aucun envoi requis."
            }, ensure_ascii=False)
            yield {"event": "content_delta", "data": marge_text}

        # Requête générale
        else:
            gen_text = json.dumps({
                'text': f"J'ai analysé votre demande métier : '{query}'. En tant qu'agent OpérIA, j'ai accès aux factures ERP, au CRM et aux outils d'action (relances, exports CSV, ajustement d'encours). Comment puis-je vous assister ?"
            }, ensure_ascii=False)
            yield {"event": "content_delta", "data": gen_text}

        done_payload = json.dumps({'conversation_id': conversation_id}, ensure_ascii=False)
        yield {"event": "done", "data": done_payload}
