"""Base class for all games."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class GameConfig:
    """Configuration for a game."""

    name: str
    prix_grille: float
    nombre_grilles: int | tuple[int, int]
    tirages_historiques: tuple[date, date] | None = None
    tirages_futurs: bool = False


@dataclass
class DrawResult:
    """Result of a draw."""

    date: date
    numeros: list[int]
    numeros_comp: list[int]


@dataclass
class Prediction:
    """Prediction for a draw."""

    numeros: list[int]
    numeros_comp: list[int]


class Game(ABC):
    """Base class for lottery games."""

    def __init__(self, config: GameConfig):
        self.config = config

    @abstractmethod
    def get_numero_range(self) -> tuple[int, int]:
        """Return the range of main numbers (min, max)."""
        pass

    @abstractmethod
    def get_comp_range(self) -> tuple[int, int]:
        """Return the range of complementary numbers (min, max)."""
        pass

    @abstractmethod
    def calculate_gains(self, prediction: Prediction, draw: DrawResult) -> float:
        """Calculate gains for a prediction against a draw result."""
        pass

    @abstractmethod
    def calculate_cost(self) -> float:
        """Calculate the cost for one iteration."""
        pass

    def validate_numeros(self, numeros: list[int]) -> bool:
        """Validate that numeros are within range and unique."""
        if len(numeros) != len(set(numeros)):
            return False
        min_num, max_num = self.get_numero_range()
        return all(min_num <= n <= max_num for n in numeros)

    def validate_comp(self, comp: list[int]) -> bool:
        """Validate that complementary numbers are within range and unique."""
        if len(comp) != len(set(comp)):
            return False
        min_comp, max_comp = self.get_comp_range()
        return all(min_comp <= c <= max_comp for c in comp)
