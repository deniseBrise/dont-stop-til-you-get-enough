from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, 
    QFormLayout, QGroupBox, QSpinBox, QDateEdit, QCheckBox, 
    QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate

from src.core.registry import registry
from src.core.database import add_tasks

class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)

        # 1. Sélection du Jeu
        self.game_layout = QHBoxLayout()
        self.game_combo = QComboBox()
        self.game_combo.addItems(["-- Sélectionner un jeu --"] + list(registry.games.keys()))
        self.game_combo.currentTextChanged.connect(self.on_game_selected)
        
        self.game_layout.addWidget(QLabel("Jeu :"))
        self.game_layout.addWidget(self.game_combo)
        self.main_layout.addLayout(self.game_layout)

        # GroupBox pour les Paramètres du jeu
        self.game_params_group = QGroupBox("Paramètres du Jeu")
        self.game_params_layout = QFormLayout(self.game_params_group)
        self.main_layout.addWidget(self.game_params_group)
        self.game_widgets = {} # Va contenir les widgets générés pour le jeu (clé = nom_parametre)

        # 2. Sélection du Modèle
        self.model_layout = QHBoxLayout()
        self.model_combo = QComboBox()
        self.model_combo.addItems(["-- Sélectionner un modèle --"])
        self.model_combo.currentTextChanged.connect(self.on_model_selected)
        
        self.model_layout.addWidget(QLabel("Modèle :"))
        self.model_layout.addWidget(self.model_combo)
        self.main_layout.addLayout(self.model_layout)

        # GroupBox pour les Paramètres du modèle
        self.model_params_group = QGroupBox("Paramètres du Modèle")
        self.model_params_layout = QFormLayout(self.model_params_group)
        self.main_layout.addWidget(self.model_params_group)
        self.model_widgets = {}

        # 3. Paramètres de l'étude (Itérations)
        self.study_group = QGroupBox("Configuration de l'Étude")
        self.study_layout = QFormLayout(self.study_group)
        self.iterations_spinbox = QSpinBox()
        self.iterations_spinbox.setRange(1, 10000)
        self.iterations_spinbox.setValue(1)
        self.study_layout.addRow("Nombre d'itérations :", self.iterations_spinbox)
        self.main_layout.addWidget(self.study_group)

        # Bouton d'ajout
        self.add_button = QPushButton("Ajouter à la file d'attente (Générer les tâches)")
        self.add_button.clicked.connect(self.generate_tasks)
        self.main_layout.addWidget(self.add_button)

        # Spacer pour pousser vers le haut
        self.main_layout.addStretch()

        self.on_game_selected(self.game_combo.currentText())

    def clear_layout(self, layout):
        """Supprime tous les widgets d'un layout."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _build_dynamic_form(self, schema: dict, layout: QFormLayout, widget_dict: dict):
        """Génère des widgets PyQt dynamiquement basé sur un dictionnaire schema de la classe BaseGame ou BaseModel."""
        self.clear_layout(layout)
        widget_dict.clear()

        for param_name, param_info in schema.items():
            param_type = param_info.get("type", "str")
            label_text = param_info.get("label", param_name)
            
            widget = None
            if param_type == "int":
                widget = QSpinBox()
                widget.setRange(param_info.get("min", -99999), param_info.get("max", 99999))
                widget.setValue(param_info.get("default", 0))
            elif param_type == "date":
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                if param_info.get("default") == "today":
                    widget.setDate(QDate.currentDate())
            elif param_type == "bool":
                widget = QCheckBox()
                widget.setChecked(param_info.get("default", False))
                
            if widget:
                layout.addRow(label_text, widget)
                widget_dict[param_name] = widget

    def on_game_selected(self, game_name):
        self.model_combo.clear()
        self.model_combo.addItems(["-- Sélectionner un modèle --"])
        self.clear_layout(self.game_params_layout)
        self.game_widgets.clear()

        game_class = registry.get_game_class(game_name)
        if game_class:
            # Génération dynamique des paramètres du jeu
            schema = game_class.get_parameters_schema()
            self._build_dynamic_form(schema, self.game_params_layout, self.game_widgets)
            
            # Mise à jour des modèles compatibles
            compatible_models = game_class.get_compatible_models()
            for model_name in compatible_models:
                if model_name in registry.models:
                    self.model_combo.addItem(model_name)

    def on_model_selected(self, model_name):
        self.clear_layout(self.model_params_layout)
        self.model_widgets.clear()
        
        model_class = registry.get_model_class(model_name)
        if model_class:
            schema = model_class.get_parameters_schema()
            self._build_dynamic_form(schema, self.model_params_layout, self.model_widgets)

    def _extract_values(self, widget_dict: dict) -> dict:
        """Extrait les valeurs des widgets dynamiques selon leur type."""
        values = {}
        for name, widget in widget_dict.items():
            if isinstance(widget, QSpinBox):
                values[name] = widget.value()
            elif isinstance(widget, QDateEdit):
                # Format ISO YYYY-MM-DD
                values[name] = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QCheckBox):
                values[name] = widget.isChecked()
        return values

    def generate_tasks(self):
        """Génère les itérations et les ajoute à SQLite en PENDING."""
        game_name = self.game_combo.currentText()
        model_name = self.model_combo.currentText()

        if game_name == "-- Sélectionner un jeu --" or model_name == "-- Sélectionner un modèle --":
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un jeu et un modèle valides.")
            return

        game_params = self._extract_values(self.game_widgets)
        model_params = self._extract_values(self.model_widgets)
        iterations = self.iterations_spinbox.value()

        tasks = []
        for i in range(1, iterations + 1):
            tasks.append({
                "game_name": game_name,
                "game_params": game_params,
                "model_name": model_name,
                "model_params": model_params,
                "iteration": i
            })
        
        add_tasks(tasks)
        QMessageBox.information(self, "Succès", f"{iterations} tâche(s) ajoutée(s) à la file d'attente.")
