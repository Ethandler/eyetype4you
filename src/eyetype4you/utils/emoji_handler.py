import re
import unicodedata
import pyautogui
import keyboard
from typing import Dict, Optional

class EmojiHandler:
    def __init__(self):
        self._emoji_pattern = re.compile(
            "["
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251" 
            "]+"
        )
        
    def is_emoji(self, char: str) -> bool:
        """Check if a character is an emoji."""
        return bool(self._emoji_pattern.match(char))
        
    def insert_emoji(self, emoji: str) -> None:
        """Insert an emoji using system clipboard."""
        # Store current clipboard content
        old_clipboard = pyautogui.hotkey('ctrl', 'c')
        
        # Copy emoji to clipboard
        pyautogui.write(emoji)
        
        # Paste emoji
        pyautogui.hotkey('ctrl', 'v')
        
        # Restore clipboard if needed
        if old_clipboard:
            keyboard.write(old_clipboard)
            
    def get_emoji_name(self, emoji: str) -> Optional[str]:
        """Get the Unicode name of an emoji."""
        try:
            return unicodedata.name(emoji)
        except ValueError:
            return None