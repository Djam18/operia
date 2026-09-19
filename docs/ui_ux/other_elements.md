# Éléments d'Interface, Composants & Micro-Interactions (Other Elements) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Composants Sémantiques Clés

### 1.1 Badge d'Exécution d'Outil MCP (`ToolExecutionBadge.vue`)
Présent dans le fil de discussion pour assurer une traçabilité visuelle immédiate des requêtes :
- **Structure :**
  - Icône chevron déroulable + Nom technique de l'outil (ex: `erp.factures.query`).
  - Statut d'exécution (`ok`, `partial`, `error`) avec code couleur associé (vert `#10B981`, orange `#F59E0B`, rouge `#EF4444`).
  - Latence mesurée en millisecondes (ex: `142ms`, `210ms`).
  - Résumé textuel concis (ex: `statut=impayé ET retard_jours>30 → 12 comptes, 37 factures`).
- **Comportement au clic :** Déplie une vue modale ou tiroir affichant les arguments d'entrée JSON et la réponse brute retournée par le serveur MCP.

---

### 1.2 Carte d'Action à Valider (`StagedActionCard.vue`)
Composant central de sécurité humaine garantissant le principe HITL :
- **En-tête de carte :**
  - Bandeau orange/ambre d'avertissement avec icône bouclier/attention.
  - Titre : `ACTION À VALIDER` + Pill `En attente`.
- **Corps :**
  - Titre principal de l'opération en gras (ex: *Envoyer une relance à 8 clients*).
  - Sous-titre explicatif (ex: *L'agent a ciblé les factures échues de plus de 30 jours sans litige ouvert.*).
  - Grille récapitulative à 3 colonnes :
    - **Destinataires :** Nombre de contacts ciblés (ex: *8 contacts*).
    - **Type :** Typologie d'opération (ex: *Relance facture*).
    - **Canal :** Canal d'expédition (ex: *Email*).
- **Avertissement de Conséquence (Callout Conséquence) :**
  - Fond pastel orangé `#FFFBEB` avec bordure `#FDE68A`.
  - Texte explicite : *"Conséquence : les messages seront envoyés aux contacts financiers. Action externe irréversible."*
- **Boutons d'Action :**
  - Bouton primaire : `Valider et exécuter` (Fond bleu cyan `#06B6D4` en mode console ou violet `#4F46E5` en mode OpérIA).
  - Bouton secondaire : `Refuser` (Bordure neutre, texte rouge ou gris ardoise).
  - Bouton optionnel : `Examiner` / `Voir les détails` pour ouvrir la prévisualisation du contenu.

---

### 1.3 Badges de Statut (Status Pills)

| Statut | Pictogramme | Couleurs (Texte / Fond) | Exemple d'Usage |
| :--- | :---: | :--- | :--- |
| **En attente** | Horloge 🕒 | `#D97706` / `#FEF3C7` | Actions dans la file, validations requises |
| **Terminé** | Coche ✔ | `#059669` / `#D1FAE5` | Actions exécutées, sources synchronisées |
| **Approuvé** | Coche double ✔✔ | `#059669` / `#D1FAE5` | Action validée en attente d'envoi batch |
| **En cours** | Cercle rotatif ⟳ | `#2563EB` / `#DBEAFE` | Tâche d'arrière-plan ou sync messagerie |
| **Échec** | Croix ✖ | `#DC2626` / `#FEE2E2` | Échec de connexion ou d'envoi |

---

## 2. Micro-Interactions & États

1. **Badge dynamique de la barre latérale :**
   - L'item de menu `Opérations` arbore une pastille orange `[7]` qui s'actualise sans rechargement de page dès qu'une nouvelle action préparée est générée.
2. **Indicateur de statut agent :**
   - En bas à gauche du menu latéral : pastille verte pulsante `● Agent opérationnel`.
   - Si un connecteur critique est hors service, la pastille passe au jaune `● Mode dégradé` ou au rouge `● Maintenance requise`.
3. **Barre de saisie du chat :**
   - Mention discrète sous l'input : `🛡 Validation requise avant toute action sensible`.
   - Bouton d'envoi violet avec flèche incurvée réactive à la touche `Entrée`.

---

## 3. Accessibilité & Normes RGAA / WCAG 2.1 AA

- **Ratios de contraste :** Minimum 4.5:1 pour tous les textes fonctionnels et 3:1 pour les composants graphiques et bordures d'alerte.
- **Navigation au clavier :** Raccourci `Tab` séquentiel permettant d'accéder directement aux boutons *Valider* et *Refuser* sans recourir à la souris.
- **Rôles ARIA :**
  - `role="alert"` sur le bloc d'action à valider pour notification immédiate des lecteurs d'écran.
  - `aria-live="polite"` sur le flux de streaming des messages de l'agent.
