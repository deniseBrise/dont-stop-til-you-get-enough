"""Database queries for lottery data."""

from datetime import date
from typing import Literal

from src.db.schema import get_connection


def get_game_by_name(name: str) -> dict | None:
    """Get game by name."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, type, prix_grille FROM games WHERE name = ?", (name,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "type": row[2],
        "prix_grille": row[3],
    }


def get_all_games() -> list[dict]:
    """Get all games."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, type, prix_grille FROM games ORDER BY name")
    rows = cursor.fetchall()
    conn.close()

    return [{"id": r[0], "name": r[1], "type": r[2], "prix_grille": r[3]} for r in rows]


def get_model_by_name(name: str) -> dict | None:
    """Get model by name."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, description FROM models WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "description": row[2],
    }


def get_all_models() -> list[dict]:
    """Get all models."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, description FROM models ORDER BY name")
    rows = cursor.fetchall()
    conn.close()

    return [{"id": r[0], "name": r[1], "description": r[2]} for r in rows]


def get_draws_for_game(
    game_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int | None = None,
) -> list[dict]:
    """Get draws for a game within a date range."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, game_id, draw_date, numeros, numeros_comp, jackpot FROM draws WHERE game_id = ?"
    params = [game_id]

    if start_date:
        query += " AND draw_date >= ?"
        params.append(start_date.isoformat())

    if end_date:
        query += " AND draw_date <= ?"
        params.append(end_date.isoformat())

    query += " ORDER BY draw_date DESC"

    if limit:
        query += " LIMIT ?"
        params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "game_id": r[1],
            "draw_date": r[2],
            "numeros": eval(r[3]),  # Safe here since we control the data
            "numeros_comp": eval(r[4]),
            "jackpot": r[5],
        }
        for r in rows
    ]


def get_latest_draw(game_id: int) -> dict | None:
    """Get the most recent draw for a game."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, game_id, draw_date, numeros, numeros_comp, jackpot
           FROM draws WHERE game_id = ? ORDER BY draw_date DESC LIMIT 1""",
        (game_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "game_id": row[1],
        "draw_date": row[2],
        "numeros": eval(row[3]),
        "numeros_comp": eval(row[4]),
        "jackpot": row[5],
    }


def get_batch_results(batch_id: int) -> list[dict]:
    """Get all results for a batch."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, batch_id, iteration, draw_date, prediction,
                  matched_numeros, matched_comp, gain, cost
           FROM batch_results WHERE batch_id = ? ORDER BY iteration""",
        (batch_id,),
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "batch_id": r[1],
            "iteration": r[2],
            "draw_date": r[3],
            "prediction": eval(r[4]),
            "matched_numeros": r[5],
            "matched_comp": r[6],
            "gain": r[7],
            "cost": r[8],
        }
        for r in rows
    ]


def get_batch_metrics(batch_id: int) -> dict | None:
    """Get metrics for a batch."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT batch_id, total_gains, total_cost, roi,
                  bons_numeros_min, bons_numeros_max, bons_numeros_avg,
                  gain_min, gain_max
           FROM batch_metrics WHERE batch_id = ?""",
        (batch_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "batch_id": row[0],
        "total_gains": row[1],
        "total_cost": row[2],
        "roi": row[3],
        "bons_numeros_min": row[4],
        "bons_numeros_max": row[5],
        "bons_numeros_avg": row[6],
        "gain_min": row[7],
        "gain_max": row[8],
    }
