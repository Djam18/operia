# Software Requirements Specification (SRS) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Norme de référence :** ISO/IEC/IEEE 29148:2018  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Introduction

### 1.1 Objet
Ce document spécifie les exigences logicielles complètes pour le système **OpérIA**. Il définit les fonctions, les contraintes opérationnelles, les interfaces externes (notamment le protocole MCP) et les exigences de performance nécessaires au déploiement de la solution en environnement d'entreprise.

### 1.2 Portée du système
OpérIA est un système d'aide à la décision et d'orchestration opérationnelle automatisée avec contrôle humain. Il est composé :
- D'un backend d'intelligence artificielle et d'orchestration développé en **Python (FastAPI)** ;
- D'un serveur d'outils standardisé via le protocole **MCP (Model Context Protocol)** ;
- D'un frontend web moderne développé avec le framework **Nuxt 3 / Vue 3**.

---

## 2. Description Générale

### 2.1 Architecture Fonctionnelle Globale
Le système s'articule autour de quatre couches interactives :
```
[ Utilisateur (Navigateur Web Nuxt 3) ]
             ▲
             │ HTTPS / SSE / WebSocket
             ▼
[ Serveur Backend FastAPI (Gateway & Orchestrateur) ]
             ▲
    ┌────────┴────────┐
    ▼                 ▼
[ Moteur LLM ]   [ Serveur MCP d'Outils ]
(Tool Calling)   (Lecture BDD, CRM, ERP, Messagerie)
                      │
                      ▼
             [ Action Staging Area ]
             (Mise en attente validation)
                      │
           [ Validation Humaine ]
                      │
                      ▼
             [ Exécution Réelle ]
```

### 2.2 Caractéristiques des Utilisateurs
- **Opérateur Métier (Financier, ADV, Commercial) :** Compétences bureautiques standards, formule des requêtes en langage naturel, responsable de la validation des actions.
- **Responsable d'équipe / Superviseur :** Contrôle des actions transverses, analyse de la performance et de la productivité.
- **Administrateur Technique / SecOps :** Gestion des connexions de données, autorisations de sécurité et supervision des logs.

---

## 3. Exigences Fonctionnelles Détaillées

### 3.1 Module 1 : Gestion des Conversations & Requêtes en Langage Naturel (REQ-NLQ)
- **REQ-NLQ-01 :** Le système doit permettre à l'utilisateur de soumettre une requête en français en langage naturel via une invite de commande interactive.
- **REQ-NLQ-02 :** Le système doit parser l'intention de l'utilisateur et déterminer s'il s'agit d'une simple interrogation de données, d'une génération de rapport ou d'une demande de préparation d'action.
- **REQ-NLQ-03 :** Le système doit maintenir le contexte de la conversation (historique des échanges, filtres précédents, entités mentionnées).
- **REQ-NLQ-04 :** L'interface doit afficher en continu l'état d'activité de l'agent ("Agent prêt", "Analyse en cours", "Outils exécutés").

### 3.2 Module 2 : Protocole MCP & Exécution des Outils (REQ-MCP)
- **REQ-MCP-01 :** Tous les connecteurs de données et de services tiers doivent implémenter la spécification standard **Model Context Protocol (MCP)**.
- **REQ-MCP-02 :** Les outils doivent être formellement typés avec des schémas JSON stricts (JSON Schema).
- **REQ-MCP-03 :** Les outils de lecture (`read-only`) doivent pouvoir s'exécuter de façon autonome par l'agent :
  - `erp.factures.query` (recherche de factures, calcul des retards) ;
  - `crm.comptes.enrich` (récupération des contacts et détails clients) ;
  - `warehouse.commandes.inspect` (analyse des stocks et commandes bloquées) ;
  - `bi.ventes.aggregate` (agrégation de marges et chiffres d'affaires).
- **REQ-MCP-04 :** L'interface doit présenter à l'opérateur une trace visuelle non bloquante des outils appelés (nom de l'outil, paramètres, temps de réponse, statut `ok` / `partial` / `error`).

### 3.3 Module 3 : Préparation et Mise en File des Actions (REQ-STG)
- **REQ-STG-01 :** Toute action ayant un effet de bord externe (écriture en base, envoi d'email, export de fichier contenant des données nominatives) doit être capturée dans un état transitoire `STAGED_ACTION` (Action préparée).
- **REQ-STG-02 :** Une action préparée doit comporter :
  - Un identifiant unique (`action_id`, ex: `act-4821`) ;
  - Une typologie (`RELANCE`, `EXPORT_CSV`, `RESUME_RAPPORT`, `UPDATE_DATA`) ;
  - Un indicateur de criticité (`SENSIBLE` vs `STANDARD`) ;
  - Un résumé explicite de la conséquence opérationnelle ;
  - La cible et le volume concerné (ex: "8 destinataires · 42 680 €") ;
  - Le contenu complet du payload (ex: corps du mail généré, critères d'export).
- **REQ-STG-03 :** Le système doit interdire toute exécution directe sans passage par cet état préparé.

### 3.4 Module 4 : Validation Humaine (Human-In-The-Loop - REQ-HITL)
- **REQ-HITL-01 :** L'interface utilisateur doit offrir deux points d'accès pour la validation :
  - Directement au sein de la conversation (Carte interactive dans le fil du chat) ;
  - Dans la vue dédiée "Opérations" regroupant toutes les actions en attente.
- **REQ-HITL-02 :** L'opérateur doit pouvoir :
  - Examiner le détail exhaustif de l'action ;
  - **Valider et exécuter** l'action ;
  - **Refuser / Annuler** l'action avec saisie optionnelle d'un motif ;
  - Valider par lot plusieurs actions sélectionnées ("Valider la sélection").
- **REQ-HITL-03 :** Une fois validée par un clic opérateur authentifié, l'action bascule à l'état `EXECUTING` puis `COMPLETED`.

### 3.5 Module 5 : Sources de Données & Synchronisation (REQ-DATA)
- **REQ-DATA-01 :** L'application doit lister l'ensemble des sources connectées avec leur typologie (CRM, Base financière, ERP, Messagerie, Référentiel).
- **REQ-DATA-02 :** Pour chaque source, le système affiche le volume d'enregistrements, la date/heure de dernière synchronisation et l'état (`Terminé`, `En cours`, `Erreur`).
- **REQ-DATA-03 :** Un bouton manuel "Actualiser" doit déclencher le rafraîchissement des métadonnées des sources.

### 3.6 Module 6 : Journalisation & Audit (REQ-AUDIT)
- **REQ-AUDIT-01 :** Chaque interaction doit être inscrite dans un journal immuable.
- **REQ-AUDIT-02 :** Chaque entrée d'audit conserve : horodatage, utilisateur authentifié, requête d'origine, outils invoqués avec leurs entrées/sorties, identifiant d'action préparée, décision humaine (nom du validateur, timestamp), statut final d'exécution.
- **REQ-AUDIT-03 :** La page "Historique" doit permettre la recherche textuelle et le filtrage par statut (`En attente`, `Terminé`, `Échec`, `Refusé`).

---

## 4. Exigences d'Interface Externe

### 4.1 Interface Utilisateur (Web GUI)
- Développée sous Nuxt 3 (SSR/SPA) avec Tailwind CSS.
- Résolution minimale supportée : 1280x800 pixels (optimisé pour affichages desktop 1920x1080 et ultra-larges).
- Deux modes visuels : Mode Métier Clair (OpérIA palette indigo `#6366F1`) et Mode Console d'Exploitation Sombre (Atlas `#0B0F17`).

### 4.2 Interfaces Logicielles (API & Protocoles)
- **FastAPI Backend :** Endpoints REST JSON pour la gestion des sessions, de l'état des actions et des paramètres.
- **Streaming SSE (`/api/v1/agent/chat/stream`) :** Transmission en flux continu des tokens générés par le LLM et des événements de cycle de vie des outils.
- **MCP Client / Server Protocol :** Communication via JSON-RPC 2.0 sur transport stdio ou HTTP/SSE selon les spécifications Anthropic/Open-Source MCP.

---

## 5. Exigences Non-Fonctionnelles

### 5.1 Sécurité (NFR-SEC)
- Authentification par jetons JWT signés asymétriquement (RS256).
- Contrôle d'accès basé sur les rôles (RBAC : Opérateur, Superviseur, Administrateur).
- Protection contre les injections de prompt : découplage strict entre les instructions système et les données non fiables renvoyées par les outils.

### 5.2 Performance & Disponibilité (NFR-PERF)
- Disponibilité opérationnelle : 99,9 % pendant les heures ouvrées (07h00 - 20h00 CET).
- Temps de traitement d'une action après validation humaine : < 1,5 seconde.
- Rendu de l'interface : First Contentful Paint < 1,2 s, Cumulative Layout Shift < 0,05.
