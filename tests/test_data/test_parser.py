"""Tests for data modules."""

import pytest
from pathlib import Path
from datetime import date

from src.data.parser import CSVParser, ParsedDraw


class TestCSVParser:
    """Tests for CSV parser."""

    def test_parsed_draw_creation(self):
        """Test ParsedDraw creation."""
        draw = ParsedDraw(
            game_type="loto",
            draw_date=date(2024, 1, 1),
            numeros=[1, 2, 3, 4, 5],
            numeros_comp=[6],
            jackpot=2000000.0,
        )

        assert draw.game_type == "loto"
        assert draw.draw_date == date(2024, 1, 1)
        assert draw.numeros == [1, 2, 3, 4, 5]
        assert draw.numeros_comp == [6]
        assert draw.jackpot == 2000000.0

    def test_euromillion_parsed_draw(self):
        """Test Euromillion ParsedDraw creation."""
        draw = ParsedDraw(
            game_type="euromillion",
            draw_date=date(2024, 1, 1),
            numeros=[1, 2, 3, 4, 5],
            numeros_comp=[1, 2],
            jackpot=100000000.0,
        )

        assert draw.game_type == "euromillion"
        assert draw.numeros_comp == [1, 2]
