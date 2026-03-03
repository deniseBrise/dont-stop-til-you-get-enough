# Prédiction & Évaluation de Jeux de Hasard

Application Python (PyQt6) permettant de comparer des données réelles de jeux de hasard (Loto, Euromillions...) avec des prédictions mathématiques basées sur différents modèles. L'objectif est de trouver les combinaisons jeu/modèle/paramètres offrant les meilleurs indices de gains (FIAT, ROI, etc.).

## 🚀 État du projet (En cours de développement)

Le projet suit une architecture modulaire permettant l'ajout facile de nouveaux jeux et modèles via un système de "plugins" dynamiques.

### Ce qui est implémenté (Phases 1 à 3) :
- **Architecture Core** : Classes mères `BaseGame` et `BaseModel` établissant les contrats d'interface.
- **Gestionnaire de file d'attente (SQLite)** : Mémorisation des itérations à calculer (statuts `PENDING`, `RUNNING`, `DONE`).
- **Interface Utilisateur Dynamique** : Génération de l'onglet *Configuration* à la volée. L'UI lit le schéma de données exigées par le jeu/modèle sélectionné et génère les widgets correspondants (QSpinBox, QDateEdit...).
- **Jeu Loto (FDJ)** : Module capable de télécharger/parser l'historique officiel CSV de la FDJ et contenant le système de calcul de gains (Hits, Net Profit).
- **Modèle "Valeurs Fixes"** : Un modèle *Proof of Concept* renvoyant toujours une grille configurée par l'utilisateur.

### Ce qui reste à faire :
- **Phase 4** : Le `Worker` (Thread d'arrière-plan). Il dépilera la base SQLite pour exécuter les modèles, les comparer avec l'historique pandas et sauvegarder les résultats en base, sans figer l'interface.
- **Phase 5** : L'onglet *Résultats*. Un tableau interactif avec tri et filtrage pour analyser les métriques.

## ⚙️ Prérequis et Installation

Ce projet utilise [uv](https://github.com/astral-sh/uv) comme gestionnaire de dépendances ultra-rapide.

1. Clonez ce dépôt.
2. Assurez-vous d'avoir `uv` installé sur votre système.
3. Installez les dépendances et créez l'environnement virtuel automatiquement :
   ```bash
   uv sync
   ```
4. Lancez l'application :
   ```bash
   uv run src/main.py
   ```

## 📂 Structure du code

```text
├── .gitignore
├── pyproject.toml / uv.lock
├── README.md
├── data/                   # (Ignoré par git) Base SQLite et fichiers CSV
└── src/
    ├── main.py             # Point d'entrée de l'application
    ├── core/
    │   ├── base_game.py    # Classe abstraite pour les jeux
    │   ├── base_model.py   # Classe abstraite pour les modèles
    │   ├── database.py     # Gestionnaire SQLite (File d'attente)
    │   └── registry.py     # Chargeur dynamique des classes
    ├── games/
    │   └── loto.py         # Implémentation du Loto FDJ
    ├── models/
    │   └── same_value.py   # Modèle de test (Valeur Fixe)
    └── gui/
        ├── main_window.py  # (Sera séparé si besoin)
        └── config_tab.py   # Onglet dynamique de configuration
```

## 🛠️ Contribuer : Ajouter un Jeu ou un Modèle
Il suffit de créer un fichier `.py` dans `src/games/` héritant de `BaseGame`, ou dans `src/models/` héritant de `BaseModel`. L'application le détectera et générera l'interface graphique automatiquement au prochain lancement !
