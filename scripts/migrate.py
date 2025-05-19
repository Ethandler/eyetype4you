#!/usr/bin/env python3
"""
Migration script for EyeType4You project restructuring.
"""

import os
import shutil
from pathlib import Path
import logging
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("migration")

# Root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

class Migrator:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.src_dir = ROOT_DIR / "src" / "eyetype4you"
        self.data_dir = ROOT_DIR / "data"
        self.docs_dir = ROOT_DIR / "docs"
        self.module_mappings = {
            r"bot_personality.*\.py$": self.src_dir / "bot",
            r"personality_dialog.*\.py$": self.src_dir / "bot",
            r"word_memory.*\.py$": self.src_dir / "core",
            r"typing_engine.*\.py$": self.src_dir / "core",
            r"main_window.*\.py$": self.src_dir / "ui",
            r"dialogs.*\.py$": self.src_dir / "ui",
            r"themes.*\.py$": self.src_dir / "ui",
            r"emoji_handler.*\.py$": self.src_dir / "utils",
            r"window_utils.*\.py$": self.src_dir / "utils",
        }
        self.data_mappings = {
            r"word_memory\.json$": self.data_dir,
            r"emoji_annotations\.json$": self.data_dir,
            r"templates.*\.json$": self.data_dir / "templates",
        }
        self.doc_mappings = {
            r"README\.md$": self.docs_dir,
            r"README\.txt$": self.docs_dir,
            r"user_guide\.md$": self.docs_dir,
        }

    def ensure_dir(self, path):
        """Ensure directory exists, creating it if necessary."""
        path.mkdir(parents=True, exist_ok=True)
        return path

    def move_file(self, src, dest, overwrite=False):
        """Move a file, creating directories as needed."""
        if dest.exists() and not overwrite:
            logger.warning(f"File already exists, skipping move: {dest}")
            return False
        self.ensure_dir(dest.parent)
        if not self.dry_run:
            shutil.move(src, dest)
        logger.info(f"Moved: {src} -> {dest}")
        return True

    def update_imports(self, file_path):
        """Update imports in the given file to reflect new module structure."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        updated_content = re.sub(
            r'from (\w+)_module import (\w+)',
            r'from eyetype4you.\1 import \2',
            content
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        logger.info(f"Updated imports in: {file_path}")

    def migrate_files(self):
        """Run the migration process."""
        # Create core directories
        self.ensure_dir(self.src_dir)
        self.ensure_dir(self.data_dir)
        self.ensure_dir(self.docs_dir)
        
        # Create module directories
        module_dirs = [
            self.src_dir / name for name in 
            ["bot", "core", "ui", "utils", "multibot"]
        ]
        for dir_path in module_dirs:
            self.ensure_dir(dir_path)
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write(f'"""\n{dir_path.name} module for EyeType4You.\n"""\n')
        
        # Move Python files to appropriate locations
        count = 0
        for pattern, dest_dir in self.module_mappings.items():
            for src_file in ROOT_DIR.glob(pattern):
                if self.move_file(src_file, dest_dir / src_file.name):
                    self.update_imports(dest_dir / src_file.name)
                    count += 1
        
        # Move data files
        for pattern, dest_dir in self.data_mappings.items():
            for src_file in ROOT_DIR.glob(pattern):
                if self.move_file(src_file, dest_dir / src_file.name):
                    count += 1
        
        # Move documentation
        for pattern, dest_dir in self.doc_mappings.items():
            for src_file in ROOT_DIR.glob(pattern):
                if self.move_file(src_file, dest_dir / src_file.name):
                    count += 1
        
        # Create new main.py launcher
        with open(ROOT_DIR / "main.py", 'w', encoding='utf-8') as f:
            f.write('''#!/usr/bin/env python3
"""
EyeType4You launcher.
"""

import sys
from eyetype4you.main import main

if __name__ == "__main__":
    sys.exit(main())
''')
        
        logger.info("Migration completed successfully!")
        return count

def main():
    """Run the migration process."""
    migrator = Migrator(dry_run=False)
    migrator.migrate_files()

if __name__ == "__main__":
    main()