# Déploiement & DevOps (Deployment Guide) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Topologie des Conteneurs

La solution est entièrement conteneurisée selon une architecture multi-services :

| Service | Image de Base | Rôle | Port Interne |
| :--- | :--- | :--- | :--- |
| **frontend** | `node:20-alpine` | Application Nuxt 3 (SSR/SPA) | `3000` |
| **backend** | `python:3.12-slim` | API FastAPI & Orchestrateur Agent | `8000` |
| **mcp-gateway** | `python:3.12-slim` | Serveurs MCP ERP/CRM/Messaging | `8080` |
| **postgres** | `postgres:16-alpine` | Base relationnelle & Logs d'audit | `5432` |
| **redis** | `redis:7-alpine` | Cache, sessions & files d'attente | `6379` |

---

## 2. Configuration Docker Compose (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: operia_db
      POSTGRES_USER: operia_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - operia-internal

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - operia-internal

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    restart: unless-stopped
    env_file: .env
    depends_on:
      - postgres
      - redis
    networks:
      - operia-internal
      - operia-public
    ports:
      - "8000:8000"

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    restart: unless-stopped
    environment:
      - NUXT_PUBLIC_API_BASE=http://backend:8000/api/v1
    depends_on:
      - backend
    networks:
      - operia-public
    ports:
      - "3000:3000"

networks:
  operia-internal:
    internal: true
  operia-public:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

---

## 3. Variables d'Environnement Clés (`.env.example`)

```ini
# Application
ENVIRONMENT=production
LOG_LEVEL=info
SECRET_KEY=change_me_super_secret_jwt_key_32_bytes_min

# Base de Données
DATABASE_URL=postgresql+asyncpg://operia_user:secure_pwd@postgres:5432/operia_db
REDIS_URL=redis://:secure_redis@redis:6379/0

# Moteur LLM
LLM_PROVIDER=anthropic # ou openai, google-gemini
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_API_KEY=sk-ant-api-prod-xxxxxxx

# Serveurs MCP
MCP_SERVER_ERP_URL=http://mcp-gateway:8080/erp
MCP_SERVER_CRM_URL=http://mcp-gateway:8080/crm
MCP_SERVER_MAIL_URL=http://mcp-gateway:8080/mailer

# Garde-fous HITL
REQUIRE_HITL_FOR_ALL_SENSITIVE=true
MAX_AUTO_EXPORT_ROWS=0 # 0 = tout export soumis à validation
```

---

## 4. Pipeline d'Intégration & Déploiement Continu (CI/CD)

1. **Lint & Typage :** `ruff check` + `mypy` (Backend), `eslint` + `vue-tsc` (Frontend).
2. **Tests Automatisés :** Exécution de Pytest avec base de données de test et Vitest.
3. **Scan de Vulnérabilités :** Analyse des images Docker via Trivy.
4. **Migration de Schéma :** `alembic upgrade head` exécuté en job Kubernetes avant le déploiement des nouveaux pods backend.
5. **Déploiement Zéro-Downtime :** Déploiement Rolling Update (Kubernetes) ou Blue/Green.
