# AGENTS.md — dont-stop-til-you-get-enough

Guide **succinct** pour toute personne (ou agent IA) intervenant sur ce projet.

## Fonctionnement du projet

Trois documents gouvernent le projet :

| Document | Rôle | Règle |
|----------|------|-------|
| `SPECS.md` | **Source de vérité** (exigences, conception, contraintes) | **Modifiable uniquement avec l'approbation explicite du Boss.** Ne jamais l'altérer sans accord. |
| `IMPLEMENTATION.md` | **Suivi détaillé** des développements (faits / à faire) | Journal vivant : à mettre à jour à chaque avancée. |
| `AGENTS.md` | Ce guide (fonctionnement & conventions) | — |

- Avant toute tâche : **lire `SPECS.md`**, puis consulter `IMPLEMENTATION.md`.
- Après toute tâche : **mettre à jour `IMPLEMENTATION.md`** (statuts, journal, décisions).
- Si une décision fait évoluer la conception : la proposer au Boss ; ne modifier
  `SPECS.md` qu'après approbation, puis répercuter dans `IMPLEMENTATION.md`.
- **`README.md` doit toujours suivre le code courant** : le tenir à jour à chaque
  évolution (en français). Tant qu'il n'y a pas de code, il reste minimal.

## Comportement attendu de l'agent

- Apporter des réponses **pertinentes, fiables, rigoureuses, simples** (pas
  d'over-engineering) et **explicites**.
- **Ne jamais inventer** quand on ne sait pas : le dire clairement.
- Décider puis agir ; si vraiment ambigu, une question ciblée — pas dix reconsidérations.
- Vérifier plutôt que supposer, relire avant d'éditer pour éviter les conflits.
- **Préfixer systématiquement** toute donnée inventée ou de test comme telle
  (ex. `[FICTIF]`, `[FIXTURE]`, `[EXEMPLE]`).
- **Toujours prouver** ce qui est avancé (source, test, commande, référence `fichier:ligne`).
- Utiliser les **skills** disponibles quand c'est pertinent.
- Pour tout **choix d'architecture**, proposer **2 ou 3 solutions** pertinentes
  avec leurs compromis.
- **Proposer de mettre à jour les versions** des applicatifs et modules quand c'est nécessaire.

## Langues (règle stricte)

- **Code** : identifiants, commentaires et docstrings en **anglais**.
- **Documentation** : `SPECS.md`, `AGENTS.md`, `IMPLEMENTATION.md`, `README.md` en **français**.
- **UI** : chaînes localisées **français + anglais** (i18n, extensible).

## Contraintes techniques essentielles

- **Python ≥ 3.13** ; application **graphique** web **Dash / Plotly**.
- Gros tableaux : **AG Grid Community** ; stockage : **SQLite** (mode WAL).
- **Aucune licence payante** : dépendances et assets **libres / open-source** uniquement.
- Architecture **modulaire / plugin** : 1 jeu = 1 fichier (`src/games/`), 1 modèle =
  1 fichier (`src/models/`), **auto-découverts** (drop-in).

## TDD & tests

- Travailler en **TDD** : écrire les tests avant (ou à mesure de) le code.
- Couvrir les trois niveaux : **unitaires**, **intégration**, **fonctionnels**.
- Assurer un **minimum de couverture de code** (cible indicative : **≥ 80 %** sur
  les modules critiques — games, models, batch, db ; seuil à ajuster avec le Boss).
- Tests dans `tests/` (`test_*.py`, pytest) ; fixtures pour le setup partagé.
- Toute donnée inventée dans les tests est **explicitement marquée** comme fixture.

## Conventions de code (résumé — détail dans `SPECS.md` § 15)

- **Type hints** sur toutes les signatures ; `dataclasses` pour les structures simples.
- Nommage : modules/fonctions `snake_case`, classes `PascalCase`, constantes `UPPER_SNAKE_CASE`.
- **Imports absolus** ; docstrings sur les fonctions publiques ; éviter l'opérateur walrus.
- Exceptions personnalisées par module ; **jamais de stack trace exposée** à l'utilisateur.
- Config via `.env` (aucun secret commité).
- `ruff check .` + `ruff format .` avant commit.
- Commits : **conventional commits** (`feat:`, `fix:`, `docs:`, `chore:`, `test:`).

## Commandes (quand le code existera)

```bash
uv pip install -e .            # installer les dépendances
python src/app.py              # lancer l'application Dash
pytest tests/                  # tests
ruff check . && ruff format .  # lint + format
```

> Tant que le projet est au stade « specs », ces commandes ne s'appliquent pas encore.
> L'avancement est suivi dans `IMPLEMENTATION.md`.
