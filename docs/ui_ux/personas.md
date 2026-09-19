# Personas Utilisateurs (Personas) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Alex Martin — Direction Financière & Recouvrement

- **Rôle :** Responsable du contrôle de gestion et du recouvrement client.
- **Expérience :** 8 ans en finance d'entreprise, maîtrise approfondie de SAP et Sage.
- **Objectifs Quotidiens :**
  - Réduire le délai moyen de paiement (DSO) de l'entreprise sous la barre des 45 jours.
  - Suivre quotidiennement les factures impayées dépassant 30 jours sans passer deux heures à extraire des fichiers Excel.
  - Relancer diplomatiquement mais fermement les clients défaillants avec mise en copie du service comptable.
- **Points de Friction :**
  - Peur panique qu'un outil automatisé envoie un email d'injonction de payer à un grand compte stratégique avec lequel une négociation est en cours.
  - Lenteur des extractions ERP traditionnelles.
- **Requêtes Fréquentes dans OpérIA :**
  - *"Quels clients ont plus de 30 jours de retard de paiement, et combien cela représente ?"*
  - *"Prépare une relance pour ces comptes, avec la comptabilité en copie."*
- **Usage Clé :** Consultation du Dashboard le matin, examen du widget prioritaire *"À VALIDER"*, validation unitaire des relances dans la conversation.

---

## 2. Sophie Bernard — Responsable Relation Client & ADV

- **Rôle :** Responsable Administration des Ventes et Suivi Clientèle.
- **Expérience :** 5 ans en CRM (Salesforce / HubSpot), orientée satisfaction client.
- **Objectifs Quotidiens :**
  - Segmenter rapidement les bases de données clients pour les campagnes de réactivation commerciale.
  - Identifier les blocages logistiques impactant la livraison des commandes.
  - Obtenir des exports de données propres sans mobiliser l'équipe informatique.
- **Points de Friction :**
  - Dépendance envers le service data/BI pour générer des extractions de fichiers CSV.
  - Risque d'extraire des données obsolètes ou non conformes au RGPD.
- **Requêtes Fréquentes dans OpérIA :**
  - *"Exporte la liste des clients actifs T3 ayant passé commande récemment."*
  - *"Quelles sont les commandes en retard d'expédition ce matin ?"*
- **Usage Clé :** Utilisation fréquente de l'historique d'audit pour prouver la traçabilité des listes transmises au marketing.

---

## 3. Marc Leroy — Directeur Commercial

- **Rôle :** Membre du Comité de Direction, pilotage de l'équipe commerciale de 25 personnes.
- **Expérience :** 15 ans dans le management commercial B2B.
- **Objectifs Quotidiens :**
  - Avoir une vision consolidée de la marge par zone géographique et de l'état d'avancement du pipe de vente.
  - Rédiger des notes de synthèse claires pour le comité de direction hebdomadaire sans y passer sa soirée du dimanche.
- **Points de Friction :**
  - Trop d'informations techniques dispersées ; manque de synthèses exécutives percutantes.
- **Requêtes Fréquentes dans OpérIA :**
  - *"Résume la marge par région sur le trimestre."*
  - *"Donne-moi une synthèse du pipeline commercial T3."*
- **Usage Clé :** Consultation des résumés générés directement dans l'agent, copie des synthèses prêtes à l'emploi.

---

## 4. David Laurent — RSSI & Administrateur Sécurité (SecOps)

- **Rôle :** Responsable de la Sécurité des Systèmes d'Information et de la conformité DSI.
- **Expérience :** 12 ans en cyberdéfense et gouvernance de données sensibles.
- **Objectifs Quotidiens :**
  - Garantir l'inviolabilité des données bancaires et personnelles de l'entreprise.
  - S'assurer qu'aucun modèle de langage externe ne puisse déclencher des actions en écriture de manière autonome.
  - Disposer d'une preuve d'audit inaltérable pour chaque validation ou refus d'opération.
- **Points de Friction :**
  - Méfiance vis-à-vis des agents IA "boîte noire" qui prennent des initiatives incontrôlées.
- **Usage Clé :** Contrôle régulier de l'onglet **Paramètres** (`/settings`) pour vérifier que les verrous d'actions sensibles sont cochés, et audit des logs sur la page **Historique** (`/history`).
