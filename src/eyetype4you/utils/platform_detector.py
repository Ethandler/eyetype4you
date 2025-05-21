"""
Platform detection utilities for EyeType4You.
"""

import os
import sys
import platform
import logging

logger = logging.getLogger(__name__)

def is_wsl() -> bool:
    """Detect if running under Windows Subsystem for Linux."""
    if 'linux' not in sys.platform.lower():
        return False
    try:
        with open('/proc/version', 'r') as f:
            version_info = f.read().lower()
            is_wsl_env = 'microsoft' in version_info or 'wsl' in version_info
            if is_wsl_env:
                logger.debug("WSL environment detected")
            return is_wsl_env
    except (IOError, FileNotFoundError) as e:
        logger.debug(f"Could not check /proc/version: {e}")
        return False

def get_platform_info() -> dict:
    """Get detailed platform information."""
    info = {
        'system': platform.system(),
        'release': platform.release(),
        'wsl': is_wsl(),
        'display': os.environ.get('DISPLAY', ''),
        'python_version': platform.python_version(),
        'machine': platform.machine()
    }
    logger.debug(f"Platform info: {info}")
    return info
