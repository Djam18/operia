# Sécurité, Confidentialité & Conformité (Security) — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Version :** 1.0.0  
**Date :** 18 Septembre 2026  

---

## 1. Modèle de Menace & Matrice des Risques

Dans un agent IA d'opérations métier connecté aux données financières et aux canaux de communication, les vecteurs d'attaque sont spécifiques :

| Risque | Scénario d'Attaque | Mesure de Défense OpérIA |
| :--- | :--- | :--- |
| **Injection Indirecte de Prompt (IPI)** | Un client véreux glisse un prompt malveillant dans l'objet d'une facture pour forcer un virement ou une suppression de compte. | **Cloisonnement strict :** Les données issues des outils MCP sont traitées comme du texte non fiable, et toute action modifiante reste bloquée par la validation humaine obligatoire. |
| **Exécution Non Autorisée d'Action** | Un bug de raisonnement du LLM ordonne l'envoi d'emails sans avertissement. | **Garde-fou au niveau du code (Hard Rule) :** Le backend FastAPI intercepte tout outil sensible et rend techniquement impossible son exécution sans signature de session utilisateur. |
| **Fuite de Données Personnelles** | Export massif ou inclusion de données confidentielles dans les prompts envoyés à des modèles tiers. | Masquage dynamique des PII (noms, IBAN, téléphones), chiffrement au repos AES-256 et contrats de non-conservation des données avec le fournisseur d'inférence. |
| **Usurpation d'Identité de Validation** | Rejeu de requête d'approbation d'action. | Jeton anti-CSRF, horodatage court et vérification des habilitations RBAC au moment du clic de validation. |

---

## 2. Architecture de Sécurité en Profondeur

```
[ Niveau 1 : Filtrage Réseau & WAF ]
         │
[ Niveau 2 : Authentification OAuth2 / JWT RS256 & RBAC ]
         │
[ Niveau 3 : Sanitization & Détection d'Injection de Prompt ]
         │
[ Niveau 4 : Orchestrateur Agentique & Garde-Fou HITL Inviolable ]
         │
[ Niveau 5 : Passerelle MCP Sandboxée (Permissions Read-Only granulaires) ]
         │
[ Niveau 6 : Journal d'Audit Immuable PostgreSQL (Append-Only) ]
```

---

## 3. Gestion des Identités & Habilitations (RBAC)

| Rôle | Consultation Dashboard / Chat | Exécution d'Outils Lecture | Validation Relance Standard (< 50 k€) | Validation Relance Majeure / Export Nominatif | Gestion des Paramètres & Connecteurs |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Opérateur Métier** | Oui | Oui | Oui | Non (Soumis à validation N+1) | Non |
| **Superviseur Métier** | Oui | Oui | Oui | Oui | Non |
| **Administrateur / DSI** | Oui | Oui | Oui | Oui | Oui |

---

## 4. Sécurisation du Protocole MCP

- **Pas d'accès direct à la base de données :** Le modèle n'a jamais accès à une chaîne de connexion SQL (`DATABASE_URL`). Il n'a connaissance que des signatures de fonctions exposées par les serveurs MCP.
- **Principe du Moindre Privilège :** Les comptes de service utilisés par les connecteurs de lecture disposent d'un compte de base de données en `SELECT` strict sur une vue restreinte, sans droit sur les tables de journalisation système ou de mots de passe.

---

## 5. Conformité Réglementaire & RGPD

1. **Minimisation des données :** Seules les colonnes strictement nécessaires à la question posée sont chargées dans le contexte LLM.
2. **Droit à l'oubli :** Les identifiants des clients sont anonymisables sur demande conformément à l'article 17 du RGPD sans casser l'intégrité référentielle des audits financiers.
3. **Localisation des données :** Hébergement des bases de données et des instances de traitement en Union Européenne (Région France / Allemagne, cloud qualifié SecNumCloud ou équivalent).
