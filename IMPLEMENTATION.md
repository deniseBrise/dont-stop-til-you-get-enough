# IMPLEMENTATION — dont-stop-til-you-get-enough

> Suivi **détaillé** des développements faits et à faire.
> Ce document est un **journal vivant** : il est mis à jour au fil de l'avancement.
> Il **découle** de `SPECS.md` (source de vérité) — il ne la remplace pas.
> Langue : français. Code/commentaires : anglais (voir `AGENTS.md`).

## Légende des statuts

| Marqueur | Signification |
|----------|----------------|
| `[ ]` | À faire |
| `[~]` | En cours |
| `[x]` | Fait |
| `[!]` | Bloqué / en attente de décision |

Références : `FRn` = exigence fonctionnelle (SPECS § 6) · `USn.n` = user story (SPECS § 16).

---

## Progression globale

- **Phase actuelle :** Specs (SPECS.md établi). Aucun code produit.
- **Avancement :** 0 % (initialisation from scratch).
- **Branche :** `flush/qwen/from-scratch-with-python`.

---

## 0. Initialisation du projet

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | `pyproject.toml` (deps : dash, plotly, dash-ag-grid, python-dotenv ; dev : pytest, ruff) | Python ≥ 3.13 · aucune licence payante |
| `[ ]` | `.gitignore` | reprendre/adapter (data/, .venv, caches, .env) |
| `[ ]` | `.python-version`, `uv.lock` | via uv |
| `[ ]` | `.env.example` + mécanisme de config | FR34 |
| `[ ]` | `LICENSE` (MIT) | |
| `[ ]` | `README.md` (français) | présentation + démarrage |
| `[ ]` | Arborescence `src/` (app, games, models, data, batch, db, ui, utils) | SPECS § 12.2 |
| `[ ]` | Dossier `assets/` (logos libres de droits) | point ouvert § 18.9 |

## 1. Socle — persistance SQLite

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | Connexion SQLite + mode **WAL** + écritures atomiques | FR32 · SPECS § 9 |
| `[ ]` | Schéma : `games`, `draws`, `models`, `model_params`, `batches`, `batch_results`, `batch_metrics` | SPECS § 9.1 (générique, métriques clé/valeur) |
| `[ ]` | Migrations | dossier `db/migrations/` |
| `[ ]` | Wrappers de requêtes (raw SQL, pas d'ORM) | |
| `[ ]` | Index (`idx_draws_game_date`, `idx_batch_results_batch`, `idx_batches_status`) | |

## 2. Architecture plugin (auto-découverte)

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | Interface/classe de base **Jeu** (règles, paramètres, gains, métriques, parcours UI, source données, modèles compatibles) | FR4–FR5 · SPECS § 4.1 |
| `[ ]` | Interface/classe de base **Modèle** (identité, jeux compatibles, paramètres, algorithme) | FR8–FR9 · SPECS § 5.1 |
| `[ ]` | Mécanisme d'**auto-découverte** (scan `games/`, `models/`) | FR4, FR8 · point ouvert § 18.7 |
| `[ ]` | Association modèle ↔ jeu (filtrage des modèles compatibles) | FR9 |

## 3. Jeux

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | **Loto** (`games/loto.py`) : règles 5/49 + 1/10, paramètres, gains, métriques, parcours | FR7 · SPECS § 4.2 · barème à trancher § 18.2 |
| `[ ]` | **Euromillion** (`games/euromillion.py`) : règles 5/50 + 2/12, Étoile+, gains, métriques, parcours | FR7 · SPECS § 4.3 |
| `[ ]` | **Video Poker — Jacks or Better** (`games/video_poker.py`) : distribution, conservation, table de paiement, métriques (RTP, variance, freq. mains), parcours | FR7 · SPECS § 4.4 |
| `[ ]` | Gestion variantes Loto (Grand-Loto / Super-Loto) | point ouvert § 18.4 |

## 4. Modèles

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | **Aléatoire / Random** (`models/random.py`) : paramètre `seed` | FR11 · SPECS § 5.2 |
| `[ ]` | **Valeur fixe / Fixed Value** (`models/fixed_value.py`) : numéros/cartes fixes | FR11 · SPECS § 5.2 (ex-`SameValue`) |
| `[ ]` | **Fréquences / chauds-froids** (`models/frequency.py`) : fenêtre, chauds/froids/équilibré | FR11 · SPECS § 5.2 |
| `[ ]` | Stratégies Video Poker (conservation) | FR20 · point ouvert § 18.6 |

## 5. Données

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | Téléchargement **auto FDJ** (Loto, Euromillion) + parsing | FR23 · source à figer § 18.3 |
| `[ ]` | **Retry réseau** avec backoff | FR26 · valeurs § 18.1 |
| `[ ]` | **Import manuel** CSV (fallback) | FR24 |
| `[ ]` | **Génération aléatoire** Video Poker (nb de mains paramétrable) | FR25 · SPECS § 8.2 |
| `[ ]` | Date dernier téléchargement + notification nouvelles données | FR27 |

## 6. Moteur de batch

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | Lancement d'un batch (jeu + config + modèle + N itérations), ID unique | FR12, FR18 · SPECS § 7.1 |
| `[ ]` | Gestion des **ranges** → 1 batch par valeur | FR13 |
| `[ ]` | **Parallélisme** `ProcessPoolExecutor`, workers ajustables en live | FR14, FR33 · comportement § 18.5 |
| `[ ]` | **Progression + résultats en live** | FR15 · valeurs § 18.1 |
| `[ ]` | **Arrêt propre** | FR16 |
| `[ ]` | **Reprise après crash** (état persisté, dernier point stable) | FR17 · SPECS § 7.4 |

## 7. Interface utilisateur (Dash)

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | Application Dash (point d'entrée `app.py`) | SPECS § 12 |
| `[ ]` | **Dashboard** : liste des jeux avec logos | FR1 · SPECS § 11.1 |
| `[ ]` | **Parcours par jeu** (défini par le jeu) | FR2 · SPECS § 11.1 |
| `[ ]` | Gros tableaux **AG Grid Community** (tri, filtres, pagination) | FR22, FR31 |
| `[ ]` | Graphiques **Plotly** interactifs | FR22 |
| `[ ]` | Progression live (barre + résultats) | FR15 |
| `[ ]` | **i18n FR/EN** (bascule de langue, extensible) | FR3 · SPECS § 11.2 |
| `[ ]` | Comparaison / tri / filtre / group by des batchs | FR29, FR30 |
| `[ ]` | Vue analyse statistique (fréquences, écarts) | FR21 |
| `[ ]` | Messages d'erreur lisibles (jamais de stack trace) | SPECS § 11.3 |

## 8. Métriques

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | Métriques **par jeu** (déclarées par le jeu) | FR28 · SPECS § 10 |
| `[ ]` | Loteries : ROI, gains/coûts totaux, bons numéros (min/max/moy) | SPECS § 10 |
| `[ ]` | Video Poker : RTP, variance, fréquence des mains, gains/coûts | SPECS § 10 |
| `[ ]` | Stockage clé/valeur (`batch_metrics`) | SPECS § 9.1 |

## 9. Tests & qualité

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[ ]` | Fixtures pytest + structure `tests/` | SPECS § 15 |
| `[ ]` | Tests `games/`, `models/`, `data/`, `batch/`, `db/` | couverture modules critiques |
| `[ ]` | `ruff check .` + `ruff format .` | avant commit |
| `[ ]` | Type hints complets | SPECS § 15 |

## 10. Documentation

| Statut | Tâche | Notes |
|--------|-------|-------|
| `[x]` | `SPECS.md` (source de vérité) | établi |
| `[x]` | `IMPLEMENTATION.md` (ce fichier) | établi |
| `[x]` | `AGENTS.md` (fonctionnement) | établi |
| `[ ]` | `README.md` (français) | à l'initialisation du code |

---

## Décisions à consigner (points ouverts SPECS § 18)

> À remplir au fur et à mesure des décisions (avec approbation du Boss pour tout
> ce qui touche `SPECS.md`).

| # | Sujet | Décision | Date |
|---|-------|----------|------|
| 1 | Valeurs chiffrées NFR (live, progression, retry) | _à décider à l'implémentation_ | — |
| 2 | Barèmes de gains loteries | _à spécifier_ | — |
| 3 | Source FDJ exacte (URL/format) | _à figer_ | — |
| 4 | Grand-Loto / Super-Loto (modélisation) | _à trancher_ | — |
| 5 | Changement de workers en live (comportement) | _à préciser_ | — |
| 6 | Stratégies Video Poker du MVP | _à définir_ | — |
| 7 | Mécanique d'auto-découverte (interface exacte) | _à définir_ | — |
| 8 | Packaging/distribution grand public | _hors MVP, à anticiper_ | — |
| 9 | Assets / logos (provenance libre) | _à sourcer_ | — |

---

## Journal de progression

| Date | Événement |
|------|-----------|
| 2026-09-13 | Flush du projet (from scratch). Création de `SPECS.md`, `IMPLEMENTATION.md`, `AGENTS.md` sur la branche `flush/qwen/from-scratch-with-python`. Aucun code. |
