import importlib
import pkgutil
import inspect
from typing import Type, Dict

from src.core.base_game import BaseGame
from src.core.base_model import BaseModel

class Registry:
    """
    Gestionnaire pour découvrir et charger dynamiquement les classes de Jeu et de Modèle.
    """
    def __init__(self):
        self.games: Dict[str, Type[BaseGame]] = {}
        self.models: Dict[str, Type[BaseModel]] = {}
        self.discover_modules()

    def discover_modules(self):
        """Scanne les dossiers src/games/ et src/models/ pour trouver les classes compatibles."""
        # Importer les jeux
        try:
            import src.games
            for _, module_name, _ in pkgutil.iter_modules(src.games.__path__):
                mod = importlib.import_module(f"src.games.{module_name}")
                for name, obj in inspect.getmembers(mod):
                    if inspect.isclass(obj) and issubclass(obj, BaseGame) and obj is not BaseGame:
                        self.games[obj.get_name()] = obj
        except ImportError:
            pass  # Dossier src/games/ n'existe pas encore ou est vide

        # Importer les modèles
        try:
            import src.models
            for _, module_name, _ in pkgutil.iter_modules(src.models.__path__):
                mod = importlib.import_module(f"src.models.{module_name}")
                for name, obj in inspect.getmembers(mod):
                    if inspect.isclass(obj) and issubclass(obj, BaseModel) and obj is not BaseModel:
                        self.models[obj.get_name()] = obj
        except ImportError:
            pass  # Dossier src/models/ n'existe pas encore ou est vide

    def get_game_class(self, name: str) -> Type[BaseGame]:
        return self.games.get(name)

    def get_model_class(self, name: str) -> Type[BaseModel]:
        return self.models.get(name)

# Instance unique globale (Singleton)
registry = Registry()
