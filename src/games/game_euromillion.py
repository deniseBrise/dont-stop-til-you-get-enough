"""Euromillion game implementation."""

from dataclasses import dataclass

from game_base import Game, GameConfig, DrawResult, Prediction


# Euromillion price constants
EUROMILLION_PRICE = 2.50
ETOILE_PLUS_PRICE = 1.00

# Euromillion number ranges
EUROMILLION_NUMERO_MIN = 1
EUROMILLION_NUMERO_MAX = 50
EUROMILLION_NUMERO_COUNT = 5
EUROMILLION_ETOILE_MIN = 1
EUROMILLION_ETOILE_MAX = 12
EUROMILLION_ETOILE_COUNT = 2


class EuromillionConfig(GameConfig):
    """Configuration for Euromillion game."""

    etoile_plus: bool | str = False  # True, False, or "both"
    prix_etoile_plus: float = ETOILE_PLUS_PRICE


class Euromillion(Game):
    """Euromillion lottery game."""

    def __init__(self, config: EuromillionConfig):
        super().__init__(config)
        self.etoile_plus = config.etoile_plus
        self.prix_etoile_plus = config.prix_etoile_plus

    def get_numero_range(self) -> tuple[int, int]:
        return (EUROMILLION_NUMERO_MIN, EUROMILLION_NUMERO_MAX)

    def get_comp_range(self) -> tuple[int, int]:
        return (EUROMILLION_ETOILE_MIN, EUROMILLION_ETOILE_MAX)

    def calculate_cost(self) -> float:
        """Calculate cost for one iteration."""
        nombre_grilles = self.config.nombre_grilles
        if isinstance(nombre_grilles, tuple):
            nombre_grilles = nombre_grilles[0]

        cost = self.config.prix_grille * nombre_grilles

        if self.etoile_plus is True or self.etoile_plus == "both":
            cost += self.prix_etoile_plus * nombre_grilles

        return cost

    def calculate_gains(self, prediction: Prediction, draw: DrawResult) -> float:
        """Calculate gains for a prediction against a draw result."""
        main_matches = len(set(prediction.numeros) & set(draw.numeros))
        comp_matches = len(set(prediction.numeros_comp) & set(draw.numeros_comp))

        # Simplified gain calculation - would need actual FDJ gain table
        gains = 0.0

        # Main number matches (5) + stars (2) = Jackpot
        if main_matches == 5 and comp_matches == 2:
            gains += 200000000  # Jackpot
        elif main_matches == 5 and comp_matches == 1:
            gains += 1000000
        elif main_matches == 5:
            gains += 100000
        elif main_matches == 4 and comp_matches == 2:
            gains += 10000
        elif main_matches == 4:
            gains += 500

        return gains
