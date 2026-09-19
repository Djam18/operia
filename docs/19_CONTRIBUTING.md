# Guide de Contribution (Contributing Guidelines) — OpérIA

Bienvenue dans le guide de contribution du projet **OpérIA**. Ce document détaille les standards de développement, les processus de revue et les exigences de sécurité requises pour toute contribution.

---

## 1. Principes Directeurs

1. **La sécurité prime sur la rapidité :** Tout code introduisant un appel d'outil modifiant sans passage par l'objet `StagedAction` sera systématiquement rejeté lors de la revue.
2. **Typage strict obligatoire :** Aucun `Any` non justifié en Python (FastAPI/Pydantic) ou TypeScript (Nuxt 3/Vue).
3. **Tests automatisés systématiques :** Chaque nouvelle fonctionnalité doit comporter ses tests unitaires et, le cas échéant, son scénario d'évaluation LLM ou test Playwright.

---

## 2. Configuration de l'Environnement Local

### Prérequis
- Python 3.12+ avec `uv` ou `poetry`
- Node.js 20+ avec `pnpm`
- Docker et Docker Compose
- Serveur PostgreSQL 16 local ou via conteneur

### Installation pas à pas

```bash
# 1. Cloner le dépôt
git clone git@github.com:operia/operia-core.git
cd operia-core

# 2. Démarrer les services d'infrastructure (Postgres, Redis)
docker compose up -d postgres redis

# 3. Backend FastAPI
cd backend
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# 4. Frontend Nuxt 3 (dans un autre terminal)
cd ../frontend
pnpm install
pnpm dev
```

---

## 3. Normes de Code & Outillage

- **Backend Python :**
  - Formateur & Linter : `ruff check .` et `ruff format .`
  - Analyseur de types : `mypy --strict app`
  - Tests : `pytest tests/`
- **Frontend TypeScript / Vue :**
  - Linter : `pnpm lint` (ESLint + Prettier)
  - Contrôle des types Vue : `pnpm vue-tsc --noEmit`
  - Tests unitaires : `pnpm test:unit` (Vitest)
  - Tests E2E : `pnpm test:e2e` (Playwright)

---

## 4. Convention de Commits & Branches

Le projet applique rigoureusement la convention [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/) :

- `feat(agent): ajout du support multi-devises dans erp.factures.query`
- `fix(hitl): correction du blocage de double validation sur les actions expirées`
- `docs(api): mise à jour des spécifications OpenAPI pour les flux SSE`
- `test(mcp): ajout des scénarios de simulation d'indisponibilité CRM`

Format des branches :  
`feat/nom-fonctionnalite`, `fix/identifiant-anomalie`, `docs/mise-a-jour`.

---

## 5. Processus de Pull Request (PR)

1. Ouvrir une PR claire en référençant le ticket associé (Issue).
2. Vérifier que l'ensemble des pipelines CI passent au vert.
3. Obtenir l'approbation d'au moins deux relecteurs, dont un validateur sécurité (SecOps) pour toute modification touchant aux modules `auth`, `mcp` ou `operations`.
