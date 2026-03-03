import sys
import os

# Ajout du chemin racine au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
)

from src.core.database import init_db
from src.gui.config_tab import ConfigTab
from src.core.worker import EvaluationWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prédiction & Évaluation de Jeux de Hasard")
        self.resize(800, 600)
        
        # Initialisation Base de données
        init_db()

        # Onglets
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Onglet 1: Configuration
        self.config_tab = ConfigTab()
        self.tabs.addTab(self.config_tab, "Configuration")

        # Onglet 2: Résultats (Sera implémenté plus tard)
        self.results_tab = QWidget()
        self.results_tab.setLayout(QVBoxLayout())
        self.tabs.addTab(self.results_tab, "Résultats")
        
        # Initialisation et démarrage du Worker
        self.worker = EvaluationWorker()
        self.worker.start()

    def closeEvent(self, event):
        """S'assurer de tuer proprement le Worker à la fermeture de l'application."""
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
