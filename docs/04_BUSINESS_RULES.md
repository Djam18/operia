# Règles Métier & Garde-Fous (Business Rules) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Matrice de Classification des Actions

Toute commande ou outil exécuté par OpérIA appartient obligatoirement à l'une des deux catégories suivantes :

| Catégorie | Description | Mode d'Exécution | Exemples d'Outils |
| :--- | :--- | :--- | :--- |
| **CL-READ (Lecture Seule)** | Requêtes d'interrogation, calculs mathématiques, agrégations statistiques, lectures de tables sans modification. | **Autonome (Automatique)** | `erp.factures.query`<br>`crm.comptes.enrich`<br>`warehouse.commandes.inspect`<br>`bi.ventes.aggregate` |
| **CL-SENSITIVE (Action Sensible)** | Tout événement provoquant un effet de bord persistant : envoi d'email à un tiers, écriture ou mise à jour dans un ERP/CRM, suppression, export massif de données nominatives. | **Validation Humaine Obligatoire (HITL)** | `mailer.send_bulk_relance`<br>`crm.opportunites.update`<br>`exporter.generate_csv`<br>`erp.commandes.unblock` |

---

## 2. Règles Métier Formelles (BR-xxx)

### 2.1 Gouvernance et Validation Humaine (HITL)

- **BR-HITL-001 (Règle d'Or de Non-Exécution Autonome) :**  
  Aucune action de catégorie `CL-SENSITIVE` ne peut être exécutée de manière autonome par le LLM. L'agent doit obligatoirement encapsuler les paramètres dans un objet `StagedAction` et stopper son exécution en attendant un signal explicite d'un utilisateur humain authentifié.

- **BR-HITL-002 (Information Explicite des Conséquences) :**  
  Toute action soumise à validation humaine doit formuler explicitement dans l'interface :
  1. Le type et le nombre de destinataires ou d'entités modifiées (ex: *"8 destinataires"*).
  2. L'impact financier ou matériel cumulé (ex: *"42 680 € concernés"*).
  3. Le canal de transmission (ex: *"Email externe"*, *"Modification base CRM"*).
  4. La mention explicite d'irréversibilité : *"Envoi externe irréversible : rien n'est envoyé avant votre validation explicite"*.

- **BR-HITL-003 (Expirations des Actions en Attente) :**  
  Toute action préparée non validée dans un délai de **7 jours ouvrés** passe automatiquement à l'état `EXPIRED`. Elle ne peut plus être exécutée afin d'éviter d'appliquer des relances ou des modifications basées sur des données financières devenues obsolètes.

- **BR-HITL-004 (Double Habilitation au-delà du Seuil Critique) :**  
  Si le montant cumulé d'une action de relance ou de modification comptable dépasse **50 000 € HT**, ou si le nombre d'enregistrements clients exportés excède **5 000 lignes**, l'action requiert l'approbation d'un utilisateur disposant du rôle `SUPERVISOR` ou `DIRECTION`.

---

### 2.2 Règles Financières & Recouvrement

- **BR-FIN-001 (Critère de Retard de Paiement Échu) :**  
  Une facture est déclarée en retard échu si `Date_du_Jour - Date_Echeance > 0 jours`.  
  La requête standard de relance de niveau 1 cible les factures avec `retard_jours > 30 jours`.

- **BR-FIN-002 (Exclusion des Comptes en Litige) :**  
  L'agent doit systématiquement croiser les factures en retard avec les dossiers CRM. Si un compte possède le drapeau `litige_ouvert == True` ou une contestation active, l'agent **ne doit pas** inclure ce compte dans le lot de relance automatique, et doit signaler l'exclusion dans sa synthèse récapitulative.

- **BR-FIN-003 (Périodicité Minimale des Relances) :**  
  Deux relances par email pour un même compte client doivent être espacées d'au moins **7 jours calendaires**, sauf instruction explicite contraire de l'opérateur avec confirmation manuelle.

---

### 2.3 Protection des Données & Exports (RGPD)

- **BR-SEC-001 (Export de Données Nominatives) :**  
  Tout export CSV ou Excel contenant des données personnelles (Nom, Prénom, Email direct, Numéro de téléphone portable) est classé d'office comme `SENSIBLE`.

- **BR-SEC-002 (Génération de Liens Éphémères) :**  
  Les fichiers d'export générés après validation humaine sont stockés dans un espace de stockage chiffré et téléchargeables via des liens pré-signés à durée de vie limitée à **15 minutes**.

- **BR-SEC-003 (Masquage dans les Prompts) :**  
  Les numéros de carte bancaire, coordonnées IBAN complètes et mots de passe sont automatiquement caviardés (anonymisés) par une couche de sanitization avant d'être transmis au modèle de langage.

---

### 2.4 Synchronisation et Fraîcheur des Données

- **BR-DATA-001 (Indicateur d'Obsolescence des Données) :**  
  Si la dernière synchronisation d'une source métier remonte à plus de **2 heures** pour les données financières ou plus de **24 heures** pour les référentiels, l'agent doit apposer un avertissement visuel : *"Données non actualisées depuis X minutes/heures"*.

- **BR-DATA-002 (Annulation en Cas de Conflit de Données) :**  
  Lors de la validation d'une action, si la facture a été encaissée ou si la commande a été modifiée entre la préparation de l'action et le clic de validation humaine, l'exécution est interrompue avec l'erreur `CONCURRENCY_CONFLICT` et l'opérateur est invité à réactualiser sa demande.
