"""Random prediction model."""

import random
from dataclasses import dataclass
from datetime import datetime

from model_base import Model, ModelConfig, ModelPrediction


@dataclass
class RandomConfig(ModelConfig):
    """Configuration for Random model."""

    seed_type: str = "timestamp"  # "timestamp" or "fixed"


class RandomModel(Model):
    """Random prediction model."""

    def __init__(
        self,
        config: RandomConfig,
        numero_count: int,
        comp_count: int,
        numero_range: tuple[int, int],
        comp_range: tuple[int, int],
    ):
        super().__init__(config)
        self.numero_count = numero_count
        self.comp_count = comp_count
        self.numero_range = numero_range
        self.comp_range = comp_range

        # Set random seed
        if config.seed_type == "timestamp":
            random.seed(datetime.now().timestamp())
        else:
            random.seed(config.seed_type)

    def predict(self) -> ModelPrediction:
        """Generate random prediction."""
        numeros = random.sample(
            range(self.numero_range[0], self.numero_range[1] + 1), self.numero_count
        )
        numeros_comp = random.sample(
            range(self.comp_range[0], self.comp_range[1] + 1), self.comp_count
        )
        return ModelPrediction(
            numeros=sorted(numeros), numeros_comp=sorted(numeros_comp)
        )

    def get_numero_count(self) -> int:
        return self.numero_count

    def get_comp_count(self) -> int:
        return self.comp_count

    def get_numero_range(self) -> tuple[int, int]:
        return self.numero_range

    def get_comp_range(self) -> tuple[int, int]:
        return self.comp_range
