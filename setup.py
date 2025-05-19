"""
Setup script for EyeType4You package.

This script handles the installation and packaging of the EyeType4You application.
It defines package metadata, dependencies, and entry points for command-line
and GUI execution.
"""
from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="eyetype4you",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "eyetype4you=eyetype4you.main:main",
        ],
        "gui_scripts": [
            "eyetype4you-gui=eyetype4you.main:main",
        ],
    },
    python_requires=">=3.8",
)