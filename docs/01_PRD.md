# Product Requirements Document (PRD) — OpérIA

**Nom du produit :** OpérIA (Agent IA d'Opérations Métier)  
**Version du document :** 1.0.0  
**Date :** 18 Septembre 2026  
**Auteur :** Équipe Produit & Architecture IA  
**Statut :** Validé  

---

## 1. Vision & Positionnement

### 1.1 Contexte du marché
Les directions opérationnelles (financières, commerciales, supply chain, relation client) passent quotidiennement jusqu'à 40 % de leur temps à naviguer entre des systèmes d'information hétérogènes (ERP, CRM, bases comptables, messageries professionnelles) pour :
- Extraire des données dispersées et croiser des rapports ;
- Identifier des anomalies ou retards (impayés, ruptures, commandes bloquées) ;
- Rédiger manuellement des relances, générer des exports ou consolider des synthèses.

L'automatisation classique (RPA ou scripts rigides) échoue face à l'imprévu et impose des règles statiques. L'adoption brute des LLM génériques (ChatGPT, Copilot généraliste) pose quant à elle des risques majeurs : hallucinations, fuites de données confidentielles et surtout **perte de contrôle sur les actions irréversibles**.

### 1.2 La proposition de valeur d'OpérIA
**OpérIA** est un agent d'opérations métier intelligent fondé sur une architecture moderne **Python · FastAPI · MCP (Model Context Protocol) · Nuxt/Vue**. Il réconcilie puissance générative et rigueur opérationnelle :
1. **Interrogation en langage naturel :** Les collaborateurs formulent leurs besoins métier sans écrire de requêtes SQL ou naviguer dans 10 onglets d'ERP.
2. **Exécution outillée (Tool-Calling via MCP) :** L'agent interroge des connecteurs standardisés et sécurisés (ERP, CRM, entrepôt de données, messagerie).
3. **Préparation d'actions concrètes :** L'agent ne se contente pas de répondre : il prépare des opérations complexes (brouillons d'emails de relance ciblés, exports CSV/Excel filtrés, résumés exécutifs).
4. **Validation humaine systématique (Human-in-the-Loop - HITL) :** **Aucune action sensible (envoi externe, écriture en base, export massif) n'est exécutée sans approbation humaine explicite préalable.**

---

## 2. Objectifs & Indicateurs Clés de Succès (KPIs)

| Objectif Produit | Indicateur Métrique (KPI) | Cible V1 |
| :--- | :--- | :--- |
| **Gain de productivité opérationnelle** | Temps moyen de préparation d'une campagne de relance ou d'un rapport | Réduction de 75 % (de 45 min à < 10 min) |
| **Sécurité & Maîtrise des risques** | Taux d'actions sensibles exécutées sans validation humaine | **0,00 % (Zéro tolérance)** |
| **Fiabilité des requêtes métier** | Taux d'exactitude des extractions de données (zéro hallucination de chiffres) | > 99 % |
| **Adoption & Satisfaction** | Taux d'acceptation/validation des actions préparées par l'agent | > 90 % |
| **Temps de réponse système** | Latence de génération d'une réponse avec appel d'outil (P95) | < 3,5 secondes |

---

## 3. Personas Cibles

1. **Alex Martin — Directeur Financier / Responsable Recouvrement**
   - *Besoin :* Suivre les encours clients, détecter immédiatement les factures en retard de plus de 30 jours, préparer les emails de relance échelonnés avec mise en copie comptable.
   - *Attente clé :* Voir exactement qui va recevoir quoi et le montant exact avant d'approuver.
2. **Sophie Bernard — Responsable Relation Client & Administration des Ventes**
   - *Besoin :* Extraire les listes de clients inactifs, segmenter les comptes selon leur typologie d'achat, exporter des données qualifiées.
   - *Attente clé :* Obtenir un fichier prêt à l'emploi sans mobiliser l'équipe data/IT.
3. **Marc Leroy — Directeur Commercial**
   - *Besoin :* Synthétiser la performance commerciale du trimestre, identifier les goulets d'étranglement logistiques (commandes bloquées).
   - *Attente clé :* Résumés clairs, directement exploitables en comité de direction.
4. **Administrateur / SecOps & DSI**
   - *Besoin :* Gouvernance des accès, paramétrage des seuils de criticité, traçabilité exhaustive de chaque appel d'outil et décision humaine.

---

## 4. Périmètre Fonctionnel (Scope V1)

### 4.1 Dans le périmètre (In-Scope)
- **Interface Conversationnelle Avancée (Module Agent) :**
  - Chat en langage naturel avec streaming SSE.
  - Cartes interactives d'outils montrant les requêtes exécutées en lecture seule (`erp.factures.query`, `crm.comptes.enrich`).
  - Bloc interactif "Action préparée à valider" avec détails, destinataires, impact et boutons Valider/Refuser.
- **Tableau de Bord Exécutif (Dashboard) :**
  - Métriques synthétiques (Requêtes, Actions préparées, En attente de validation, Terminées).
  - Flux d'activité récente avec statut en temps réel.
  - Widget prioritaire "À Valider" pour traitement rapide d'une urgence.
- **Centre de Gestion des Opérations (Opérations) :**
  - File d'attente centralisée de toutes les actions préparées.
  - Filtrage par état : *Toutes*, *En attente*, *Terminées*, *Refusées*.
  - Validation unitaire ou par lot ("Valider la sélection").
- **Observabilité des Sources Métier (Données) :**
  - Inventaire des sources connectées (ERP, CRM, Base financière, Messagerie, Référentiel catalogue).
  - Statut de synchronisation, volumétrie et horodatage de dernière mise à jour.
- **Journal d'Audit et Traçabilité (Historique) :**
  - Traçabilité complète du cycle de vie : *Requête → Analyse → Action préparée → Validation → Exécution*.
  - Filtres par utilisateur, date, outil utilisé et statut.
- **Garde-fous & Configuration (Paramètres) :**
  - Définition stricte des types d'actions soumises à validation humaine obligatoire (Envoi d'emails externes, Modification de données métier, Export de données clients).
  - Statut des connecteurs d'intégration métier.

### 4.2 Hors périmètre (Out-of-Scope V1)
- Exécution 100 % autonome d'actions destructives (suppression de comptes, annulation massive de commandes).
- Prise d'appels vocaux en direct (V1 exclusivement texte / chat et dashboards).
- Connecteurs ERP propriétaires non documentés (V1 supporte API REST, MCP standard et connecteurs SQL).

---

## 5. Exigences Non-Fonctionnelles Générales
- **Ergonomie :** Interface Nuxt 3 / Tailwind CSS ultra-réactive, accessible, respectant la charte violet/indigo d'OpérIA et disposant d'un mode sombre / console opérateur haute densité.
- **Sécurité :** Authentification JWT/OAuth2, conformité RGPD intégrale, masquage des données sensibles dans les logs LLM.
- **Scalabilité :** Architecture microservices/modulaire asynchrone avec FastAPI et Redis pour le découplage des tâches longues.

---

## 6. Feuille de Route Prévisionnelle (Roadmap)
- **V1.0 :** Core Agent, MCP Connectors (ERP/CRM/Email), File de validation HITL, Vues Dashboard / Agent / Opérations / Données / Historique / Paramètres.
- **V1.1 :** Support multi-approbations (double validation hiérarchique pour les montants > 50 000 €), connecteurs Slack/Teams.
- **V1.2 :** Planificateur autonome de veilles (actions préparées en tâche de fond nocturne soumises au réveil de l'opérateur).
