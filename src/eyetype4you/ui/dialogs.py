from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QListWidget, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from ..multibot.manager import MultiBotManager
from ..bot.personality_dialog import PersonalityDialog

class MultiBotDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bot_manager = MultiBotManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Initialize the multi-bot manager UI."""
        self.setWindowTitle("Multi-Bot Manager")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        
        # Bot list
        self.bot_list = QListWidget()
        layout.addWidget(self.bot_list)
        
        # Progress bars
        self.progress_bars = {}
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Add Bot")
        add_button.clicked.connect(self.add_bot)
        button_layout.addWidget(add_button)
        
        remove_button = QPushButton("Remove Bot")
        remove_button.clicked.connect(self.remove_selected_bot)
        button_layout.addWidget(remove_button)
        
        stop_button = QPushButton("Stop All")
        stop_button.clicked.connect(self.stop_all_bots)
        button_layout.addWidget(stop_button)
        
        layout.addLayout(button_layout)
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(100)
        
    def add_bot(self):
        """Add a new bot with custom personality."""
        dialog = PersonalityDialog(self)
        if dialog.exec_():
            personality = dialog.get_personality()
            name = personality.name
            if self.bot_manager.add_bot(name, personality):
                self.bot_list.addItem(name)
                progress = QProgressBar()
                self.progress_bars[name] = progress
                layout = self.layout()
                layout.insertWidget(layout.count() - 1, progress)
                
    def remove_selected_bot(self):
        """Remove the selected bot."""
        current = self.bot_list.currentItem()
        if current:
            name = current.text()
            if self.bot_manager.remove_bot(name):
                self.bot_list.takeItem(self.bot_list.row(current))
                if name in self.progress_bars:
                    self.progress_bars[name].deleteLater()
                    del self.progress_bars[name]
                    
    def stop_all_bots(self):
        """Stop all running bots."""
        self.bot_manager.stop_all()
        
    def update_status(self):
        """Update progress bars and status indicators."""
        # To be implemented based on typing progress
        pass