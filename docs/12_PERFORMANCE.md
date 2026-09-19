# Exigences de Performance & Optimisations (Performance) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Budgets de Latence & Niveaux de Service (SLO)

Dans les captures de production d'OpérIA, les temps d'exécution des outils MCP sont mesurés et affichés directement dans la trace d'interaction (ex: `erp.factures.query: 142ms`, `crm.comptes.enrich: 210ms`).

| Étape de Traitement | Cible P50 | Cible P95 | Seuil Critique (Alerte) |
| :--- | :--- | :--- | :--- |
| **Time to First Token (TTFT)** (Début de réponse LLM) | < 600 ms | < 1 200 ms | > 2 500 ms |
| **Exécution d'Outil MCP Lecture** (ex: ERP Factures) | < 150 ms | < 300 ms | > 800 ms |
| **Enrichissement CRM multi-comptes** | < 200 ms | < 450 ms | > 1 000 ms |
| **Rendu de la Carte Action Préparée** | < 80 ms | < 150 ms | > 300 ms |
| **Temps d'exécution après validation humaine** | < 800 ms | < 1 500 ms | > 3 000 ms |

---

## 2. Stratégie de Mise en Cache (Caching Strategy)

### 2.1 Cache des Données Froides & Référentiels
- **Référentiel Produit / Catalogues :** Mis en cache Redis avec une durée de vie (TTL) de **12 heures**.
- **Paramètres de Garde-Fous :** Mis en cache mémoire FastAPI (lru_cache) invalidé immédiatement lors d'une mutation sur `/settings`.

### 2.2 Mémoïsation des Requêtes de Lecture Identiques
- Pour éviter de recalculer des agrégats lourds lorsqu'un opérateur pose plusieurs questions sur la même cohorte (ex: *"Et parmi ces factures, combien pour le secteur public ?"*), les résultats bruts des outils `erp.factures.query` sont mis en cache Redis pour la session active pendant **5 minutes**.

---

## 3. Optimisation de la Base de Données

- **Indexation :**
  - Index composite `(conversation_id, created_at DESC)` sur la table `messages`.
  - Index partiel `CREATE INDEX idx_staged_actions_pending ON staged_actions (status) WHERE status = 'PENDING';` permettant un chargement instantané du badge de navigation `Opérations [7]`.
  - Index B-Tree sur `audit_logs (timestamp DESC)`.
- **Pool de Connexions :**
  - Utilisation d'un pool asynchrone `asyncpg` avec dimensionnement : `min_size=10`, `max_size=50` par réplica backend.

---

## 4. Performance Frontend & Web Vitals

- **Hydratation Sélective :** Utilisation des capacités de Nuxt 3 pour hydrater uniquement les composants interactifs (chat et cartes d'action).
- **Virtualisation de Liste :** Utilisation de `vue-virtual-scroller` dans la page `/history` et `/operations` pour supporter l'affichage fluide de plus de 10 000 entrées d'audit sans dégradation de la mémoire du navigateur.
- **Score Web Vitals :** LCP < 1,5 s, INP < 100 ms, CLS < 0,02.
