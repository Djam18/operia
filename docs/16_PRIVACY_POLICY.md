# Politique de Confidentialité & Protection des Données Personnelles — OpérIA

**Système :** OpérIA (Agent IA d'Opérations Métier)  
**Conformité :** Règlement Général sur la Protection des Données (RGPD - UE 2016/679) & Loi Informatique et Libertés  
**Date d'entrée en vigueur :** 18 Septembre 2026  
**Version :** 1.0.0  

---

## 1. Préambule & Responsable du Traitement

La présente Politique de Confidentialité régit l'utilisation des données à caractère personnel dans le cadre du déploiement et du fonctionnement de la plateforme logicielle **OpérIA**.

Le responsable du traitement des données est l'entité cliente déployant la solution OpérIA pour ses opérations internes, assistée par les garde-fous techniques intégrés au système.

---

## 2. Principes Fondamentaux de Traitement

OpérIA a été conçu selon les principes de **Privacy by Design** et **Privacy by Default** :
1. **Minimisation des Données :** L'agent IA n'accède qu'aux attributs strictement nécessaires à la formulation des réponses et à la préparation des actions (ex: nom de l'entreprise, montant de la facture, adresse email professionnelle du contact financier).
2. **Cloisonnement des Données d'Apprentissage :** Aucune donnée client, financière ou opérationnelle n'est utilisée pour ré-entraîner les modèles de fondation ou partagée avec des tiers à des fins d'apprentissage.
3. **Contrôle Humain Systématique (Article 22 du RGPD) :** Aucune décision produisant des effets juridiques ou affectant de manière significative une personne physique n'est prise de manière exclusivement automatisée. Toute action d'envoi ou de mise à jour fait l'objet d'une validation humaine préalable.

---

## 3. Données Collectées & Traitées

- **Données d'identification des utilisateurs de la plateforme :** Nom, prénom, adresse email professionnelle, rôle organisationnel, adresse IP et logs d'activité.
- **Données métier traitées via les connecteurs MCP :**
  - Données clients et fournisseurs (Raison sociale, identifiant CRM, nom du contact désigné, email professionnel) ;
  - Données de facturation et commandes (Numéros de facture, montants dus, dates d'échéance, statuts d'expédition).
- **Journaux d'Audit :** Horodatage précis des requêtes, décisions d'approbation et traces de validation.

---

## 4. Finalités & Bases Légales

| Finalité du Traitement | Base Légale (RGPD Art. 6) | Durée de Conservation |
| :--- | :--- | :--- |
| **Gestion du recouvrement & relances** | Intérêt légitime de l'entreprise / Exécution contractuelle | Durée de la relation commerciale + 5 ans (prescription légale) |
| **Génération d'exports et de synthèses métier** | Intérêt légitime d'optimisation opérationnelle | Fichiers temporaires supprimés après 15 minutes ; logs conservés 12 mois |
| **Sécurité, prévention des fraudes et traçabilité d'audit** | Obligation légale et respect des normes de gouvernance financière | 5 ans |

---

## 5. Droits des Personnes Concernées

Conformément au RGPD, toute personne physique dispose des droits suivants :
- **Droit d'accès et de rectification** (Articles 15 et 16) ;
- **Droit à l'effacement (« droit à l'oubli »)** (Article 17) ;
- **Droit à la limitation du traitement** (Article 18) ;
- **Droit d'opposition** (Article 21) ;
- **Droit de ne pas faire l'objet d'une décision automatisée** (Article 22) : garanti par conception par la file de validation humaine obligatoire d'OpérIA.

Pour exercer ces droits, les personnes concernées peuvent s'adresser au Délégué à la Protection des Données (DPO) de l'organisation à l'adresse : `dpo@operia.corp`.
