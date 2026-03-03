from typing import Dict, Any
from src.core.base_model import BaseModel

class SameValueModel(BaseModel):
    """
    Modèle de base (Proof of Concept) qui retourne toujours les mêmes grilles de numéros.
    """
    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)

    @classmethod
    def get_name(cls) -> str:
        return "Valeurs Fixes (Same Value)"

    @classmethod
    def get_parameters_schema(cls) -> Dict[str, Any]:
        schema = {}
        for i in range(1, 6):
            schema[f"numero_{i}"] = {
                "type": "int",
                "label": f"Numéro {i} (1 - 49)",
                "min": 1,
                "max": 49,
                "default": i
            }
        
        schema["numero_chance"] = {
            "type": "int",
            "label": "Numéro Chance (1 - 10)",
            "min": 1,
            "max": 10,
            "default": 1
        }
        return schema

    def predict(self, game_history: Any, target_date: Any) -> Any:
        """
        Dans ce modèle naïf, on n'utilise pas game_history ni target_date,
        on retourne simplement les numéros renseignés dans les paramètres de constructeur.
        """
        
        numeros = [
            self.params.get("numero_1", 1),
            self.params.get("numero_2", 2),
            self.params.get("numero_3", 3),
            self.params.get("numero_4", 4),
            self.params.get("numero_5", 5)
        ]
        
        # On va s'assurer qu'il n'y a pas de doublons dans la grille (bien que l'UI ne l'empêche pas encore)
        # Mais dans le Loto une grille comporte 5 numéros distincts
        unique_numeros = list(set(numeros))
        
        chance = self.params.get("numero_chance", 1)

        return {
            "numeros": unique_numeros,
            "chance": chance
        }
