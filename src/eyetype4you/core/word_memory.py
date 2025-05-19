"""
Word Memory System for EyeType4You.
"""

import json
import time
import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)

class WordMemory:
    def __init__(self, memory_file: Union[str, Path], auto_save: bool = True):
        self._memory: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._memory_file = Path(memory_file)
        self._modified = False
        self._auto_save = auto_save
        self._load_memory()
        logger.info(f"Word memory initialized with {len(self._memory)} words")

    def _load_memory(self) -> bool:
        if not self._memory_file.exists():
            logger.info(f"Memory file not found: {self._memory_file}")
            return False
        try:
            with open(self._memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            with self._lock:
                self._memory = data
                self._modified = False
            logger.info(f"Loaded {len(self._memory)} words from memory file")
            return True
        except Exception as e:
            logger.error(f"Error loading memory file: {e}", exc_info=True)
            return False

    def save_memory(self) -> bool:
        if not self._modified:
            logger.debug("No changes to save")
            return True
        try:
            self._memory_file.parent.mkdir(parents=True, exist_ok=True)
            with self._lock:
                with open(self._memory_file, 'w', encoding='utf-8') as f:
                    json.dump(self._memory, f, indent=2)
                self._modified = False
            logger.info(f"Saved {len(self._memory)} words to memory file")
            return True
        except Exception as e:
            logger.error(f"Error saving memory file: {e}", exc_info=True)
            return False

    def record_word_usage(self, word: str) -> None:
        if not word or len(word) < 2:
            return
        word = word.lower()
        with self._lock:
            current_time = time.time()
            if word not in self._memory:
                self._memory[word] = {
                    'count': 1,
                    'first_seen': current_time,
                    'last_used': current_time,
                    'confidence': 0.1
                }
            else:
                self._memory[word]['count'] += 1
                self._memory[word]['last_used'] = current_time
                count = self._memory[word]['count']
                self._memory[word]['confidence'] = min(0.95, 0.1 + (count * 0.05))
            self._modified = True
        if self._auto_save:
            self.save_memory()

    def get_word_confidence(self, word: str) -> float:
        if not word:
            return 0.0
        word = word.lower()
        with self._lock:
            if word not in self._memory:
                return 0.0
            memory_entry = self._memory[word]
            base_confidence = memory_entry.get('confidence', 0.0)
            current_time = time.time()
            days_since_use = (current_time - memory_entry['last_used']) / (60 * 60 * 24)
            decay_factor = 1.0 - min(0.9, (days_since_use / 7) * 0.1)
            return base_confidence * decay_factor

    def get_memory_stats(self) -> Dict[str, Any]:
        with self._lock:
            total_words = len(self._memory)
            if total_words == 0:
                return {
                    'total_words': 0,
                    'avg_confidence': 0.0,
                    'high_confidence_words': 0,
                    'total_usages': 0
                }
            total_confidence = 0.0
            high_confidence = 0
            total_usages = 0
            for word_data in self._memory.values():
                conf = word_data.get('confidence', 0.0)
                total_confidence += conf
                if conf > 0.7:
                    high_confidence += 1
                total_usages += word_data.get('count', 0)
            return {
                'total_words': total_words,
                'avg_confidence': total_confidence / total_words,
                'high_confidence_words': high_confidence,
                'total_usages': total_usages
            }

    def reset_memory(self) -> None:
        with self._lock:
            self._memory = {}
            self._modified = True
        logger.warning("Word memory reset (all data cleared)")
        if self._auto_save:
            self.save_memory()

    def get_difficult_words(self, limit: int = 10) -> Dict[str, float]:
        with self._lock:
            sorted_words = sorted(
                [(word, data.get('confidence', 0.0)) 
                 for word, data in self._memory.items()],
                key=lambda x: x[1]
            )
            return dict(sorted_words[:limit])