import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
)

from src.core.database import init_db
from src.gui.config_tab import ConfigTab

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

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
