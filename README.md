# OpérIA — Agent IA d'Opérations Métier

> **Stack :** Python 3.12 · FastAPI · MCP (Model Context Protocol) · Vue 3 / Nuxt · TypeScript · Tailwind CSS · SQLite / PostgreSQL

OpérIA est un agent outillé (*tool-calling agent*) capable d’interroger des données métier volumineuses en langage naturel et de préparer des actions complexes (relances financières, exports qualifiés, résumés stratégiques), avec **validation humaine systématique (Human-In-The-Loop — HITL)** avant toute action sensible.

---

## 🌍 Contexte Multi-Régions & International (Afrique & Europe)

OpérIA a été conçu pour opérer dans des contextes d'entreprises panafricaines et internationales :
- **Afrique de l'Ouest (UEMOA / CEDEAO) :** Hubs d'Abidjan, Dakar, Bamako (Devise : FCFA / XOF) — *Ex: SOTRA Logistique, Cacao Ivoire Export, Sahel Telecom*.
- **Afrique du Nord (Maghreb) :** Casablanca, Tanger, Tunis (Devise : MAD / Dirham, TND) — *Ex: Casablanca Tech Solutions, Tanger Med Logistique*.
- **Afrique Centrale (CEMAC) :** Douala, Libreville (Devise : FCFA / XAF) — *Ex: Douala Shipping Agency*.
- **Afrique de l'Est & Anglophone :** Nairobi, Lagos (Devise : KES, NGN, USD) — *Ex: Nairobi Mobile Pay*.
- **Europe / International :** Paris, Lyon, Bruxelles (Devise : EUR) — *Ex: Nova Conseil, Atelier N7, Groupe Atlas*.

---

## ⚡ Solution de Performance : Zéro Traitement Lourd Inutile

Charger des dizaines de milliers de lignes brutes dans le contexte d'un LLM ou en mémoire Python est une mauvaise pratique (lenteur, saturation mémoire, coûts excessifs).

**L'architecture OpérIA résout ce problème par :**
1. **Pushdown SQL direct au niveau de la base :**
   - Index composites b-tree sur `(status, days_overdue)`, `(region, currency)` et `(customer_id)`.
   - Les requêtes et agrégations statistiques sur **plus de 12 500 factures** s'exécutent en **moins de 15 millisecondes** !
2. **Synthèse statistique de haut niveau pour l'agent :**
   - L'outil MCP calcule les montants agrégés par devise et isole les 5 créances les plus critiques.
   - L'agent reçoit un JSON compact et formule une réponse instantanée et claire sans latence.

---

## 🛠️ Architecture Seamless Dual-Mode (Local & En Ligne)

1. **Mode Local / Hors-ligne (par défaut) :**
   - Fonctionne à 100 % hors-ligne avec la base SQLite embarquée et le moteur agentique réactif déterministe.
   - Zéro dépendance à internet, idéal pour les démonstrations immédiates.
2. **Mode En Ligne (Cloud Ready) :**
   - En renseignant `GEMINI_API_KEY` ou `RESEND_API_KEY` dans `backend/.env`, l'agent bascule automatiquement sur les modèles cloud et l'envoi d'emails réels aux clients.
   - En cas de perte de réseau ou dépassement de quota, le système bascule sur le mode local sans planter.

---

## 🚀 Démarrage Rapide

### 1. Démarrer le Backend (FastAPI)
```bash
cd backend
# Activer l'environnement virtuel existant
source .venv/bin/activate
# Lancer le serveur API sur le port 8000
uvicorn app.main:app --reload --port 8000
```
- API Docs Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)
- Santé API : [http://localhost:8000/health](http://localhost:8000/health)

### 2. Démarrer le Frontend (Vite / TypeScript)
```bash
cd frontend
# Lancer le serveur de développement sur le port 3000
npx vite --port 3000
```
- Interface OpérIA : [http://localhost:3000/](http://localhost:3000/)
- Console Sombre Atlas : [http://localhost:3000/console](http://localhost:3000/console)

---

## 🧪 Exécution des Tests

## 🧪 Exécution des Tests

### 1. Tests Backend (Pytest) : 13/13 Réussis
```bash
cd backend
source .venv/bin/activate
# Tests API + Évaluation IA (Zéro-hallucination, HITL, Latence)
pytest -v
```
- `tests/test_api.py` (8 tests) : santé, sources, listing, validation HITL, refus, validation en lot, streaming SSE.
- `tests/test_agent_evals.py` (5 tests) : sélection d'outils, zéro-hallucination sur chiffres réels, garde-fou HITL obligatoire, résistance aux injections, SLA latence < 250ms sur 12 500+ lignes.

### 2. Tests Frontend Unitaires & Composants (Vitest + TypeScript)
```bash
cd frontend
npx vitest run
```
*Vérifie le store réactif Pinia, le composant de garde-fou `StagedActionCard` et les traces d'outils `ToolExecutionBadge`.*

### 3. Contrôle Strict TypeScript
```bash
cd frontend
npx vue-tsc --noEmit
```

### 4. Tests E2E Complets (Playwright)
```bash
cd frontend
npx playwright test
```
*Utilise directement le navigateur Google Chrome système global (`/usr/bin/google-chrome`), sans aucun téléchargement supplémentaire, et orchestre automatiquement Backend FastAPI et Frontend Vite.*

---

## 📁 Structure du Projet

```
ai agent/
├── backend/
│   ├── app/
│   │   ├── api/endpoints.py          # Routes REST et streaming SSE
│   │   ├── core/config.py            # Configuration et détection de mode
│   │   ├── db/
│   │   │   ├── database.py           # Moteur async SQLAlchemy
│   │   │   ├── models.py             # Modèles SQL avec indexations performantes
│   │   │   └── seed.py               # Générateur de 12 500+ factures Afrique & Europe
│   │   ├── mcp/tools.py              # Outils MCP optimisés (<15ms)
│   │   └── services/
│   │       ├── agent_service.py      # Moteur d'orchestration de l'agent
│   │       └── operations_service.py # Service de validation et audit HITL
│   ├── tests/test_api.py             # Suite de tests Pytest (8 tests)
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── types/index.ts            # Interfaces TypeScript strictes
│   │   ├── stores/agent.ts           # Store Pinia typé
│   │   ├── router/index.ts           # Vue Router typé
│   │   ├── components/               # Composants UI (ActionCard, ToolBadge, Sidebar)
│   │   └── views/                    # 6 vues opérationnelles + Console Atlas
│   ├── tests/                        # Tests Vitest & Playwright
│   ├── package.json
│   └── tsconfig.json
├── docs/                             # Documentation complète (PRD, SRS, Sécurité, etc.)
└── docker-compose.yml
```
