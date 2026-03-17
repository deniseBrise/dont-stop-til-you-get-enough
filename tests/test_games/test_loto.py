"""Tests for Loto game."""

import pytest
from datetime import date

from src.games.game_loto import Loto, LotoConfig
from src.games.game_base import DrawResult, Prediction


class TestLoto:
    """Tests for Loto game."""

    def test_loto_config_creation(self):
        """Test LotoConfig creation."""
        config = LotoConfig(
            name="Loto",
            prix_grille=2.20,
            nombre_grilles=1,
        )
        assert config.prix_grille == 2.20
        assert config.nombre_grilles == 1

    def test_loto_number_range(self):
        """Test Loto number range."""
        config = LotoConfig(name="Loto", prix_grille=2.20, nombre_grilles=1)
        loto = Loto(config)
        assert loto.get_numero_range() == (1, 49)
        assert loto.get_comp_range() == (1, 10)

    def test_loto_calculate_cost(self):
        """Test Loto cost calculation."""
        config = LotoConfig(
            name="Loto",
            prix_grille=2.20,
            nombre_grilles=5,
        )
        loto = Loto(config)
        assert loto.calculate_cost() == 11.0  # 5 * 2.20

    def test_loto_calculate_cost_with_second_tirage(self):
        """Test Loto cost with second tirage."""
        config = LotoConfig(
            name="Loto",
            prix_grille=2.20,
            nombre_grilles=5,
        )
        loto = Loto(config)
        loto.second_tirage = True
        loto.prix_second_tirage = 0.80
        # 5 * 2.20 + 5 * 0.80 = 11.0 + 4.0 = 15.0
        assert loto.calculate_cost() == 15.0

    def test_validate_numeros_valid(self):
        """Test validation of valid numbers."""
        config = LotoConfig(name="Loto", prix_grille=2.20, nombre_grilles=1)
        loto = Loto(config)
        assert loto.validate_numeros([1, 2, 3, 4, 5]) is True

    def test_validate_numeros_duplicate(self):
        """Test validation rejects duplicates."""
        config = LotoConfig(name="Loto", prix_grille=2.20, nombre_grilles=1)
        loto = Loto(config)
        assert loto.validate_numeros([1, 2, 3, 4, 4]) is False

    def test_validate_numeros_out_of_range(self):
        """Test validation rejects out of range."""
        config = LotoConfig(name="Loto", prix_grille=2.20, nombre_grilles=1)
        loto = Loto(config)
        assert loto.validate_numeros([1, 2, 3, 4, 50]) is False  # 50 > 49

    def test_calculate_gains_jackpot(self):
        """Test gain calculation for jackpot."""
        config = LotoConfig(name="Loto", prix_grille=2.20, nombre_grilles=1)
        loto = Loto(config)

        prediction = Prediction(numeros=[1, 2, 3, 4, 5], numeros_comp=[6])
        draw = DrawResult(date=date.today(), numeros=[1, 2, 3, 4, 5], numeros_comp=[6])

        gains = loto.calculate_gains(prediction, draw)
        # Jackpot (5 main) + comp match = 2000000 + 10
        assert gains == 2000010

    def test_calculate_gains_no_match(self):
        """Test gain calculation for no match."""
        config = LotoConfig(name="Loto", prix_grille=2.20, nombre_grilles=1)
        loto = Loto(config)

        prediction = Prediction(numeros=[1, 2, 3, 4, 5], numeros_comp=[6])
        draw = DrawResult(
            date=date.today(), numeros=[10, 11, 12, 13, 14], numeros_comp=[7]
        )

        gains = loto.calculate_gains(prediction, draw)
        assert gains == 0
