import abc
from typing import Dict, Any

class BaseModel(abc.ABC):
    """
    Classe de base dont hériteront tous les modèles de prédiction mathématiques.
    """
    def __init__(self, params: Dict[str, Any]):
        self.params = params

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Retourne le nom d'affichage du modèle."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_parameters_schema(cls) -> Dict[str, Any]:
        """
        Retourne la définition des paramètres du modèle pour l'interface.
        Ex: {"numero_1": {"type": "int", "min": 1, "max": 49}}
        """
        pass

    @abc.abstractmethod
    def predict(self, game_history: Any, target_date: Any) -> Any:
        """
        Calcule et retourne la prédiction pour une date donnée en se basant sur l'historique.
        """
        pass
