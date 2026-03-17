"""Manual data fetcher for lottery data."""

from pathlib import Path

from src.data.parser import CSVParser


class ManualDataFetcher:
    """Allows manual loading of lottery data files."""

    def __init__(self):
        self.parser = CSVParser()

    def load_csv_file(self, file_path: Path, game_type: str) -> dict:
        """
        Manually load a CSV file for a game type.

        Args:
            file_path: Path to the CSV file
            game_type: Either "loto" or "euromillion"

        Returns:
            Dictionary with results
        """
        if not file_path.exists():
            return {
                "success": False,
                "message": f"File not found: {file_path}",
                "imported": 0,
            }

        try:
            if game_type == "loto":
                draws = self.parser.parse_loto_csv(file_path)
            elif game_type == "euromillion":
                draws = self.parser.parse_euromillion_csv(file_path)
            else:
                return {
                    "success": False,
                    "message": f"Unknown game type: {game_type}",
                    "imported": 0,
                }

            imported = self.parser.import_to_database(draws)

            return {
                "success": True,
                "message": f"Imported {imported} draws",
                "imported": imported,
                "total": len(draws),
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error loading file: {str(e)}",
                "imported": 0,
            }
