#!/usr/bin/env python3
"""
EyeType4You launcher script.

This script is a simple entry point that imports and runs the main function
from the eyetype4you package. It makes it possible to run the application
directly from the project root without installing the package.
"""

import sys
import os

# Add src directory to path if running from source
if os.path.exists(os.path.join(os.path.dirname(__file__), 'src')):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from eyetype4you.main import main
except ImportError as e:
    print(f"Error importing eyetype4you package: {e}")
    print("Make sure you have installed dependencies with: pip install -r requirements.txt")
    sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())