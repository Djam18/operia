# Spécifications Complètes d'Interface UI/UX (Specification Complete) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Structure Globale de l'Application (Layout Shell)

L'application repose sur une mise en page moderne à panneau latéral fixe (Sidebar) et zone de contenu dynamique :

```
┌────────────────────────────────────────────────────────────────────────┐
│ [Logo] OpérIA            │ [Barre Supérieure Contextuelle / Titre]     │
│ Agent d'opérations       │                                            │
├──────────────────────────┼────────────────────────────────────────────┤
│ [+ Nouvelle conversation]│                                            │
│                          │                                            │
│ ⊞ Dashboard              │                                            │
│ 🤖 Agent                 │                                            │
│ ⚙ Opérations        [7] │            ZONE PRINCIPALE                 │
│ 🗄 Données               │               DE TRAVAIL                   │
│ 🕒 Historique            │                                            │
│ ⚙ Paramètres             │                                            │
│                          │                                            │
├──────────────────────────┤                                            │
│ ● Agent opérationnel     │                                            │
│ [Avatar AM] Alex Martin  │                                            │
│ Direction financière     │                                            │
└──────────────────────────┴────────────────────────────────────────────┘
```

### 1.1 Barre Latérale Permanente (Left Sidebar)
- **Logo :** Icône violette carrée arrondie avec motif agent blanc + texte **OpérIA** (H2 bold) et sous-titre gris *"Agent d'opérations"*.
- **Bouton Primaire :** `+ Nouvelle conversation` (Fond violet `#4F46E5`, texte blanc, arrondi 8px).
- **Navigation Principale (6 items) :**
  1. `Dashboard` : Icône grille 4 carrés.
  2. `Agent` : Icône robot / bot.
  3. `Opérations` : Icône double engrenage + **Badge numérique dynamique orange `7`** indiquant le nombre d'actions sensibles en attente d'approbation.
  4. `Données` : Icône base de données / cylindres.
  5. `Historique` : Icône horloge circulaire.
  6. `Paramètres` : Icône engrenage de configuration.
- **Pied de Barre Latérale (Footer) :**
  - Indicateur de santé système : Point vert pulsant + texte *"Agent opérationnel"*.
  - Profil utilisateur connecté : Avatar avec initiales `AM`, nom *"Alex Martin"*, sous-titre *"Direction financière"* et chevron d'options de compte.

---

## 2. Spécification Détaillée des Écrans

---

### Écran 1 : Dashboard (`/`) — Vue d'Ensemble Opérationnelle

- **En-tête de page :**
  - Titre principal : `Bonjour Alex`
  - Sous-titre : `Voici ce que votre agent a préparé aujourd'hui.`
  - Bouton supérieur droit : `💬 Interroger l'agent` (action rapide ouvrant `/agent`).
- **Ligne de 4 Indicateurs Clés (KPI Cards) :**
  1. **Requêtes :** Valeur `128` · Libellé `+12 cette semaine` · Icône bulle de discussion.
  2. **Actions préparées :** Valeur `42` · Libellé `Sur les 30 derniers jours` · Icône document.
  3. **En attente :** Valeur `7` · Libellé `Votre validation est requise` · Encadrement et texte orange ambré d'alerte avec icône horloge.
  4. **Terminées :** Valeur `35` · Libellé `Taux de réussite 97,2 %` · Icône coche de validation.
- **Zone Centrale à 2 Colonnes (Grille Asymétrique) :**
  - **Colonne Gauche (Activité Récente) :**
    - Titre : `Activité récente` avec sous-titre `Dernières opérations traitées par l'agent` et lien `Tout voir →`.
    - Liste des 4 dernières opérations sous forme de cartes plates bordées :
      - *Export clients préparé* (1 248 clients actifs · CRM · Il y a 8 min · Badge `⚠️ En attente`).
      - *Résumé commercial généré* (Performance T3 · Base de données · Il y a 24 min · Badge `✔ Terminé`).
      - *Relance facture préparée* (8 destinataires · Email · Il y a 41 min · Badge `⚠️ En attente`).
      - *Analyse des commandes* (Commandes septembre · ERP · Il y a 1 h · Badge `✔ Terminé`).
  - **Colonne Droite (Widget Prioritaire "À VALIDER") :**
    - Carte d'accentuation haute priorité bordée d'orange.
    - En-tête : `🕒 À VALIDER — 3 actions sont prioritaires`.
    - Focus Action : `Relance de factures échues` (8 emails préparés · 42 680 € concernés).
    - Callout Conséquence : `Conséquence : les messages seront envoyés aux contacts financiers.`
    - Boutons d'action : `Détails` (bouton neutre) et `Examiner` (bouton violet franc).

---

### Écran 2 : Agent (`/agent`) — Console de Conversation & Validation

- **Sous-panneau Conversations Récentes (Gauche) :**
  - Titre `Conversations` + bouton `+`.
  - Barre de recherche `🔍 Rechercher`.
  - Liste chronologique :
    - *Factures impayées* (Aujourd'hui, 10:14) — Sélectionné.
    - *Export clients actifs* (Hier, 16:42).
    - *Analyse des commandes* (15 sept., 09:18).
- **Zone Principale de Chat (Centre) :**
  - **Barre supérieure :**
    - Titre du fil : `Factures impayées`.
    - Statut : `● Agent prêt · 3 sources connectées`.
    - Pastille de sécurité : `🛡 Mode contrôlé`.
    - Menu contextuel `•••`.
  - **Message Utilisateur :**
    - Bulle droite : *"Donne-moi les factures impayées depuis plus de 30 jours."*
  - **Message Assistant :**
    - Texte explicatif : *"J'ai trouvé 23 factures correspondant à ce critère, pour un montant total de 86 420 €. Huit clients dépassent votre seuil de relance automatique."*
    - **Widget Tableau de Factures :**
      - Titre : `Factures identifiées (23 résultats)`.
      - Lignes :
        - Nova Conseil | FAC-2026-184 | 12 800 € | 47 jours
        - Atelier N7 | FAC-2026-207 | 8 450 € | 39 jours
        - Groupe Atlas | FAC-2026-221 | 6 920 € | 34 jours
      - Lien d'expansion : `Voir les 23 factures >`.
    - **Composant Trace d'Outils :**
      - Bloc déroulé : `🛠 Outils utilisés : CRM et base de données [✔ Completed]`.
    - **Composant Carte "ACTION À VALIDER" :**
      - Bordure et fond ambré clair.
      - Titre : `🛡 ACTION À VALIDER` avec badge `⚠️ En attente`.
      - Intitulé : `Envoyer une relance à 8 clients`.
      - Description : `L'agent a ciblé les factures échues de plus de 30 jours sans litige ouvert.`
      - Grille métriques : Destinataires: *8 contacts* | Type: *Relance facture* | Canal: *Email*.
      - Boutons : `Valider et exécuter` / `Refuser`.
  - **Barre Inférieure de Saisie :**
    - Input avec placeholder : `Demandez une analyse ou préparez une action...`.
    - Mention d'intégrité : `🛡 Validation requise avant toute action sensible`.
    - Bouton d'envoi violet.
- **Panneau Latéral Droit (Contexte de Travail) :**
  - Titre : `Contexte de travail`.
  - **Sources actives :**
    - Base de données (✔ vert)
    - CRM clients (✔ vert)
    - Messagerie (✔ vert)
  - **Périmètre :** `Finance · France`.
  - **Fraîcheur :** `Données actualisées il y a 4 min`.

---

### Écran 3 : Opérations (`/operations`) — Centre de Gestion des Validations

- **En-tête de page :**
  - Titre : `Opérations`.
  - Sous-titre : `Examinez les actions préparées avant leur exécution.`
  - Bouton supérieur droit : `Valider la sélection` (bouton violet).
- **Onglets de Filtrage :**
  - `Toutes 12` (actif violet)
  - `En attente 7`
  - `Terminées`
- **Liste des Cartes d'Opérations :**
  1. *Relance de factures échues* · 8 emails · 42 680 € concernés · Demandé par Alex Martin · Badge `⚠️ En attente` · Bouton `Voir les détails`.
  2. *Export des clients actifs* · 1 248 lignes · format CSV · Demandé par Sophie Bernard · Badge `⚠️ En attente` · Bouton `Voir les détails`.
  3. *Synthèse du pipeline T3* · Rapport commercial · 12 pages · Demandé par Agent OpérIA · Badge `✔ Terminé` · Bouton `Voir les détails`.
  4. *Mise à jour des priorités* · 17 opportunités CRM · Demandé par Marc Leroy · Badge `✔ Approuvé` · Bouton `Voir les détails`.

---

### Écran 4 : Données (`/data`) — Supervision des Sources Connectées

- **En-tête de page :**
  - Titre : `Données`.
  - Sous-titre : `Sources métier accessibles à l'agent, avec leur niveau d'actualisation.`
  - Bouton supérieur droit : `🔄 Actualiser`.
- **Bannière d'État :**
  - Fond bleu ciel pastel : `🗄 5 sources connectées · Dernière synchronisation il y a 2 minutes`.
- **Tableau Central des Sources :**
  - Colonnes : `Source`, `Type`, `Enregistrements`, `Mise à jour`, `État`.
  - Lignes :
    - Clients | CRM | 4 820 | Il y a 4 min | `✔ Terminé`
    - Factures | Base financière | 18 406 | Il y a 2 min | `✔ Terminé`
    - Commandes | ERP | 32 104 | Il y a 12 min | `✔ Terminé`
    - Messages commerciaux | Messagerie | 7 892 | Il y a 1 h | `⟳ En cours`
    - Catalogue produits | Référentiel | 684 | Hier, 18:10 | `✔ Terminé`
- **Pied de Tableau :** `5 résultats · Page 1 sur 1`.

---

### Écran 5 : Historique (`/history`) — Journal d'Audit du Cycle de Vie

- **En-tête de page :**
  - Titre : `Historique`.
  - Sous-titre : `Une trace complète, de la demande jusqu'au résultat.`
- **Fil d'Ariane du Cycle de Vie :**
  - Composant visuel séquentiel : `Requête → Analyse → Action préparée → Validation → Exécution`.
- **Barre d'Outils :** Champ `Rechercher dans l'historique...` + Bouton `Filtres`.
- **Tableau d'Audit :**
  - Colonnes : `Date`, `Utilisateur`, `Demande`, `Outil`, `Action`, `Statut`.
  - Lignes :
    - 17 sept. · 10:14 | Alex Martin | Factures > 30 jours | Finance + CRM | Relance email | `⚠️ En attente`
    - 17 sept. · 09:58 | Sophie Bernard | Clients actifs T3 | CRM | Export CSV | `⚠️ En attente`
    - 16 sept. · 16:42 | Marc Leroy | Résumé du pipeline | CRM | Rapport généré | `✔ Terminé`
    - 16 sept. · 14:20 | Alex Martin | Commandes en retard | ERP | Analyse | `✔ Terminé`
    - 15 sept. · 11:06 | Sophie Bernard | Contacts sans activité | CRM | Liste segmentée | `✖ Échec`

---

### Écran 6 : Paramètres (`/settings`) — Garde-Fous & Connexions

- **En-tête de page :**
  - Titre : `Paramètres`.
  - Sous-titre : `Définissez le périmètre de travail et les garde-fous de l'agent.`
- **Section 1 : Contrôle et validations**
  - Sous-titre : `Les actions sensibles restent soumises à une décision humaine.`
  - 3 Toggles / Cases à cocher actives :
    - [x] `🛡 Envoi d'emails externes`
    - [x] `🛡 Modification de données métier`
    - [x] `🛡 Export de données clients`
- **Section 2 : Connexions métier**
  - Cartes d'intégration :
    - *Base financière* : Statut vert `Connectée` + Bouton `Configurer`.
    - *Messagerie* : Statut vert `Connectée` + Bouton `Configurer`.

---

### Écran 7 : Vue Console Haute Densité Sombre (`Atlas` — `home.png`)

- **Top Navigation :**
  - Logo `Atlas · COPILOTE DONNÉES MÉTIER`.
  - Onglets supérieurs : `Console` (actif) | `Sources` | `Journal`.
  - Compteur d'alerte : `● 3 actions en attente de validation` + Profil `CM`.
- **Header :**
  - Titre : `Console d'interrogation`.
  - Sous-titre : `Posez vos questions métier en langage naturel. Atlas prépare les relances, exports et résumés, puis attend votre validation avant toute action sensible.`
  - Compteurs chiffrés : `REQUÊTES AUJOURD'HUI: 148` | `ACTIONS VALIDÉES: 23`.
- **Panneau de Gauche :**
  - `PÉRIMÈTRE DE DONNÉES` (ERP Factures [lecture seule], CRM Comptes clients [lecture seule], Entrepôt Ventes [lecture seule], Messagerie sortante [écriture - validation requise]).
  - `QUESTIONS FRÉQUENTES` (3 boutons de suggestion rapide).
- **Centre (Interrogation & Traces Monospace) :**
  - Trace `erp.factures.query: ok · 142ms`
  - Trace `crm.comptes.enrich: partial · 210ms (12 comptes enrichis · 1 contact manquant [Nord Logistique])`
  - Action préparée liée : `action act-4821 en attente de validation dans la file à droite`.
- **Panneau de Droite (File de Validation Dédiée) :**
  - `FILE DE VALIDATION (3 en attente)`.
  - Cartes d'actions empilées :
    - *Relance de paiement — 12 comptes* (84 210 € · Envoi externe irréversible) avec boutons `Valider et exécuter` / `Refuser`.
    - *Export CSV — commandes bloquées* (342 lignes · Données nominatives) avec boutons `Valider et exécuter` / `Refuser`.
    - *Résumé hebdomadaire — marge par région* (Brouillon interne) avec boutons `Valider et exécuter` / `Refuser`.
