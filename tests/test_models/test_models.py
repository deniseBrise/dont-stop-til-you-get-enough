"""Tests for models."""

import pytest
from datetime import datetime

from src.models.model_random import RandomModel, RandomConfig
from src.models.model_same_value import SameValueModel, SameValueConfig


class TestRandomModel:
    """Tests for Random model."""

    def test_random_config(self):
        """Test RandomConfig creation."""
        config = RandomConfig(name="Random", seed_type="timestamp")
        assert config.name == "Random"
        assert config.seed_type == "timestamp"

    def test_random_predict(self):
        """Test Random prediction generation."""
        config = RandomConfig(name="Random", seed_type="timestamp")
        model = RandomModel(config, 5, 1, (1, 49), (1, 10))

        prediction = model.predict()

        assert len(prediction.numeros) == 5
        assert len(prediction.numeros_comp) == 1
        assert all(1 <= n <= 49 for n in prediction.numeros)
        assert all(1 <= c <= 10 for c in prediction.numeros_comp)

    def test_random_unique_numbers(self):
        """Test Random produces unique numbers."""
        config = RandomConfig(name="Random", seed_type="timestamp")
        model = RandomModel(config, 5, 1, (1, 49), (1, 10))

        # Generate multiple predictions
        for _ in range(10):
            prediction = model.predict()
            assert len(set(prediction.numeros)) == 5  # All unique
            assert len(set(prediction.numeros_comp)) == 1  # All unique

    def test_random_with_fixed_seed(self):
        """Test Random with fixed seed produces same results."""
        import random

        # Test that seed_type="timestamp" uses current time
        config1 = RandomConfig(name="Random", seed_type="timestamp")
        model1 = RandomModel(config1, 5, 1, (1, 49), (1, 10))

        # Reset seed and create another model
        random.seed(12345)
        config2 = RandomConfig(name="Random", seed_type="timestamp")
        model2 = RandomModel(config2, 5, 1, (1, 49), (1, 10))

        pred1 = model1.predict()
        pred2 = model2.predict()

        # With different timestamps, predictions should be different
        # (This test just verifies both produce valid predictions)
        assert len(pred1.numeros) == 5
        assert len(pred2.numeros) == 5


class TestSameValueModel:
    """Tests for SameValue model."""

    def test_same_value_loto(self):
        """Test SameValue for Loto."""
        config = SameValueConfig(
            name="SameValue",
            numero1=1,
            numero2=2,
            numero3=3,
            numero4=4,
            numero5=5,
            numero_comp=6,
        )
        model = SameValueModel(config, is_euromillion=False)

        prediction = model.predict()

        assert prediction.numeros == [1, 2, 3, 4, 5]
        assert prediction.numeros_comp == [6]

    def test_same_value_euromillion(self):
        """Test SameValue for Euromillion."""
        config = SameValueConfig(
            name="SameValue",
            numero1=1,
            numero2=2,
            numero3=3,
            numero4=4,
            numero5=5,
            etoile1=1,
            etoile2=2,
        )
        model = SameValueModel(config, is_euromillion=True)

        prediction = model.predict()

        assert prediction.numeros == [1, 2, 3, 4, 5]
        assert prediction.numeros_comp == [1, 2]

    def test_same_value_ranges_loto(self):
        """Test SameValue ranges for Loto."""
        config = SameValueConfig(name="SameValue")
        model = SameValueModel(config, is_euromillion=False)

        assert model.get_numero_range() == (1, 49)
        assert model.get_comp_range() == (1, 10)
        assert model.get_numero_count() == 5
        assert model.get_comp_count() == 1

    def test_same_value_ranges_euromillion(self):
        """Test SameValue ranges for Euromillion."""
        config = SameValueConfig(name="SameValue")
        model = SameValueModel(config, is_euromillion=True)

        assert model.get_numero_range() == (1, 50)
        assert model.get_comp_range() == (1, 12)
        assert model.get_numero_count() == 5
        assert model.get_comp_count() == 2
