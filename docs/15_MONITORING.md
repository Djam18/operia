# Observabilité & Métriques (Monitoring & Observability) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Stack Observabilité :** Prometheus · OpenTelemetry · Grafana · Loki  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Piliers d'Observabilité

```
        ┌──────────────────────────────────────────────┐
        │             GRAFANA DASHBOARDS               │
        └───────▲──────────────▲───────────────▲───────┘
                │              │               │
        Prometheus       OpenTelemetry       Loki
        (Métriques)        (Traces)         (Logs)
                │              │               │
       [ FastAPI App ]  [ MCP Servers ]  [ Redis/PG ]
```

---

## 2. Métriques Clés Exposées (Prometheus)

Endpoint d'export : `GET /metrics`

### 2.1 Métriques Métier & HITL
- `operia_requests_total{department}` : Compteur total de requêtes formulées (ex: 128 aujourd'hui).
- `operia_staged_actions_total{action_type}` : Nombre d'actions préparées (ex: 42 sur les 30 derniers jours).
- `operia_staged_actions_pending` : Jauge d'actions en attente de décision humaine (ex: 7).
- `operia_hitl_decisions_total{decision="approved|refused"}` : Répartition des choix humains.
- `operia_hitl_review_duration_seconds` : Histogramme du temps écoulé entre la préparation et la décision humaine.

### 2.2 Métriques Outils & Protocole MCP
- `operia_mcp_tool_calls_total{tool_name, status}` : Nombre d'appels par outil (`ok`, `partial`, `error`).
- `operia_mcp_tool_duration_seconds{tool_name}` : Durée d'exécution de chaque connecteur (P50, P95, P99).

### 2.3 Métriques LLM & Coûts
- `operia_llm_tokens_consumed_total{model, type="prompt|completion"}` : Suivi précis des volumes de jetons.
- `operia_llm_estimated_cost_euros` : Coût financier estimé par direction utilisatrice.

---

## 3. Règles d'Alerte Critiques (Alertmanager)

| Règle | Condition | Gravité | Notification |
| :--- | :--- | :--- | :--- |
| **Alerte Déconnexion MCP** | `rate(operia_mcp_tool_calls_total{status="error"}[5m]) > 0.05` | Critique | Slack #alertes-ops + PagerDuty |
| **Alerte Retard Synchronisation** | `time() - operia_data_source_last_sync_timestamp > 3600` | Avertissement | Notification DSI |
| **Alerte Accumulation Actions** | `operia_staged_actions_pending > 50` | Avertissement | Alerte managériale |
| **Alerte Tentative Injection** | `operia_security_injection_attempts_total > 0` | Immédiate | SecOps / Sécurité |

---

## 4. Tableaux de Bord Grafana Recommandés

1. **Dashboard Opérationnel :** KPIs du jour (Requêtes, taux de validation 97,2 %, file d'attente active).
2. **Dashboard Performance Technique :** Latences des outils MCP, temps de réponse SSE, santé des pods Kubernetes.
3. **Dashboard Gouvernance IA :** Consommation de tokens, audits des refus, distribution des actions par département.
