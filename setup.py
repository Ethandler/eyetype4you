# setup.py
import sys
from cx_Freeze import setup, Executable

# 1) Files & packages to include in the frozen EXE
build_exe_options = {
    "packages": [
        "tkinter",
        "PIL",
        "pyautogui",
        "emoji",
        "pyperclip",
    ],
    "include_files": [
        # your bot’s assets
        ("assets/eyes.png", "assets/eyes.png"),
        # emoji lookup table
        ("emoji_annotations.json", "emoji_annotations.json"),
        # initial memory file (will be mutated at runtime)
        ("word_memory.json", "word_memory.json"),
    ],
}

# 2) MSI‐specific options: create Desktop & Start Menu shortcuts
bdist_msi_options = {
    "data": {
        "Shortcut": [
            (
                "DesktopShortcut",       # internal shortcut name
                "DesktopFolder",         # location
                "Eyetype4You",           # shortcut name
                "TARGETDIR",             # component
                "[TARGETDIR]\\Eyetype4You.exe",  # target executable
                None, None, None, None, None, None
            ),
            (
                "StartMenuShortcut",
                "StartMenuFolder",
                "Eyetype4You",
                "TARGETDIR",
                "[TARGETDIR]\\Eyetype4You.exe",
                None, None, None, None, None, None
            ),
        ]
    }
}

# 3) Use a GUI‐only base on Windows to suppress the console window
base = "Win32GUI" if sys.platform == "win32" else None

# 4) Define the executable
executables = [
    Executable(
        script="main.py",
        base=base,
        icon="assets/eyes.ico",    # your multi‐size .ico
        target_name="Eyetype4You.exe"
    )
]

# 5) Finally, call setup() with both EXE and MSI options
setup(
    name="Eyetype4You",
    version="1.0",
    description="Human-like typing bot with emoji support",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables
)
# Note: To build the EXE, run this script with Python. The output will be in the 'build' directory.
# To create an MSI installer, run the command: python setup.py bdist_msi
# Note: Ensure you have cx_Freeze installed. You can install it using pip: pip install cx_Freeze
# Note: The above code is a simplified version of the setup.py file. You may need to adjust paths and options based on your project structure.