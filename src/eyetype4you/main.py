#!/usr/bin/env python3
"""
EyeType4You - Main application entry point.

This module initializes and launches the EyeType4You application.
It handles command-line arguments, sets up logging, and creates the main window.

Usage:
    python -m eyetype4you.main [--debug]
    
Options:
    --debug     Enable debug logging
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='eyetype4you.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

# Import UI modules after logging is configured
try:
    # Import UI components - adjust based on your actual implementation
    # from eyetype4you.ui.main_window import MainWindow
    # from PyQt5.QtWidgets import QApplication
    pass
except ImportError as e:
    logger.critical(f"Failed to import required modules: {e}")
    print(f"Error: Failed to import required modules: {e}")
    print("Please ensure all dependencies are installed by running: pip install -r requirements.txt")
    sys.exit(1)


def get_data_dir():
    """
    Determine the data directory based on how the application is run.
    
    When running as an installed package or frozen executable, use app-specific
    locations. When running from source, use the project's data directory.
    
    Returns:
        Path: Path object pointing to the data directory
    """
    # When running as an installed package or frozen executable
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys._MEIPASS)
    # When running from source
    else:
        base_dir = Path(__file__).resolve().parent.parent.parent
    
    data_dir = base_dir / 'data'
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
    
    return data_dir


def main():
    """
    Main application entry point.
    
    Initializes the application, sets up logging, and launches the UI.
    Handles command-line arguments and configures the runtime environment.
    
    Returns:
        int: Application exit code
    """
    parser = argparse.ArgumentParser(description='EyeType4You - Human-like typing automation')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()
    
    # Update logging level if debug flag is provided
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Initialize application
    # Placeholder for your actual application initialization
    # app = QApplication(sys.argv)
    # app.setApplicationName("EyeType4You")
    
    # Set application data
    data_dir = get_data_dir()
    logger.info(f"Using data directory: {data_dir}")
    
    # Create main window
    try:
        # Placeholder for your actual main window creation
        # window = MainWindow(data_dir)
        # window.show()
        # return app.exec_()
        logger.info("Application started successfully")
        return 0
    except Exception as e:
        logger.critical(f"Failed to start application: {e}", exc_info=True)
        print(f"Error: Failed to start application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())