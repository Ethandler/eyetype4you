from typing import Optional, Dict, Callable
import random
import time
import threading
import logging
from ..utils.emoji_handler import EmojiHandler
from ..bot.bot_personality import BotPersonality

# Configure module logger
logger = logging.getLogger(__name__)

class TypingEngine:
    """
    Typing Engine for EyeType4You.
    """
    def __init__(
        self,
        personality: Optional[BotPersonality] = None,
        speed: float = 0.12,
        error_rate: float = 0.02,
        correction_delay: float = 0.3,
        punctuation_delay: Optional[Dict[str, float]] = None,
        word_memory = None
    ):
        self.personality = personality or BotPersonality()
        self.emoji_handler = EmojiHandler()
        self._running = False
        self._lock = threading.Lock()
        self.speed = speed
        self.error_rate = error_rate
        self.correction_delay = correction_delay
        self.punctuation_delay = punctuation_delay or {}
        self.word_memory = word_memory or []

    def set_speed(self, speed: float) -> None:
        self.speed = speed

    def set_error_rate(self, error_rate: float) -> None:
        self.error_rate = error_rate

    def _get_char_delay(self, char: str) -> float:
        base_delay = self.speed
        variance = random.uniform(-0.1, 0.1) * base_delay
        return max(0.01, base_delay + variance)

    def _should_make_error(self, char: str, word: str) -> bool:
        return random.random() < self.error_rate

    def _generate_typo(self, char: str) -> str:
        return self.personality.get_nearby_key(char)

    def type_text(
        self,
        text: str,
        type_callback: Callable[[str], None],
        backspace_callback: Callable[[], None],
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> bool:
        self._running = True
        for char in text:
            if not self._running:
                return False

            if self._should_make_error(char, text):
                typo = self._generate_typo(char)
                type_callback(typo)
                time.sleep(self.correction_delay)
                backspace_callback()
                type_callback(char)
            else:
                type_callback(char)

            if progress_callback:
                progress_callback(text.index(char) / len(text))

            time.sleep(self._get_char_delay(char))
        return True

    def stop_typing(self) -> None:
        self._running = False

    @property
    def is_typing(self) -> bool:
        return self._running

    @property
    def speed(self) -> float:
        return self.speed

    @property
    def error_rate(self) -> float:
        return self.error_rate