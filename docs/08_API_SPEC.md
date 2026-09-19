# Spécification des APIs & Contrats MCP (API Spec) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Spécification :** OpenAPI 3.1 & MCP Protocol v1.0  
**Protocole d'Échange :** REST / JSON & SSE (Server-Sent Events)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Endpoints de l'API Backend FastAPI

Base URL : `/api/v1`

### 1.1 Module Conversation & Agent

#### `POST /agent/chat/stream`
Initié par le frontend Nuxt pour dialoguer en langage naturel avec l'agent et recevoir les tokens ainsi que les événements d'outils en streaming.
- **En-têtes :** `Authorization: Bearer <jwt>`, `Accept: text/event-stream`
- **Request Body :**
```json
{
  "conversation_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "query": "Donne-moi les factures impayées depuis plus de 30 jours."
}
```
- **Flux SSE (Server-Sent Events) :**
```
event: thinking
data: {"status": "Analyse de la demande en cours..."}

event: tool_call_started
data: {"tool": "erp.factures.query", "parameters": {"retard_jours__gt": 30}}

event: tool_call_completed
data: {"tool": "erp.factures.query", "status": "ok", "duration_ms": 142, "summary": "12 comptes, 37 factures"}

event: content_delta
data: {"text": "J'ai trouvé 23 factures correspondant à ce critère..."}

event: staged_action_created
data: {
  "action_id": "act-4821",
  "title": "Envoyer une relance à 8 clients",
  "target_count": 8,
  "financial_amount": 42680.00,
  "channel": "Email",
  "consequence_warning": "Envoi externe irréversible : rien n'est envoyé avant votre validation explicite."
}

event: done
data: {"conversation_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d"}
```

---

### 1.2 Module Opérations & Validation Humaine (HITL)

#### `GET /operations`
Récupère la liste des actions préparées.
- **Paramètres de requête :**
  - `status` (optionnel) : `ALL` | `PENDING` | `COMPLETED` | `REFUSED`
  - `page` : default `1`
  - `limit` : default `20`
- **Réponse 200 OK :**
```json
{
  "total": 12,
  "pending_count": 7,
  "items": [
    {
      "action_id": "act-4821",
      "title": "Relance de factures échues",
      "description": "8 emails · 42 680 € concernés",
      "requested_by": "Alex Martin",
      "status": "PENDING",
      "criticality": "SENSITIVE",
      "created_at": "2026-09-18T10:14:00Z"
    },
    {
      "action_id": "act-4820",
      "title": "Export des clients actifs",
      "description": "1 248 lignes · format CSV",
      "requested_by": "Sophie Bernard",
      "status": "PENDING",
      "criticality": "SENSITIVE",
      "created_at": "2026-09-18T09:58:00Z"
    }
  ]
}
```

#### `POST /operations/{action_id}/validate`
Valide et déclenche l'exécution définitive de l'action sensible.
- **Réponse 200 OK :**
```json
{
  "action_id": "act-4821",
  "status": "COMPLETED",
  "executed_at": "2026-09-18T10:20:15Z",
  "result": {
    "sent_count": 8,
    "failed_count": 0,
    "audit_id": "8f8b89c3-7b4d-452f-859a-112233445566"
  }
}
```

#### `POST /operations/{action_id}/refuse`
Rejette l'action préparée et annule toute transmission.
- **Request Body :** `{"reason": "Client Nova Conseil a promis un virement demain."}`
- **Réponse 200 OK :** `{"action_id": "act-4821", "status": "REFUSED"}`

#### `POST /operations/batch-validate`
Valide une sélection d'actions par lot.
- **Request Body :** `{"action_ids": ["act-4821", "act-4820"]}`
- **Réponse 200 OK :** `{"validated_count": 2, "failed_ids": []}`

---

### 1.3 Module Sources de Données (`/data`)

#### `GET /data-sources`
Retourne la liste des sources connectées et leurs métriques.
- **Réponse 200 OK :**
```json
[
  {
    "id": "crm-clients",
    "name": "Clients",
    "type": "CRM",
    "record_count": 4820,
    "last_synced_at": "2026-09-18T17:00:00Z",
    "status": "COMPLETED"
  },
  {
    "id": "fin-factures",
    "name": "Factures",
    "type": "Base financière",
    "record_count": 18406,
    "last_synced_at": "2026-09-18T17:02:00Z",
    "status": "COMPLETED"
  },
  {
    "id": "erp-commandes",
    "name": "Commandes",
    "type": "ERP",
    "record_count": 32104,
    "last_synced_at": "2026-09-18T16:52:00Z",
    "status": "COMPLETED"
  },
  {
    "id": "mail-commercial",
    "name": "Messages commerciaux",
    "type": "Messagerie",
    "record_count": 7892,
    "last_synced_at": "2026-09-18T16:04:00Z",
    "status": "IN_PROGRESS"
  },
  {
    "id": "ref-produits",
    "name": "Catalogue produits",
    "type": "Référentiel",
    "record_count": 684,
    "last_synced_at": "2026-09-17T18:10:00Z",
    "status": "COMPLETED"
  }
]
```

#### `POST /data-sources/refresh`
Déclenche une actualisation manuelle des compteurs et statuts des connecteurs MCP.

---

### 1.4 Module Historique & Traçabilité (`/history`)

#### `GET /history`
- **Paramètres :** `query`, `tool`, `user`, `status`, `date_from`, `date_to`, `page`, `limit`
- **Réponse 200 OK :**
```json
{
  "total": 5,
  "items": [
    {
      "date": "17 sept. · 10:14",
      "user": "Alex Martin",
      "query": "Factures > 30 jours",
      "tool": "Finance + CRM",
      "action": "Relance email",
      "status": "PENDING"
    },
    {
      "date": "17 sept. · 09:58",
      "user": "Sophie Bernard",
      "query": "Clients actifs T3",
      "tool": "CRM",
      "action": "Export CSV",
      "status": "PENDING"
    },
    {
      "date": "16 sept. · 16:42",
      "user": "Marc Leroy",
      "query": "Résumé du pipeline",
      "tool": "CRM",
      "action": "Rapport généré",
      "status": "COMPLETED"
    },
    {
      "date": "16 sept. · 14:20",
      "user": "Alex Martin",
      "query": "Commandes en retard",
      "tool": "ERP",
      "action": "Analyse",
      "status": "COMPLETED"
    },
    {
      "date": "15 sept. · 11:06",
      "user": "Sophie Bernard",
      "query": "Contacts sans activité",
      "tool": "CRM",
      "action": "Liste segmentée",
      "status": "FAILED"
    }
  ]
}
```

---

## 2. Contrat d'Outils MCP (Model Context Protocol)

Exemple de définition d'un outil MCP exposé à l'agent :

```json
{
  "name": "erp.factures.query",
  "description": "Recherche les factures dans la base financière selon les critères de retard et de statut. Outil de lecture seule.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "retard_jours__gt": {
        "type": "integer",
        "description": "Nombre de jours d'échéance dépassés minimum (ex: 30)"
      },
      "statut": {
        "type": "string",
        "enum": ["impaye", "partiel", "paye"],
        "default": "impaye"
      }
    },
    "required": ["retard_jours__gt"]
  }
}
```
