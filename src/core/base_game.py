import abc
from typing import Dict, Any
import pandas as pd

class BaseGame(abc.ABC):
    """
    Classe de base dont hériteront tous les jeux (Loto, Euromillions, etc.)
    """
    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.history = pd.DataFrame()

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Retourne le nom d'affichage du jeu."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_parameters_schema(cls) -> Dict[str, Any]:
        """
        Retourne la définition des paramètres pour générer l'interface dynamiquement.
        Ex: {"date_debut": {"type": "date"}, "nb_grilles": {"type": "int", "min": 1}}
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_compatible_models(cls) -> list[str]:
        """Retourne la liste des noms des modèles compatibles avec ce jeu."""
        pass

    @abc.abstractmethod
    def fetch_history(self) -> None:
        """Télécharge ou met à jour l'historique des résultats pour ce jeu."""
        pass

    @abc.abstractmethod
    def calculate_metrics(self, predicted_grid: Any, real_grid: Any) -> Dict[str, float]:
        """
        Compare la grille prédite avec la grille réelle et retourne les indicateurs de gain.
        Ex: {"fiat_gain": 15.5, "roi": 0.5, "cost": 2.20}
        """
        pass
