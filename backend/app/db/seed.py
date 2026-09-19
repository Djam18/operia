import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, insert, update
from app.db.models import Customer, Invoice, StagedAction, DataSource, AuditLog, Conversation, Message, User
from app.core.auth import hash_password

async def seed_database(db: AsyncSession):
    # 1. Check User & Base Entities Idempotency
    user_count = (await db.execute(select(func.count(User.id)))).scalar() or 0
    if user_count == 0:
        user = User(
            id="user-alex",
            email="admin@operia.io",
            hashed_password=hash_password("admin123"),
            full_name="Alex Martin",
            role="ADMIN",
            department="Direction financière internationale"
        )
        db.add(user)

        # 2. The 5 Core Enterprises (Realistic & Focused Scenarios)
        key_customers = [
            Customer(
                id="cust-1", name="Nova Conseil", contact_email="compta@novaconseil.fr", contact_name="Jean Nova",
                country="France", city="Paris", region="Europe", currency="EUR", has_dispute=False, dunning_eligible=True,
                credit_limit=100000.0, payment_terms_days=30
            ),
            Customer(
                id="cust-2", name="Atelier N7", contact_email="finance@atelier-n7.com", contact_name="Claire Monet",
                country="France", city="Lyon", region="Europe", currency="EUR", has_dispute=False, dunning_eligible=True,
                credit_limit=25000.0, payment_terms_days=30
            ),
            Customer(
                id="cust-ci-1", name="SOTRA Logistique Abidjan", contact_email="recouvrement@sotra-ci.com", contact_name="Amadou Koné",
                country="Côte d'Ivoire", city="Abidjan", region="Afrique de l'Ouest", currency="XOF", has_dispute=False, dunning_eligible=True,
                credit_limit=50000000.0, payment_terms_days=45
            ),
            Customer(
                id="cust-ma-1", name="Casablanca Tech Solutions", contact_email="finance@casatech.ma", contact_name="Mehdi Bennani",
                country="Maroc", city="Casablanca", region="Afrique du Nord", currency="MAD", has_dispute=False, dunning_eligible=True,
                credit_limit=500000.0, payment_terms_days=30
            ),
            Customer(
                id="cust-ml-1", name="Mali Coton Agro", contact_email="contact@malicoton.ml", contact_name="Ibrahim Traoré",
                country="Mali", city="Bamako", region="Afrique de l'Ouest", currency="XOF", has_dispute=True,
                dispute_reason="Contestation sur le bon de livraison CMD-2026-084", dunning_eligible=False,
                credit_limit=20000000.0, payment_terms_days=30
            ),
        ]
        for c in key_customers:
            db.add(c)

        # 3. Data Sources with Circuit Breaker (is_connected)
        sources = [
            DataSource(id="src-fin", name="Base financière (ERP)", type="Base financière", record_count=18406, last_synced_at="Il y a 2 min", status="COMPLETED", is_connected=True),
            DataSource(id="src-crm", name="Clients & Litiges (CRM)", type="CRM", record_count=5, last_synced_at="Il y a 4 min", status="COMPLETED", is_connected=True),
            DataSource(id="src-msg", name="Messagerie (Mailpit / SMTP)", type="Messagerie", record_count=12, last_synced_at="Il y a 10 min", status="COMPLETED", is_connected=True),
            DataSource(id="src-erp", name="Commandes & Livraisons", type="ERP", record_count=28, last_synced_at="Il y a 15 min", status="COMPLETED", is_connected=True),
            DataSource(id="src-ref", name="Catalogue & Référentiel", type="Référentiel", record_count=684, last_synced_at="Hier, 18:10", status="COMPLETED", is_connected=True),
        ]
        for s in sources:
            db.add(s)

        # 4. Staged Actions
        actions = [
            StagedAction(
                action_id="act-4821",
                action_type="RELANCE_EMAIL",
                criticality="SENSITIVE",
                status="PENDING",
                title="Relance de factures échues",
                description="4 emails préparés (Mali Coton Agro exclu pour litige) · 42 680 € concernés",
                consequence_warning="Conséquence : les messages seront envoyés aux contacts financiers via SMTP Mailpit.",
                target_count=4,
                financial_amount=42680.0,
                currency="EUR",
                channel="Email",
                requested_by="Alex Martin",
                payload={"clients": ["Nova Conseil", "Atelier N7", "SOTRA Logistique Abidjan", "Casablanca Tech Solutions"]}
            ),
            StagedAction(
                action_id="act-4820",
                action_type="EXPORT_CSV",
                criticality="SENSITIVE",
                status="PENDING",
                title="Export des clients actifs",
                description="Export structuré des entreprises et encours au format CSV",
                consequence_warning="Conséquence : génération et téléchargement d'un fichier CSV opérationnel.",
                target_count=5,
                financial_amount=0.0,
                channel="Fichier CSV",
                requested_by="Sophie Bernard",
                payload={"format": "csv", "query": "clients_actifs"}
            ),
            StagedAction(
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
                requested_by="Alex Martin",
                payload={"client": "Atelier N7", "new_limit": 35000.0}
            ),
            StagedAction(
                action_id="act-4819",
                action_type="REPORT",
                criticality="STANDARD",
                status="COMPLETED",
                title="Synthèse du pipeline T3",
                description="Rapport commercial · 12 pages",
                consequence_warning="Conséquence : document interne non diffusé.",
                target_count=1,
                channel="Document",
                requested_by="Agent OpérIA",
                payload={}
            ),
            StagedAction(
                action_id="act-4818",
                action_type="UPDATE_PRIORITY",
                criticality="SENSITIVE",
                status="COMPLETED",
                title="Mise à jour des priorités",
                description="17 opportunités CRM",
                consequence_warning="Conséquence : modification directe dans le CRM.",
                target_count=17,
                channel="CRM",
                requested_by="Marc Leroy",
                payload={}
            ),
            StagedAction(
                action_id="act-4817",
                action_type="RELANCE_EMAIL",
                criticality="SENSITIVE",
                status="PENDING",
                title="Relance de niveau 1 — Hub Abidjan & Dakar",
                description="4 comptes portuaires · 18 200 000 FCFA",
                consequence_warning="Conséquence : envoi d'emails aux responsables approvisionnements.",
                target_count=4,
                financial_amount=18200000.0,
                currency="XOF",
                channel="Email",
                requested_by="Alex Martin",
                payload={}
            ),
            StagedAction(
                action_id="act-4816",
                action_type="EXPORT_CSV",
                criticality="SENSITIVE",
                status="PENDING",
                title="Export factures impayées Q3",
                description="82 factures · Format Excel",
                consequence_warning="Conséquence : transmission de données comptables.",
                target_count=82,
                financial_amount=86420.0,
                channel="Excel",
                requested_by="Alex Martin",
                payload={}
            ),
            StagedAction(
                action_id="act-4815",
                action_type="RELANCE_EMAIL",
                criticality="SENSITIVE",
                status="PENDING",
                title="Avis d'échéance proactive Casablanca",
                description="15 comptes · 450 000 MAD",
                consequence_warning="Conséquence : notification par email avant date de terme.",
                target_count=15,
                financial_amount=450000.0,
                currency="MAD",
                channel="Email",
                requested_by="Sophie Bernard",
                payload={}
            ),
            StagedAction(
                action_id="act-4814",
                action_type="UPDATE_PRIORITY",
                criticality="SENSITIVE",
                status="PENDING",
                title="Ajustement des plafonds d'encours",
                description="6 comptes stratégiques",
                consequence_warning="Conséquence : révision de limite de crédit dans l'ERP.",
                target_count=6,
                channel="ERP",
                requested_by="Alex Martin",
                payload={}
            ),
            StagedAction(
                action_id="act-4813",
                action_type="EXPORT_CSV",
                criticality="SENSITIVE",
                status="PENDING",
                title="Export du référentiel tarifaire",
                description="684 références produits",
                consequence_warning="Conséquence : extraction du catalogue complet.",
                target_count=684,
                channel="Fichier CSV",
                requested_by="Marc Leroy",
                payload={}
            )
        ]
        for a in actions:
            db.add(a)

        # 5. Audit Logs
        logs = [
            AuditLog(timestamp="17 sept. · 10:14", user="Alex Martin", query="Factures > 30 jours", tool="Finance + CRM", action="Relance email", status="PENDING"),
            AuditLog(timestamp="17 sept. · 09:58", user="Sophie Bernard", query="Clients actifs T3", tool="CRM", action="Export CSV", status="PENDING"),
            AuditLog(timestamp="16 sept. · 16:42", user="Marc Leroy", query="Résumé du pipeline", tool="CRM", action="Rapport généré", status="COMPLETED"),
            AuditLog(timestamp="16 sept. · 14:20", user="Alex Martin", query="Commandes en retard", tool="ERP", action="Analyse", status="COMPLETED"),
            AuditLog(timestamp="15 sept. · 11:06", user="Sophie Bernard", query="Contacts sans activité", tool="CRM", action="Liste segmentée", status="FAILED"),
        ]
        for l in logs:
            db.add(l)

        # 6. Initial Conversation
        conv = Conversation(id="conv-factures", title="Factures impayées")
        db.add(conv)
        msg1 = Message(conversation_id="conv-factures", sender="user", content="Donne-moi les factures impayées depuis plus de 30 jours.")
        msg2 = Message(
            conversation_id="conv-factures",
            sender="assistant",
            content="J'ai trouvé 23 factures correspondant à ce critère dans le périmètre actif, pour un montant total de 86 420 €. Huit clients dépassent votre seuil de relance automatique.",
            meta={"action_id": "act-4821"}
        )
        db.add(msg1)
        db.add(msg2)
        await db.commit()
    else:
        # Reset test action states if needed
        await db.execute(update(StagedAction).where(StagedAction.action_id == "act-4821").values(status="PENDING"))
        await db.commit()

    # 7. Check 5-Year Historical Invoices (18,406 invoices target)
    inv_count = (await db.execute(select(func.count(Invoice.id)))).scalar() or 0
    if inv_count >= 18406:
        return

    if 0 < inv_count < 18406:
        await db.execute(delete(Invoice))
        await db.commit()

    # Base Invoices (Matching exactly the screenshots: 23 invoices = 86 420 € for the primary EUR scope)
    invoices_records = [
        {"id": "FAC-2026-184", "customer_id": "cust-1", "customer_name": "Nova Conseil", "amount": 12800.0, "currency": "EUR", "region": "Europe", "days_overdue": 47, "status": "impaye", "issue_date": "2026-07-01", "due_date": "2026-08-01"},
        {"id": "FAC-2026-207", "customer_id": "cust-2", "customer_name": "Atelier N7", "amount": 8450.0, "currency": "EUR", "region": "Europe", "days_overdue": 39, "status": "impaye", "issue_date": "2026-07-10", "due_date": "2026-08-09"},
        {"id": "FAC-2026-221", "customer_id": "cust-3", "customer_name": "Groupe Atlas", "amount": 6920.0, "currency": "EUR", "region": "Europe", "days_overdue": 34, "status": "impaye", "issue_date": "2026-07-15", "due_date": "2026-08-14"},
        {"id": "FAC-2026-112", "customer_id": "cust-4", "customer_name": "Dupont Industries", "amount": 9400.0, "currency": "EUR", "region": "Europe", "days_overdue": 42, "status": "impaye", "issue_date": "2026-07-05", "due_date": "2026-08-04"},
        {"id": "FAC-2026-115", "customer_id": "cust-4", "customer_name": "Dupont Industries", "amount": 13000.0, "currency": "EUR", "region": "Europe", "days_overdue": 31, "status": "impaye", "issue_date": "2026-07-18", "due_date": "2026-08-17"},
        {"id": "FAC-2026-150", "customer_id": "cust-5", "customer_name": "Verrerie Lacroix", "amount": 17900.0, "currency": "EUR", "region": "Europe", "days_overdue": 38, "status": "impaye", "issue_date": "2026-07-11", "due_date": "2026-08-10"},
        {"id": "FAC-2026-098", "customer_id": "cust-ml-1", "customer_name": "Mali Coton Agro", "amount": 11060.0, "currency": "EUR", "region": "Afrique de l'Ouest", "days_overdue": 52, "status": "impaye", "issue_date": "2026-06-25", "due_date": "2026-07-25"},
        {"id": "FAC-2026-240", "customer_id": "cust-ci-1", "customer_name": "SOTRA Logistique Abidjan", "amount": 1450.0, "currency": "EUR", "region": "Afrique de l'Ouest", "days_overdue": 33, "status": "impaye", "issue_date": "2026-07-16", "due_date": "2026-08-15"},
        {"id": "FAC-2026-245", "customer_id": "cust-ma-1", "customer_name": "Casablanca Tech Solutions", "amount": 2140.0, "currency": "EUR", "region": "Afrique du Nord", "days_overdue": 35, "status": "impaye", "issue_date": "2026-07-14", "due_date": "2026-08-13"},
        {"id": "FAC-2026-250", "customer_id": "cust-sn-1", "customer_name": "Sahel Telecom Dakar", "amount": 3300.0, "currency": "EUR", "region": "Afrique de l'Ouest", "days_overdue": 36, "status": "impaye", "issue_date": "2026-07-13", "due_date": "2026-08-12"},
    ]
    cur_sum = sum(i["amount"] for i in invoices_records)
    rem_sum = 86420.0 - cur_sum
    per_inv = round(rem_sum / 13, 2)
    for idx in range(1, 14):
        invoices_records.append(
            {
                "id": f"FAC-2026-3{idx:02d}",
                "customer_id": "cust-1",
                "customer_name": f"Partenaire International {idx}",
                "amount": per_inv if idx < 13 else round(86420.0 - sum(i["amount"] for i in invoices_records), 2),
                "currency": "EUR",
                "region": "Europe",
                "days_overdue": 31 + (idx % 10),
                "status": "impaye",
                "issue_date": "2026-07-15",
                "due_date": "2026-08-14"
            }
        )

    # 5 full years (2021-2026) historical generation: 18,383 records + 23 baseline = 18,406
    random.seed(42)
    regions_config = [
        ("Europe", "EUR", ["Nova Conseil", "Atelier N7", "Groupe Atlas", "Dupont Industries", "Verrerie Lacroix"], 0.45),
        ("Afrique de l'Ouest", "XOF", ["SOTRA Logistique Abidjan", "Cacao Ivoire Export", "Sahel Telecom Dakar", "Dakar Port Terminal", "Mali Coton Agro"], 0.30),
        ("Afrique du Nord", "MAD", ["Casablanca Tech Solutions", "Tanger Med Logistique", "Atlas Mines & Minéraux", "Tunis Textile Export"], 0.15),
        ("Afrique Centrale", "XAF", ["Douala Shipping Agency", "Gabon Bois & Forêt"], 0.08),
        ("Afrique de l'Est", "KES", ["Nairobi Mobile Pay", "Mombasa Tea Trading"], 0.02)
    ]
    reg_weights = [r[3] for r in regions_config]
    years = [2021, 2022, 2023, 2024, 2025, 2026]
    year_weights = [0.15, 0.18, 0.20, 0.22, 0.19, 0.06]

    for i in range(1, 18384):
        reg_idx = random.choices(range(len(regions_config)), weights=reg_weights, k=1)[0]
        reg_name, curr, cust_list, _ = regions_config[reg_idx]
        cust = random.choice(cust_list)
        
        yr = random.choices(years, weights=year_weights, k=1)[0]
        if yr == 2026:
            mo = random.randint(1, 8)
            st = random.choices(["impaye", "partiel", "paye"], weights=[0.25, 0.15, 0.60], k=1)[0]
            days = random.randint(1, 95) if st != "paye" else 0
        else:
            mo = random.randint(1, 12)
            st = random.choices(["impaye", "partiel", "paye"], weights=[0.03, 0.03, 0.94], k=1)[0]
            days = random.randint(91, 180) if st != "paye" else 0

        day = random.randint(1, 28)
        issue_d = f"{yr:04d}-{mo:02d}-{day:02d}"
        due_mo = mo + 1 if mo < 12 else 1
        due_yr = yr if mo < 12 else yr + 1
        due_d = f"{due_yr:04d}-{due_mo:02d}-{day:02d}"

        if curr in ["XOF", "XAF"]:
            amt = float(random.randint(500, 25000) * 1000)
        elif curr == "MAD":
            amt = float(random.randint(5000, 350000))
        elif curr == "KES":
            amt = float(random.randint(20000, 800000))
        else:
            amt = float(random.randint(500, 45000))

        invoices_records.append({
            "id": f"FAC-HIST-{i:05d}",
            "customer_id": f"cust-{i % 20}",
            "customer_name": cust,
            "amount": amt,
            "currency": curr,
            "region": reg_name,
            "days_overdue": days,
            "status": st,
            "issue_date": issue_d,
            "due_date": due_d
        })

    # Bulk insert into SQLite via core statement (fast executemany)
    chunk_size = 2500
    for c_start in range(0, len(invoices_records), chunk_size):
        chunk = invoices_records[c_start:c_start + chunk_size]
        await db.execute(insert(Invoice).values(chunk))

    await db.commit()
