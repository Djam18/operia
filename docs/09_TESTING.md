# Stratégie de Test & Assurance Qualité (Testing) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Pyramide & Stratégie Globale de Test

Le système OpérIA allie code déterministe (FastAPI, MCP, Nuxt 3) et inférence probabiliste (LLM). La stratégie de test répond à une double exigence :
1. **Zéro régression sur la sécurité :** Une action sensible ne doit **jamais** pouvoir s'exécuter sans validation humaine explicite.
2. **Exactitude factuelle des données :** Les chiffres et requêtes extraits des outils MCP ne doivent souffrir d'aucune altération ou hallucination.

```
       / \
      / E2E \       Playwright : Validation parcours complets Nuxt -> FastAPI
     /-------\
    /  Eval   \     LLM Evals : Fiabilité du Tool-Calling, robustesse injection
   /-----------\
  / Integration \   Pytest-asyncio, TestContainers (Postgres, Redis), MCP mocks
 /---------------\
/   Tests Unitaires\ Pytest (Backend), Vitest (Frontend Pinia/Vue Components)
-------------------
```

---

## 2. Tests Unitaires & Composants

### 2.1 Backend FastAPI (Pytest)
- **Objectif de couverture :** > 85 % sur les services métiers et contrôleurs.
- **Domaines testés :**
  - Validation Pydantic de tous les payloads entrants.
  - Vérification de la classification des outils (`CL-READ` vs `CL-SENSITIVE`).
  - Intercepteur de sécurité : blocage des appels directs aux connecteurs d'envoi.
  - Génération et expiration des objets `StagedAction`.

### 2.2 Frontend Nuxt / Vue 3 (Vitest)
- **Objectif de couverture :** > 80 % sur les stores Pinia et composants réutilisables.
- **Composants critiques testés :**
  - `ActionCard.vue` : Rendu correct des boutons *Valider et exécuter* et *Refuser*, affichage de l'avertissement d'irréversibilité.
  - `ToolExecutionBadge.vue` : Gestion des états `ok`, `partial`, `error` et affichage de la latence en millisecondes.
  - `OperationsBatchBar.vue` : Activation du bouton de validation groupée lors de la sélection multiple.

---

## 3. Tests d'Intégration & Protocole MCP

- **Serveur Mock MCP :** Utilisation d'un serveur MCP de test simulant les réponses ERP et CRM avec injection de scénarios limites (comptes introuvables, erreurs 500, latence réseau élevée).
- **Test d'immuabilité d'audit :** Vérification par test automatisé qu'une requête SQL directe `DELETE FROM audit_logs` ou `UPDATE audit_logs` lève une exception PostgreSQL stricte.

---

## 4. Évaluation & Benchmarks LLM (LLM Evals)

Un banc de test automatisé exécuté à chaque pull request évalue le modèle avec un jeu de 100 prompts métier types :

| Catégorie d'Évaluation | Métrique Attendue | Critère de Succès |
| :--- | :--- | :--- |
| **Sélection de l'outil approprié** | Exactitude du nom et paramètres d'outil | 100 % sur le dataset de référence |
| **Détection du besoin de validation** | Blocage avant envoi pour action sensible | **100 % (Zéro faux négatif)** |
| **Résistance au Prompt Injection** | Échec des tentatives de contournement de validation | 100 % de rejets sécurisés |
| **Fidélité des données chiffrées** | Absence d'altération des montants issus de l'ERP | 100 % de concordance mathématique |

---

## 5. Tests End-to-End (Playwright)

Scénarios automatisés dans un navigateur Chromium sans tête :
1. **Scénario Relance Factures :**
   - Connexion sous le compte Alex Martin ;
   - Envoi du prompt *"Donne-moi les factures impayées > 30 jours"* ;
   - Vérification de l'apparition de la réponse et de la carte d'action à valider ;
   - Clic sur *Valider et exécuter* ;
   - Contrôle du passage de la carte à l'état *Terminé* et de l'incrémentation du compteur dans l'historique.
2. **Scénario Rejet d'Action :**
   - Clic sur *Refuser* avec saisie d'un motif ;
   - Vérification qu'aucun appel à l'API d'envoi d'email n'a été émis.
