# Glossaire Métier & Technique (Glossary) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

| Terme Français | Équivalent Anglais | Définition Métier / Technique dans OpérIA |
| :--- | :--- | :--- |
| **Agent Outillé** | *Tool-Calling Agent* | Agent logiciel basé sur un grand modèle de langage (LLM) capable de sélectionner et d'appeler des fonctions informatiques externes typées pour accomplir des tâches. |
| **Model Context Protocol (MCP)** | *Model Context Protocol (MCP)* | Protocole ouvert standardisant la manière dont les applications fournissent du contexte et des outils aux modèles de langage en toute sécurité. |
| **Validation Humaine Systématique (HITL)** | *Human-in-the-Loop (HITL)* | Principe architectural imposant qu'aucune action ayant un impact réel (envoi de mail, écriture en base, export) ne soit déclenchée sans l'approbation d'un utilisateur humain. |
| **Action Préparée** | *Staged Action* | Objet intermédiaire généré par l'agent regroupant l'ensemble des paramètres, cibles et brouillons d'une opération, en attente de validation humaine. |
| **Mode Contrôlé** | *Controlled Mode* | État opérationnel garanti d'OpérIA dans lequel les garde-fous de sécurité sont actifs et verrouillent toute velléité d'exécution autonome. |
| **Action Sensible** | *Sensitive Action* | Opération comportant un caractère irréversible ou impactant des tiers (envoi d'email externe, modification comptable, export de données personnelles). |
| **Facture Échue / Impayée** | *Overdue / Outstanding Invoice* | Créance client dont la date d'échéance de règlement est dépassée selon les règles comptables (notamment le palier critique > 30 jours). |
| **Relance Client** | *Dunning / Payment Reminder* | Message formel expédié à un contact payeur l'invitant à solder une facture impayée, souvent avec copie à l'équipe comptabilité. |
| **Contexte de Travail** | *Workspace Context* | Panneau latéral informant l'opérateur des sources actives connectées, du périmètre géographique et de la fraîcheur des données. |
| **Périmètre de Données** | *Data Scope* | Ensemble des tables et connecteurs accessibles en lecture seule à l'agent pour une session donnée. |
| **Journal d'Audit Immuable** | *Immutable Audit Trail* | Enregistrement chronologique inaltérable de chaque requête, appel d'outil, proposition d'action et validation humaine. |
| **Streaming SSE** | *Server-Sent Events (SSE)* | Protocole web unidirectionnel permettant au serveur FastAPI de pousser des tokens et des statuts d'outils en temps réel vers Nuxt 3. |
| **Double Habilitation** | *Four-Eyes Principle / Dual Control* | Règle de gouvernance imposant qu'une action dépassant un certain seuil financier (> 50 000 €) soit approuvée par un responsable hiérarchique. |
