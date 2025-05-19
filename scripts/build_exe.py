#!/usr/bin/env python3
"""
PyInstaller build script for EyeType4You.
"""

import os
import shutil
import subprocess
from pathlib import Path

def clean_build():
    """Remove previous build artifacts."""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def copy_assets():
    """Ensure assets are in the correct location."""
    if not os.path.exists('assets'):
        os.makedirs('assets')

def build_executable(onedir=False, console=False):
    """Build the executable using PyInstaller."""
    try:
        pyinstaller_args = [
            'pyinstaller',
            '--clean',
            '--noconfirm',
            '--name=EyeType4You',
            '--add-data=assets;assets',
            '--add-data=word_memory.json;.'
        ]
        if onedir:
            pyinstaller_args.append('--onedir')
        else:
            pyinstaller_args.append('--onefile')
        if console:
            pyinstaller_args.append('--console')
        else:
            pyinstaller_args.append('--windowed')
        pyinstaller_args.append('--icon=assets/eyes.ico')
        pyinstaller_args.append('eyetype4you.spec')
        
        subprocess.run(pyinstaller_args, check=True)
        print("Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        return False

def main():
    clean_build()
    copy_assets()
    success = build_executable()
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())