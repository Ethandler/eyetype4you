import sys
import json
import time
import random
import threading
import emoji
import pyautogui
import pyperclip
import ctypes
from typing import Dict, List
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QSlider, QTextEdit, QFrame, QCheckBox,
                           QDialog, QMenu, QAction, QMenuBar, QProgressBar, QMessageBox, QToolTip,
                           QGraphicsOpacityEffect)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QColor, QPalette, QPainter, QTextCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QRect, QPoint, QPropertyAnimation, QEasingCurve

pyautogui.PAUSE = 0  # Remove default pause between actions for max speed
pyautogui.FAILSAFE = False  # Disable fail-safe for smoother operation

# Windows API for window handling
user32 = ctypes.windll.user32

# Common misspellings dictionary 
AUTOCORRECT_DICT = {
    "teh": "the",
    "adn": "and",
    "waht": "what",
    "taht": "that",
    "thier": "their",
    "recieve": "receive",
    "wierd": "weird",
    "alot": "a lot",
    "definately": "definitely",
    "seperate": "separate",
    "occured": "occurred",
    "occurance": "occurrence",
    "greatful": "grateful",
    "accomodate": "accommodate",
    "untill": "until",
    "doesnt": "doesn't",
    "dont": "don't",
    "cant": "can't",
    "wont": "won't",
    "shouldnt": "shouldn't",
    "couldnt": "couldn't",
    "wouldnt": "wouldn't",
    "isnt": "isn't",
    "wasnt": "wasn't",
    "werent": "weren't",
    "havent": "haven't",
    "hasnt": "hasn't",
    "didnt": "didn't",
    "im": "I'm",
    "ive": "I've",
    "youre": "you're",
    "theyre": "they're",
    "weve": "we've",
    "theyve": "they've",
    "cant": "can't",
    "wouldve": "would've",
    "shouldve": "should've",
    "couldve": "could've",
    "mispell": "misspell",
    "beleive": "believe",
    "acheive": "achieve",
    "reccomend": "recommend",
    "tommorrow": "tomorrow",
    "advertisment": "advertisement",
    "neccessary": "necessary",
    "occasionaly": "occasionally",
    "embarass": "embarrass",
    "concious": "conscious",
    "truely": "truly",
    "rigth": "right",
}

keyboard_neighbors = {
    'a': ['s', 'q', 'z'],        'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'],   'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'e': ['w', 's', 'd', 'r'],   'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'], 'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'j', 'k', 'o'],   'j': ['h', 'u', 'i', 'k', 'm', 'n'],
    'k': ['j', 'i', 'o', 'l', ',', 'm'], 'l': ['k', 'o', 'p', ';', '.', ','],
    'm': ['n', 'j', 'k', ','],   'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'k', 'l', 'p'],   'p': ['o', 'l', ';', '['],
    'q': ['a', 's', 'w'],        'r': ['e', 'd', 'f', 't'],
    's': ['a', 'w', 'e', 'd', 'x', 'z'], 't': ['r', 'f', 'g', 'y'],
    'u': ['y', 'h', 'j', 'i'],   'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'a', 's', 'e'],   'x': ['z', 's', 'd', 'c'],
    'y': ['t', 'g', 'h', 'u'],   'z': ['a', 's', 'x'],
    'A': ['S', 'Q', 'Z'],        'B': ['V', 'G', 'H', 'N'],
    'C': ['X', 'D', 'F', 'V'],   'D': ['S', 'E', 'R', 'F', 'C', 'X'],
    'E': ['W', 'S', 'D', 'R'],   'F': ['D', 'R', 'T', 'G', 'V', 'C'],
    'G': ['F', 'T', 'Y', 'H', 'B', 'V'], 'H': ['G', 'Y', 'U', 'J', 'N', 'B'],
    'I': ['U', 'J', 'K', 'O'],   'J': ['H', 'U', 'I', 'K', 'M', 'N'],
    'K': ['J', 'I', 'O', 'L', '<', 'M'], 'L': ['K', 'O', 'P', ':', '>', '<'],
    'M': ['N', 'J', 'K', '<'],   'N': ['B', 'H', 'J', 'M'],
    'O': ['I', 'K', 'L', 'P'],   'P': ['O', 'L', ':', '{'],
    'Q': ['A', 'S', 'W'],        'R': ['E', 'D', 'F', 'T'],
    'S': ['A', 'W', 'E', 'D', 'X', 'Z'], 'T': ['R', 'F', 'G', 'Y'],
    'U': ['Y', 'H', 'J', 'I'],   'V': ['C', 'F', 'G', 'B'],
    'W': ['Q', 'A', 'S', 'E'],   'X': ['Z', 'S', 'D', 'C'],
    'Y': ['T', 'G', 'H', 'U'],   'Z': ['A', 'S', 'X'],
    ';': ['l', 'p', '\'', ':'], ':': ['L', 'P', '"'],
    '\'': [';', ],               '"': [':'],
    ',': ['m', 'k', '.'],        '<': ['M', 'K', '>'],
    '.': ['l', ',', '/'],        '>': ['L', '<', '?'],
    '/': ['.', ';'],             '?': ['>', ':'],
    '-': ['0', '='],             '_': [')', '+'],
    '=': ['-', '['],             '+': ['_', '{'],
    '[': ['p', ']'],             '{': ['p', '}'],
    ']': ['[', '\\'],            '}': ['{', '|'],
    '\\': [']'],                 '|': ['}']
}

class StyleSheet:
    """Class to store application stylesheets"""
    
    MAIN = """
        QMainWindow, QDialog {
            background-color: #2e2e2e;
        }
        QPushButton {
            background-color: #0099FF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 16px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #33BFFF;
        }
        QPushButton:pressed {
            background-color: #007ACC;
        }
        QPushButton#closeButton {
            background-color: #FF5252;
            color: white;
            font-weight: bold;
        }
        QPushButton#closeButton:hover {
            background-color: #FF7777;
        }
        QPushButton#closeButton:pressed {
            background-color: #CC4444;
        }
        QLabel {
            color: #e0e0e0;
            font-size: 14px;
        }
        QLabel#titleLabel {
            font-size: 20px;
            font-weight: bold;
            color: #0099FF;
        }
        QSlider {
            height: 24px;
        }
        QSlider::groove:vertical {
            background: #444444;
            width: 8px;
            border-radius: 4px;
        }
        QSlider::handle:vertical {
            background: #0099FF;
            height: 20px;
            width: 20px;
            margin: 0 -6px;
            border-radius: 10px;
        }
        QSlider::sub-page:vertical {
            background: #0099FF;
            border-radius: 4px;
        }
        QTextEdit {
            background-color: #2e2e2e;
            color: #e0e0e0;
            border: 1px solid #444444;
            border-radius: 4px;
            font-family: 'Consolas';
            font-size: 18px;
        }
        QProgressBar {
            background-color: #444444;
            border-radius: 8px;
            text-align: center;
            color: transparent;
        }
        QProgressBar::chunk {
            background-color: #0099FF;
            border-radius: 8px;
        }
        QCheckBox {
            color: #e0e0e0;
            font-size: 14px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
    """
    # Cyberpunk (Dark City/Koi)
    CYBERPUNK = """
        QMainWindow, QDialog {
            background-color: #10101a;
        }
        QPushButton {
            background-color: #1a1a2e;
            color: #f8f8ff;
            border: none;
            border-radius: 8px;
            padding: 12px 16px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #23234d;
        }
        QPushButton:pressed {
            background-color: #0f3460;
        }
        QPushButton#closeButton {
            background-color: #ff2e63;
            color: #fff;
            font-weight: bold;
        }
        QPushButton#closeButton:hover {
            background-color: #ff5e8e;
        }
        QPushButton#closeButton:pressed {
            background-color: #b2224b;
        }
        QPushButton#templateButton {
            background-color: #08d9d6;
            color: #1a1a2e;
            font-size: 12px;
            padding: 8px 10px;
        }
        QPushButton#templateButton:hover {
            background-color: #20e7e4;
        }
        QLabel {
            color: #f8f8ff;
            font-size: 14px;
        }
        QLabel#titleLabel {
            font-size: 20px;
            font-weight: bold;
            color: #08d9d6;
        }
        QLabel#statusLabel {
            color: #08d9d6;
            font-size: 12px;
            border: 1px solid #23234d;
            border-radius: 4px;
            padding: 4px;
            background-color: #1a1a2e;
        }
        QSlider {
            height: 24px;
        }
        QSlider::groove:horizontal, QSlider::groove:vertical {
            background: #23234d;
            border-radius: 4px;
        }
        QSlider::handle:horizontal, QSlider::handle:vertical {
            background: #08d9d6;
            border-radius: 10px;
        }
        QSlider::sub-page:horizontal, QSlider::sub-page:vertical {
            background: #ff2e63;
            border-radius: 4px;
        }
        QTextEdit {
            background-color: #181828;
            color: #f8f8ff;
            border: 1px solid #23234d;
            border-radius: 4px;
            font-family: 'Consolas';
            font-size: 18px;
        }
        QProgressBar {
            background-color: #23234d;
            border-radius: 8px;
            text-align: center;
            color: transparent;
        }
        QProgressBar::chunk {
            background-color: #08d9d6;
            border-radius: 8px;
        }
        QCheckBox {
            color: #f8f8ff;
            font-size: 14px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        QToolTip {
            background-color: #1a1a2e;
            color: #f8f8ff;
            border: 1px solid #08d9d6;
            padding: 5px;
        }
        QScrollBar:vertical {
            border: none;
            background: #23234d;
            width: 10px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #08d9d6;
            min-height: 20px;
            border-radius: 5px;
        }
        QComboBox {
            background-color: #1a1a2e;
            color: #f8f8ff;
            border: 1px solid #23234d;
            border-radius: 4px;
            padding: 4px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #1a1a2e;
            color: #f8f8ff;
            selection-background-color: #08d9d6;
            selection-color: #1a1a2e;
        }
    """
    # Pink City (Light Mode)
    PINK_CITY = """
        QMainWindow, QDialog {
            background-color: #fff0f6;
        }
        QPushButton {
            background-color: #ffb6d5;
            color: #7a316f;
            border: none;
            border-radius: 8px;
            padding: 12px 16px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #ffd6e0;
        }
        QPushButton:pressed {
            background-color: #ff6f91;
        }
        QPushButton#closeButton {
            background-color: #ff6f91;
            color: #fff;
            font-weight: bold;
        }
        QPushButton#closeButton:hover {
            background-color: #ffb6d5;
        }
        QPushButton#closeButton:pressed {
            background-color: #d72660;
        }
        QPushButton#templateButton {
            background-color: #d72660;
            color: #fff0f6;
            font-size: 12px;
            padding: 8px 10px;
        }
        QPushButton#templateButton:hover {
            background-color: #ff6f91;
        }
        QLabel {
            color: #7a316f;
            font-size: 14px;
        }
        QLabel#titleLabel {
            font-size: 20px;
            font-weight: bold;
            color: #d72660;
        }
        QLabel#statusLabel {
            color: #7a316f;
            font-size: 12px;
            border: 1px solid #ffd6e0;
            border-radius: 4px;
            padding: 4px;
            background-color: #fff6fa;
        }
        QSlider {
            height: 24px;
        }
        QSlider::groove:horizontal, QSlider::groove:vertical {
            background: #ffd6e0;
            border-radius: 4px;
        }
        QSlider::handle:horizontal, QSlider::handle:vertical {
            background: #d72660;
            border-radius: 10px;
        }
        QSlider::sub-page:horizontal, QSlider::sub-page:vertical {
            background: #ffb6d5;
            border-radius: 4px;
        }
        QTextEdit {
            background-color: #fff0f6;
            color: #7a316f;
            border: 1px solid #ffd6e0;
            border-radius: 4px;
            font-family: 'Consolas';
            font-size: 18px;
        }
        QProgressBar {
            background-color: #ffd6e0;
            border-radius: 8px;
            text-align: center;
            color: transparent;
        }
        QProgressBar::chunk {
            background-color: #d72660;
            border-radius: 8px;
        }
        QCheckBox {
            color: #7a316f;
            font-size: 14px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        QToolTip {
            background-color: #fff6fa;
            color: #7a316f;
            border: 1px solid #d72660;
            padding: 5px;
        }
        QScrollBar:vertical {
            border: none;
            background: #ffd6e0;
            width: 10px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: #d72660;
            min-height: 20px;
            border-radius: 5px;
        }
        QComboBox {
            background-color: #fff6fa;
            color: #7a316f;
            border: 1px solid #ffd6e0;
            border-radius: 4px;
            padding: 4px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #fff6fa;
            color: #7a316f;
            selection-background-color: #d72660;
            selection-color: #fff0f6;
        }
    """

class AutoCorrectTextEdit(QTextEdit):
    """QTextEdit with autocorrect functionality"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.autocorrect_enabled = True
        self.last_word = ""
        self.textChanged.connect(self.check_for_correction)
        
    def toggle_autocorrect(self, enabled):
        """Enable or disable autocorrect"""
        self.autocorrect_enabled = enabled
    
    def check_for_correction(self):
        """Check if the last word typed needs correction"""
        if not self.autocorrect_enabled:
            return
            
        cursor = self.textCursor()
        current_pos_before_space = cursor.position() # Position where space was typed

        # Check if the character just typed is a space or common punctuation that ends a word
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
        last_char_typed = cursor.selectedText()
        cursor.clearSelection() # Reset selection

        if last_char_typed in [" ", ".", ",", "!", "?", ";", "\n"]:
            # Move cursor to the end of the potential word (before the space/punctuation)
            check_cursor = self.textCursor()
            check_cursor.setPosition(current_pos_before_space -1) # Position before the space/punct
            
            check_cursor.select(QTextCursor.WordUnderCursor) # Selects the word the cursor is at/after
            word_to_check = check_cursor.selectedText()
            
            # Clean the word (e.g. if select captures punctuation with it)
            cleaned_word = word_to_check.strip(".,;:!?\"'()[]{}").lower()

            if cleaned_word and cleaned_word in AUTOCORRECT_DICT:
                correction = AUTOCORRECT_DICT[cleaned_word]
                if word_to_check != correction: # Avoid re-correction or case changes if not needed
                    # The selection (word_to_check) is already made by check_cursor.select
                    check_cursor.insertText(correction)
                    # Cursor is now after the corrected word. self.setTextCursor might be needed if issues.
        return # Original was return outside if

class TypingThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, text, delay, error_rate, punc_pause_prob, space_pause_prob, thinking_pause_prob):
        super().__init__()
        self.text = text
        self.delay = delay
        self.error_rate = error_rate
        self.punc_pause_prob = punc_pause_prob
        self.space_pause_prob = space_pause_prob
        self.thinking_pause_prob = thinking_pause_prob
        self.running = True
        self.target_window = None
        
    def run(self):
        try:
            time.sleep(2)  # Give user time to click into target window
            
            # Get and store the active window handle
            self.target_window = user32.GetForegroundWindow()
            if not user32.IsWindow(self.target_window):
                self.error.emit("Invalid target window selected at start.")
                self.finished.emit()
                return
            
            total = len(self.text)
            i = 0
            current_line_indent = ''
            
            while i < total and self.running:
                try:
                    if not user32.IsWindow(self.target_window):
                        self.error.emit("Target window closed or became invalid during typing.")
                        break # Exit the loop

                    # Ensure target window is in focus before each keystroke
                    if self.target_window and user32.GetForegroundWindow() != self.target_window:
                        user32.SetForegroundWindow(self.target_window)
                        time.sleep(0.05)  # Increased delay to allow window focus to change
                        
                    ch = self.text[i]
                    # autotab logic
                    if ch == '\n':
                        prev_newline = self.text.rfind('\n', 0, i)
                        if prev_newline == -1:
                            prev_line = self.text[:i]
                        else:
                            prev_line = self.text[prev_newline+1:i]
                        leading_ws = ''
                        for c in prev_line:
                            if c in (' ', '\t'):
                                leading_ws += c
                            else:
                                break
                        current_line_indent = leading_ws
                        if prev_line.rstrip().endswith(':'):
                            current_line_indent += '    '
                        pyautogui.typewrite('\n')
                        time.sleep(self.delay)
                        # Check if indentation already exists at cursor
                        if current_line_indent:
                            # Copy a few chars at cursor to clipboard
                            pyautogui.hotkey('shift', 'end')
                            pyautogui.hotkey('ctrl', 'c')
                            typed = pyperclip.paste()
                            # Only type missing part of indent
                            missing = current_line_indent
                            if typed.startswith(current_line_indent):
                                missing = ''
                            elif typed and current_line_indent.startswith(typed):
                                missing = current_line_indent[len(typed):]
                            if missing:
                                pyautogui.typewrite(missing)
                                time.sleep(self.delay * len(missing))
                        i += 1
                        self.progress.emit(int((i / total) * 100))
                        continue

                    # typo?
                    if ch.isalnum() and random.random() < self.error_rate:
                        if (nb := keyboard_neighbors.get(ch, [])):
                            typo = random.choice(nb)
                            pyautogui.typewrite(typo)
                            time.sleep(self.delay)
                            pyautogui.press("backspace")
                            time.sleep(self.delay)
                    # type or emoji-paste
                    if emoji.is_emoji(ch):
                        pyperclip.copy(ch)
                        pyautogui.hotkey("ctrl", "v")
                    else:
                        pyautogui.typewrite(ch)
                    time.sleep(self.delay)

                    # punctuation pause
                    if ch in ".!?," and random.random() < self.punc_pause_prob:
                        time.sleep(random.uniform(0.1, 0.25))
                    # space pause
                    if ch == " " and random.random() < self.space_pause_prob:
                        time.sleep(random.uniform(0.07, 0.18))
                    # thinking pause
                    if random.random() < self.thinking_pause_prob:
                        time.sleep(random.uniform(0.7, 1.5))
                    
                    i += 1
                    self.progress.emit(int((i / total) * 100))
                    
                except Exception as e:
                    self.error.emit(f"Error during typing: {e}")
                    # Continue with next character
                    i += 1
                    continue
            
            self.progress.emit(0)
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(f"Critical error in typing thread: {e}")
            self.finished.emit()
        
    def stop(self):
        self.running = False

class QuickTemplate(QFrame):
    """Widget for quick text templates"""
    
    template_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        
        # Templates (these can be saved/loaded from a file)
        self.templates = [
            "Hello! How can I help you today?",
            "Thank you for your message. I'll get back to you as soon as possible.",
            "Best regards,\nEyetype4You",
            "This is a test template with emoji 😊👍✨"
        ]
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Title
        title_label = QLabel("✏️ Quick Templates")
        title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(title_label)
        
        # Template buttons
        for i, template in enumerate(self.templates):
            # Show first 40 chars
            short_text = template[:40] + ("..." if len(template) > 40 else "")
            btn = QPushButton(short_text)
            btn.setObjectName("templateButton")
            btn.clicked.connect(lambda _, t=template: self.template_selected.emit(t))
            # Help tooltip showing full template
            btn.setToolTip(template.replace("\n", "<br>"))
            layout.addWidget(btn)
        
        # Add button
        add_btn = QPushButton("➕ Add New")
        add_btn.setObjectName("templateButton")
        add_btn.clicked.connect(self.add_template)
        layout.addWidget(add_btn)
    
    def add_template(self):
        # This would save to the templates list
        # For now just show a dialog saying feature coming soon
        QMessageBox.information(self, "Coming Soon", 
                              "Custom templates will be available in the next update!")

class StatusIndicator(QFrame):
    """Widget showing current settings status"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Speed indicator
        self.speed_label = QLabel()
        self.speed_label.setObjectName("statusLabel")
        
        # Error rate indicator
        self.error_label = QLabel()
        self.error_label.setObjectName("statusLabel")
        
        # Theme indicator
        self.theme_label = QLabel()
        self.theme_label.setObjectName("statusLabel")
        
        layout.addWidget(self.speed_label)
        layout.addStretch()
        layout.addWidget(self.error_label)
        layout.addStretch()
        layout.addWidget(self.theme_label)
        
        self.update_status()
    
    def update_status(self):
        # Update speed
        speed = self.parent.typing_speed
        self.speed_label.setText(f"⚡ Speed: {speed:.2f}s")
        
        # Update error rate
        error = self.parent.error_rate * 100
        self.error_label.setText(f"🎯 Error Rate: {error:.1f}%")
        
        # Update theme
        theme = self.parent.theme
        theme_name = "Cyberpunk" if theme == "cyberpunk" else "Pink City"
        self.theme_label.setText(f"🎨 Theme: {theme_name}")

class TypingBot(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Setup main window
        self.setWindowTitle("Eyetype4You Bot")
        self.setGeometry(100, 100, 800, 600)
        
        # Load memory
        self.word_memory = self.load_memory()
        
        # Typing parameters
        self.error_rate = 1/83
        self.punc_pause_prob = 0.18
        self.space_pause_prob = 0.08
        self.thinking_pause_prob = 0.025
        self.theme = 'cyberpunk'  # Default theme
        self.typing_thread = None
        self.typing_speed = 0.12  # Default typing speed in seconds
        
        # Create the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Setup UI components
        self.setup_menu()
        self.setup_ui()
        
        # Apply theme
        self.apply_theme()
        
        # Add welcome animation after UI is set up
        QTimer.singleShot(200, self.animate_welcome)
    
    def animate_welcome(self):
        """Create welcome animation for the eye image"""
        if hasattr(self, 'eye_label') and self.eye_label:
            # Initial state - make invisible
            self.eye_label.setGraphicsEffect(None)  # Clear any previous effects
            
            # Create opacity effect
            self.opacity_effect = QGraphicsOpacityEffect(self.eye_label)
            self.opacity_effect.setOpacity(0.0)
            self.eye_label.setGraphicsEffect(self.opacity_effect)
            
            # Create fade-in animation
            self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
            self.fade_anim.setDuration(1500)
            self.fade_anim.setStartValue(0.0)
            self.fade_anim.setEndValue(1.0)
            self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
            self.fade_anim.finished.connect(self.show_welcome_tooltip)
            
            # Start animation
            self.fade_anim.start()
    
    def show_welcome_tooltip(self):
        """Show welcome tooltip after animation completes"""
        if hasattr(self, 'eye_label') and self.eye_label and \
           hasattr(self, 'opacity_effect') and self.opacity_effect.opacity() >= 0.99: # Check if fully opaque (allow for float precision)
            QToolTip.showText(
                self.eye_label.mapToGlobal(QPoint(self.eye_label.width() // 2, 
                                                 self.eye_label.height() // 2)),
                "Welcome to Eyetype4You!<br>The intelligent typing assistant",
                self.eye_label,
                QRect(), # Empty rect, let Qt decide based on position
                3000  # Show for 3000 milliseconds (3 seconds)
            )
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        # Create Settings menu as parent
        settings_menu = menubar.addMenu("⚙️ Settings")
        
        # Add Speed submenu
        speed_menu = settings_menu.addMenu("⚡ Speed")
        
        # Add speed presets
        speed_slow = QAction("Slow (0.20s)", self)
        speed_slow.triggered.connect(lambda: self.set_speed(20))
        
        speed_normal = QAction("Normal (0.12s)", self)
        speed_normal.triggered.connect(lambda: self.set_speed(12))
        
        speed_fast = QAction("Fast (0.08s)", self)
        speed_fast.triggered.connect(lambda: self.set_speed(8))
        
        speed_very_fast = QAction("Very Fast (0.05s)", self)
        speed_very_fast.triggered.connect(lambda: self.set_speed(5))
        
        # Add custom speed option
        speed_custom = QAction("Custom Speed...", self)
        speed_custom.triggered.connect(self.open_speed_dialog)
        
        # Add actions to speed menu
        speed_menu.addAction(speed_slow)
        speed_menu.addAction(speed_normal)
        speed_menu.addAction(speed_fast)
        speed_menu.addAction(speed_very_fast)
        speed_menu.addSeparator()
        speed_menu.addAction(speed_custom)
        
        # Add Errors submenu
        errors_menu = settings_menu.addMenu("🎯 Errors")
        
        # Add error rate presets
        errors_none = QAction("No Errors (0%)", self)
        errors_none.triggered.connect(lambda: self.set_error_rate(0))
        
        errors_low = QAction("Low (1%)", self)
        errors_low.triggered.connect(lambda: self.set_error_rate(1))
        
        errors_medium = QAction("Medium (2%)", self)
        errors_medium.triggered.connect(lambda: self.set_error_rate(2))
        
        errors_high = QAction("High (5%)", self)
        errors_high.triggered.connect(lambda: self.set_error_rate(5))
        
        # Add custom error rate option
        errors_custom = QAction("Custom Error Rate...", self)
        errors_custom.triggered.connect(self.open_error_dialog)
        
        # Add actions to errors menu
        errors_menu.addAction(errors_none)
        errors_menu.addAction(errors_low)
        errors_menu.addAction(errors_medium)
        errors_menu.addAction(errors_high)
        errors_menu.addSeparator()
        errors_menu.addAction(errors_custom)
        
        # Add theme option
        theme_menu = settings_menu.addMenu("🎨 Theme")
        
        self.theme_group = []
        theme_cyberpunk = QAction("Cyberpunk (Dark City)", self)
        theme_cyberpunk.setCheckable(True)
        theme_cyberpunk.triggered.connect(lambda: self.set_theme("cyberpunk"))
        theme_menu.addAction(theme_cyberpunk)
        self.theme_group.append(theme_cyberpunk)
        theme_pink = QAction("Pink City (Light)", self)
        theme_pink.setCheckable(True)
        theme_pink.triggered.connect(lambda: self.set_theme("pink"))
        theme_menu.addAction(theme_pink)
        self.theme_group.append(theme_pink)
        
        # Add autocorrect toggle
        theme_menu.addSeparator()
        self.autocorrect_action = QAction("✅ Autocorrect", self)
        self.autocorrect_action.setCheckable(True)
        self.autocorrect_action.setChecked(True)
        self.autocorrect_action.triggered.connect(self.toggle_autocorrect)
        theme_menu.addAction(self.autocorrect_action)
        
        # Set default checked
        if getattr(self, 'theme', 'cyberpunk') == 'cyberpunk':
            theme_cyberpunk.setChecked(True)
        else:
            theme_pink.setChecked(True)
            
    def setup_ui(self):
        # Bot image with reference for animation
        self.eye_label = QLabel()
        self.eye_label.setAlignment(Qt.AlignCenter)
        try:
            pixmap = QPixmap("assets/eyes.png").scaled(175, 175, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.eye_label.setPixmap(pixmap)
        except:
            # Fallback if image is missing
            self.eye_label.setText("👁️ 👁️")
            self.eye_label.setStyleSheet("font-size: 64px;")
        
        # Control buttons with tooltips
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("▶️ Start Typing")
        self.start_button.setFixedSize(140, 50)
        self.start_button.setToolTip("Click to begin typing your text.<br>You'll have 4 seconds to focus on your target window.")
        self.start_button.clicked.connect(self.start_typing)
        
        self.close_button = QPushButton("✖ Close")
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedSize(140, 50)
        self.close_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.close_button.clicked.connect(self.close)
        
        # Progress bar with percentage label
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(80, 15)
        self.progress_bar.setValue(0)
        
        self.progress_label = QLabel("0%")
        self.progress_label.setAlignment(Qt.AlignCenter)
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        progress_layout.setAlignment(Qt.AlignCenter)
        
        # Status indicator
        self.status_indicator = StatusIndicator(self)
        
        # Main content layout
        content_layout = QHBoxLayout()
        
        # Text edit area with placeholder and autocorrect
        self.text_edit = AutoCorrectTextEdit(self)
        self.text_edit.setPlaceholderText("Enter text to type...\n\nTip: You can include emoji like 😊 👍 ⭐\n\nAutocorrect is enabled - common misspellings will be fixed as you type!")
        
        # Quick templates sidebar
        self.templates_widget = QuickTemplate(self)
        self.templates_widget.template_selected.connect(self.insert_template)
        
        content_layout.addWidget(self.text_edit, 3)
        content_layout.addWidget(self.templates_widget, 1)
        
        # Add everything to main layout
        self.main_layout.addWidget(self.eye_label)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.close_button)
        button_layout.addStretch()
        button_layout.addLayout(progress_layout)
        
        self.main_layout.addLayout(button_layout)
        self.main_layout.addWidget(self.status_indicator)
        self.main_layout.addLayout(content_layout)
        
    def insert_template(self, template_text):
        """Insert template text at cursor position"""
        self.text_edit.insertPlainText(template_text)
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"{value}%")
    
    def set_error_rate(self, value):
        """Set the error rate to a specific percentage"""
        self.error_rate = value / 100
        if hasattr(self, 'status_indicator'):
            self.status_indicator.update_status()
    
    def set_speed(self, value):
        """Set the typing speed in seconds (value is 1-50, representing 0.01s to 0.50s)"""
        self.typing_speed = value / 100
        if hasattr(self, 'status_indicator'):
            self.status_indicator.update_status()
    
    def set_theme(self, theme_name):
        """Switch between themes and update all widgets"""
        self.theme = theme_name
        # Uncheck all, check only the selected
        for action in self.theme_group:
            action.setChecked(False)
        if theme_name == "cyberpunk":
            self.theme_group[0].setChecked(True)
        else:
            self.theme_group[1].setChecked(True)
        self.apply_theme()
        if hasattr(self, 'status_indicator'):
            self.status_indicator.update_status()
    
    def apply_theme(self):
        # Apply stylesheet for the selected theme
        if getattr(self, 'theme', 'cyberpunk') == 'cyberpunk':
            self.setStyleSheet(StyleSheet.CYBERPUNK)
        else:
            self.setStyleSheet(StyleSheet.PINK_CITY)
    
    def load_memory(self) -> Dict:
        try:
            with open("word_memory.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_memory(self) -> None:
        with open("word_memory.json", "w", encoding="utf-8") as f:
            json.dump(self.word_memory, f, indent=2)
    
    def show_popup(self, title, message, kind="info"):
        dialog = PopupDialog(self, title, message, kind)
        dialog.exec_()
    
    def open_settings(self):
        dialog = SettingsDialog(self, self.error_rate, self.dark_mode)
        dialog.exec_()
    
    def start_typing(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            self.show_popup("Warning", "Enter text first!", kind="warn")
            return
        
        delay = self.typing_speed
        
        self.show_popup("Ready", "Click into target window within 2 seconds.\nOnce started, typing will continue in that window even if you click elsewhere.")
        
        # Start typing in a separate thread
        if self.typing_thread and self.typing_thread.isRunning():
            self.typing_thread.stop()
            self.typing_thread.wait()
        
        self.typing_thread = TypingThread(
            text, delay, self.error_rate, 
            self.punc_pause_prob, self.space_pause_prob, 
            self.thinking_pause_prob
        )
        self.typing_thread.progress.connect(self.update_progress)
        self.typing_thread.finished.connect(self.typing_finished)
        self.typing_thread.error.connect(self.handle_typing_error)
        self.typing_thread.start()
    
    def handle_typing_error(self, error_msg):
        """Handle errors from typing thread"""
        print(f"Error: {error_msg}")
        # Could show a status message but don't interrupt typing
    
    def typing_finished(self):
        self.progress_bar.setValue(0)
        self.progress_label.setText("0%")
        self.show_popup("Done", "Typing complete!")
        self.save_memory()
    
    def toggle_autocorrect(self, checked):
        """Toggle autocorrect functionality"""
        if hasattr(self, 'text_edit') and isinstance(self.text_edit, AutoCorrectTextEdit):
            self.text_edit.toggle_autocorrect(checked)
    
    def open_error_dialog(self):
        """Open a dialog to set custom error rate"""
        current_rate = int(self.error_rate * 100)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Custom Error Rate")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout(dialog)
        
        # Add a horizontal slider for error rate
        slider_layout = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(20)
        slider.setValue(current_rate)
        
        # Add labels
        slider_layout.addWidget(QLabel("Low"))
        slider_layout.addWidget(slider)
        slider_layout.addWidget(QLabel("High"))
        
        # Add value display
        value_label = QLabel(f"{current_rate}%")
        value_label.setAlignment(Qt.AlignCenter)
        
        # Update value label when slider changes
        def update_label(value):
            value_label.setText(f"{value}%")
        
        slider.valueChanged.connect(update_label)
        
        # Add buttons
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: self.apply_custom_error_rate(slider.value(), dialog))
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(apply_button)
        
        # Add all widgets to main layout
        layout.addLayout(slider_layout)
        layout.addWidget(value_label)
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def apply_custom_error_rate(self, value, dialog):
        """Apply the custom error rate and close the dialog"""
        self.set_error_rate(value)
        dialog.accept()
        
    def open_speed_dialog(self):
        """Open a dialog to set custom speed"""
        current_speed = int(self.typing_speed * 100)
        dialog = QDialog(self)
        dialog.setWindowTitle("Custom Speed")
        dialog.setFixedSize(300, 150)
        layout = QVBoxLayout(dialog)
        # Add a horizontal slider for speed
        slider_layout = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(50)
        slider.setValue(current_speed)
        # Add labels
        slider_layout.addWidget(QLabel("Fast"))
        slider_layout.addWidget(slider)
        slider_layout.addWidget(QLabel("Slow"))
        # Add value display
        value_label = QLabel(f"{current_speed/100:.2f}s")
        value_label.setAlignment(Qt.AlignCenter)
        # Update value label when slider changes
        def update_label(value):
            value_label.setText(f"{value/100:.2f}s")
        slider.valueChanged.connect(update_label)
        # Add buttons
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.reject)
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(lambda: self.apply_custom_speed(slider.value(), dialog))
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(apply_button)
        # Add all widgets to main layout
        layout.addLayout(slider_layout)
        layout.addWidget(value_label)
        layout.addLayout(button_layout)
        dialog.exec_()
    
    def apply_custom_speed(self, value, dialog):
        """Apply the custom speed and close the dialog"""
        self.set_speed(value)
        dialog.accept()
    
    def closeEvent(self, event):
        if self.typing_thread and self.typing_thread.isRunning():
            self.typing_thread.stop()
            self.typing_thread.wait()
        event.accept()

class PopupDialog(QDialog):
    def __init__(self, parent, title, message, kind="info"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(420, 180)
        self.setModal(True)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title_label = QLabel(title)
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        
        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        
        button = QPushButton("OK")
        button.setFixedSize(120, 40)
        if kind != "info":
            button.setObjectName("closeButton")
        button.clicked.connect(self.accept)
        
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addWidget(message_label, alignment=Qt.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

class SettingsDialog(QDialog):
    def __init__(self, parent, error_rate, dark_mode):
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setFixedSize(300, 200)
        
        self.parent = parent
        self.error_rate = error_rate
        self.dark_mode = dark_mode
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        error_label = QLabel("Error rate (%)")
        
        self.error_slider = QSlider(Qt.Horizontal)
        self.error_slider.setMinimum(0)
        self.error_slider.setMaximum(20)
        self.error_slider.setValue(int(error_rate * 100))
        self.error_slider.valueChanged.connect(self.update_error_rate)
        
        self.dark_mode_check = QCheckBox("Dark Mode")
        self.dark_mode_check.setChecked(dark_mode)
        self.dark_mode_check.toggled.connect(self.toggle_dark_mode)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button.setFixedSize(120, 40)
        
        layout.addWidget(error_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.error_slider)
        layout.addWidget(self.dark_mode_check)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
    
    def update_error_rate(self, value):
        self.error_rate = value / 100
        self.parent.error_rate = self.error_rate
    
    def toggle_dark_mode(self, checked):
        self.dark_mode = checked
        self.parent.dark_mode = checked
        self.parent.apply_theme()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TypingBot()
    window.show()
    sys.exit(app.exec_())

# Packaging instructions:
# 1. pip install pyinstaller
# 2. pyinstaller --onefile --windowed main.py
# This creates a user-friendly EXE without opening VSCode.
