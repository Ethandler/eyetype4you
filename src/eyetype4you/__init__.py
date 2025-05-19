"""
EyeType4You - Human-like typing automation tool.
"""

from .core.typing_engine import TypingEngine
from .bot.bot_personality import BotPersonality
from .ui.main_window import MainWindow
from .multibot.manager import MultiBotManager

__version__ = "1.0.0"
__author__ = "EyeType4You Team"
__all__ = ['TypingEngine', 'BotPersonality', 'MainWindow', 'MultiBotManager']