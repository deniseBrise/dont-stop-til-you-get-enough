import sqlite3
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

# Fixation du chemin de la base de données dans un dossier data/ à la racine
DB_PATH = Path("data/database.sqlite")

def init_db():
    """Initialise la base de données et crée la table task_queue si elle n'existe pas."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS task_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT NOT NULL,
            game_params TEXT NOT NULL,
            model_name TEXT NOT NULL,
            model_params TEXT NOT NULL,
            iteration INTEGER NOT NULL,
            status TEXT DEFAULT 'PENDING',
            results TEXT,
            exception_log TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_tasks(tasks: List[Dict[str, Any]]):
    """Ajoute une liste de tâches (itérations) dans la file d'attente."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for task in tasks:
        c.execute('''
            INSERT INTO task_queue (game_name, game_params, model_name, model_params, iteration)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            task['game_name'],
            json.dumps(task['game_params']),
            task['model_name'],
            json.dumps(task['model_params']),
            task['iteration']
        ))
    conn.commit()
    conn.close()

def get_pending_task() -> Optional[Dict[str, Any]]:
    """Récupère une tâche en attente ('PENDING') et la passe en 'RUNNING'.
    Retourne la tâche sous forme de dictionnaire ou None si la file est vide."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Trouver une tâche en attente
    c.execute("SELECT * FROM task_queue WHERE status = 'PENDING' LIMIT 1")
    row = c.fetchone()
    
    if row:
        task_id = row['id']
        # La marquer immédiatement comme en cours d'exécution
        c.execute("UPDATE task_queue SET status = 'RUNNING', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        
        # Convertir en dict et parser le JSON
        task_dict = dict(row)
        task_dict['game_params'] = json.loads(task_dict['game_params'])
        task_dict['model_params'] = json.loads(task_dict['model_params'])
        return task_dict
        
    conn.close()
    return None

def update_task_status(task_id: int, status: str, results: Dict[str, Any] = None, error: str = None):
    """Met à jour le statut d'une tâche (ex: DONE ou ERROR) et enregistre les résultats."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    res_str = json.dumps(results) if results else None
    c.execute('''
        UPDATE task_queue 
        SET status = ?, results = ?, exception_log = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (status, res_str, error, task_id))
    conn.commit()
    conn.close()

def clear_queue():
    """Vide entièrement la file d'attente."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM task_queue")
    conn.commit()
    conn.close()
