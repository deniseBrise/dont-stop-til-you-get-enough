"""SameValue prediction model."""

from dataclasses import dataclass

from model_base import Model, ModelConfig, ModelPrediction


@dataclass
class SameValueConfig(ModelConfig):
    """Configuration for SameValue model."""

    numero1: int = 1
    numero2: int = 2
    numero3: int = 3
    numero4: int = 4
    numero5: int = 5
    numero_comp: int = 6
    etoile1: int = 1
    etoile2: int = 2


class SameValueModel(Model):
    """SameValue prediction model - always returns fixed numbers."""

    def __init__(self, config: SameValueConfig, is_euromillion: bool = False):
        super().__init__(config)
        self.config = config
        self.is_euromillion = is_euromillion

    def predict(self) -> ModelPrediction:
        """Generate fixed prediction."""
        if self.is_euromillion:
            numeros = [
                self.config.numero1,
                self.config.numero2,
                self.config.numero3,
                self.config.numero4,
                self.config.numero5,
            ]
            numeros_comp = [self.config.etoile1, self.config.etoile2]
        else:
            numeros = [
                self.config.numero1,
                self.config.numero2,
                self.config.numero3,
                self.config.numero4,
                self.config.numero5,
            ]
            numeros_comp = [self.config.numero_comp]

        return ModelPrediction(
            numeros=sorted(numeros), numeros_comp=sorted(numeros_comp)
        )

    def get_numero_count(self) -> int:
        return 5

    def get_comp_count(self) -> int:
        return 2 if self.is_euromillion else 1

    def get_numero_range(self) -> tuple[int, int]:
        return (1, 50) if self.is_euromillion else (1, 49)

    def get_comp_range(self) -> tuple[int, int]:
        return (1, 12) if self.is_euromillion else (1, 10)
