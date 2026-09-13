# SPECS — dont-stop-til-you-get-enough

> ## Source de vérité
> Ce document est la **référence unique** du projet. Il ne peut être modifié
> **qu'avec l'approbation explicite du Boss**. Toute décision de conception,
> exigence ou contrainte doit y être consignée avant implémentation.
>
> - **Langue du document :** français. Le code (identifiants, commentaires,
>   docstrings) est en **anglais** — voir `AGENTS.md`.
> - **Suivi des développements :** voir `IMPLEMENTATION.md`.
> - **Licence du projet :** MIT.
> - **Dépendances :** libres / open-source uniquement — **aucune licence payante**.

| Métadonnée | Valeur |
|------------|--------|
| Auteur | Boss (avec assistance) |
| Date de création | 2026-09-13 |
| Version | 0.1.0 (initiale — from scratch) |
| Statut | Établi · modifiable sur approbation explicite |
| Type | Application web (Dash / Plotly) |
| Domaine | Data science · analyse statistique des jeux de hasard |
| Cible | Grand public |

---

## 1. Vision & objectifs

Outil d'exploration, d'analyse et de simulation des **jeux de hasard**. Le projet
repose sur **trois piliers** complémentaires :

1. **Backtester des modèles de prédiction** — rejouer des stratégies sur un
   historique (réel ou simulé) et mesurer leur performance.
2. **Aider à jouer** — proposer des grilles / numéros / stratégies à jouer,
   en s'appuyant sur l'analyse et les modèles.
3. **Analyse statistique pure** — explorer et visualiser les données (fréquences,
   écarts, distributions, graphiques).

**Démarche :** projet personnel motivé par la curiosité — démontrer que certains
modèles peuvent être rentables, **ou prouver le contraire**. Les résultats sont
présentés de façon neutre et factuelle.

> Le projet ne prétend **pas** garantir de gains. Les jeux de hasard restent
> dominés par l'aléa ; l'outil vise à le **mesurer**, pas à le vaincre.

---

## 2. Public cible & critères de succès

### Public cible

**Grand public** : utilisateurs non techniques. L'application doit être :

- utilisable **sans documentation** ni connaissances en programmation ;
- **visuelle** et claire (graphiques, tableaux lisibles) ;
- **robuste** (pas de perte de données, pas de messages d'erreur techniques bruts).

### Critères de succès

**Expérience utilisateur**

- Prise en main immédiate : le parcours est guidé jeu par jeu.
- Comparaisons de modèles claires et visuelles.
- Paramétrage flexible sans être intimidant.
- Interface disponible en **français et en anglais**.

**Technique**

- Architecture **modulaire** : ajouter un jeu ou un modèle = déposer un fichier.
- Code simple, typé, documenté, testé.
- Batchs **résilients** : reprise après crash, arrêt propre.
- Données collectées automatiquement (loteries) ou générées (video poker).

**Résultats mesurables**

- Les 3 jeux du MVP fonctionnent de bout en bout.
- Backtest complet sur historique (loteries) / sur données simulées (video poker).
- Comparaison visuelle des résultats (métriques par jeu).
- Persistance SQLite fiable et crash-safe.

---

## 3. Périmètre

### MVP

| Axe | Contenu |
|-----|---------|
| **Jeux** | Loto (FDJ), Euromillion (FDJ), Video Poker (Jacks or Better) |
| **Modèles** | Aléatoire (Random), Valeur fixe (Fixed Value), Fréquences / chauds-froids |
| **Piliers** | Backtest · Aide au jeu · Analyse statistique |
| **Moteur** | Batch complet : itérations, ranges, parallélisme, reprise crash, arrêt propre |
| **Données** | FDJ : téléchargement auto + import manuel (fallback). Video Poker : génération aléatoire paramétrable |
| **Persistance** | SQLite (fichier local, mode WAL) |
| **UI** | Dash (Plotly) : dashboard, parcours par jeu, gros tableaux (AG Grid Community), graphiques |
| **i18n** | Français + anglais (extensible) |

### Hors MVP (phases ultérieures)

- Davantage de jeux et de modèles (l'architecture le permet déjà).
- Visualisations avancées (heatmaps, animations).
- Export des résultats (formats à décider).
- Langues supplémentaires.
- Déploiement/hébergement grand public (packaging, distribution).

---

## 4. Jeux

### 4.1 Architecture « jeu = plugin »

Chaque jeu est **auto-porteur** et défini dans **un fichier séparé**. L'application
**découvre automatiquement** les jeux disponibles (auto-découverte *drop-in* :
déposer un fichier conforme dans le dossier `games/` suffit à rendre le jeu
disponible, sans configuration).

Un fichier de jeu déclare au minimum :

| Élément | Rôle |
|---------|------|
| Identité | clé unique, noms localisés (FR/EN), logo, description, version |
| Règles | structure du tirage (plages de numéros, compléments, etc.) |
| Paramètres | options configurables par l'utilisateur (et leurs valeurs par défaut) |
| Calcul des gains | barème / table de paiement |
| **Métriques** | indicateurs pertinents **propres au jeu** (voir § 10) |
| **Parcours UI** | étapes/pages de configuration et de résultat **propres au jeu** |
| Source de données | historique (FDJ) ou génération (video poker) |
| Signature | interface/signature que les modèles doivent satisfaire pour être détectés compatibles |

> Conséquence clé : **le parcours utilisateur peut différer d'un jeu à l'autre**,
> car il est défini par le jeu lui-même. Le dashboard se contente de lister les
> jeux ; chacun pilote ensuite son propre enchaînement d'écrans.

### 4.2 Loto (FDJ)

- **Tirage :** 5 numéros sur 1–49 + 1 numéro complémentaire sur 1–10.
- **Variantes / options :** 2nd tirage, Joker+ ; variantes de mise (Loto, Grand-Loto,
  Super-Loto) — modélisation exacte à trancher (voir § 18).
- **Paramètres utilisateur :** nombre de grilles, options (2nd tirage, Joker+),
  plage de tirages historiques (dates), mise.
- **Données :** historique officiel FDJ (téléchargement auto + import manuel).
- **Métriques typiques :** ROI, gains/coûts totaux, bons numéros (min/max/moy).

### 4.3 Euromillion (FDJ)

- **Tirage :** 5 numéros sur 1–50 + 2 étoiles sur 1–12.
- **Options :** Étoile+.
- **Paramètres utilisateur :** nombre de grilles, option Étoile+, plage de tirages
  historiques (dates), mise.
- **Données :** historique officiel FDJ (téléchargement auto + import manuel).
- **Métriques typiques :** ROI, gains/coûts totaux, bons numéros + étoiles (min/max/moy).

### 4.4 Video Poker — Jacks or Better

- **Principe :** une main de 5 cartes est distribuée ; le joueur choisit quelles
  cartes **garder** ; les cartes remplacées sont tirées ; le gain suit la **table
  de paiement**.
- **Variante MVP :** **Jacks or Better** (table « full-pay » 9/6 indicative) :

| Main | Paiement (× mise, 1 crédit) |
|------|------------------------------|
| Quinte flush royale | 250 |
| Quinte flush | 50 |
| Carré | 25 |
| Full | 9 |
| Couleur | 6 |
| Quinte | 4 |
| Brelan | 3 |
| Double paire | 2 |
| Paire de valets ou mieux | 1 |
| Autre | 0 |

- **Pas d'historique de tirages** : chaque main est aléatoire. L'outil **génère des
  données aléatoires** (nombre de mains/tirages **paramétrable**) pour simuler.
- **« Modèle » pour ce jeu** = une **stratégie de conservation** (quelles cartes
  garder selon la main). Ex. stratégie optimale, « toujours garder une paire », etc.
- **« Backtest » pour ce jeu** = **simulation Monte-Carlo** de N mains pour estimer
  le retour et la variance.
- **Métriques typiques :** RTP (%), variance, fréquence des mains, gains/coûts totaux.

---

## 5. Modèles de prédiction

### 5.1 Architecture « modèle = plugin »

Chaque modèle est défini dans **un fichier séparé** et **auto-découvert**
(*drop-in* dans le dossier `models/`). Les modèles sont compatibles avec un jeu via un simple **test de signature** (chaque jeu expose une signature/interface ; tout modèle qui la satisfait est détecté compatible) :
on peut ajouter autant de modèles qu'on veut **pour un jeu donné**. L'application ne propose que les modèles **compatibles** avec le jeu sélectionné.

Un fichier de modèle déclare au minimum :

| Élément | Rôle |
|---------|------|
| Identité | clé unique, noms localisés (FR/EN), description, version |
| Paramètres | options configurables (et valeurs par défaut) |
| Algorithme | la logique de prédiction / de stratégie |

### 5.2 Modèles du MVP

| Clé (code) | Nom FR | Nom EN | Principe | Paramètres |
|------------|--------|--------|----------|------------|
| `random` | Aléatoire | Random | Tirage aléatoire (référence / *baseline*) | `seed` (timestamp ou valeur fixe) |
| `fixed_value` | Valeur fixe | Fixed Value | Joue toujours les mêmes numéros/cartes | les numéros/cartes choisis |
| `frequency` | Fréquences / chauds-froids | Frequencies / hot-cold | Choisit selon les statistiques des tirages passés (numéros les plus/moins sortis) | fenêtre d'analyse, chauds/froids/équilibré |

> Pour le **Video Poker**, les « modèles » sont des **stratégies de conservation**
> (voir § 4.4) ; les trois modèles ci-dessus s'appliquent principalement aux loteries.
> Les modèles compatibles sont **détectés** par chaque jeu (test de signature).

---

## 6. Exigences fonctionnelles (FR)

### A. Navigation & dashboard

| ID | Exigence |
|----|----------|
| FR1 | Le dashboard affiche la liste des jeux disponibles (avec logo), issus de l'auto-découverte. |
| FR2 | L'utilisateur sélectionne un jeu ; l'app enchaîne sur le **parcours défini par ce jeu**. |
| FR3 | L'interface est disponible en **français et anglais** (bascule de langue), extensible. |

### B. Jeux (plugins)

| ID | Exigence |
|----|----------|
| FR4 | Chaque jeu est défini dans un fichier séparé et **auto-découvert** (drop-in). |
| FR5 | Chaque jeu déclare règles, paramètres, calcul des gains, métriques, parcours UI, source de données et détecte les modèles compatibles. |
| FR6 | L'utilisateur configure les paramètres du jeu (spécifiques à chaque jeu). |
| FR7 | Jeux du MVP : Loto, Euromillion, Video Poker (Jacks or Better). |

### C. Modèles (plugins)

| ID | Exigence |
|----|----------|
| FR8 | Chaque modèle est défini dans un fichier séparé et **auto-découvert** (drop-in). |
| FR9 | Les modèles sont associés aux jeux ; seuls les modèles **compatibles** sont proposés pour le jeu choisi. |
| FR10 | L'utilisateur configure les paramètres du modèle. |
| FR11 | Modèles du MVP : Aléatoire, Valeur fixe, Fréquences / chauds-froids. |

### D. Backtest & batchs

| ID | Exigence |
|----|----------|
| FR12 | L'utilisateur lance un batch : jeu + configuration + modèle + N itérations. |
| FR13 | Un paramètre fourni en **range** (ou choix multiple) génère **1 batch par valeur**. |
| FR14 | Les calculs sont **parallélisés** (workers CPU ajustables). |
| FR15 | La **progression** et les **résultats** s'affichent en **live**. |
| FR16 | L'utilisateur peut **arrêter proprement** les batchs en cours. |
| FR17 | L'app **reprend** les batchs après un arrêt ou un **crash** (depuis le dernier point stable). |
| FR18 | Chaque batch a un **ID unique** auto-incrémenté. |

### E. Aide au jeu

| ID | Exigence |
|----|----------|
| FR19 | L'app propose des grilles/numéros à jouer selon un modèle et/ou l'analyse (pilier « aide au jeu »). |
| FR20 | Pour le Video Poker, l'app propose la **stratégie de conservation** (quelles cartes garder). |

### F. Analyse statistique

| ID | Exigence |
|----|----------|
| FR21 | L'app affiche des analyses statistiques des données (fréquences, écarts, distributions). |
| FR22 | L'app fournit des **graphiques interactifs** (Plotly) et des **gros tableaux** (AG Grid Community). |

### G. Données

| ID | Exigence |
|----|----------|
| FR23 | Téléchargement **automatique** des historiques FDJ (Loto, Euromillion) + parsing. |
| FR24 | **Import manuel** (upload CSV) en secours si le téléchargement échoue. |
| FR25 | **Génération de données aléatoires** pour le Video Poker (nombre de mains paramétrable). |
| FR26 | **Retry réseau** (avec backoff) en cas d'échec de téléchargement. |
| FR27 | L'app affiche la date du dernier téléchargement et signale si de nouvelles données sont disponibles. |

### H. Résultats & comparaison

| ID | Exigence |
|----|----------|
| FR28 | L'app affiche les **métriques** d'un batch (spécifiques au jeu). |
| FR29 | L'utilisateur **compare** plusieurs batchs/modèles. |
| FR30 | L'utilisateur **trie, filtre et regroupe** les batchs et résultats. |
| FR31 | Les résultats sont présentés en gros tableaux + graphiques associés. |

### I. Persistance & configuration

| ID | Exigence |
|----|----------|
| FR32 | Les données sont persistées en **SQLite** (mode WAL, crash-safe). |
| FR33 | L'utilisateur ajuste le **nombre de workers** en live. |
| FR34 | La configuration passe par `.env` (aucune valeur en dur, aucun secret commité). |

---

## 7. Moteur de backtest & batchs

### 7.1 Définition d'un batch

Un **batch** = une exécution combinant :

- 1 **jeu** (et sa configuration : grilles, dates, options, …) ;
- 1 **modèle** (et ses paramètres) ;
- **N itérations** appliquées.

Règles :

- **Ranges** : un paramètre en range / choix multiple → **1 batch par valeur**.
- **ID** : entier unique auto-incrémenté.
- Paramètres identiques ≠ regroupement automatique.

### 7.2 Itérations

- Paramètre général (stepper) à côté du bouton « Lancer ».
- Pour les **loteries** : chaque itération rejoue le modèle sur l'historique.
- Pour le **Video Poker** : chaque itération simule des mains générées aléatoirement.

### 7.3 Parallélisme

- Calculs répartis sur des **workers CPU** (`ProcessPoolExecutor`).
- Nombre de workers **ajustable en live** (le comportement exact au changement —
  redémarrage de l'itération courante ou du batch — est à préciser, voir § 18).

### 7.4 Résilience

- **Reprise après crash** : l'état des batchs (itérations complétées) est persisté
  en SQLite ; au démarrage, les batchs non terminés repartent du dernier point stable.
- **Arrêt propre** : l'utilisateur peut stopper les batchs sans corrompre les données.

### 7.5 Temps réel

- Progression et résultats remontés en **live** vers l'UI (principe : quasi temps
  réel ; les valeurs précises de fréquence de rafraîchissement sont décidées à
  l'implémentation — voir § 13).

---

## 8. Données

### 8.1 Loteries (Loto, Euromillion)

- **Source principale :** historiques officiels **FDJ** (téléchargement automatique).
- **Secours :** **import manuel** (upload de fichiers CSV) si le téléchargement échoue.
- **Robustesse réseau :** retry avec backoff (voir § 13).
- **Responsabilité :** le scraping/téléchargement et le respect du rate-limit
  incombent à l'utilisateur ; l'outil fournit le fallback manuel.
- **Transparence :** date du dernier téléchargement affichée ; notification si de
  nouvelles données sont disponibles.

### 8.2 Video Poker

- **Aucun historique** (mains aléatoires indépendantes).
- L'outil **génère** les données : nombre de mains/tirages **paramétrable**.
- La génération alimente la simulation Monte-Carlo (RTP, variance, fréquence des mains).

---

## 9. Persistance (SQLite)

- **Stockage :** fichier SQLite **local** (un seul fichier à sauvegarder/copier).
- **Mode WAL** + écritures atomiques → résistance aux crashes, lecture pendant écriture.
- **Reprise :** l'état des batchs (`status`, `completed_iterations`) porte la reprise après crash.

### 9.1 Schéma indicatif

> Schéma **générique** pour supporter plusieurs jeux et des métriques par jeu.
> Les détails fins (colonnes exactes, types) sont affinés à l'implémentation
> (suivi dans `IMPLEMENTATION.md`).

| Table | Rôle | Colonnes clés (indicatif) |
|-------|------|---------------------------|
| `games` | Jeux disponibles (auto-découverts) | `key` (unique), `name_fr`, `name_en`, `type` |
| `draws` | Historique / données de tirage | `game_id`, `draw_date`, `numbers`, `extra_numbers`, `jackpot`, `source` (fdj/manual/generated) |
| `models` | Modèles disponibles | `key` (unique), `name_fr`, `name_en`, `description` |
| `model_params` | Paramètres de modèle | `model_id`, `param_key`, `param_value` |
| `batches` | Exécutions | `game_id`, `model_id`, `game_params`, `model_params`, `status`, `total_iterations`, `completed_iterations`, `created_at` |
| `batch_results` | Résultat par itération | `batch_id`, `iteration`, `ref` (date/main), `prediction`, `outcome`, `gain`, `cost` |
| `batch_metrics` | Métriques **par jeu** (clé/valeur) | `batch_id`, `metric_key`, `metric_value` |

- `batch_metrics` en **clé/valeur** permet à chaque jeu de définir ses propres
  indicateurs sans schéma rigide.
- Index prévus sur `draws(game_id, draw_date)`, `batch_results(batch_id)`, `batches(status)`.

---

## 10. Métriques

Les **métriques sont définies par jeu** (chaque jeu déclare ses indicateurs
pertinents). L'outil affiche, au minimum :

**Loteries (Loto, Euromillion)**

| Métrique | Description |
|----------|-------------|
| ROI (%) | `(gains − coûts) / coûts × 100` |
| Gains totaux | Somme des gains |
| Coût total | Somme des coûts (grilles + options) |
| Bons numéros (min/max/moy) | Nombre de numéros corrects par itération |

**Video Poker (Jacks or Better)**

| Métrique | Description |
|----------|-------------|
| RTP (%) | Retour théorique au joueur (gains / mises) |
| Variance | Dispersion des gains (volatilité) |
| Fréquence des mains | Distribution des mains obtenues |
| Gains / coûts totaux | Sommes cumulées |

> D'autres indicateurs pertinents peuvent être ajoutés par jeu (ex. écart max,
> fréquence de sortie, distribution des gains). Chaque jeu en est responsable.

---

## 11. Interface utilisateur (Dash / Plotly)

### 11.1 Structure générale

- **Dashboard d'accueil** : liste des jeux **avec logos** (jeux auto-découverts).
- **Parcours par jeu** : défini **dans le fichier du jeu** (peut différer d'un jeu
  à l'autre). Enchaîne configuration → lancement → résultats.
- Accès aux **trois piliers** (backtest, aide au jeu, analyse) selon le jeu.

### 11.2 Composants UI

- **Gros tableaux de données** : AG Grid **Community** (gratuit) via Dash — tri,
  filtres, pagination/virtualisation pour gros volumes.
- **Graphiques interactifs** : Plotly (open-source).
- **Progression live** : barre de progression + résultats mis à jour en continu.
- **Sélecteur de langue** : français / anglais.

### 11.3 Principes UX (grand public)

- Lisibilité avant tout ; pas de jargon technique exposé.
- Jamais de stack trace à l'utilisateur (messages lisibles + journalisation interne).
- Parcours guidé, valeurs par défaut pertinentes.

---

## 12. Architecture

### 12.1 Stack

| Élément | Choix | Licence |
|---------|-------|---------|
| Langage | Python ≥ 3.13 | — |
| UI / graphiques | **Dash + Plotly** (open-source) | MIT |
| Tableaux | **AG Grid Community** (via `dash-ag-grid`) | MIT |
| Stockage | **SQLite** (raw SQL + wrappers, pas d'ORM) | Domaine public |
| Parallélisme | `concurrent.futures.ProcessPoolExecutor` | stdlib |
| i18n | mécanisme de localisation FR/EN (extensible) | — |
| Packaging | uv | MIT/Apache |
| Tests | pytest | MIT |
| Lint / format | ruff | MIT |

> **Contrainte ferme :** uniquement des composants **libres / open-source**,
> **aucune licence payante** (pas d'AG Grid Enterprise, pas de Dash Enterprise, etc.).

### 12.2 Structure cible

```
dont-stop-til-you-get-enough/
├── SPECS.md              # Source de vérité (ce fichier)
├── IMPLEMENTATION.md     # Suivi détaillé des développements
├── AGENTS.md             # Fonctionnement & conventions pour agents
├── README.md             # (à créer) présentation — en français
├── LICENSE               # MIT
├── pyproject.toml / uv.lock
├── .env / .env.example
│
├── src/
│   ├── app.py            # Application Dash (point d'entrée)
│   ├── games/            # 1 fichier par jeu (loto.py, euromillion.py, video_poker.py) + base
│   ├── models/           # 1 fichier par modèle (random.py, fixed_value.py, frequency.py) + base
│   ├── data/             # téléchargement FDJ, parsing, import manuel, génération video poker
│   ├── batch/            # moteur de batch, workers, état/reprise
│   ├── db/               # connexion SQLite, schéma, requêtes, migrations
│   ├── ui/               # dashboard, parcours par jeu, composants (tables, graphs), i18n
│   └── utils/            # logging, helpers
│
├── assets/               # logos/ressources libres de droits
├── tests/                # test_games/, test_models/, test_data/, test_batch/, test_db/
└── data/                 # (hors git) database.db, downloads/
```

### 12.3 Auto-découverte (drop-in)

- Au démarrage, l'app **scanne** `src/games/` et `src/models/`.
- Tout fichier conforme (respectant l'interface de base) est **enregistré** comme
  jeu/modèle disponible — **sans modification d'un fichier central**.
- Chaque jeu détecte quels modèles sont compatibles ; l'UI filtre en conséquence.

### 12.4 Flux de données

```
Dashboard (choix du jeu)
      ↓
Parcours du jeu  →  Config jeu  →  Config modèle  →  Moteur de batch
                                                          ↓
                                              ProcessPoolExecutor (workers)
                                                          ↓
                              Données (FDJ / générées) → Résultats → SQLite → UI (tables + graphs)
```

**Points d'intégration :** Jeu + Modèle = prédiction/stratégie · Batch + DB =
persistance d'état · UI + Batch = progression temps réel · Data + DB = stockage.

---

## 13. Exigences non fonctionnelles (NFR)

> Les **principes** sont fixés ; les **valeurs chiffrées** précises (fréquences de
> rafraîchissement, nombre de tentatives, délais) sont décidées à l'implémentation
> et consignées dans `IMPLEMENTATION.md`.

### Performance

- **Résultats en live** : pendant un batch, les résultats s'affichent au fur et à
  mesure (quasi temps réel).
- **Progression fluide** : la progression est rafraîchie régulièrement.
- Gros volumes : tableaux et graphiques doivent rester réactifs (virtualisation AG Grid).

### Fiabilité

- **Anti-crash** : SQLite en mode **WAL**, écritures atomiques ; aucune corruption
  ni perte de données en cas de crash.
- **Reprise** : tout batch interrompu reprend depuis le dernier point stable.
- **Robustesse réseau** : **retry avec backoff** lors des téléchargements FDJ.

### Maintenabilité & extensibilité

- Code simple, typé, documenté.
- Architecture modulaire : ajouter un jeu/modèle = déposer un fichier.
- Séparation claire des responsabilités (games / models / data / batch / db / ui).

### Accessibilité & UX

- Utilisable sans documentation (grand public).
- Messages d'erreur lisibles ; jamais de stack trace exposée.
- Interface localisée FR/EN.

---

## 14. Contraintes

- **Langage :** Python (≥ 3.13).
- **UI :** application **graphique**, user-friendly, à l'aise avec les **gros
  tableaux de données** et les **graphiques associés** → Dash/Plotly + AG Grid Community.
- **Licences :** **aucune licence payante** ; dépendances et assets **libres/open-source**.
- **Stockage :** **SQLite** local (un fichier à sauvegarder/copier).
- **Données FDJ :** téléchargement/scraping ; rate-limit sous responsabilité de
  l'utilisateur ; fallback manuel obligatoire.
- **i18n :** français + anglais, extensible.
- **Langues du projet :** code/commentaires en **anglais** ; documentation
  (`SPECS.md`, `AGENTS.md`, `IMPLEMENTATION.md`, `README.md`) en **français**.

---

## 15. Conventions de développement

> Détail complet et règles pour les agents dans `AGENTS.md`. Résumé ici.

### Nommage

| Élément | Convention | Exemple |
|---------|-----------|---------|
| Modules | `snake_case` | `video_poker.py`, `fixed_value.py` |
| Classes | `PascalCase` | `LotoGame`, `RandomModel` |
| Fonctions / variables | `snake_case` | `calculate_roi` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_WORKERS` |
| Tables SQL | `snake_case` pluriel | `games`, `batch_results` |
| Index | `idx_table_colonne` | `idx_draws_game_date` |
| Tests | `test_*.py` | `test_batch.py` |

### Python

- **Type hints** sur toutes les signatures de fonctions.
- PEP 8, f-strings, `dataclasses` pour les structures simples.
- **Imports absolus** dans le package.
- Docstrings sur toutes les fonctions publiques.
- Éviter l'opérateur walrus (`:=`) pour la clarté.

### Gestion d'erreurs

- Exceptions personnalisées par module (`DataDownloadError`, `BatchProcessingError`, …).
- Logger l'erreur + message lisible pour l'utilisateur ; jamais de stack trace exposée.

### Configuration

- Toute la config via `.env` (`os.getenv()` / `python-dotenv`) ; aucun secret commité.

### Tests

- Dans `tests/`, pattern `test_*.py`, fixtures pytest.
- Objectif : bonne couverture des modules critiques (games, models, batch, db).

### Workflow

- Branches : préfixes `feature/`, `bugfix/`, `hotfix/`, `flush/`.
- Commits : **conventional commits** (`feat:`, `fix:`, `docs:`, `chore:`, `test:`).
- `ruff check .` et `ruff format .` avant commit.
- Pas de `print` de debug ; pas de TODO sans référence.

### Langues

- **Code** (identifiants, commentaires, docstrings) : **anglais**.
- **Documentation** (`SPECS.md`, `AGENTS.md`, `IMPLEMENTATION.md`, `README.md`) : **français**.
- **UI** : chaînes localisées FR/EN.

---

## 16. User stories (Epics)

### Epic 1 — Navigation & jeux

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US1.1 | Voir la liste des jeux sur le dashboard | Jeux auto-découverts, affichés avec logos |
| US1.2 | Sélectionner un jeu et suivre son parcours | Le parcours est celui défini par le jeu |
| US1.3 | Basculer la langue FR/EN | Toute l'UI est traduite |

### Epic 2 — Configuration des modèles

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US2.1 | Choisir un modèle compatible avec le jeu | Seuls les modèles compatibles sont proposés |
| US2.2 | Configurer les paramètres du modèle | Paramètres et valeurs par défaut du modèle |

### Epic 3 — Backtest & batchs

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US3.1 | Lancer un batch | Jeu + config + modèle + N itérations ; ID unique ; ranges → plusieurs batchs |
| US3.2 | Voir la progression et les résultats en live | Progression + résultats mis à jour en continu |
| US3.3 | Arrêter les batchs | Arrêt propre, sans corruption |
| US3.4 | Reprendre après crash | Reprise depuis le dernier point stable (SQLite) |
| US3.5 | Ajuster les workers en live | Le nombre de workers est modifiable |

### Epic 4 — Aide au jeu

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US4.1 | Obtenir des grilles/numéros suggérés | Suggestions selon modèle/analyse |
| US4.2 | Obtenir la stratégie Video Poker | Conservation optimale des cartes proposée |

### Epic 5 — Analyse & résultats

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US5.1 | Consulter les métriques d'un batch | Métriques propres au jeu |
| US5.2 | Comparer plusieurs batchs | Filtres, tris, group by ; gros tableaux + graphiques |
| US5.3 | Explorer les statistiques des données | Fréquences, écarts, graphiques interactifs |

### Epic 6 — Données

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US6.1 | Télécharger les historiques FDJ | Auto + parsing ; retry réseau |
| US6.2 | Importer des données manuellement | Upload CSV en secours |
| US6.3 | Générer les données Video Poker | Nombre de mains paramétrable |

---

## 17. Traçabilité

| Thème FR | Emplacement | Stories |
|----------|-------------|---------|
| FR1–FR3 — Navigation | `src/ui/` | US1.1–US1.3 |
| FR4–FR7 — Jeux | `src/games/` | US1.1–US1.2 |
| FR8–FR11 — Modèles | `src/models/` | US2.1–US2.2 |
| FR12–FR18 — Batch | `src/batch/`, `src/db/` | US3.1–US3.5 |
| FR19–FR20 — Aide au jeu | `src/games/`, `src/models/`, `src/ui/` | US4.1–US4.2 |
| FR21–FR22 — Analyse | `src/ui/` | US5.3 |
| FR23–FR27 — Données | `src/data/` | US6.1–US6.3 |
| FR28–FR31 — Résultats | `src/ui/`, `src/db/` | US5.1–US5.2 |
| FR32–FR34 — Persistance/Config | `src/db/`, `.env` | US3.4–US3.5 |

---

## 18. Points ouverts / à trancher

Ces points sont **volontairement** laissés ouverts ; ils seront tranchés (avec
approbation du Boss) avant ou pendant l'implémentation, et suivis dans
`IMPLEMENTATION.md` :

1. **Valeurs chiffrées des NFR** : fréquences de rafraîchissement (live, progression),
   nombre de tentatives et délais de retry réseau. → décidées à l'implémentation.
2. **Barèmes de gains des loteries** : grille exacte des rangs de gain (Loto,
   Euromillion) à spécifier précisément.
3. **Source FDJ exacte** : URL et format des historiques (CSV/JSON) à figer.
4. **Modélisation Grand-Loto / Super-Loto** : variantes de mise du Loto — jeu
   distinct, type, ou paramètre ?
5. **Changement de workers en live** : redémarrage de l'itération courante ou du
   batch entier ?
6. **Stratégies de Video Poker** : quelles stratégies fournies au MVP (optimale,
   simplifiées) et comment les définir.
7. **Mécanique d'auto-découverte** : convention d'interface exacte pour les fichiers
   de jeux/modèles (classe de base, métadonnées).
8. **Packaging/distribution grand public** : comment l'app est livrée/hébergée
   (hors MVP, mais à anticiper).
9. **Assets / logos** : provenance des logos de jeux (libres de droits) — éviter
   toute marque déposée sans droit.

---

*Fin du document — SPECS.md (source de vérité).*
