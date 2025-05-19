from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget)
from PyQt5.QtCore import Qt
from ..utils.templates import TemplateManager

class TemplateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.template_manager = TemplateManager()
        self.setup_ui()
        self.load_templates()
        
    def setup_ui(self):
        """Initialize the template manager UI."""
        self.setWindowTitle("Template Manager")
        self.setMinimumWidth(500)
        layout = QVBoxLayout(self)
        
        # Template list
        self.template_list = QListWidget()
        self.template_list.currentItemChanged.connect(self.load_template)
        layout.addWidget(self.template_list)
        
        # Template name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Template content
        layout.addWidget(QLabel("Content:"))
        self.content_edit = QTextEdit()
        layout.addWidget(self.content_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_template)
        button_layout.addWidget(save_button)
        
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_template)
        button_layout.addWidget(delete_button)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
    def load_templates(self):
        """Load all templates into the list widget."""
        self.template_list.clear()
        self.template_list.addItems(self.template_manager.list_templates())
        
    def load_template(self, current, previous):
        """Load selected template content."""
        if current:
            name = current.text()
            content = self.template_manager.get_template(name)
            self.name_input.setText(name)
            self.content_edit.setText(content)
        
    def save_template(self):
        """Save current template."""
        name = self.name_input.text().strip()
        content = self.content_edit.toPlainText()
        
        if name and content:
            if self.template_manager.save_template(name, content):
                self.load_templates()
                
    def delete_template(self):
        """Delete selected template."""
        current = self.template_list.currentItem()
        if current:
            name = current.text()
            if self.template_manager.delete_template(name):
                self.load_templates()
                self.name_input.clear()
                self.content_edit.clear()