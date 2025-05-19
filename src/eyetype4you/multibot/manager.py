"""
Bot Manager for handling multiple typing bots.

This module provides functionality to create, manage, and coordinate
multiple typing bots running simultaneously in different windows.
"""

import logging
import threading
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class MultiBotManager:
    """
    Manager for multiple typing bots.
    
    Handles creation, monitoring, and control of multiple bot instances
    that can type simultaneously in different target windows.
    
    Attributes:
        _bots (dict): Dictionary of active bots and their metadata
        _lock (threading.Lock): Thread synchronization lock
    """
    
    def __init__(self):
        """
        Initialize the bot manager.
        
        Sets up internal storage for bot instances and creates a
        thread lock for safe concurrent operations.
        """
        self._bots = {}  # Dict of active bots
        self._lock = threading.Lock()  # Thread safety lock
        logger.info("Bot Manager initialized")
    
    def add_bot(self, name: str, target_window=None, text=None, settings=None) -> bool:
        """
        Add a new bot to the manager.
        
        Args:
            name: Unique name for the bot
            target_window: Window to type into
            text: Text for the bot to type
            settings: Bot configuration settings
            
        Returns:
            bool: Success status (True if bot was added successfully)
        
        Raises:
            ValueError: If name is empty or None
        """
        if not name:
            raise ValueError("Bot name cannot be empty")
            
        with self._lock:
            if name in self._bots:
                logger.warning(f"Bot with name '{name}' already exists")
                return False
            
            # Create new bot instance
            # This is a placeholder - actual implementation would create a bot instance
            self._bots[name] = {
                'target': target_window,
                'text': text,
                'settings': settings,
                'status': 'ready',
                'progress': 0
            }
            
            logger.info(f"Added new bot: {name}")
            return True
    
    def start_bot(self, name: str) -> bool:
        """
        Start a specific bot.
        
        Args:
            name: Name of the bot to start
            
        Returns:
            bool: Success status (True if bot was started successfully)
        """
        with self._lock:
            if name not in self._bots:
                logger.warning(f"Bot '{name}' not found")
                return False
            
            # Start the bot
            # This is a placeholder - actual implementation would start the bot
            self._bots[name]['status'] = 'running'
            logger.info(f"Started bot: {name}")
            return True
    
    def stop_bot(self, name: str) -> bool:
        """
        Stop a specific bot.
        
        Args:
            name: Name of the bot to stop
            
        Returns:
            bool: Success status (True if bot was stopped successfully)
        """
        with self._lock:
            if name not in self._bots:
                logger.warning(f"Bot '{name}' not found")
                return False
            
            # Stop the bot
            # This is a placeholder - actual implementation would stop the bot
            self._bots[name]['status'] = 'stopped'
            logger.info(f"Stopped bot: {name}")
            return True
    
    def stop_all_bots(self) -> int:
        """
        Stop all running bots.
        
        Returns:
            int: Number of bots stopped
        """
        count = 0
        with self._lock:
            for name in self._bots:
                if self._bots[name]['status'] == 'running':
                    self._bots[name]['status'] = 'stopped'
                    count += 1
            
            logger.info(f"Stopped {count} bots")
            return count
    
    def get_bot_status(self, name: str) -> Optional[Dict]:
        """
        Get the status of a specific bot.
        
        Args:
            name: Name of the bot
            
        Returns:
            Dict or None: Bot status information if found, None otherwise
        """
        with self._lock:
            if name not in self._bots:
                logger.warning(f"Bot '{name}' not found")
                return None
            
            return self._bots[name].copy()
    
    def get_all_bots(self) -> List[Dict]:
        """
        Get information about all bots.
        
        Returns:
            List[Dict]: List of bot status dictionaries with bot names
        """
        with self._lock:
            return [
                {'name': name, **bot.copy()}
                for name, bot in self._bots.items()
            ]
    
    def remove_bot(self, name: str) -> bool:
        """
        Remove a bot from the manager.
        
        Args:
            name: Name of the bot to remove
            
        Returns:
            bool: Success status (True if bot was removed successfully)
        """
        with self._lock:
            if name not in self._bots:
                logger.warning(f"Bot '{name}' not found")
                return False
            
            # Stop the bot if it's running
            if self._bots[name]['status'] == 'running':
                self.stop_bot(name)
            
            # Remove the bot
            del self._bots[name]
            logger.info(f"Removed bot: {name}")
            return True