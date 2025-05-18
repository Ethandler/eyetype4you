"""
Personality Dialog Module for Eyetype4You

This module provides the UI components for selecting, creating, and managing bot personalities.
"""

from PyQt5.QtWidgets import (QDialog, QTabWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QListWidget, QPushButton, QLineEdit, 
                            QTextEdit, QSlider, QComboBox, QCheckBox, 
                            QMessageBox, QWidget, QGroupBox, QFormLayout,
                            QDoubleSpinBox, QSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from bot_personality import BotPersonality

class PersonalityDialog(QDialog):
    """Dialog for selecting and managing bot personalities."""
    
    # Signal emitted when a personality is selected
    personality_selected = pyqtSignal(str)
    
    def __init__(self, parent=None, current_personality_id="natural_typist"):
        super().__init__(parent)
        self.setWindowTitle("Bot Personalities")
        self.setMinimumSize(600, 500)
        
        self.current_personality_id = current_personality_id
        
        # Initialize attributes that will be created in setup methods
        # This ensures they exist even if there's a problem with the setup sequence
        self.details_title = None
        self.details_description = None
        self.details_params = None
        self.personality_list = None
        self.select_button = None
        self.custom_list = None
        self.edit_button = None
        self.delete_button = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the dialog UI."""
        main_layout = QVBoxLayout(self)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.select_tab = QWidget()
        self.create_tab = QWidget()
        self.manage_tab = QWidget()
        
        self.tabs.addTab(self.select_tab, "Select Personality")
        self.tabs.addTab(self.create_tab, "Create New")
        self.tabs.addTab(self.manage_tab, "Manage Custom")
        
        # Initialize tab contents
        self.setup_select_tab()
        self.setup_create_tab()
        self.setup_manage_tab()
        
        main_layout.addWidget(self.tabs)
        
        # Add close button at the bottom
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        main_layout.addWidget(close_button)
    
    def setup_select_tab(self):
        """Set up the personality selection tab."""
        layout = QVBoxLayout(self.select_tab)
        
        # Instructions
        instructions = QLabel("Select a personality for your typing bot:")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Main content area with personalities list and details
        content_layout = QHBoxLayout()
        
        # Personality list (left)
        list_layout = QVBoxLayout()
        self.personality_list = QListWidget()
        self.personality_list.currentItemChanged.connect(self.on_personality_selected)
        
        # Load personalities
        personality_ids = BotPersonality.get_all_personality_ids()
        for personality_id in personality_ids:
            personality = BotPersonality(personality_id)
            self.personality_list.addItem(personality.name)
            # Store the ID as item data
            item = self.personality_list.item(self.personality_list.count() - 1)
            item.setData(Qt.UserRole, personality_id)
            
            # Select the current personality
            if personality_id == self.current_personality_id:
                self.personality_list.setCurrentItem(item)
        
        list_layout.addWidget(self.personality_list)
        content_layout.addLayout(list_layout, 1)
        
        # Personality details (right)
        details_layout = QVBoxLayout()
        self.details_title = QLabel("Select a personality")
        self.details_title.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.details_description = QTextEdit()
        self.details_description.setReadOnly(True)
        self.details_description.setMinimumHeight(100)
        
        self.details_params = QTextEdit()
        self.details_params.setReadOnly(True)
        
        details_layout.addWidget(self.details_title)
        details_layout.addWidget(self.details_description)
        details_layout.addWidget(QLabel("Typing Parameters:"))
        details_layout.addWidget(self.details_params)
        
        content_layout.addLayout(details_layout, 2)
        layout.addLayout(content_layout)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.select_button = QPushButton("Select This Personality")
        self.select_button.setEnabled(False)
        self.select_button.clicked.connect(self.apply_selected_personality)
        
        buttons_layout.addWidget(self.select_button)
        layout.addLayout(buttons_layout)
    
    def setup_create_tab(self):
        """Set up the personality creation tab."""
        layout = QVBoxLayout(self.create_tab)
        
        # Instructions
        instructions = QLabel("Create a new personality by adjusting the parameters below:")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Form layout for personality parameters
        form_layout = QFormLayout()
        
        # Basic info
        self.create_name = QLineEdit()
        self.create_name.setPlaceholderText("e.g., 'My Custom Typist'")
        
        self.create_description = QTextEdit()
        self.create_description.setPlaceholderText("Describe this personality's typing style...")
        self.create_description.setMaximumHeight(80)
        
        form_layout.addRow("Name:", self.create_name)
        form_layout.addRow("Description:", self.create_description)
        
        # Core typing parameters
        params_group = QGroupBox("Typing Parameters")
        params_layout = QFormLayout(params_group)
        
        self.create_delay = QDoubleSpinBox()
        self.create_delay.setRange(0.01, 0.5)
        self.create_delay.setSingleStep(0.01)
        self.create_delay.setValue(0.12)
        self.create_delay.setDecimals(2)
        
        self.create_error_rate = QDoubleSpinBox()
        self.create_error_rate.setRange(0.0, 0.1)
        self.create_error_rate.setSingleStep(0.001)
        self.create_error_rate.setValue(0.012)
        self.create_error_rate.setDecimals(3)
        
        self.create_punc_pause = QDoubleSpinBox()
        self.create_punc_pause.setRange(0.0, 1.0)
        self.create_punc_pause.setSingleStep(0.01)
        self.create_punc_pause.setValue(0.18)
        self.create_punc_pause.setDecimals(2)
        
        self.create_space_pause = QDoubleSpinBox()
        self.create_space_pause.setRange(0.0, 1.0)
        self.create_space_pause.setSingleStep(0.01)
        self.create_space_pause.setValue(0.08)
        self.create_space_pause.setDecimals(2)
        
        self.create_thinking_pause = QDoubleSpinBox()
        self.create_thinking_pause.setRange(0.0, 0.1)
        self.create_thinking_pause.setSingleStep(0.005)
        self.create_thinking_pause.setValue(0.025)
        self.create_thinking_pause.setDecimals(3)
        
        params_layout.addRow("Typing Speed (delay in sec):", self.create_delay)
        params_layout.addRow("Error Rate (0.0-0.1):", self.create_error_rate)
        params_layout.addRow("Punctuation Pause Prob (0.0-1.0):", self.create_punc_pause)
        params_layout.addRow("Space Pause Prob (0.0-1.0):", self.create_space_pause)
        params_layout.addRow("Thinking Pause Prob (0.0-0.1):", self.create_thinking_pause)
        
        # Advanced parameters
        advanced_group = QGroupBox("Advanced Parameters")
        advanced_layout = QFormLayout(advanced_group)
        
        self.create_correction_style = QComboBox()
        self.create_correction_style.addItems(["immediate", "delayed", "none"])
        
        self.create_emoji_handling = QComboBox()
        self.create_emoji_handling.addItems(["direct", "pause", "confused"])
        
        self.create_rhythm_variation = QCheckBox("Vary typing rhythm naturally")
        self.create_double_space = QCheckBox("Use double spaces after periods")
        self.create_code_aware = QCheckBox("Code-aware (better indentation)")
        
        advanced_layout.addRow("Correction Style:", self.create_correction_style)
        advanced_layout.addRow("Emoji Handling:", self.create_emoji_handling)
        advanced_layout.addRow("", self.create_rhythm_variation)
        advanced_layout.addRow("", self.create_double_space)
        advanced_layout.addRow("", self.create_code_aware)
        
        # Add groups to layout
        layout.addLayout(form_layout)
        layout.addWidget(params_group)
        layout.addWidget(advanced_group)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.create_button = QPushButton("Create Personality")
        self.create_button.clicked.connect(self.create_personality)
        
        buttons_layout.addWidget(self.create_button)
        layout.addLayout(buttons_layout)
    
    def setup_manage_tab(self):
        """Set up the personality management tab."""
        layout = QVBoxLayout(self.manage_tab)
        
        # Instructions
        instructions = QLabel("Manage your custom personalities:")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Custom personalities list
        self.custom_list = QListWidget()
        self.custom_list.currentItemChanged.connect(self.on_custom_selected)
        
        # Load custom personalities
        custom_personalities = BotPersonality.get_custom_personalities()
        for personality_id, data in custom_personalities.items():
            self.custom_list.addItem(data.get("name", personality_id))
            # Store the ID as item data
            item = self.custom_list.item(self.custom_list.count() - 1)
            item.setData(Qt.UserRole, personality_id)
        
        layout.addWidget(self.custom_list)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.edit_button = QPushButton("Edit")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.edit_custom_personality)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self.delete_custom_personality)
        
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        layout.addLayout(buttons_layout)
    
    def on_personality_selected(self, current, previous):
        """Handle selection of a personality from the list."""
        # Check if UI elements exist
        if not hasattr(self, 'select_button') or not hasattr(self, 'details_title') or \
           not hasattr(self, 'details_description') or not hasattr(self, 'details_params'):
            print("Warning: UI elements not properly initialized")
            return
        
        if not current:
            self.select_button.setEnabled(False)
            if self.details_title:
                self.details_title.setText("Select a personality")
            if self.details_description:
                self.details_description.setText("")
            if self.details_params:
                self.details_params.setText("")
            return
        
        # Get personality ID from item data
        personality_id = current.data(Qt.UserRole)
        
        # Load personality
        personality = BotPersonality(personality_id)
        
        # Update details area
        if self.details_title:
            self.details_title.setText(personality.name)
        if self.details_description:
            self.details_description.setText(personality.description)
        
        # Format parameters
        params_text = f"""
        <b>Typing Speed:</b> {personality.base_delay:.2f} sec delay<br>
        <b>Error Rate:</b> {personality.error_rate * 100:.1f}%<br>
        <b>Punctuation Pause Probability:</b> {personality.punc_pause_prob * 100:.0f}%<br>
        <b>Space Pause Probability:</b> {personality.space_pause_prob * 100:.0f}%<br>
        <b>Thinking Pause Probability:</b> {personality.thinking_pause_prob * 100:.1f}%<br>
        <br>
        <b>Correction Style:</b> {personality.correction_style}<br>
        <b>Emoji Handling:</b> {personality.emoji_handling}<br>
        <b>Code-Aware:</b> {"Yes" if personality.is_code_aware else "No"}<br>
        <b>Rhythm Variation:</b> {"Yes" if personality.uses_rhythm_variation else "No"}<br>
        <b>Double Space After Period:</b> {"Yes" if personality.uses_double_space_after_period else "No"}<br>
        """
        
        if personality.common_misspellings:
            params_text += "<br><b>Common Misspellings:</b><br>"
            for correct, misspelled in personality.common_misspellings[:5]:
                params_text += f"&nbsp;&nbsp;'{correct}' as '{misspelled}'<br>"
            if len(personality.common_misspellings) > 5:
                params_text += f"&nbsp;&nbsp;... and {len(personality.common_misspellings) - 5} more"
        
        if self.details_params:
            self.details_params.setHtml(params_text)
        
        # Enable select button
        if self.select_button:
            self.select_button.setEnabled(True)
    
    def on_custom_selected(self, current, previous):
        """Handle selection of a custom personality."""
        if not hasattr(self, 'edit_button') or not hasattr(self, 'delete_button'):
            print("Warning: UI elements not properly initialized")
            return
        
        if self.edit_button:
            self.edit_button.setEnabled(current is not None)
        if self.delete_button:
            self.delete_button.setEnabled(current is not None)
    
    def apply_selected_personality(self):
        """Apply the selected personality and close the dialog."""
        if not hasattr(self, 'personality_list') or not self.personality_list:
            print("Warning: personality_list not properly initialized")
            return
        
        if not self.personality_list.currentItem():
            return
        
        # Get personality ID from item data
        personality_id = self.personality_list.currentItem().data(Qt.UserRole)
        
        # Emit signal with the selected personality ID
        self.personality_selected.emit(personality_id)
        
        # Close the dialog
        self.accept()
    
    def create_personality(self):
        """Create a new personality from the form inputs."""
        # Get values from form
        name = self.create_name.text().strip()
        description = self.create_description.toPlainText().strip()
        
        # Validate required fields
        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter a name for the personality.")
            return
            
        # Create personality ID from name (lowercase, spaces to underscores)
        personality_id = name.lower().replace(" ", "_")
        
        # Create personality data
        personality_data = {
            "name": name,
            "description": description,
            "base_delay": self.create_delay.value(),
            "error_rate": self.create_error_rate.value(),
            "punc_pause_prob": self.create_punc_pause.value(),
            "space_pause_prob": self.create_space_pause.value(),
            "thinking_pause_prob": self.create_thinking_pause.value(),
            "correction_style": self.create_correction_style.currentText(),
            "emoji_handling": self.create_emoji_handling.currentText(),
            "rhythm_variation": self.create_rhythm_variation.isChecked(),
            "double_space_after_period": self.create_double_space.isChecked(),
            "code_aware": self.create_code_aware.isChecked(),
            "common_misspellings": []  # Could add UI for this in a future enhancement
        }
        
        # Save personality
        success = BotPersonality.save_custom_personality(personality_id, personality_data)
        
        if success:
            QMessageBox.information(self, "Success", f"Created personality: {name}")
            
            # Add to selection list
            item = QListWidget.QListWidgetItem(name)
            item.setData(Qt.UserRole, personality_id)
            self.personality_list.addItem(item)
            self.personality_list.setCurrentItem(item)
            
            # Add to custom list
            item = QListWidget.QListWidgetItem(name)
            item.setData(Qt.UserRole, personality_id)
            self.custom_list.addItem(item)
            
            # Switch to select tab
            self.tabs.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Error", "Failed to create personality. Please try again.")
    
    def edit_custom_personality(self):
        """Edit the selected custom personality."""
        if not self.custom_list.currentItem():
            return
            
        # Get personality ID from item data
        personality_id = self.custom_list.currentItem().data(Qt.UserRole)
        
        # Not implemented in this version
        QMessageBox.information(self, "Not Implemented", 
                               "Editing custom personalities will be available in a future update.")
    
    def delete_custom_personality(self):
        """Delete the selected custom personality."""
        if not self.custom_list.currentItem():
            return
            
        # Get personality ID and name from item data
        personality_id = self.custom_list.currentItem().data(Qt.UserRole)
        personality_name = self.custom_list.currentItem().text()
        
        # Confirm deletion
        confirm = QMessageBox.question(
            self, "Confirm Deletion", 
            f"Are you sure you want to delete the personality '{personality_name}'?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            # Delete personality
            success = BotPersonality.delete_custom_personality(personality_id)
            
            if success:
                # Remove from custom list
                row = self.custom_list.currentRow()
                self.custom_list.takeItem(row)
                
                # Remove from selection list if present
                for i in range(self.personality_list.count()):
                    if self.personality_list.item(i).data(Qt.UserRole) == personality_id:
                        self.personality_list.takeItem(i)
                        break
                
                QMessageBox.information(self, "Success", f"Deleted personality: {personality_name}")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete personality. Please try again.") 