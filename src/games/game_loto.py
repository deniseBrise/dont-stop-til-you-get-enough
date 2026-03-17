"""Loto game implementation."""

from dataclasses import dataclass

from game_base import Game, GameConfig, DrawResult, Prediction


# Loto price constants
LOTO_PRICE = 2.20
GRAND_LOTO_PRICE = 3.00
SUPER_LOTO_PRICE = 5.00
SECOND_TIRAGE_PRICE = 0.80

# Loto number ranges
LOTO_NUMERO_MIN = 1
LOTO_NUMERO_MAX = 49
LOTO_NUMERO_COUNT = 5
LOTO_COMP_MIN = 1
LOTO_COMP_MAX = 10
LOTO_COMP_COUNT = 1


class LotoConfig(GameConfig):
    """Configuration for Loto game."""

    type_loto: str = "loto"  # "loto", "grand-loto", "super_loto"
    second_tirage: bool | str = False  # True, False, or "both"
    prix_second_tirage: float = SECOND_TIRAGE_PRICE


class Loto(Game):
    """Loto lottery game."""

    TYPE_PRICES = {
        "loto": LOTO_PRICE,
        "grand_loto": GRAND_LOTO_PRICE,
        "super_loto": SUPER_LOTO_PRICE,
    }

    def __init__(self, config: LotoConfig):
        super().__init__(config)
        self.type_loto = config.type_loto
        self.second_tirage = config.second_tirage
        self.prix_second_tirage = config.prix_second_tirage

    def get_numero_range(self) -> tuple[int, int]:
        return (LOTO_NUMERO_MIN, LOTO_NUMERO_MAX)

    def get_comp_range(self) -> tuple[int, int]:
        return (LOTO_COMP_MIN, LOTO_COMP_MAX)

    def calculate_cost(self) -> float:
        """Calculate cost for one iteration."""
        nombre_grilles = self.config.nombre_grilles
        if isinstance(nombre_grilles, tuple):
            nombre_grilles = nombre_grilles[0]

        cost = self.config.prix_grille * nombre_grilles

        if self.second_tirage is True or self.second_tirage == "both":
            cost += self.prix_second_tirage * nombre_grilles

        return cost

    def calculate_gains(self, prediction: Prediction, draw: DrawResult) -> float:
        """Calculate gains for a prediction against a draw result."""
        main_matches = len(set(prediction.numeros) & set(draw.numeros))
        comp_matches = len(set(prediction.numeros_comp) & set(draw.numeros_comp))

        # Simplified gain calculation - would need actual FDJ gain table
        gains = 0.0

        # Main number matches
        if main_matches == 5:
            gains += 2000000  # Jackpot
        elif main_matches == 4:
            gains += 1000
        elif main_matches == 3:
            gains += 50
        elif main_matches == 2:
            gains += 10

        # Complementary matches
        if comp_matches == 1:
            gains += 10

        return gains
