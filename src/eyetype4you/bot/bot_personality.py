from dataclasses import dataclass
from typing import Dict, List
import random

@dataclass
class BotPersonality:
    name: str = "Default"
    base_typing_speed: float = 0.12  # seconds between keystrokes
    error_rate: float = 0.02  # 2% chance of typo
    correction_delay: float = 0.3  # pause before correcting
    line_break_pause: float = 0.8  # pause at line breaks
    punctuation_pause: float = 0.4  # pause after punctuation
    
    # Keyboard layout for realistic typos
    _nearby_keys: Dict[str, List[str]] = None
    
    def __post_init__(self):
        self._init_keyboard_layout()
    
    def should_make_typo(self) -> bool:
        """Determines if the next character should be a typo."""
        return random.random() < self.error_rate
    
    def get_nearby_key(self, char: str) -> str:
        """Returns a character physically near the intended one."""
        if char.lower() in self._nearby_keys:
            return random.choice(self._nearby_keys[char.lower()])
        return char
    
    def _init_keyboard_layout(self) -> None:
        """Initialize QWERTY keyboard layout for realistic typos."""
        self._nearby_keys = {
            'a': ['q', 'w', 's', 'z'],
            'b': ['v', 'g', 'h', 'n'],
            'c': ['x', 'd', 'f', 'v'],
            'd': ['s', 'e', 'r', 'f', 'c', 'x'],
            'e': ['w', 's', 'd', 'r'],
            'f': ['d', 'r', 't', 'g', 'v', 'c'],
            'g': ['f', 't', 'y', 'h', 'b', 'v'],
            'h': ['g', 'y', 'u', 'j', 'n', 'b'],
            'i': ['u', 'j', 'k', 'o'],
            'j': ['h', 'u', 'i', 'k', 'm', 'n'],
            'k': ['j', 'i', 'o', 'l', 'm'],
            'l': ['k', 'o', 'p', 'm'],
            'm': ['n', 'j', 'k', 'l'],
            'n': ['b', 'h', 'j', 'm'],
            'o': ['i', 'k', 'l', 'p'],
            'p': ['o', 'l'],
            'q': ['w', 'a', '1', '2'],
            'r': ['e', 'd', 'f', 't'],
            's': ['a', 'w', 'e', 'd', 'x', 'z'],
            't': ['r', 'f', 'g', 'y'],
            'u': ['y', 'h', 'j', 'i'],
            'v': ['c', 'f', 'g', 'b'],
            'w': ['q', 'a', 's', 'e'],
            'x': ['z', 's', 'd', 'c'],
            'y': ['t', 'g', 'h', 'u'],
            'z': ['a', 's', 'x'],
            '1': ['q', '2'],
            '2': ['1', 'q', 'w', '3'],
            '3': ['2', 'w', 'e', '4'],
            '4': ['3', 'e', 'r', '5'],
            '5': ['4', 'r', 't', '6'],
            '6': ['5', 't', 'y', '7'],
            '7': ['6', 'y', 'u', '8'],
            '8': ['7', 'u', 'i', '9'],
            '9': ['8', 'i', 'o', '0'],
            '0': ['9', 'o', 'p', '-'],
            '-': ['0', 'p', '[', '='],
            '=': ['-', '[', ']'],
            ' ': ['c', 'v', 'b', 'n', 'm']  # Common thumb position errors
        }
    
    @classmethod
    def create_custom(cls, **kwargs):
        """Creates a custom personality with specified parameters."""
        return cls(**kwargs)