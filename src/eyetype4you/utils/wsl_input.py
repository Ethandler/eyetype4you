"""
WSL-specific input utilities for EyeType4You.
"""

import subprocess
import logging
import shlex
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_wsl_input() -> bool:
    """Verify WSL input capabilities and dependencies."""
    try:
        result = subprocess.run(['which', 'xdotool'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode != 0:
            logger.warning("xdotool not found. Install with: sudo apt install xdotool")
            return False
        result = subprocess.run(['xset', 'q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if result.returncode != 0:
            logger.warning("X11 connection failed. Check DISPLAY environment variable and X server.")
            return False
        logger.info("WSL input environment verified successfully")
        return True
    except Exception as e:
        logger.error(f"Error setting up WSL input: {e}", exc_info=True)
        return False

def type_text_wsl(text: str) -> bool:
    """Type text using xdotool in WSL environment."""
    if not text:
        return True
    try:
        safe_text = shlex.quote(text)
        subprocess.run(['xdotool', 'type', safe_text], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error typing text in WSL: {e}", exc_info=True)
        return False

def send_key_wsl(key: str) -> bool:
    """Send a specific key using xdotool in WSL environment."""
    if not key:
        return False
    try:
        subprocess.run(['xdotool', 'key', key], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error sending key '{key}' in WSL: {e}", exc_info=True)
        return False

def get_active_window_wsl() -> Optional[str]:
    """Get the active window using xdotool in WSL environment."""
    try:
        result = subprocess.run(['xdotool', 'getactivewindow'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting active window in WSL: {e}", exc_info=True)
        return None
