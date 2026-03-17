"""Base class for all prediction models."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ModelConfig:
    """Configuration for a prediction model."""

    name: str


@dataclass
class ModelPrediction:
    """Prediction output from a model."""

    numeros: list[int]
    numeros_comp: list[int]


class Model(ABC):
    """Base class for prediction models."""

    def __init__(self, config: ModelConfig):
        self.config = config

    @abstractmethod
    def predict(self) -> ModelPrediction:
        """Generate a prediction."""
        pass

    @abstractmethod
    def get_numero_count(self) -> int:
        """Return the number of main numbers to predict."""
        pass

    @abstractmethod
    def get_comp_count(self) -> int:
        """Return the number of complementary numbers to predict."""
        pass

    @abstractmethod
    def get_numero_range(self) -> tuple[int, int]:
        """Return the range of main numbers (min, max)."""
        pass

    @abstractmethod
    def get_comp_range(self) -> tuple[int, int]:
        """Return the range of complementary numbers (min, max)."""
        pass
