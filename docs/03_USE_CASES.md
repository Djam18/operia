# Cas d'Usage Métier (Use Cases) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## Sommaire des Cas d'Usage

| Code | Titre du Cas d'Usage | Acteur Principal | Criticité Action |
| :--- | :--- | :--- | :--- |
| **UC-01** | Détection et relance ciblée des factures impayées à > 30 jours | Alex Martin (Dir. Financière) | **Sensible (Envoi externe)** |
| **UC-02** | Export qualifié de données clients (CRM) au format CSV | Sophie Bernard (Responsable ADV) | **Sensible (Données nominatives)** |
| **UC-03** | Synthèse de performance commerciale & marge trimestrielle | Marc Leroy (Dir. Commercial) | Standard (Lecture & Synthèse) |
| **UC-04** | Analyse des commandes bloquées en entrepôt / ERP | Alex Martin / Opérateur Logistique | Standard / Préparation d'action |
| **UC-05** | Validation ou Refus dans le Centre des Opérations | Tout opérateur habilité | **Contrôle d'exécution (HITL)** |
| **UC-06** | Audit complet et traçabilité d'une opération contestée | Administrateur / DAF | Audit & Contrôle |

---

## UC-01 : Détection et Relance Ciblée des Factures Impayées (> 30 jours)

### Acteur principal
Alex Martin — Direction financière

### Préconditions
- La source "Base financière" et la source "CRM" sont connectées et synchronisées.
- L'utilisateur est connecté et dispose des droits de validation financière.

### Déclencheur
L'utilisateur saisit dans l'interface Agent :  
*"Donne-moi les factures impayées depuis plus de 30 jours."*  
Puis :  
*"Prépare une relance pour ces comptes, avec la comptabilité en copie."*

### Scénario Nominal
1. L'opérateur pose sa question en langage naturel dans l'invite de discussion.
2. L'agent analyse la demande et invoque l'outil MCP `erp.factures.query(retard_jours__gt=30, statut="impaye")`.
3. L'outil retourne les résultats : 23 factures identifiées pour un montant total de 86 420 €.
4. L'agent enrichit les données via `crm.comptes.enrich(client_ids=[...])` pour identifier les contacts payeurs et filtrer les clients sous contentieux.
5. L'agent affiche un tableau interactif synthétique des premiers comptes (Nova Conseil: 12 800 €, Atelier N7: 8 450 €, Groupe Atlas: 6 920 €) avec un lien permettant d'explorer les 23 résultats.
6. L'agent détecte que 8 clients dépassent le seuil critique de relance sans litige en cours.
7. L'agent génère un bloc **"Action à Valider"** (ID: `act-4821`) intitulé *"Envoyer une relance à 8 clients"* avec :
   - Nombre de destinataires : 8 contacts comptables ;
   - Montant total ciblé : 42 680 € ;
   - Canal : Email avec template professionnel et mise en copie automatique de la comptabilité ;
   - Conséquence mise en exergue : *"Action sensible : Envoi externe irréversible. Rien n'est envoyé sans votre validation."*
8. L'opérateur clique sur **"Examiner"** pour prévisualiser le texte de l'email généré.
9. L'opérateur clique sur **"Valider et exécuter"**.
10. Le backend FastAPI ordonne au service de messagerie l'envoi effectif des 8 messages et journalise l'opération.
11. L'interface affiche le statut mis à jour : *"Terminé - 8 emails envoyés avec succès"*.

### Extensions & Exceptions
- **4a. Contact manquant dans le CRM :** Si l'outil signale un contact absent (ex: Nord Logistique), l'agent avertit l'opérateur avec un statut `partial` et isole le compte sans bloquer les 7 autres.
- **9a. Refus par l'opérateur :** Si l'opérateur juge le moment inopportun, il clique sur **"Refuser"**. L'action passe au statut `REFUSED` dans le journal sans aucun envoi.

---

## UC-02 : Export Qualifié de Données Clients (CRM) en CSV

### Acteur principal
Sophie Bernard — Responsable Relation Client

### Déclencheur
L'utilisateur formule : *"Prépare un export CSV des clients actifs T3 ayant passé commande au cours des 90 derniers jours."*

### Scénario Nominal
1. L'agent interroge le connecteur MCP CRM pour identifier les comptes répondant aux critères temporels et statutaires.
2. Le système calcule le volume : 1 248 lignes de clients actifs.
3. Conformément à la règle de gouvernance RGPD (export de données clients nominatives), l'agent ne génère pas de téléchargement immédiat et soumet une carte d'action à valider.
4. L'action `Export des clients actifs` apparaît dans le Dashboard et dans le centre des Opérations avec la mention *"Action sensible : Contient des données personnelles"*.
5. Sophie Bernard valide l'action après avoir vérifié le périmètre des colonnes (Raison sociale, Ville, CA T3, Statut).
6. Le backend génère un fichier sécurisé avec signature temporaire d'URL (valable 15 minutes) et journalise l'export nominatif dans l'historique d'audit.

---

## UC-03 : Synthèse de Performance Commerciale & Marge Trimestrielle

### Acteur principal
Marc Leroy — Directeur Commercial

### Déclencheur
L'utilisateur demande : *"Résume la marge par région sur le trimestre et prépare une note pour le comité commercial."*

### Scénario Nominal
1. L'agent interroge l'entrepôt de ventes (`bi.ventes.aggregate(groupby="region", period="Q3")`).
2. L'agent effectue les calculs de variation par rapport au trimestre N-1.
3. L'agent génère une synthèse structurée en texte clair avec puces et ratios de performance.
4. Comme l'action demandée est la création d'un rapport de synthèse interne (document brouillon sans impact externe immédiat), l'agent génère le document sous statut standard et propose de l'archiver ou de l'envoyer en relecture.
5. L'action est enregistrée dans l'historique comme *"Rapport généré - Synthèse pipeline T3"*.

---

## UC-04 : Analyse et Déblocage des Commandes en Logistique

### Acteur principal
Opérateur Logistique / Alex Martin

### Déclencheur
L'utilisateur demande : *"Y a-t-il des commandes bloquées en logistique ? Pourquoi ?"*

### Scénario Nominal
1. L'agent utilise `warehouse.commandes.inspect(statut="bloque")`.
2. L'outil relève 342 lignes de commandes en attente d'expédition pour rupture de stock ou attente de contrôle de solvabilité.
3. L'agent présente une répartition par motif de blocage : 70 % rupture fournisseur, 30 % blocage encours financier.
4. L'agent propose deux actions distinctes :
   - Un export CSV pour le responsable des approvisionnements ;
   - Une mise à jour groupée des priorités pour les clients stratégiques.
5. Chaque action est isolée dans la file de validation avant toute modification de statut dans l'ERP.

---

## UC-05 : Validation ou Refus dans le Centre des Opérations (`/operations`)

### Acteur principal
Superviseur ou DAF

### Scénario Nominal
1. L'utilisateur accède à la page `/operations`.
2. Il visualise le badge *"7 en attente"* et filtre sur l'onglet **En attente**.
3. La liste affiche les cartes détaillées :
   - Type d'opération (Relance, Export CSV, Synthèse) ;
   - Demandeur et date de préparation ;
   - Volume et montants financiers impliqués.
4. L'utilisateur coche 3 actions vérifiées et clique sur le bouton supérieur **"Valider la sélection"**.
5. Le frontend envoie une requête batch à l'API FastAPI (`POST /api/v1/operations/batch-validate`).
6. Le statut bascule en temps réel à l'écran : les cartes passent dans l'onglet **Terminées** avec une coche verte.

---

## UC-06 : Traçabilité et Audit d'une Action (`/history`)

### Acteur principal
Responsable Conformité / SecOps / DSI

### Scénario Nominal
1. En cas de réclamation d'un client déclarant avoir reçu un email injustifié, l'auditeur se rend sur `/history`.
2. Il filtre par outil *"Finance + CRM"* ou recherche le nom du client dans la barre de recherche.
3. Il retrouve la ligne d'événement :
   - Date et heure exacte de la requête ;
   - Identifiant de l'utilisateur ayant formulé la demande ;
   - Outils exécutés et données brutes retournées ;
   - Identifiant de la personne ayant cliqué sur le bouton de validation ;
   - Trace horodatée de l'envoi SMTP.
4. L'export du rapport de traçabilité est téléchargeable sous forme de preuve d'audit inaltérable.
