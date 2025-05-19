from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Theme(ABC):
    """Base theme class defining the interface for UI themes."""
    name: str
    
    @property
    @abstractmethod
    def text_editor_style(self) -> str:
        """CSS styling for the text editor."""
        pass
        
    @property
    @abstractmethod
    def button_style(self) -> str:
        """CSS styling for buttons."""
        pass

class CyberpunkTheme(Theme):
    """Dark cyberpunk theme with neon blue accents."""
    def __init__(self):
        super().__init__("Cyberpunk (Dark City)")
        
    @property
    def text_editor_style(self) -> str:
        return """
        QTextEdit {
            background-color: #1a1a1a;
            color: #00ffff;
            border: 1px solid #00aaff;
            border-radius: 5px;
            font-family: 'Consolas';
            font-size: 14px;
        }
        """
        
    @property
    def button_style(self) -> str:
        return """
        QPushButton {
            background-color: #2a2a2a;
            color: #00ffff;
            border: 2px solid #00aaff;
            border-radius: 5px;
            padding: 5px 15px;
        }
        QPushButton:hover {
            background-color: #00aaff;
            color: #ffffff;
        }
        """

class PinkCityTheme(Theme):
    """Light modern theme with pink accents."""
    def __init__(self):
        super().__init__("Pink City (Light)")
        
    @property
    def text_editor_style(self) -> str:
        return """
        QTextEdit {
            background-color: #ffffff;
            color: #ff69b4;
            border: 1px solid #ff1493;
            border-radius: 5px;
            font-family: 'Segoe UI';
            font-size: 14px;
        }
        """
        
    @property
    def button_style(self) -> str:
        return """
        QPushButton {
            background-color: #ffffff;
            color: #ff1493;
            border: 2px solid #ff69b4;
            border-radius: 5px;
            padding: 5px 15px;
        }
        QPushButton:hover {
            background-color: #ff69b4;
            color: #ffffff;
        }
        """