# Journal des Modifications (Changelog) — OpérIA

Toutes les modifications notables apportées à ce projet sont documentées dans ce fichier.
Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/), et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

---

## [1.0.0] - 2026-09-18

### Ajouté
- **Module Dashboard :** Tableau de bord unifié avec 4 indicateurs clés (Requêtes, Actions préparées, En attente, Terminées avec taux de réussite 97,2 %).
- **Module Agent Conversationnel :** Chat avec streaming SSE, cartes interactives d'exécution d'outils (`erp.factures.query`, `crm.comptes.enrich`) et widget interactif d'action sensible avec double action Valider/Refuser.
- **Module Opérations :** File de validation centralisée des actions avec filtrage par statut (*Toutes*, *En attente*, *Terminées*) et support de la validation par lot (*Valider la sélection*).
- **Module Données :** Inventaire des 5 sources connectées (CRM, Base financière, ERP, Messagerie, Référentiel) avec horodatage de synchronisation et bouton manuel d'actualisation.
- **Module Historique :** Traçabilité chronologique complète du cycle de vie opérationnel (Requête → Analyse → Action préparée → Validation → Exécution) avec moteur de recherche textuelle et filtres.
- **Module Paramètres :** Configuration des garde-fous d'actions sensibles (Envoi d'emails, Modification de données, Export clients) et gestion des connecteurs.
- **Architecture Technique :** Intégration complète du protocole MCP (Model Context Protocol) pour découpler le LLM des sources de données.
- **Double Vue Thématique :** Support du mode clair OpérIA et de la console sombre haute densité Atlas.

---

## [0.9.0] - 2026-09-01

### Ajouté
- Implémentation du protocole MCP standardisé sur transport JSON-RPC.
- Intercepteur de sécurité `StagedAction` dans FastAPI bloquant toute transmission directe.
- Intégration des tests end-to-end avec Playwright.

### Modifié
- Refonte de la barre latérale gauche avec badge numérique dynamique sur les opérations en attente.
- Amélioration de la latence des requêtes SQL sur les factures impayées (< 150 ms).

---

## [0.5.0] - 2026-08-15

### Ajouté
- Prototype initial de console d'interrogation (Atlas).
- Connecteur ERP en lecture seule pour la détection des impayés à plus de 30 jours.
- Générateur d'emails de relance niveau 1 et 2 avec mise en copie comptable.

---

## [0.1.0] - 2026-07-01

### Ajouté
- Initialisation du dépôt de code (FastAPI + Nuxt 3).
- Définition des premiers schémas Pydantic et de la politique de validation humaine (HITL).
