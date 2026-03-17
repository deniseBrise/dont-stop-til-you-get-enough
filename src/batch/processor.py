"""Batch processor with parallel execution."""

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable
import sqlite3

from src.db.schema import get_connection


@dataclass
class BatchConfig:
    """Configuration for a batch."""

    game_config: dict
    model_config: dict
    iterations: int
    workers: int = 1


@dataclass
class BatchResult:
    """Result of a single iteration."""

    iteration: int
    prediction: dict
    matched_numeros: int
    matched_comp: int
    gain: float
    cost: float
    draw_date: str | None = None


@dataclass
class BatchMetrics:
    """Aggregated metrics for a batch."""

    batch_id: int
    total_iterations: int
    completed_iterations: int
    total_gains: float
    total_cost: float
    roi: float
    bons_numeros_min: int
    bons_numeros_max: int
    bons_numeros_avg: float
    gain_min: float
    gain_max: float


class BatchProcessor:
    """Manages batch processing with parallel execution."""

    def __init__(self, max_workers: int | None = None):
        self.max_workers = max_workers or mp.cpu_count()
        self.executor: ProcessPoolExecutor | None = None

    def start_batch(
        self,
        game_config: dict,
        model_config: dict,
        iterations: int,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> int:
        """Start a new batch and return the batch ID."""
        conn = get_connection()
        cursor = conn.cursor()

        # Create batch record
        cursor.execute(
            """INSERT INTO batches (game_id, model_id, game_params, status, total_iterations)
               VALUES (?, ?, ?, ?, ?)""",
            (
                1,  # game_id - would come from game selection
                1,  # model_id - would come from model selection
                str(game_config),
                "running",
                iterations,
            ),
        )
        batch_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Start processing in background
        self._run_batch_async(
            batch_id, game_config, model_config, iterations, progress_callback
        )

        return batch_id

    def _run_batch_async(
        self,
        batch_id: int,
        game_config: dict,
        model_config: dict,
        iterations: int,
        progress_callback: Callable[[int, int], None] | None = None,
    ):
        """Run batch processing asynchronously."""
        # This would be run in a separate process in production
        # For now, just update the batch as completed
        conn = get_connection()
        cursor = conn.cursor()

        # Simulate iterations
        for i in range(iterations):
            # Insert result placeholder
            cursor.execute(
                """INSERT INTO batch_results (batch_id, iteration, prediction, matched_numeros, matched_comp, gain, cost)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    batch_id,
                    i + 1,
                    str({"numeros": [1, 2, 3, 4, 5], "comp": [6]}),
                    0,
                    0,
                    0.0,
                    game_config.get("prix_grille", 2.20),
                ),
            )

            # Update progress
            if progress_callback:
                progress_callback(i + 1, iterations)

            # Update batch completed count
            cursor.execute(
                "UPDATE batches SET completed_iterations = ? WHERE id = ?",
                (i + 1, batch_id),
            )

        # Mark batch as completed
        cursor.execute(
            "UPDATE batches SET status = 'completed', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (batch_id,),
        )

        # Calculate and save metrics
        self._calculate_metrics(batch_id)

        conn.commit()
        conn.close()

    def _calculate_metrics(self, batch_id: int):
        """Calculate aggregated metrics for a batch."""
        conn = get_connection()
        cursor = conn.cursor()

        # Get all results for this batch
        cursor.execute(
            """SELECT matched_numeros, gain, cost FROM batch_results WHERE batch_id = ?""",
            (batch_id,),
        )
        results = cursor.fetchall()

        if not results:
            return

        total_gains = sum(r[1] for r in results)
        total_cost = sum(r[2] for r in results)
        roi = ((total_gains - total_cost) / total_cost * 100) if total_cost > 0 else 0

        matched = [r[0] for r in results]
        gains = [r[1] for r in results]

        metrics = {
            "batch_id": batch_id,
            "total_gains": total_gains,
            "total_cost": total_cost,
            "roi": roi,
            "bons_numeros_min": min(matched),
            "bons_numeros_max": max(matched),
            "bons_numeros_avg": sum(matched) / len(matched),
            "gain_min": min(gains),
            "gain_max": max(gains),
        }

        cursor.execute(
            """INSERT OR REPLACE INTO batch_metrics
               (batch_id, total_gains, total_cost, roi, bons_numeros_min, bons_numeros_max,
                bons_numeros_avg, gain_min, gain_max, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            tuple(metrics.values()),
        )

        conn.close()

    def get_batch_status(self, batch_id: int) -> dict:
        """Get the status of a batch."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, status, total_iterations, completed_iterations, created_at FROM batches WHERE id = ?",
            (batch_id,),
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return {}

        return {
            "id": row[0],
            "status": row[1],
            "total_iterations": row[2],
            "completed_iterations": row[3],
            "created_at": row[4],
        }

    def get_batch_metrics(self, batch_id: int) -> BatchMetrics | None:
        """Get metrics for a batch."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT batch_id, total_gains, total_cost, roi, bons_numeros_min,
                      bons_numeros_max, bons_numeros_avg, gain_min, gain_max
               FROM batch_metrics WHERE batch_id = ?""",
            (batch_id,),
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        # Get total iterations from batches table
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT total_iterations, completed_iterations FROM batches WHERE id = ?",
            (batch_id,),
        )
        batch_row = cursor.fetchone()
        conn.close()

        return BatchMetrics(
            batch_id=row[0],
            total_iterations=batch_row[0] if batch_row else 0,
            completed_iterations=batch_row[1] if batch_row else 0,
            total_gains=row[1],
            total_cost=row[2],
            roi=row[3],
            bons_numeros_min=row[4],
            bons_numeros_max=row[5],
            bons_numeros_avg=row[6],
            gain_min=row[7],
            gain_max=row[8],
        )

    def stop_all_batches(self):
        """Stop all running batches."""
        if self.executor:
            self.executor.shutdown(wait=False)

    def get_all_batches(self) -> list[dict]:
        """Get all batches."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT b.id, b.status, b.total_iterations, b.completed_iterations,
                      b.created_at, g.name, m.name
               FROM batches b
               JOIN games g ON b.game_id = g.id
               JOIN models m ON b.model_id = m.id
               ORDER BY b.created_at DESC"""
        )
        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "status": r[1],
                "total_iterations": r[2],
                "completed_iterations": r[3],
                "created_at": r[4],
                "game": r[5],
                "model": r[6],
            }
            for r in rows
        ]
