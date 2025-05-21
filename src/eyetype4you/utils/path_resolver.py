"""
Path resolution utilities for EyeType4You.
"""

import os
import sys
import logging
from pathlib import Path
from .platform_detector import is_wsl

logger = logging.getLogger(__name__)

def get_data_dir() -> Path:
    """
    Get the appropriate data directory based on platform.
    """
    if getattr(sys, 'frozen', False):
        if is_wsl():
            base = Path(os.environ.get('HOME', '/home'))
            data_dir = base / '.local' / 'share' / 'eyetype4you'
            logger.debug(f"Using WSL data directory: {data_dir}")
        else:
            base = Path(sys._MEIPASS)
            data_dir = base / 'data'
            logger.debug(f"Using frozen Windows data directory: {data_dir}")
    else:
        base = Path(__file__).resolve().parent.parent.parent.parent
        data_dir = base / 'data'
        logger.debug(f"Using development data directory: {data_dir}")
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_config_dir() -> Path:
    """
    Get the appropriate configuration directory based on platform.
    """
    if is_wsl():
        base = Path(os.environ.get('HOME', '/home'))
        config_dir = base / '.config' / 'eyetype4you'
        logger.debug(f"Using WSL config directory: {config_dir}")
    else:
        appdata = os.environ.get('APPDATA', '')
        if appdata:
            config_dir = Path(appdata) / 'EyeType4You'
            logger.debug(f"Using Windows config directory: {config_dir}")
        else:
            config_dir = Path.cwd() / 'config'
            logger.debug(f"Using fallback config directory: {config_dir}")
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_user_home_dir() -> Path:
    if is_wsl():
        return Path(os.environ.get('HOME', '/home'))
    else:
        return Path(os.path.expanduser("~"))

def normalize_path(path: str) -> str:
    return str(Path(path))
