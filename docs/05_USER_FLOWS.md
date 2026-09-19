# Parcours Utilisateur & Diagrammes d'États (User Flows) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Cycle de Vie Global d'une Opération (State Machine)

Toute interaction opérationnelle dans OpérIA suit un cycle de vie strict et audité :

```mermaid
stateDiagram-v2
    [*] --> Requete_Initiee: Saisie utilisateur
    Requete_Initiee --> Analyse_Intention: FastAPI Orchestrator
    Analyse_Intention --> Execution_Outils_Lecture: Appel Outils MCP (Read-Only)
    Execution_Outils_Lecture --> Synthese_Affichee: Aucune action requise
    Synthese_Affichee --> [*]
    
    Execution_Outils_Lecture --> Action_Preparee: Détection action sensible
    Action_Preparee --> En_Attente_Validation: Mise en file (STAGED_ACTION)
    
    state En_Attente_Validation {
        [*] --> Notification_UI
        Notification_UI --> Examen_Detail: Clic "Examiner"
        Examen_Detail --> Decision_Humaine
    }
    
    Decision_Humaine --> Action_Validee: Clic "Valider et exécuter"
    Decision_Humaine --> Action_Refusee: Clic "Refuser"
    
    Action_Validee --> Execution_Reelle: Appel connecteur sortant (Mailer/ERP)
    Execution_Reelle --> Statut_Termine: Succès 200 OK
    Execution_Reelle --> Statut_Echec: Erreur technique
    
    Action_Refusee --> Journal_Audit: Motif enregistré
    Statut_Termine --> Journal_Audit: Preuve inaltérable
    Statut_Echec --> Journal_Audit: Alerte levée
    
    Journal_Audit --> [*]
```

---

## 2. Parcours Détaillés (User Flows)

### Parcours 1 : Interrogation Conversationnelle & Validation dans le Chat (`/agent`)

```mermaid
sequenceDiagram
    autonumber
    actor User as Opérateur (Alex)
    participant UI as Frontend Nuxt 3
    participant API as FastAPI Backend
    participant LLM as Moteur LLM (Tool-Calling)
    participant MCP as Serveur MCP Outils
    participant DB as Base de Données / CRM

    User->>UI: Saisit "Donne-moi les factures impayées > 30 jours"
    UI->>API: POST /api/v1/agent/chat/stream
    API->>LLM: Prompt enrichi avec catalogue MCP
    LLM-->>API: Tool Call: erp.factures.query(retard_jours__gt=30)
    API->>MCP: Invoque erp.factures.query
    MCP->>DB: Exécute requête SQL lecture seule
    DB-->>MCP: 23 factures trouvées (86 420 €)
    MCP-->>API: Données JSON normalisées
    API-->>UI: SSE Event: tool_call_done (erp.factures.query, 142ms, ok)
    API->>LLM: Injection des résultats de l'outil
    LLM-->>API: Synthèse textuelle + Proposition de relance
    API-->>UI: SSE Event: assistant_message_chunk
    UI->>User: Affiche le tableau synthétique des factures

    User->>UI: Saisit "Prépare une relance pour ces comptes..."
    UI->>API: POST /api/v1/agent/chat/stream
    API->>LLM: Intention: Préparation d'action
    LLM-->>API: Generate StagedAction (8 emails ciblés, 42 680 €)
    API->>API: Enregistre StagedAction #act-4821 (status: PENDING)
    API-->>UI: SSE Event: staged_action_created (#act-4821)
    UI->>User: Affiche la carte "ACTION À VALIDER" avec boutons Valider/Refuser

    User->>UI: Clic sur "Valider et exécuter"
    UI->>API: POST /api/v1/operations/act-4821/validate
    API->>MCP: Invoque mailer.send_bulk_relance(...)
    MCP-->>API: 8 emails délivrés avec succès
    API-->>UI: 200 OK (Action terminée)
    UI->>User: Notification de succès et badge "Terminé"
```

---

### Parcours 2 : Validation Groupée depuis le Centre des Opérations (`/operations`)

1. **Entrée :** L'utilisateur constate un badge dynamique sur l'onglet de navigation `Opérations [7]`.
2. **Consultation :** Il clique sur l'onglet `Opérations`. L'écran affiche la liste des 7 actions en attente avec leurs critères clés :
   - *Relance de factures échues* (8 emails · 42 680 € · Alex Martin)
   - *Export des clients actifs* (1 248 lignes CSV · Sophie Bernard)
3. **Sélection :** L'utilisateur coche les cases associées aux actions prêtes.
4. **Validation par lot :** Il clique sur le bouton primaire `Valider la sélection`.
5. **Confirmation modale :** Un dialogue de sécurité récapitule :  
   *"Vous êtes sur le point d'exécuter 2 actions sensibles. Voulez-vous continuer ?"*
6. **Exécution :** Après confirmation, les actions basculent en cours puis dans l'onglet `Terminées`. Le compteur du badge passe à `[5]`.

---

### Parcours 3 : Supervision des Sources de Données (`/data`)

```mermaid
flowchart TD
    A[Accès page /data] --> B[Affichage des 5 sources connectées]
    B --> C{Statut des sources ?}
    C -->|Toutes au vert 'Terminé'| D[Système opérationnel nominal]
    C -->|Une source 'En cours'| E[Synchronisation en arrière-plan]
    C -->|Une source 'Erreur'| F[Affichage badge rouge & log d'erreur]
    
    D --> G[Clic sur 'Actualiser']
    G --> H[FastAPI déclenche ping MCP de chaque connecteur]
    H --> I[Mise à jour horodatage 'Dernière synchronisation']
```

---

### Parcours 4 : Configuration des Garde-Fous (`/settings`)

1. L'administrateur ou DAF accède à `/settings`.
2. Le bloc **Contrôle et validations** présente 3 options critiques :
   - [x] *Envoi d'emails externes* (obligatoire par défaut)
   - [x] *Modification de données métier* (obligatoire par défaut)
   - [x] *Export de données clients* (obligatoire par défaut)
3. Si un utilisateur tente de décocher une case, un message d'alerte sécurité requiert son mot de passe et un motif d'audit.
4. Le bloc **Connexions métier** affiche l'état des connecteurs (Base financière, Messagerie) avec un bouton d'accès direct `Configurer`.
