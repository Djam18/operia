# Parcours Utilisateurs Détaillés (User Journeys) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## Parcours 1 : Alex Martin — Direction Financière (Recouvrement Rapide du Matin)

### Contexte & Objectif
Alex démarre sa journée à 09h00. Son objectif est de vérifier les créances échues et de lancer la campagne de relance hebdomadaire sans y consacrer plus de 10 minutes.

### Déroulement Pas à Pas
1. **Connexion & Accueil :**
   - Alex arrive sur le **Dashboard** (`/`).
   - Il voit immédiatement : *"Bonjour Alex — Voici ce que votre agent a préparé aujourd'hui."*
   - Le bloc prioritaire à droite affiche : *"À VALIDER : 3 actions sont prioritaires — Relance de factures échues (8 emails préparés · 42 680 € concernés)"*.
2. **Examen de l'Action :**
   - Alex clique sur le bouton violet **"Examiner"**.
   - Il est redirigé vers l'interface **Agent** sur la conversation *"Factures impayées"*.
3. **Analyse de la Recommandation :**
   - Il consulte le tableau interactif : 23 factures trouvées pour 86 420 €, dont 8 éligibles à la relance automatique sans litige.
   - Il déroule le bloc *"Outils utilisés : CRM et base de données [Completed]"* pour vérifier les requêtes.
4. **Validation de l'Action :**
   - Alex vérifie la carte *"ACTION À VALIDER"* : Destinataires (8 contacts), Type (Relance facture), Canal (Email).
   - Rassuré par la mention *"Validation requise avant toute action sensible"*, il clique sur **"Valider et exécuter"**.
5. **Confirmation & Clôture :**
   - Un toast vert apparaît : *"8 emails de relance envoyés avec succès. Action archivée."*
   - Le compteur du Dashboard passe de 7 à 6 en attente.

---

## Parcours 2 : Sophie Bernard — ADV (Export Sécurisé de Données Clients)

### Contexte & Objectif
Sophie doit fournir à l'équipe marketing la liste des 1 200 clients actifs du trimestre pour une opération promotionnelle.

### Déroulement Pas à Pas
1. **Formulation de la Demande :**
   - Sophie ouvre une nouvelle conversation dans l'onglet **Agent**.
   - Elle tape : *"Exporte les clients actifs T3 au format CSV avec leurs contacts principaux."*
2. **Préparation par l'Agent :**
   - L'agent consulte le CRM, filtre 1 248 fiches clients et prépare le fichier.
   - L'agent répond : *"J'ai préparé l'export de 1 248 lignes. Cette action impliquant des données nominatives sensibles, elle a été placée dans votre file de validation."*
3. **Validation & Téléchargement :**
   - Sophie clique sur la carte d'action pour valider l'export.
   - Un lien de téléchargement éphémère (15 minutes) s'affiche. Elle télécharge le fichier CSV chiffré.
   - L'opération est immédiatement tracée dans `/history` avec son nom d'utilisateur.

---

## Parcours 3 : Marc Leroy — Direction Commerciale (Synthèse Pipeline T3)

### Contexte & Objectif
À 16h30, Marc prépare le comité de direction du lendemain. Il souhaite une synthèse synthétique de la performance des ventes.

### Déroulement Pas à Pas
1. **Requête :**
   - Marc clique sur le raccourci *"Questions fréquentes"* : *"Résume la marge par région sur le trimestre"*.
2. **Analyse de Données :**
   - L'agent appelle `bi.ventes.aggregate` et synthétise les résultats en un résumé structuré de 300 mots.
3. **Exploitation :**
   - Marc copie le texte généré pour l'intégrer à son support de présentation. L'action est classée en *Rapport généré (Terminé)* sans nécessiter de blocage sensible.

---

## Parcours 4 : Superviseur / SecOps (Contrôle des Sources & Audit)

### Contexte & Objectif
Vérifier l'intégrité de la plateforme et le bon fonctionnement des flux de données métier.

### Déroulement Pas à Pas
1. **Vérification Données (`/data`) :**
   - L'auditeur contrôle les 5 sources. Il constate que la *Messagerie* est *En cours* de synchronisation et que les 4 autres sont au vert *Terminé*.
   - Il clique sur *"Actualiser"* pour forcer un contrôle d'état.
2. **Consultation de l'Historique (`/history`) :**
   - Il inspecte les dernières actions de la journée.
   - Il filtre sur le statut *Échec* pour analyser l'incident du 15 sept. (Contacts sans activité) et constate que le connecteur CRM avait renvoyé un dépassement de quota.
