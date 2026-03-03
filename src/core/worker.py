import time
import json
import traceback
import pandas as pd
from datetime import datetime
from PyQt6.QtCore import QThread, pyqtSignal

from src.core.database import get_pending_task, update_task_status
from src.core.registry import registry

class EvaluationWorker(QThread):
    """
    Thread d'arrière-plan chargé de dépiler la base de données (statut PENDING),
    d'exécuter les prédictions, de les comparer à l'historique et d'enregistrer les métriques.
    """
    # Signaux pour communiquer avec l'UI principale (si besoin plus tard)
    task_started = pyqtSignal(int)
    task_finished = pyqtSignal(int, dict)
    task_error = pyqtSignal(int, str)
    
    def __init__(self):
        super().__init__()
        self._is_running = True
        self._is_paused = False
        
        # Cache des instances de jeux pour éviter de recharger l'historique csv à chaque itération
        self.cached_games = {}

    def stop(self):
        self._is_running = False

    def pause(self):
        self._is_paused = True

    def resume(self):
        self._is_paused = False

    def run(self):
        print("[WORKER] Démarrage du thread d'évaluation.")
        while self._is_running:
            if self._is_paused:
                time.sleep(1)
                continue

            # 1. Récupérer une tâche
            task = get_pending_task()
            if not task:
                # Plus rien dans la file d'attente, on dort un peu
                time.sleep(2)
                continue

            task_id = task['id']
            self.task_started.emit(task_id)
            print(f"[WORKER] Démarrage de la tâche ID:{task_id}")

            try:
                # 2. Récupérer ou initialiser le Jeu
                game_name = task['game_name']
                game_params = task['game_params']
                
                # Clé de cache pour ne pas recharcher le même jeu avec les mêmes paramètres 
                # (Attention : si les dates changent, on doit peut-être recharger ? 
                # En l'état, l'historique entier est chargé dans pandas, on filtrera ensuite sur les dates)
                cache_key = f"{game_name}_{json.dumps(game_params, sort_keys=True)}"
                
                if cache_key not in self.cached_games:
                    game_class = registry.get_game_class(game_name)
                    if not game_class:
                        raise ValueError(f"Jeu '{game_name}' introuvable dans le registre.")
                    
                    game_instance = game_class(game_params)
                    game_instance.fetch_history() # Télécharge/Charge le CSV
                    self.cached_games[cache_key] = game_instance
                
                game = self.cached_games[cache_key]
                if game.history.empty:
                    raise ValueError(f"L'historique du jeu '{game_name}' est vide ou n'a pas pu être chargé.")

                # 3. Initialiser le Modèle
                model_name = task['model_name']
                model_params = task['model_params']
                model_class = registry.get_model_class(model_name)
                if not model_class:
                    raise ValueError(f"Modèle '{model_name}' introuvable dans le registre.")
                
                model = model_class(model_params)

                # 4. Filtrer l'historique selon les dates demandées dans l'onglet Config
                # Format attendu : YYYY-MM-DD
                date_debut = pd.to_datetime(game_params.get("date_debut", "2000-01-01"))
                date_fin = pd.to_datetime(game_params.get("date_fin", datetime.today().strftime('%Y-%m-%d')))
                
                # /!\ Cette colonne de date dépend du jeu. Loto l'appelle "date_de_tirage".
                # Pour le rendre générique, les jeux devraient assurer que leur date est dans une colonne standard.
                # Supposons ici que 'date_de_tirage' est la convention pour nos jeux de tirage type FDJ.
                mask = (game.history['date_de_tirage'] >= date_debut) & (game.history['date_de_tirage'] <= date_fin)
                historique_filtre = game.history.loc[mask]

                if historique_filtre.empty:
                    raise ValueError("Aucun tirage trouvé dans l'historique pour les dates sélectionnées.")

                # 5. Exécution : Comparaison pour chaque tirage filtré
                total_cost = 0.0
                total_fiat_gain = 0.0
                total_hits = 0 # Nombre de tirages rapportant un gain
                
                # Le modèle predict() peut être appelé une fois pour toute la période (modèle macro)
                # ou pour chaque tirage. Dans notre modèle SameValue, il est constant.
                # Appelons-le une première fois ici au global par soucis de POC.
                predicted_grid = model.predict(game.history, date_debut)

                # Iterrows() est lent pour de très gros datasets, mais suffisant pour quelques milliers de lignes.
                for index, real_grid_row in historique_filtre.iterrows():
                    metrics = game.calculate_metrics(predicted_grid, real_grid_row)
                    total_cost += metrics["cost"]
                    total_fiat_gain += metrics["fiat_gain"]
                    if metrics.get("is_win", False):
                        total_hits += 1

                # Consolidation des résultats globaux de cette tâche (cette itération)
                net_profit = total_fiat_gain - total_cost
                global_roi = (net_profit / total_cost) if total_cost > 0 else 0.0
                hit_rate = (total_hits / len(historique_filtre)) * 100

                final_results = {
                    "total_cost": round(total_cost, 2),
                    "total_fiat_gain": round(total_fiat_gain, 2),
                    "net_profit": round(net_profit, 2),
                    "global_roi": round(global_roi, 4),
                    "hit_rate_percent": round(hit_rate, 2),
                    "draws_analyzed": len(historique_filtre)
                }

                # 6. Sauvegarde en DONE dans SQLite
                update_task_status(task_id, "DONE", results=final_results)
                self.task_finished.emit(task_id, final_results)
                print(f"[WORKER] Tâche ID:{task_id} terminée avec succès. ROI: {final_results['global_roi']}")

            except Exception as e:
                error_msg = traceback.format_exc()
                print(f"[WORKER] Erreur sur la tâche ID:{task_id} :\n{error_msg}")
                update_task_status(task_id, "ERROR", error=str(e))
                self.task_error.emit(task_id, str(e))

        print("[WORKER] Thread d'évaluation stoppé.")
