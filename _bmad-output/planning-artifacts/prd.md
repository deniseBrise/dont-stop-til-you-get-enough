---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-02b-vision
  - step-02c-executive-summary
  - step-03-success
  - step-04-journeys
  - step-05-domain
  - step-06-innovation
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
inputDocuments:
  - _bmad-output/project-context.md
workflowType: 'prd'
classification:
  projectType: web_app_streamlit
  domain: scientific_data
  complexity: medium
  projectContext: brownfield
---

# Product Requirements Document - dont-stop-til-you-get-enough

**Author:** Boss
**Date:** 2026-03-10

## Executive Summary

Outil d'exploration et d'analyse des jeux de hasard. Application Streamlit permettant de tester différents modèles de prédiction sur les jeux de hasard (Loto, Euromillion, ...), de les back-tester sur l'historique complet des tirages, et de comparer leur performance ROI.

Projet personnel motivé par la curiosité — démontrer que certains modèles peuvent être rentables OU prouver le contraire. Comparaison visuelle des modèles (Random, SameValue, extensibles) avec métriques détaillées par jeu.

## Project Classification

- **Type**: Web Application (Streamlit)
- **Domaine**: Data Science / Analyse statistique
- **Complexité**: Medium
- **Context**: Brownfield
- **Langues**: Français + English

## Success Criteria

### User Success

- L'application est facile à utiliser sans documentation
- Les comparaisons de modèles sont claires et visuelles
- L'utilisateur peut faire les analyses qu'il veut (paramètres flexibles)
- L'interface affiche différemment selon le jeu (Loto vs Euromillion)

### Technical Success

- Le code est simple et maintenable
- Les batchs peuvent être relancés après crash (SQLite, reprise)
- Les calculs parallèles fonctionnent (workers ajustables)
- Données automatiquement collectées (FDJ) et parsées

### Measurable Outcomes

- Téléchargement des données historiques fonctionnel pour Loto et Euromillion
- Backtest complet sur l'historique avec 2 modèles minimum
- Comparaison visuelle des résultats (ROI, gains, bons numéros)
- Cache SQLite persisté et crash-safe

## Product Scope

### MVP

- 2 jeux : Loto, Euromillion
- 2 modèles : Random, SameValue
- Téléchargement automatique des données FDJ (CSV)
- Mode backtest et prédiction (paramètre du jeu)
- Backtest sur historique + prédiction sur prochains tirages
- Comparaison des modèles avec métriques (ROI, gains, bons numéros)
- Cache SQLite pour reprise après crash
- Parallélisation des calculs (workers CPU)
- Arrêt propre des batchs en cours

### Phase 2

- Plus de jeux de hasard
- Plus de modèles de prédiction
- Visualisations avancées (graphiques, heatmaps)
- Export des résultats

## User Journeys

### Parcours 1 : Premier lancement

1. Ouvre l'app → sélectionne "Loto"
2. Configure les paramètres du jeu (itérations, tirages, grilles, options, mode)
3. Configure le modèle (Random ou SameValue avec ses paramètres)
4. Lance le(s) batch → voit les résultats

### Parcours 2 : Comparaison de modèles

1. Configure paramètres du jeu + modèle 1 → lance batch → résultats
2. Configure modèle 2 → lance batch → résultats
3. Compare les résultats

### Parcours 3 : Batch processing long

1. Configure un batch (ranges de paramètres) → lance
2. Batch en cours → peut arrêter proprement
3. L'app crash/reboot → reprend là où ça s'est arrêté
4. Retourne voir les résultats

## Domain-Specific Requirements

### Technical Constraints

- **SQLite**: Stockage local, un fichier à sauvegarder/copier-coller pour reprise
- **Licence**: MIT
- **Données**: Scraping manuel (rate limit incombe à l'utilisateur), fallback téléchargement manuel à prévoir

### Real-Time Features

- Progression visible en direct pendant les batchs
- Résultats et comparaisons mis à jour en live à chaque prédiction

### Browser Support

- Chrome, Firefox, Safari, Edge

## Functional Requirements

### FR1: Jeu - Gestion des jeux

- FR1: L'utilisateur peut sélectionner un jeu (Loto, Euromillion)
- FR2: L'utilisateur peut configurer les paramètres du jeu (itérations, tirages, grilles, options, mode, 2nd tirage, joker+, ...)

### FR2: Modèle - Gestion des modèles

- FR3: L'utilisateur peut sélectionner un modèle de prédiction (Random, SameValue, ...)
- FR4: L'utilisateur peut configurer les paramètres du modèle
- FR5: L'utilisateur peut ajouter de nouveaux modèles à prédire avec leurs paramètres respectifs

### FR3: Données - Gestion des données

- FR6: L'application peut télécharger automatiquement les données FDJ
- FR7: L'application peut parser les fichiers CSV des tirages
- FR8: L'utilisateur peut fournir les données manuellement (fallback)
- FR9: L'application affiche la date du dernier téléchargement
- FR10: L'application notifie si de nouvelles données sont disponibles

### FR4: Batch Processing

- FR11: L'utilisateur peut lancer un batch avec des ranges de paramètres
- FR12: L'application affiche dans une même vue : workers + batches en cours + progression
- FR13: L'utilisateur peut arrêter tous les batches en cours
- FR14: L'application peut reprendre les batches arrêtés par l'utilisateur ou après un crash

### FR5: Résultats & Comparaison

- FR15: L'application affiche la progression en direct
- FR16: L'application met à jour les résultats en live
- FR17: L'utilisateur peut comparer les résultats de plusieurs batchs/prédictions
- FR18: L'utilisateur peut trier et filtrer les batchs et résultats
- FR19: L'application calcule les métriques (ROI, gains, bons numéros)

### FR6: Configuration Système

- FR20: L'utilisateur peut ajuster le nombre de workers en live
- FR21: L'application persiste les données en SQLite
- FR22: L'utilisateur peut copier-coller la BDD pour reprise

## Non-Functional Requirements

### Performance

- Batch processing : les calculs s'affichent à chaque itération (mise à jour < 1 seconde entre chaque prédiction)
- Progression live : progression mise à jour toutes les 500ms

### Reliability

- Les données SQLite sont préservées après crash (atomic writes, WAL mode)
- Reprise après crash : toutes les données de batchs en cours sont sauvegardées en base
- Gestion des erreurs réseau lors du scraping : retry automatique avec backoff exponentiel (3 tentatives)

### Maintainability

- Code simple et documenté (docstrings, commentaires pour les fonctions complexes)
- Structure claire pour ajouter de nouveaux jeux/modèles (architecture modulaire)
