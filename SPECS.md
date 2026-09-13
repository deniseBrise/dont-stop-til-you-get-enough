# SPECS — dont-stop-til-you-get-enough

**Auteur :** Boss · **Date de synthèse :** 2026-09-13 · **Licence :** MIT

Document de référence unique. Synthèse des artefacts de planification BMAD :
`_bmad-output/project-context.md`, `_bmad-output/planning-artifacts/{prd,architecture,user-stories,prd-validation-report}.md`.

---

## 1. Vision

Outil d'exploration et d'analyse des jeux de hasard. Application Streamlit permettant de :

- tester différents modèles de prédiction sur les jeux de hasard (Loto, Euromillion, …),
- les back-tester sur l'historique complet des tirages,
- comparer leur performance (ROI, gains, bons numéros).

Projet personnel motivé par la curiosité : démontrer que certains modèles peuvent être rentables **ou prouver le contraire**.

### Classification

| Aspect | Valeur |
|--------|--------|
| Type | Web Application (Streamlit) |
| Domaine | Data Science / Analyse statistique (`scientific_data`) |
| Complexité | Medium (non régulé) |
| Contexte | Brownfield |
| Langues | Français + English |
| Navigateurs | Chrome, Firefox, Safari, Edge |

---

## 2. Critères de succès

### Succès utilisateur

- L'application est facile à utiliser sans documentation.
- Les comparaisons de modèles sont claires et visuelles.
- L'utilisateur peut faire les analyses qu'il veut (paramètres flexibles).
- L'interface s'affiche différemment selon le jeu (Loto vs Euromillion).

### Succès technique

- Le code est simple et maintenable.
- Les batchs peuvent être relancés après crash (SQLite, reprise).
- Les calculs parallèles fonctionnent (workers ajustables).
- Données automatiquement collectées (FDJ) et parsées.

### Résultats mesurables

- Téléchargement des données historiques fonctionnel pour Loto et Euromillion.
- Backtest complet sur l'historique avec 2 modèles minimum.
- Comparaison visuelle des résultats (ROI, gains, bons numéros).
- Cache SQLite persisté et crash-safe.

---

## 3. Périmètre

### MVP

- 2 jeux : **Loto**, **Euromillion**
- 2 modèles : **Random**, **SameValue**
- Téléchargement automatique des données FDJ (CSV)
- Mode backtest et prédiction (paramètre du jeu)
- Backtest sur historique + prédiction sur prochains tirages
- Comparaison des modèles avec métriques (ROI, gains, bons numéros)
- Cache SQLite pour reprise après crash
- Parallélisation des calculs (workers CPU)
- Arrêt propre des batchs en cours

### Phase 2 (hors MVP)

- Plus de jeux de hasard
- Plus de modèles de prédiction
- Visualisations avancées (graphiques, heatmaps)
- Export des résultats (formats à décider)

---

## 4. Parcours utilisateur

### Parcours 1 — Premier lancement

1. Ouvre l'app → sélectionne « Loto »
2. Configure les paramètres du jeu (itérations, tirages, grilles, options, mode)
3. Configure le modèle (Random ou SameValue avec ses paramètres)
4. Lance le(s) batch → voit les résultats

### Parcours 2 — Comparaison de modèles

1. Configure paramètres du jeu + modèle 1 → lance batch → résultats
2. Configure modèle 2 → lance batch → résultats
3. Compare les résultats

### Parcours 3 — Batch processing long

1. Configure un batch (ranges de paramètres) → lance
2. Batch en cours → peut arrêter proprement
3. L'app crash / reboot → reprend là où ça s'est arrêté
4. Retourne voir les résultats

---

## 5. Exigences fonctionnelles

22 FR réparties en 6 catégories.

### FR-1 · Jeu — Gestion des jeux → `src/games/`

| ID | Exigence |
|----|----------|
| FR1 | L'utilisateur peut sélectionner un jeu (Loto, Euromillion) |
| FR2 | L'utilisateur peut configurer les paramètres du jeu (itérations, tirages, grilles, options, mode, 2nd tirage, joker+, …) |

### FR-2 · Modèle — Gestion des modèles → `src/models/`

| ID | Exigence |
|----|----------|
| FR3 | L'utilisateur peut sélectionner un modèle de prédiction (Random, SameValue, …) |
| FR4 | L'utilisateur peut configurer les paramètres du modèle |
| FR5 | L'utilisateur peut ajouter de nouveaux modèles à prédire avec leurs paramètres respectifs |

### FR-3 · Données — Gestion des données → `src/data/`

| ID | Exigence |
|----|----------|
| FR6 | L'application peut télécharger automatiquement les données FDJ |
| FR7 | L'application peut parser les fichiers CSV des tirages |
| FR8 | L'utilisateur peut fournir les données manuellement (fallback) |
| FR9 | L'application affiche la date du dernier téléchargement |
| FR10 | L'application notifie si de nouvelles données sont disponibles |

### FR-4 · Batch Processing → `src/batch/`

| ID | Exigence |
|----|----------|
| FR11 | L'utilisateur peut lancer un batch avec des ranges de paramètres |
| FR12 | L'application affiche dans une même vue : workers + batches en cours + progression |
| FR13 | L'utilisateur peut arrêter tous les batches en cours |
| FR14 | L'application peut reprendre les batches arrêtés par l'utilisateur ou après un crash |

### FR-5 · Résultats & Comparaison → `src/ui/pages/results.py`

| ID | Exigence |
|----|----------|
| FR15 | L'application affiche la progression en direct |
| FR16 | L'application met à jour les résultats en live |
| FR17 | L'utilisateur peut comparer les résultats de plusieurs batchs/prédictions |
| FR18 | L'utilisateur peut trier et filtrer les batchs et résultats |
| FR19 | L'application calcule les métriques (ROI, gains, bons numéros) |

### FR-6 · Configuration Système → `.env`, `src/db/`

| ID | Exigence |
|----|----------|
| FR20 | L'utilisateur peut ajuster le nombre de workers en live |
| FR21 | L'application persiste les données en SQLite |
| FR22 | L'utilisateur peut copier-coller la BDD pour reprise |

---

## 6. Exigences non fonctionnelles

### Performance

- Batch processing : les calculs s'affichent à chaque itération (mise à jour **< 1 seconde** entre chaque prédiction).
- Progression live : progression mise à jour **toutes les 500 ms**.

### Fiabilité

- Les données SQLite sont préservées après crash (**atomic writes**, **mode WAL**).
- Reprise après crash : toutes les données de batchs en cours sont sauvegardées en base.
- Erreurs réseau lors du scraping : **retry automatique avec backoff exponentiel (3 tentatives)**.

### Maintenabilité

- Code simple et documenté (docstrings, commentaires pour les fonctions complexes).
- Structure claire pour ajouter de nouveaux jeux/modèles (architecture modulaire).

### Contraintes

- **SQLite** : stockage local, un seul fichier à sauvegarder/copier-coller pour reprise.
- **Données** : scraping manuel, le rate limit incombe à l'utilisateur ; fallback téléchargement manuel à prévoir.
- **Pas de dépendance externe** au-delà de Streamlit / pytest / ruff — rester simple.

---

## 7. Modèle de domaine

### 7.1 Paramètres des jeux

#### Loto

| Paramètre | Type | UI | Défaut |
|-----------|------|-----|--------|
| Type | Loto / Grand-Loto / Super-Loto | Select | Loto |
| Prix grille | float | Input | 2,20 € / 3,00 € / 5,00 € |
| Nombre de grilles | int ou range | Double slider (1-1000) | 1 |
| 2nd tirage | True / False / Les deux | Radio | False |
| Prix 2nd tirage | float | Input | 0,80 € |
| Tirages historiques | range de dates | Double slider dates | — |

Numéros : 5 numéros sur 1-49 + 1 numéro complémentaire sur 1-10.

#### Euromillion

| Paramètre | Type | UI | Défaut |
|-----------|------|-----|--------|
| Prix grille | float | Input | 2,50 € |
| Nombre de grilles | int ou range | Double slider (1-1000) | 1 |
| Etoile+ | True / False / Les deux | Radio | False |
| Prix Etoile+ | float | Input | 1,00 € |
| Tirages historiques | range de dates | Double slider dates | — |

Numéros : 5 numéros sur 1-50 + 2 étoiles sur 1-12.

### 7.2 Paramètres des modèles

#### Random

| Paramètre | Type | UI | Défaut |
|-----------|------|-----|--------|
| seed | timestamp / valeur fixe | Select | timestamp |

#### SameValue — Loto

| Paramètre | Type | UI | Défaut |
|-----------|------|-----|--------|
| numero1…numero5 | int | Input (1-49) | 1, 2, 3, 4, 5 |
| numero_comp | int | Input (1-10) | 6 |

#### SameValue — Euromillion

| Paramètre | Type | UI | Défaut |
|-----------|------|-----|--------|
| numero1…numero5 | int | Input (1-50) | 1, 2, 3, 4, 5 |
| etoile1, etoile2 | int | Input (1-12) | 1, 2 |

### 7.3 Définition d'un batch

Un **batch** = une exécution avec :

- 1 jeu (Loto ou Euromillion)
- 1 configuration de jeu (grilles, dates, …)
- 1 modèle (Random ou SameValue avec ses paramètres)
- N itérations appliquées

Règles :

- **Paramètres en range** : si un paramètre est un range ou un choix multiple → **1 batch par valeur**.
- **Batch ID** : entier unique auto-incrémenté.
- **Paramètres identiques ≠ regroupement automatique**.

### 7.4 Itérations

- Paramètre général (stepper) dans la vue Batch Run, à côté du bouton « Lancer ».
- N dépend des autres paramètres jeu/modèle.
- Affiche toujours la prédiction du « prochain tirage ».

### 7.5 Métriques (par batch)

| Métrique | Description |
|----------|-------------|
| Bons numéros (min / max / moy) | Nombre de numéros corrects trouvés |
| Gains totaux | Somme des gains |
| Coût total | Somme des coûts (grilles + options) |
| ROI | `((gains - coûts) / coûts) × 100` |

---

## 8. Interface utilisateur

### Pages

| Page | Description |
|------|-------------|
| Home | Sélection du jeu (Loto / Euromillion) |
| Config Jeu | Paramètres du jeu |
| Config Modèle | Sélection du modèle + paramètres |
| Batch Run | Lancement des batchs, vue workers, progression, menu contextuel |
| Résultats | Comparaison des batchs, tables, filtres, tri, group by |

### Menu contextuel par batch

Dépendant du jeu / modèle :

- **Info** — affiche les informations détaillées du batch.
- **Voir prochain tirage** — affiche les prédictions pour N itérations.
- **Mettre à jour batch** — compare les prédictions aux résultats réels, continue jusqu'au prochain tirage non historisé.

### Vue Résultats

- Plusieurs modes de vue (vues SQL prédéfinies).
- Liste des itérations par timestamp de tirage.
- Filter by / sort by / group by.
- Présentation différente selon le jeu.

---

## 9. Architecture

### 9.1 Stack

| Élément | Choix |
|---------|-------|
| Langage | Python ≥ 3.13 (patterns compatibles 3.11+) |
| UI | Streamlit (vanilla, **pas de template**) |
| Stockage | SQLite (raw SQL + fonctions wrapper, **pas d'ORM**) |
| Parallélisme | `concurrent.futures.ProcessPoolExecutor` |
| Temps réel | `st.empty()` + `time.sleep()` (natif Streamlit) |
| Packaging | uv |
| Tests | pytest |
| Lint / format | ruff (line-length 88) |
| Typage | mypy (optionnel) |

**Décision starter :** Vanilla Streamlit — le contexte projet définit déjà la stack, le focus est le traitement de données et non une app IA complexe ; l'overhead d'un template est inutile.

### 9.2 Structure cible

```
dont-stop-til-you-get-enough/
├── .env / .env.example      # Variables d'environnement
├── LICENSE                  # MIT
├── pyproject.toml / uv.lock
│
├── src/
│   ├── main.py              # Point d'entrée Streamlit
│   ├── games/               # game_base.py, game_loto.py, game_euromillion.py
│   ├── models/              # model_base.py, model_random.py, model_same_value.py
│   ├── data/                # downloader.py, parser.py, fetcher.py
│   ├── batch/               # processor.py, worker.py, state.py
│   ├── db/                  # connection.py, schema.py, queries.py, migrations/
│   ├── ui/
│   │   ├── pages/           # home.py, game_config.py, model_config.py, batch_run.py, results.py
│   │   └── components/      # progress.py, tables.py
│   └── utils/               # logging.py
│
├── tests/                   # test_games/, test_models/, test_data/, test_batch/, test_db/
└── data/                    # (hors git) database.db, downloads/
```

### 9.3 Frontières des composants

| Composant | Responsabilité |
|-----------|----------------|
| `games/` | Logique de jeu (règles, tirage, calcul des gains) |
| `models/` | Algorithmes de prédiction |
| `data/` | Données externes (téléchargement, parsing) |
| `batch/` | Orchestration des traitements |
| `db/` | Persistance |
| `ui/` | Présentation Streamlit |

### 9.4 Flux de données

```
User Input (UI) → Game Config → Model Config → Batch Processor
                                      ↓
                              ProcessPoolExecutor
                                      ↓
                              Results → DB → UI Display
```

**Points d'intégration :** Game + Model = génération de prédiction · Batch + DB = persistance d'état · UI + Batch = progression temps réel · Data + DB = stockage historique.

### 9.5 Schéma de base de données

SQLite, mode WAL, écritures atomiques. Tables implémentées (`src/db/schema.py`) :

| Table | Rôle | Colonnes clés |
|-------|------|---------------|
| `games` | Jeux disponibles | `name` (unique), `type`, `prix_grille` |
| `draws` | Historique des tirages | `game_id`, `draw_date`, `numeros`, `numeros_comp`, `jackpot` — unique `(game_id, draw_date)` |
| `models` | Modèles disponibles | `name` (unique), `description` |
| `model_params` | Paramètres de modèle | `model_id`, `param_name`, `param_value` — unique `(model_id, param_name)` |
| `batches` | Exécutions | `game_id`, `model_id`, `game_params`, `status`, `total_iterations`, `completed_iterations` |
| `batch_results` | Résultat par itération | `batch_id`, `iteration`, `draw_date`, `prediction`, `matched_numeros`, `matched_comp`, `gain`, `cost` |
| `batch_metrics` | Agrégats par batch | `batch_id` (unique), `total_gains`, `total_cost`, `roi`, `bons_numeros_{min,max,avg}`, `gain_{min,max}` |

Index : `idx_draws_game_date`, `idx_batch_results_batch`, `idx_batches_status`.

Seed initial : jeux `Loto` (2,20 €), `Grand-Loto` (3,00 €), `Super-Loto` (5,00 €), `Euromillion` (2,50 €) ; modèles `Random`, `SameValue`.

> Le `status` de `batches` (`pending` par défaut) et `completed_iterations` portent la reprise après crash (FR14) : au démarrage, les batchs non terminés repartent du dernier point stable.

---

## 10. Conventions de développement

### Nommage

| Élément | Convention | Exemple |
|---------|-----------|---------|
| Tables | `snake_case` pluriel | `games`, `batches`, `results` |
| Colonnes | `snake_case` | `game_id`, `created_at` |
| Clés étrangères | `table_id` | `game_id`, `model_id` |
| Index | `idx_table_column` | `idx_games_name` |
| Fonctions / variables | `snake_case` | `get_game_by_id` |
| Classes | `PascalCase` | `LotoGame`, `RandomModel` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_WORKERS`, `DEFAULT_ITERATIONS` |
| Fonctions privées | `_prefixe_underscore` | `_parse_row` |
| Modules | `snake_case` préfixé par domaine | `game_loto.py`, `model_random.py` |
| Tests | `test_*.py` | `test_batch_processing.py` |

### Formats

- JSON : champs en `snake_case`
- Dates : ISO 8601 (`YYYY-MM-DD HH:MM:SS`)
- Booléens : `true`/`false` (Python : `True`/`False`)
- NULL explicite dans le schéma

### Règles Python

- Type hints sur **toutes** les signatures de fonction
- PEP 8, f-strings
- **Éviter l'opérateur walrus** (`:=`) pour la clarté
- `dataclasses` pour les structures de données simples
- **Imports absolus** dans le package
- Docstrings sur toutes les fonctions publiques

### Gestion d'erreurs

- Exceptions personnalisées par module (`DataDownloadError`, `BatchProcessingError`, …)
- Logger l'erreur + message lisible pour l'utilisateur
- **Ne jamais exposer de stack trace à l'utilisateur**

### Configuration

- Toute la config via `.env` — aucune valeur en dur, aucun secret commité
- `os.getenv()` ou `python-dotenv`

### Tests

- Dans `tests/` à la racine, pattern `test_*.py`
- Fixtures pytest pour le setup partagé
- Objectif **> 80 % de couverture**

### Workflow

- Branches : préfixes `feature/`, `bugfix/`, `hotfix/`
- Commits : conventional commits (`feat:`, `fix:`, `docs:`)
- PR : au moins une review, tests verts
- `ruff check .` et `ruff format .` avant commit
- Pas de `print` de debug, pas de TODO sans référence d'issue

### Commandes

```bash
uv pip install -e .          # Installer les dépendances
streamlit run src/main.py    # Lancer l'app
pytest tests/                # Tests
ruff check . && ruff format . # Lint + format
python -m src.db.schema      # Initialiser + seeder la BDD
```

### Anti-patterns

```python
# ✗ Mauvais — pas de type hints, mauvais nommage
def CalcROI(x, y):
    return (x-y)/y*100

class lotogame:
    pass

# ✓ Bon
def calculate_roi(gains: float, cost: float) -> float:
    """Calculate ROI percentage."""
    if cost == 0:
        return 0.0
    return (gains - cost) / cost * 100

class LotoGame:
    """Loto game implementation."""

    def __init__(self, game_id: int):
        self.game_id = game_id
```

---

## 11. User stories

### Epic 1 — Configuration du Jeu

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US1.1 | Sélectionner un jeu (Loto / Euromillion) pour configurer ses paramètres | Liste déroulante ; les paramètres affichés correspondent au jeu |
| US1.2 | Configurer les paramètres du Loto | Voir § 7.1 Loto |
| US1.3 | Configurer les paramètres Euromillion | Voir § 7.1 Euromillion |

### Epic 2 — Configuration du Modèle

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US2.1 | Sélectionner un modèle de prédiction | Liste des modèles (Random, SameValue) ; paramètres correspondants |
| US2.2 | Configurer Random | `seed` : timestamp / valeur fixe |
| US2.3 | Configurer SameValue Loto | `numero1-5` (1-49), `numero_comp` (1-10) |
| US2.4 | Configurer SameValue Euromillion | `numero1-5` (1-50), `etoile1-2` (1-12) |

### Epic 3 — Exécution des Batchs

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US3.1 | Lancer un batch avec mes paramètres | Bouton « Lancer » + stepper itérations ; range → plusieurs batchs ; ID unique auto-incrémenté |
| US3.2 | Voir la progression en direct | Vue workers + batches en cours ; refresh 500 ms ; résultats en live |
| US3.3 | Arrêter tous les batchs en cours | Bouton « Arrêter tout » ; arrêt propre, sans corruption de données |
| US3.4 | Reprise automatique après crash | État sauvegardé en SQLite ; reprise depuis le dernier point stable |
| US3.5 | Voir les prédictions du prochain tirage | Menu contextuel par batch ; bouton « Voir prochain tirage » ; affiche les N itérations prédites |
| US3.6 | Mettre à jour un batch quand l'historique évolue | Compare prédiction et vrai résultat ; continue jusqu'au prochain tirage non historisé |

### Epic 4 — Résultats et Comparaison

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US4.1 | Consulter les résultats d'un batch | Métriques bons numéros (min/max/moy), gains totaux, coût total, ROI ; présentation par jeu |
| US4.2 | Comparer plusieurs batchs | Filtres, tris, group by ; liste des itérations par timestamp |
| US4.3 | Ajuster le nombre de workers en live | Slider / input ; les batchs en cours redémarrent si nécessaire |

### Epic 5 — Gestion des Données

| ID | Story | Critères d'acceptation |
|----|-------|------------------------|
| US5.1 | Télécharger automatiquement les données FDJ | Scraping du site FDJ (Loto, Euromillion) ; parsing CSV automatique |
| US5.2 | Fournir les données manuellement | Upload de fichiers CSV ; fallback si le scraping échoue |
| US5.3 | Merger l'historique Loto | Merge Loto + Grand-Loto + Super-Loto en BDD |

---

## 12. Traçabilité

| Catégorie FR | Emplacement | Stories |
|--------------|-------------|---------|
| FR1-FR2 — Jeu | `src/games/` | US1.1-US1.3 |
| FR3-FR5 — Modèle | `src/models/` | US2.1-US2.4 |
| FR6-FR10 — Données | `src/data/` | US5.1-US5.3 |
| FR11-FR14 — Batch | `src/batch/` | US3.1-US3.6 |
| FR15-FR19 — Résultats | `src/ui/` | US4.1-US4.2 |
| FR20-FR22 — Config | `.env`, `src/db/` | US4.3 |

Chaîne de traçabilité validée : Executive Summary → Success Criteria → User Journeys → FRs → Scope. **0 exigence orpheline**, 0 parcours sans FR.

---

## 13. Validation de la spec et points ouverts

PRD validé le 2026-03-10 — statut global **Pass**, qualité holistique **4/5**, complétude 100 % (6/6 sections), SMART moyenne **4,9/5** sur 22 FR.

### Écarts relevés par la validation

1. **4 NFR non mesurables à l'origine** (« calculs fluides sans lag », « mise à jour en temps réel », « ne doivent pas être corrompues », « pas de données perdues »). → **Résolu** : chiffrées en § 6 (< 1 s, 500 ms, WAL + atomic writes, persistance en base).
2. **FR4 trop générique** — les paramètres de modèle configurables restent à préciser exigence par exigence ; le § 7.2 tient lieu de référence en attendant.
3. **Critères d'acceptation testables** — à ajouter sur les FR clés pour améliorer la testabilité.

### Décisions différées (post-MVP)

- Formats d'export des résultats
- Visualisations avancées

### Points à trancher avant implémentation complète

- **Barèmes de gains** : le calcul des gains (`Game.calculate_gains`) suppose une grille de rangs par jeu, non spécifiée dans les artefacts BMAD.
- **Source FDJ exacte** : URL et format CSV des historiques ne sont pas figés dans la spec.
- **Redémarrage sur changement de workers** (US4.3) : « les batchs en cours redémarrent si nécessaire » — comportement à préciser (redémarrage de l'itération courante ou du batch entier).
- **Gestion du `Grand-Loto` / `Super-Loto`** : ce sont des `type` de jeu distincts en base (§ 9.5) alors que l'UI les présente comme un paramètre du Loto (§ 7.1), et US5.3 demande leur merge — clarifier le modèle retenu.
- **`src/config.py`** est référencé dans la table de mapping de l'architecture mais absent de l'arborescence cible ; la configuration passe par `.env`.
