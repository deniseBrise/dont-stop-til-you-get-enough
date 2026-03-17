"""Database schema for the application."""

import sqlite3
from pathlib import Path
from datetime import date


DB_PATH = Path(__file__).parent.parent.parent / "data" / "database.db"


def get_connection() -> sqlite3.Connection:
    """Get a database connection with WAL mode."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_schema() -> None:
    """Initialize the database schema."""
    conn = get_connection()
    cursor = conn.cursor()

    # Games table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT,
            prix_grille REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Draws table (historical data)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS draws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            draw_date DATE NOT NULL,
            numeros TEXT NOT NULL,
            numeros_comp TEXT NOT NULL,
            jackpot REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games (id),
            UNIQUE(game_id, draw_date)
        )
    """)

    # Models table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Model parameters table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER NOT NULL,
            param_name TEXT NOT NULL,
            param_value TEXT,
            FOREIGN KEY (model_id) REFERENCES models (id),
            UNIQUE(model_id, param_name)
        )
    """)

    # Batches table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            model_id INTEGER NOT NULL,
            game_params TEXT,
            status TEXT DEFAULT 'pending',
            total_iterations INTEGER,
            completed_iterations INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (game_id) REFERENCES games (id),
            FOREIGN KEY (model_id) REFERENCES models (id)
        )
    """)

    # Batch results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS batch_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id INTEGER NOT NULL,
            iteration INTEGER NOT NULL,
            draw_date DATE,
            prediction TEXT NOT NULL,
            matched_numeros INTEGER,
            matched_comp INTEGER,
            gain REAL DEFAULT 0,
            cost REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (batch_id) REFERENCES batches (id)
        )
    """)

    # Batch metrics table (aggregated results)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS batch_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id INTEGER NOT NULL UNIQUE,
            total_gains REAL DEFAULT 0,
            total_cost REAL DEFAULT 0,
            roi REAL DEFAULT 0,
            bons_numeros_min INTEGER,
            bons_numeros_max INTEGER,
            bons_numeros_avg REAL,
            gain_min REAL DEFAULT 0,
            gain_max REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (batch_id) REFERENCES batches (id)
        )
    """)

    # Create indexes
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_draws_game_date ON draws(game_id, draw_date)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_batch_results_batch ON batch_results(batch_id)"
    )
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_batches_status ON batches(status)")

    conn.commit()
    conn.close()


def seed_initial_data() -> None:
    """Seed initial game and model data."""
    conn = get_connection()
    cursor = conn.cursor()

    # Insert games
    games = [
        ("Loto", "loto", 2.20),
        ("Grand-Loto", "grand_loto", 3.00),
        ("Super-Loto", "super_loto", 5.00),
        ("Euromillion", "euromillion", 2.50),
    ]

    for name, game_type, price in games:
        cursor.execute(
            "INSERT OR IGNORE INTO games (name, type, prix_grille) VALUES (?, ?, ?)",
            (name, game_type, price),
        )

    # Insert models
    models = [
        ("Random", "Generates random numbers"),
        ("SameValue", "Always returns the same fixed numbers"),
    ]

    for name, desc in models:
        cursor.execute(
            "INSERT OR IGNORE INTO models (name, description) VALUES (?, ?)",
            (name, desc),
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_schema()
    seed_initial_data()
    print(f"Database initialized at {DB_PATH}")
