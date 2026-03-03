import os
import zipfile
import requests
import pandas as pd
from typing import Dict, Any
from io import BytesIO
from datetime import datetime
from pathlib import Path

from src.core.base_game import BaseGame

class Loto(BaseGame):
    URL_FDJ = "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afp6"
    DATA_DIR = Path("data/loto")
    CSV_PATH = DATA_DIR / "loto_history.csv"

    def __init__(self, params: Dict[str, Any]):
        super().__init__(params)
        
    @classmethod
    def get_name(cls) -> str:
        return "Loto (FDJ)"

    @classmethod
    def get_parameters_schema(cls) -> Dict[str, Any]:
        return {
            "date_debut": {"type": "date", "label": "Date de début", "default": "today"},
            "date_fin": {"type": "date", "label": "Date de fin", "default": "today"},
            "nb_grilles": {"type": "int", "label": "Nombre de grilles / jour", "min": 1, "max": 1000, "default": 1},
            "second_tirage": {"type": "bool", "label": "Activer le second tirage (0.80€)", "default": False},
            "joker_plus": {"type": "bool", "label": "Option Joker+ (1.00€)", "default": False}
        }

    @classmethod
    def get_compatible_models(cls) -> list[str]:
        return ["Valeurs Fixes (Same Value)", "Aléatoire (Random)"]

    def fetch_history(self) -> None:
        """
        Télécharge le ZIP depuis le site de la FDJ, l'extrait, et parse le CSV récent 
        vers la variable self.history.
        Note: Ceci est bloquant, il faudra l'appeler dans un processus d'arrière-plan.
        """
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # Pour le PoC: On simule d'abord la récupération si on a déjà un fichier local
        # ou on télécharge le ZIP depuis l'API. (En production l'URL ou la méthode de scrap devra être adaptée
        # car ce lien uuid peut expirer ou être modifié)
        
        try:
            print(f"[LOTO] Tentative de téléchargement depuis : {self.URL_FDJ}")
            response = requests.get(self.URL_FDJ, stream=True, timeout=10)
            if response.status_code == 200:
                print("[LOTO] Archive récupérée avec succès. Extraction...")
                with zipfile.ZipFile(BytesIO(response.content)) as z:
                    # Trouver le premier fichier CSV de l'archive
                    csv_filename = [f for f in z.namelist() if f.endswith('.csv')][0]
                    with z.open(csv_filename) as csv_file:
                        with open(self.CSV_PATH, 'wb') as out_file:
                            out_file.write(csv_file.read())
            else:
                print(f"[LOTO] Échec du téléchargement (HTTP {response.status_code}).")
        except Exception as e:
            print(f"[LOTO] Erreur de récupération: {e}. Essai de lecture du fichier local si existant.")

        # Chargement du DataFrame depuis le fichier CSV de la FDJ (séparateur point-virgule)
        if self.CSV_PATH.exists():
            print("[LOTO] Lecture du fichier d'historique local...")
            # Les données FDJ sont souvent encodées en latin-1 ou iso
            try:
                self.history = pd.read_csv(self.CSV_PATH, sep=';', encoding='latin-1', low_memory=False)
                # Formater les dates pour qu'elles soient en datetime pour la recherche
                if 'date_de_tirage' in self.history.columns:
                    self.history['date_de_tirage'] = pd.to_datetime(self.history['date_de_tirage'], format='%d/%m/%Y', errors='coerce')
                print(f"[LOTO] Historique chargé avec succès : {len(self.history)} tirages.")
            except Exception as e:
                print(f"[LOTO] Erreur de parsing du CSV : {e}")
                self.history = pd.DataFrame()
        else:
            print("[LOTO] Aucun fichier d'historique trouvé et impossible de le télécharger.")

    def calculate_metrics(self, predicted_grid: Dict[str, list], real_grid_row: pd.Series) -> Dict[str, float]:
        """
        Compare une prédiction (predicted_grid) avec une ligne de l'historique (real_grid_row).
        Retourne des indicateurs de performance.
        predicted_grid ex: {"numeros": [1,2,3,4,5], "chance": 8}
        """
        cost = 2.20
        fiat_gain = 0.0
        
        # Le second tirage coûte 0.80€ de plus
        if self.params.get("second_tirage", False):
            cost += 0.80
            
        # Joker+ (1 ou 2 jeux possibles, disons 1€ par défaut dans le PoC)
        if self.params.get("joker_plus", False):
            cost += 1.00

        # ... la logique complexe de comparaison de la FDJ (rapport de gain) 
        # sera implémentée ici de façon empirique ou via un scraper des rapports...
        # Pour le PoC : Simulation d'un gain si 2 numéros ou plus.
        
        real_numeros = [
            real_grid_row.get('boule_1', 0), real_grid_row.get('boule_2', 0),
            real_grid_row.get('boule_3', 0), real_grid_row.get('boule_4', 0),
            real_grid_row.get('boule_5', 0)
        ]
        real_chance = real_grid_row.get('numero_chance', 0)

        # Calculer l'intersection
        nb_bons_numeros = len(set(predicted_grid["numeros"]).intersection(set(real_numeros)))
        bon_chance = (predicted_grid["chance"] == real_chance)

        # Attribution des gains LOTO (grille indicative simplifiée)
        if nb_bons_numeros == 5 and bon_chance: fiat_gain = 2000000.0
        elif nb_bons_numeros == 5: fiat_gain = 100000.0
        elif nb_bons_numeros == 4 and bon_chance: fiat_gain = 1000.0
        elif nb_bons_numeros == 4: fiat_gain = 400.0
        elif nb_bons_numeros == 3 and bon_chance: fiat_gain = 50.0
        elif nb_bons_numeros == 3: fiat_gain = 20.0
        elif nb_bons_numeros == 2 and bon_chance: fiat_gain = 10.0
        elif nb_bons_numeros == 2: fiat_gain = 4.40
        elif nb_bons_numeros == 1 and bon_chance: fiat_gain = 2.20
        elif bon_chance: fiat_gain = 2.20

        net_profit = fiat_gain - cost
        roi = (net_profit / cost) if cost > 0 else 0.0

        return {
            "cost": cost,
            "fiat_gain": fiat_gain,
            "net_profit": net_profit,
            "roi": roi,
            "hits_num": nb_bons_numeros,
            "hit_chance": int(bon_chance),
            "is_win": bool(fiat_gain > 0)
        }
