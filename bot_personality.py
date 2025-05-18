"""
Bot Personality Module for Eyetype4You

This module defines the BotPersonality class which encapsulates typing behavior parameters
for different typing styles. It allows creating, saving, and loading different personality profiles
for the typing bots.
"""

import os
import json
import random
from typing import Dict, List, Any, Optional

class BotPersonality:
    """
    Defines a typing personality with specific typing characteristics.
    Each personality affects how the bot types, including speed, errors, and pauses.
    """
    
    # Default personalities included with the application
    DEFAULT_PERSONALITIES = {
        "careful_typist": {
            "name": "Careful Typist",
            "description": "Types slowly and carefully with very few errors.",
            "base_delay": 0.15,  # Slower typing
            "error_rate": 0.005,  # Very low error rate (0.5%)
            "punc_pause_prob": 0.25,  # More likely to pause at punctuation
            "space_pause_prob": 0.15,  # More likely to pause at spaces
            "thinking_pause_prob": 0.02,  # Occasional thinking pauses
            "correction_style": "immediate",  # Corrects mistakes immediately
            "common_misspellings": [],  # No specific misspelling tendencies
            "emoji_handling": "slow"  # Pauses longer before emoji
        },
        "fast_typist": {
            "name": "Fast Typist",
            "description": "Types very quickly with occasional errors.",
            "base_delay": 0.05,  # Fast typing
            "error_rate": 0.015,  # Moderate error rate (1.5%)
            "punc_pause_prob": 0.1,  # Less likely to pause at punctuation
            "space_pause_prob": 0.05,  # Less likely to pause at spaces
            "thinking_pause_prob": 0.01,  # Rare thinking pauses
            "correction_style": "immediate",  # Corrects mistakes immediately
            "common_misspellings": [],  # No specific misspelling tendencies
            "emoji_handling": "direct"  # No special pause for emoji
        },
        "programmer": {
            "name": "Programmer",
            "description": "Efficient with code, careful with syntax, types at medium speed.",
            "base_delay": 0.08,  # Medium typing speed
            "error_rate": 0.01,  # Low error rate (1%)
            "punc_pause_prob": 0.12,  # Medium pause at punctuation
            "space_pause_prob": 0.07,  # Medium pause at spaces
            "thinking_pause_prob": 0.03,  # Occasional thinking pauses
            "correction_style": "immediate",  # Corrects mistakes immediately
            "common_misspellings": [],  # No specific misspelling tendencies
            "emoji_handling": "direct",  # No special pause for emoji
            "code_aware": True  # Better handles code indentation and syntax
        },
        "natural_typist": {
            "name": "Natural Typist",
            "description": "Types with natural rhythms and occasional errors like a typical person.",
            "base_delay": 0.12,  # Default typing speed
            "error_rate": 0.012,  # Standard error rate (1.2%)
            "punc_pause_prob": 0.18,  # Standard pause at punctuation
            "space_pause_prob": 0.08,  # Standard pause at spaces
            "thinking_pause_prob": 0.025,  # Standard thinking pauses
            "correction_style": "immediate",  # Corrects mistakes immediately
            "common_misspellings": [],  # No specific misspelling tendencies
            "emoji_handling": "pause",  # Slight pause before emoji
            "rhythm_variation": True  # Varies typing rhythm naturally
        },
        "learner": {
            "name": "Learning Typist",
            "description": "Types like someone still learning, with more errors and corrections.",
            "base_delay": 0.18,  # Slower typing
            "error_rate": 0.035,  # High error rate (3.5%)
            "punc_pause_prob": 0.22,  # More likely to pause at punctuation
            "space_pause_prob": 0.12,  # More likely to pause at spaces
            "thinking_pause_prob": 0.04,  # More thinking pauses
            "correction_style": "delayed",  # Sometimes notices errors later
            "common_misspellings": [  # Tends to make specific mistakes
                ("the", "teh"),
                ("and", "adn"),
                ("with", "wiht"),
                ("their", "thier"),
                ("your", "youre"),
                ("too", "to"),
                ("you're", "your")
            ],
            "emoji_handling": "confused",  # Longer pause before emoji, may retry
            "double_space_after_period": True  # Sometimes adds double spaces after periods
        }
    }
    
    def __init__(self, personality_id: str = "natural_typist"):
        """
        Initialize a bot personality.
        
        Args:
            personality_id: The ID of the personality to load. If not found,
                           falls back to the "natural_typist" personality.
        """
        self.id = personality_id
        self.data = {}
        
        # Try to load from saved custom personalities first
        loaded = self._load_from_custom()
        
        # If not found in custom, try default personalities
        if not loaded:
            if personality_id in self.DEFAULT_PERSONALITIES:
                self.data = self.DEFAULT_PERSONALITIES[personality_id].copy()
            else:
                # Fall back to natural_typist if requested personality not found
                self.id = "natural_typist"
                self.data = self.DEFAULT_PERSONALITIES["natural_typist"].copy()
    
    @property
    def name(self) -> str:
        """Get the personality's display name."""
        return self.data.get("name", self.id)
    
    @property
    def description(self) -> str:
        """Get the personality's description."""
        return self.data.get("description", "")
    
    @property
    def base_delay(self) -> float:
        """Get the base typing delay in seconds."""
        return self.data.get("base_delay", 0.12)
    
    @property
    def error_rate(self) -> float:
        """Get the base error rate (0.0-1.0)."""
        return self.data.get("error_rate", 0.012)
    
    @property
    def punc_pause_prob(self) -> float:
        """Get the probability of pausing after punctuation (0.0-1.0)."""
        return self.data.get("punc_pause_prob", 0.18)
    
    @property
    def space_pause_prob(self) -> float:
        """Get the probability of pausing after spaces (0.0-1.0)."""
        return self.data.get("space_pause_prob", 0.08)
    
    @property
    def thinking_pause_prob(self) -> float:
        """Get the probability of random 'thinking' pauses (0.0-1.0)."""
        return self.data.get("thinking_pause_prob", 0.025)
    
    @property
    def correction_style(self) -> str:
        """Get the correction style (immediate, delayed, or none)."""
        return self.data.get("correction_style", "immediate")
    
    @property
    def common_misspellings(self) -> List[tuple]:
        """Get common misspellings for this personality."""
        return self.data.get("common_misspellings", [])
    
    @property
    def emoji_handling(self) -> str:
        """Get the emoji handling style (direct, pause, confused)."""
        return self.data.get("emoji_handling", "pause")
    
    @property
    def is_code_aware(self) -> bool:
        """Check if the personality has special code handling."""
        return self.data.get("code_aware", False)
    
    @property
    def uses_rhythm_variation(self) -> bool:
        """Check if the personality varies typing rhythm naturally."""
        return self.data.get("rhythm_variation", False)
    
    @property
    def uses_double_space_after_period(self) -> bool:
        """Check if the personality sometimes adds double spaces after periods."""
        return self.data.get("double_space_after_period", False)
    
    def get_typing_parameters(self) -> Dict[str, Any]:
        """
        Get all typing parameters as a dictionary suitable for the TypingThread.
        
        Returns:
            Dictionary of typing parameters.
        """
        return {
            "delay": self.base_delay,
            "error_rate": self.error_rate,
            "punc_pause_prob": self.punc_pause_prob,
            "space_pause_prob": self.space_pause_prob,
            "thinking_pause_prob": self.thinking_pause_prob,
            # Additional parameters that might be used by enhanced TypingThread
            "correction_style": self.correction_style,
            "emoji_handling": self.emoji_handling,
            "is_code_aware": self.is_code_aware,
            "uses_rhythm_variation": self.uses_rhythm_variation,
            "uses_double_space": self.uses_double_space_after_period,
            "common_misspellings": self.common_misspellings
        }
    
    def apply_to_typer(self, thread):
        """
        Apply this personality's settings to a TypingThread instance.
        
        Args:
            thread: The TypingThread instance to configure.
        """
        thread.delay = self.base_delay
        thread.error_rate = self.error_rate
        thread.punc_pause_prob = self.punc_pause_prob
        thread.space_pause_prob = self.space_pause_prob
        thread.thinking_pause_prob = self.thinking_pause_prob
        
        # Add additional attributes that may be used by the enhanced TypingThread
        thread.correction_style = self.correction_style
        thread.emoji_handling = self.emoji_handling
        thread.is_code_aware = self.is_code_aware
        thread.uses_rhythm_variation = self.uses_rhythm_variation
        thread.uses_double_space = self.uses_double_space_after_period
        thread.common_misspellings = self.common_misspellings
    
    def _load_from_custom(self) -> bool:
        """
        Load personality from custom saved personalities file.
        
        Returns:
            True if successfully loaded, False otherwise.
        """
        try:
            file_path = self._get_personalities_file_path()
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    custom_personalities = json.load(f)
                    if self.id in custom_personalities:
                        self.data = custom_personalities[self.id]
                        return True
            return False
        except Exception as e:
            print(f"Error loading personality: {e}")
            return False
    
    @staticmethod
    def _get_personalities_file_path() -> str:
        """
        Get the path to the personalities save file.
        
        Returns:
            Path to the personalities file.
        """
        # Store personalities in user's app data directory
        app_data_dir = os.path.join(os.path.expanduser('~'), '.eyetype4you')
        os.makedirs(app_data_dir, exist_ok=True)
        return os.path.join(app_data_dir, 'personalities.json')
    
    @classmethod
    def save_custom_personality(cls, personality_id: str, data: Dict[str, Any]) -> bool:
        """
        Save a custom personality to the personalities file.
        
        Args:
            personality_id: Unique identifier for the personality.
            data: Dictionary containing personality parameters.
            
        Returns:
            True if successfully saved, False otherwise.
        """
        try:
            file_path = cls._get_personalities_file_path()
            
            # Load existing personalities or create new dict
            custom_personalities = {}
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    custom_personalities = json.load(f)
            
            # Update with new personality
            custom_personalities[personality_id] = data
            
            # Save back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(custom_personalities, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving personality: {e}")
            return False
    
    @classmethod
    def delete_custom_personality(cls, personality_id: str) -> bool:
        """
        Delete a custom personality.
        
        Args:
            personality_id: ID of the personality to delete.
            
        Returns:
            True if successfully deleted, False otherwise.
        """
        try:
            file_path = cls._get_personalities_file_path()
            
            if not os.path.exists(file_path):
                return False
                
            with open(file_path, 'r', encoding='utf-8') as f:
                custom_personalities = json.load(f)
            
            if personality_id in custom_personalities:
                del custom_personalities[personality_id]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(custom_personalities, f, indent=2)
                return True
            
            return False
        except Exception as e:
            print(f"Error deleting personality: {e}")
            return False
    
    @classmethod
    def get_all_personality_ids(cls) -> List[str]:
        """
        Get a list of all available personality IDs.
        
        Returns:
            List of personality IDs (default and custom).
        """
        personality_ids = list(cls.DEFAULT_PERSONALITIES.keys())
        
        # Add custom personalities
        try:
            file_path = cls._get_personalities_file_path()
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    custom_personalities = json.load(f)
                    for personality_id in custom_personalities:
                        if personality_id not in personality_ids:
                            personality_ids.append(personality_id)
        except Exception as e:
            print(f"Error getting personality IDs: {e}")
        
        return personality_ids
    
    @classmethod
    def get_custom_personalities(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all custom personalities.
        
        Returns:
            Dictionary of custom personalities.
        """
        try:
            file_path = cls._get_personalities_file_path()
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading custom personalities: {e}")
            return {}

    def get_word_error_probability(self, word: str) -> float:
        """
        Get the error probability for a specific word based on the personality.
        
        Args:
            word: The word to check.
            
        Returns:
            Error probability for this word.
        """
        # Check if this word is in the common misspellings list
        for correct, misspelled in self.common_misspellings:
            if word.lower() == correct:
                # Higher chance of error for words the personality commonly misspells
                return min(self.error_rate * 3, 0.4)
        
        # Base error rate for all other words
        return self.error_rate
    
    def get_emoji_delay(self) -> float:
        """
        Get delay time before typing emoji based on personality.
        
        Returns:
            Delay time in seconds.
        """
        if self.emoji_handling == "direct":
            return 0.0
        elif self.emoji_handling == "pause":
            return random.uniform(0.2, 0.5)
        elif self.emoji_handling == "confused":
            return random.uniform(0.5, 1.2)
        else:
            return 0.1
    
    def get_typing_delay_variation(self) -> float:
        """
        Get a variation to add to the base typing delay based on personality.
        
        Returns:
            A time variation in seconds to add to the base delay.
        """
        if self.uses_rhythm_variation:
            # Create a natural typing rhythm with occasional faster/slower typing
            variance = random.gauss(0, 0.05)  # Normal distribution around 0
            return max(-self.base_delay * 0.7, variance)  # Don't go below 30% of base delay
        else:
            # Just add a small random variation for more natural feel
            return random.uniform(-0.02, 0.02)

    def should_double_space_after_period(self) -> bool:
        """
        Determine if the typist should add a double space after this period.
        
        Returns:
            True if a double space should be added, False otherwise.
        """
        if self.uses_double_space_after_period:
            return random.random() < 0.7  # 70% chance of double space
        return False

    def should_fix_typo(self) -> bool:
        """
        Determine if the typist should fix a typo they just made.
        
        Returns:
            True if the typo should be fixed, False to leave it.
        """
        if self.correction_style == "none":
            return False
        elif self.correction_style == "immediate":
            return True
        elif self.correction_style == "delayed":
            # 85% chance to fix typos
            return random.random() < 0.85
        return True 