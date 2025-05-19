from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QDoubleSpinBox, QPushButton, QComboBox)
from PyQt5.QtCore import Qt
from .bot_personality import BotPersonality

class PersonalityDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.personality = None
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the dialog UI components."""
        self.setWindowTitle("Bot Personality Configuration")
        layout = QVBoxLayout(self)
        
        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Speed configuration
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("Typing Speed:"))
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["Very Fast", "Fast", "Normal", "Slow"])
        speed_layout.addWidget(self.speed_combo)
        layout.addLayout(speed_layout)
        
        # Error rate configuration
        error_layout = QHBoxLayout()
        error_layout.addWidget(QLabel("Error Rate:"))
        self.error_spin = QDoubleSpinBox()
        self.error_spin.setRange(0.0, 0.1)
        self.error_spin.setSingleStep(0.01)
        self.error_spin.setValue(0.02)
        error_layout.addWidget(self.error_spin)
        layout.addLayout(error_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_personality)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
    def save_personality(self):
        """Create a new personality from the dialog inputs."""
        speeds = {"Very Fast": 0.05, "Fast": 0.08, "Normal": 0.12, "Slow": 0.2}
        self.personality = BotPersonality.create_custom(
            name=self.name_input.text(),
            base_typing_speed=speeds[self.speed_combo.currentText()],
            error_rate=self.error_spin.value()
        )
        self.accept()
        
    def get_personality(self) -> BotPersonality:
        """Return the configured personality."""
        return self.personality