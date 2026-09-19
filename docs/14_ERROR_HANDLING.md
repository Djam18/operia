# Gestion des Erreurs & Résilience (Error Handling) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Typologie & Taxonomie des Erreurs

Les erreurs dans OpérIA sont catégorisées selon leur domaine d'origine :

| Code Erreur | Domaine | Gravité | Comportement Système | Action Utilisateur |
| :--- | :--- | :--- | :--- | :--- |
| `ERR_MCP_UNREACHABLE` | Connecteur MCP | Haute | Bascule en mode dégradé, exclusion temporaire de la source. | Notification visuelle dans la barre de contexte. |
| `ERR_TOOL_TIMEOUT` | Exécution Outil | Moyenne | Interruption de la requête au bout de 10s, reprise avec contexte partiel. | Message dans le chat proposant de réessayer. |
| `ERR_HITL_CONCURRENCY` | Validation Action | Moyenne | Verrouillage Redlock : rejet de la seconde validation avec message d'information. | *"Cette action a déjà été validée par un autre opérateur."* |
| `ERR_DATA_OBSOLETE` | Intégrité Données | Haute | Blocage préventif de l'envoi : la facture a été soldée entre-temps. | *"Les données ont changé. L'action a été invalidée pour sécurité."* |
| `ERR_LLM_RATE_LIMIT` | Moteur IA | Moyenne | Exécution de backoff exponentiel avec gigue (jitter) jusqu'à 3 tentatives. | Bannière discrète : *"L'agent finalise sa réponse..."* |
| `ERR_AUTH_UNAUTHORIZED` | Sécurité / RBAC | Haute | Refus 403 Forbidden, journalisation d'audit immédiate. | Redirection ou refus d'action explicite. |

---

## 2. Format Standardisé des Réponses d'Erreur (RFC 7807)

Toutes les erreurs renvoyées par l'API REST FastAPI suivent le format Problem Details :

```json
{
  "type": "https://operia.corp/errors/ERR_DATA_OBSOLETE",
  "title": "Données métier modifiées avant validation",
  "status": 409,
  "detail": "La facture FAC-2026-184 pour Nova Conseil a été marquée comme payée il y a 3 minutes. L'action de relance a été automatiquement annulée.",
  "instance": "/api/v1/operations/act-4821/validate",
  "code": "ERR_DATA_OBSOLETE",
  "timestamp": "2026-09-18T17:05:00Z"
}
```

---

## 3. Stratégies de Reprise & Dégradation Élégante

1. **Cas du statut d'outil partiel (`partial`) :**
   - Comme illustré dans l'écran de console opérateur (`crm.comptes.enrich : partial · 210ms · 12 comptes enrichis · 1 contact manquant [Nord Logistique]`), l'agent **ne plante pas**. Il informe l'opérateur en toute transparence de l'anomalie partielle et poursuit le traitement des dossiers complets.
2. **Circuit Breaker sur les connecteurs MCP :**
   - Si un serveur MCP échoue 5 fois consécutives en moins de 60 secondes, le circuit s'ouvre (`OPEN`).
   - L'agent prévient : *"La source ERP est temporairement indisponible. Vos requêtes s'appuient sur les dernières données en cache."*
3. **Journalisation Systématique :**
   - Tout échec d'exécution d'action validée est immédiatement notifié au support et tracé en rouge dans la page `/history` (ex: *"Contacts sans activité · CRM · Liste segmentée · Échec"*).
