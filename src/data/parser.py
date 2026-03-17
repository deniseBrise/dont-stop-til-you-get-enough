"""CSV parser for lottery data."""

import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Literal

from src.games.game_base import DrawResult


@dataclass
class ParsedDraw:
    """Parsed draw data."""

    game_type: str
    draw_date: date
    numeros: list[int]
    numeros_comp: list[int]
    jackpot: float | None = None


class CSVParser:
    """Parses lottery CSV files."""

    def parse_loto_csv(self, csv_path: Path) -> list[ParsedDraw]:
        """Parse Loto CSV file."""
        draws = []

        # Note: The actual CSV format from FDJ would need to be analyzed
        # This is a placeholder for the expected format
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Expected columns would be something like:
                # date, numero1, numero2, numero3, numero4, numero5, numero_chance
                draw = ParsedDraw(
                    game_type="loto",
                    draw_date=datetime.strptime(row.get("date", ""), "%Y-%m-%d").date(),
                    numeros=[
                        int(row.get("numero1", 0)),
                        int(row.get("numero2", 0)),
                        int(row.get("numero3", 0)),
                        int(row.get("numero4", 0)),
                        int(row.get("numero5", 0)),
                    ],
                    numeros_comp=[int(row.get("numero_chance", 0))],
                    jackpot=float(row.get("jackpot", 0))
                    if row.get("jackpot")
                    else None,
                )
                draws.append(draw)

        return draws

    def parse_euromillion_csv(self, csv_path: Path) -> list[ParsedDraw]:
        """Parse Euromillion CSV file."""
        draws = []

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Expected columns:
                # date, numero1-5, etoile1, etoile2
                draw = ParsedDraw(
                    game_type="euromillion",
                    draw_date=datetime.strptime(row.get("date", ""), "%Y-%m-%d").date(),
                    numeros=[
                        int(row.get("numero1", 0)),
                        int(row.get("numero2", 0)),
                        int(row.get("numero3", 0)),
                        int(row.get("numero4", 0)),
                        int(row.get("numero5", 0)),
                    ],
                    numeros_comp=[
                        int(row.get("etoile1", 0)),
                        int(row.get("etoile2", 0)),
                    ],
                    jackpot=float(row.get("jackpot", 0))
                    if row.get("jackpot")
                    else None,
                )
                draws.append(draw)

        return draws

    def import_to_database(self, draws: list[ParsedDraw]) -> int:
        """Import parsed draws to database."""
        from src.db.schema import get_connection

        conn = get_connection()
        cursor = conn.cursor()

        imported = 0
        for draw in draws:
            # Get game_id
            game_id = 1 if draw.game_type == "loto" else 4  # Would lookup properly

            try:
                cursor.execute(
                    """INSERT INTO draws (game_id, draw_date, numeros, numeros_comp, jackpot)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        game_id,
                        draw.draw_date.isoformat(),
                        str(draw.numeros),
                        str(draw.numeros_comp),
                        draw.jackpot,
                    ),
                )
                imported += 1
            except sqlite3.IntegrityError:
                # Skip duplicates
                pass

        conn.commit()
        conn.close()

        return imported
