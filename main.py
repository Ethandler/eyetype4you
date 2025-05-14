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
# Testing file edit
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

# Windows constants for SendMessage/PostMessage
WM_CHAR = 0x0102
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
VK_RETURN = 0x0D
VK_BACK = 0x08
VK_TAB = 0x09
VK_SHIFT = 0x10
VK_CONTROL = 0x11

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
    'm': ['n', 'j', 'k', '<'],   'n': ['b', 'h', 'j', 'm'],
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
        self.textChanged.connect(self.check_for_correction)
        # Track sentence endings for auto-capitalization
        self.last_char_was_sentence_end = True  # Start of document is sentence end
        
    def toggle_autocorrect(self, enabled):
        """Enable or disable autocorrect"""
        self.autocorrect_enabled = enabled
    
    def keyPressEvent(self, event):
        """Override to track sentence endings and potentially auto-capitalize"""
        # Check for auto-capitalization
        if self.autocorrect_enabled and event.text() == " ":
            cursor = self.textCursor()
            pos = cursor.position()
            doc = self.document()
            text = doc.toPlainText()
            
            # Auto-capitalize standalone i to I
            if pos >= 2 and text[pos-2:pos] == "i ":
                # Check if i is standalone (surrounded by spaces or at start)
                if pos == 2 or text[pos-3] in " \n\t":
                    cursor.setPosition(pos-2)
                    cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
                    cursor.insertText("I")
                    # No need to reset cursor, it maintains position after edit
                    
        # Call base method to handle the key normally
        super().keyPressEvent(event)
        
        # After handling key, update sentence tracking
        if event.text() in ".!?":
            self.last_char_was_sentence_end = True
        elif self.last_char_was_sentence_end and event.text().strip():
            # Auto-capitalize first letter of sentences
            # First letter after sentence end that isn't whitespace
            if event.text().islower():
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
                cursor.insertText(event.text().upper())
            self.last_char_was_sentence_end = False
    
    def check_for_correction(self):
        if not self.autocorrect_enabled:
            return

        cursor = self.textCursor()
        # Use document().toPlainText() for a stable view of text, cursor.position() for current pos
        current_doc_text = self.document().toPlainText() 
        cursor_pos = cursor.position()

        # Add safety check for empty document or cursor at beginning
        if cursor_pos <= 0 or not current_doc_text:
            return

        # The character just typed is at cursor_pos - 1
        last_char_typed = current_doc_text[cursor_pos - 1]

        # Define word delimiters that trigger the autocorrection check
        delimiters = {" ", ".", ",", "!", "?", ";", "\n", "\t"}

        if last_char_typed in delimiters:
            # Find the start of the word that precedes the delimiter
            # Search backwards from the character *before* the delimiter (cursor_pos - 2)
            search_end_idx = cursor_pos - 2
            
            # Another safety check
            if search_end_idx < 0:
                return
                
            start_of_word_idx = -1

            for i in range(search_end_idx, -1, -1):
                if current_doc_text[i] in delimiters:
                    start_of_word_idx = i + 1 # Word starts after this delimiter
                    break
            else: # Loop finished without break, means no delimiter found before this word
                if search_end_idx >=0 : # Only if there were characters to form a word
                    start_of_word_idx = 0 # Word starts at the beginning of the text
            
            # Ensure a valid word was found (start_of_word_idx is valid and before or at search_end_idx)
            if start_of_word_idx != -1 and start_of_word_idx <= search_end_idx:
                # Extract the original word as it appears in the text_edit (end index for slice is exclusive)
                original_word_in_doc = current_doc_text[start_of_word_idx : cursor_pos -1]

                # Prepare word for dictionary lookup: lowercase, strip surrounding whitespace, and specific trailing punctuation
                word_for_dict_lookup_base = original_word_in_doc.strip().lower()
                
                punctuation_to_strip_for_dict = ".,;:!?\"'()[]{}"
                cleaned_word_for_dict = word_for_dict_lookup_base
                # Iteratively remove trailing punctuation that's in our defined set
                while cleaned_word_for_dict and cleaned_word_for_dict[-1] in punctuation_to_strip_for_dict:
                    cleaned_word_for_dict = cleaned_word_for_dict[:-1]

                if cleaned_word_for_dict and cleaned_word_for_dict in AUTOCORRECT_DICT:
                    correction_template = AUTOCORRECT_DICT[cleaned_word_for_dict]
                    
                    final_correction = correction_template
                    # Try to preserve original capitalization if it was just the first letter
                    original_stripped_word = original_word_in_doc.strip()
                    if original_stripped_word and original_stripped_word[0].isupper() and len(original_stripped_word) == len(cleaned_word_for_dict):
                        if cleaned_word_for_dict == original_stripped_word.lower(): # Check if it's the same word, just different case
                           final_correction = correction_template[0].upper() + correction_template[1:]
                    
                    trailing_punctuation = ""
                    # Preserve trailing punctuation from the original word if it was stripped for dict lookup
                    if len(original_stripped_word) > len(cleaned_word_for_dict):
                         potential_punct = original_stripped_word[len(cleaned_word_for_dict):]
                         is_all_known_punct = True
                         for char_p in potential_punct:
                             if char_p not in punctuation_to_strip_for_dict:
                                 is_all_known_punct = False
                                 break
                         if is_all_known_punct:
                             trailing_punctuation = potential_punct

                    # Only perform replacement if the corrected version is actually different
                    if original_word_in_doc.strip() != final_correction + trailing_punctuation:
                        self.blockSignals(True) # Prevent textChanged recursion
                        
                        mod_cursor = self.textCursor() # Use a fresh cursor for modification
                        mod_cursor.setPosition(start_of_word_idx) # Go to the start of the word to replace
                        # Select the original word slice as identified (length of original_word_in_doc)
                        mod_cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(original_word_in_doc))
                        
                        mod_cursor.insertText(final_correction + trailing_punctuation)
                        
                        self.blockSignals(False) # Re-enable signals
                        return # Correction made, exit

class DirectWindowTyper:
    """Types into a window with focus control options"""
    
    def __init__(self, hwnd, background_mode=False, notepad_mode=False):
        self.hwnd = hwnd
        self.background_mode = background_mode
        self.notepad_mode = notepad_mode
        # Get window title for better identification
        title_len = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(title_len + 1)
        user32.GetWindowTextW(hwnd, buff, title_len + 1)
        self.window_title = buff.value
        # Track success/failure of methods
        self.last_method_used = None
        self.method_success_count = {
            "direct_send": 0,
            "direct_post": 0,
            "notepad_em": 0,
            "pyautogui": 0
        }
    
    def ensure_window_focus(self):
        """Make sure the target window has focus if not in background mode"""
        if not user32.IsWindow(self.hwnd):
            return False
            
        # In background mode, we don't need focus, just check window is valid
        if self.background_mode:
            return True
            
        # If already has focus, we're good
        if user32.GetForegroundWindow() == self.hwnd:
            return True
            
        # Try to focus the window - multiple attempts
        for i in range(3):
            # If window is minimized, restore it
            if user32.IsIconic(self.hwnd):
                user32.ShowWindow(self.hwnd, 9)  # SW_RESTORE = 9
                time.sleep(0.1)
                
            # Activate the window
            if user32.SetForegroundWindow(self.hwnd):
                time.sleep(0.1)  # Wait a bit for focus
                if user32.GetForegroundWindow() == self.hwnd:
                    return True
            
            # If not successful, wait a bit longer and try again
            time.sleep(0.2)
        
        # Could not set focus after multiple attempts
        return False
    
    def try_direct_message(self, char, method="send"):
        """Try to type using direct Windows messaging"""
        try:
            # For Notepad mode, use the EM_REPLACESEL message directly
            if self.notepad_mode and char:
                EM_REPLACESEL = 0x00C2
                char_buffer = ctypes.create_unicode_buffer(char)
                if method == "send":
                    result = user32.SendMessageW(self.hwnd, EM_REPLACESEL, 1, ctypes.byref(char_buffer))
                else:
                    result = user32.PostMessageW(self.hwnd, EM_REPLACESEL, 1, ctypes.byref(char_buffer))
                if result:
                    self.method_success_count["notepad_em"] += 1
                    self.last_method_used = "notepad_em"
                    return True
                    
            # For function keys or special keys
            if char == '\n':
                # Send Enter key
                if method == "send":
                    user32.SendMessageW(self.hwnd, WM_KEYDOWN, VK_RETURN, 0)
                    user32.SendMessageW(self.hwnd, WM_KEYUP, VK_RETURN, 0)
                else:
                    user32.PostMessageW(self.hwnd, WM_KEYDOWN, VK_RETURN, 0)
                    user32.PostMessageW(self.hwnd, WM_KEYUP, VK_RETURN, 0)
            elif char == '\t':
                # Send Tab key
                if method == "send":
                    user32.SendMessageW(self.hwnd, WM_KEYDOWN, VK_TAB, 0)
                    user32.SendMessageW(self.hwnd, WM_KEYUP, VK_TAB, 0)
                else:
                    user32.PostMessageW(self.hwnd, WM_KEYDOWN, VK_TAB, 0)
                    user32.PostMessageW(self.hwnd, WM_KEYUP, VK_TAB, 0)
            elif char == '\b':
                # Send Backspace key
                if method == "send":
                    user32.SendMessageW(self.hwnd, WM_KEYDOWN, VK_BACK, 0)
                    user32.SendMessageW(self.hwnd, WM_KEYUP, VK_BACK, 0)
                else:
                    user32.PostMessageW(self.hwnd, WM_KEYDOWN, VK_BACK, 0)
                    user32.PostMessageW(self.hwnd, WM_KEYUP, VK_BACK, 0)
            elif not char:
                # Empty char is just for testing if the window accepts messages
                return True
            else:
                # Send regular character
                char_code = ord(char)
                if method == "send":
                    result = user32.SendMessageW(self.hwnd, WM_CHAR, char_code, 0)
                else:
                    result = user32.PostMessageW(self.hwnd, WM_CHAR, char_code, 0)
                
                if not result:
                    # If we're dealing with Notepad, try another approach
                    if "notepad" in self.window_title.lower() or self.notepad_mode:
                        # Notepad specific approach - EM_REPLACESEL message
                        EM_REPLACESEL = 0x00C2
                        char_buffer = ctypes.create_unicode_buffer(char)
                        if method == "send":
                            result = user32.SendMessageW(self.hwnd, EM_REPLACESEL, 1, ctypes.byref(char_buffer))
                        else:
                            result = user32.PostMessageW(self.hwnd, EM_REPLACESEL, 1, ctypes.byref(char_buffer))
                        if result:
                            self.method_success_count["notepad_em"] += 1
                            self.last_method_used = "notepad_em"
                            return True
                    return False
            return True
        except Exception as e:
            print(f"Exception in try_direct_message: {e}")
            return False
    
    def type_char(self, char):
        """Type a single character, using best available method"""
        if not user32.IsWindow(self.hwnd):
            return False
            
        # If in background mode, try direct message first
        if self.background_mode:
            # Try SendMessage first
            if self.try_direct_message(char, "send"):
                self.method_success_count["direct_send"] += 1
                self.last_method_used = "direct_send"
                return True
                
            # Try PostMessage next
            if self.try_direct_message(char, "post"):
                self.method_success_count["direct_post"] += 1
                self.last_method_used = "direct_post"
                return True
                
            # If both direct methods fail, fall back to pyautogui with focus
            if self.ensure_window_focus():
                if char == '\b':  # backspace
                    pyautogui.press('backspace')
                else:
                    pyautogui.typewrite(char)
                self.method_success_count["pyautogui"] += 1
                self.last_method_used = "pyautogui"
                return True
                
            return False
        else:
            # Regular typing with pyautogui - requires focus
            if not self.ensure_window_focus():
                # Failed to give focus to target window
                return False
            
            if char == '\b':  # backspace
                pyautogui.press('backspace')
            else:
                pyautogui.typewrite(char)
            
            self.method_success_count["pyautogui"] += 1
            self.last_method_used = "pyautogui"
            return True
        
    def get_diagnostic_info(self):
        """Return diagnostic information about which methods worked"""
        return f"SendMessage: {self.method_success_count['direct_send']}, " \
               f"PostMessage: {self.method_success_count['direct_post']}, " \
               f"NotepadEM: {self.method_success_count['notepad_em']}, " \
               f"PyAutoGUI: {self.method_success_count['pyautogui']}, " \
               f"Last method: {self.last_method_used}"
    
    def type_string(self, text, delay=0.01):
        """Type a string with optional delay between characters"""
        if not text or not user32.IsWindow(self.hwnd):
            return False
            
        success = True
        for char in text:
            if not self.type_char(char):
                success = False
                
            if delay > 0:
                time.sleep(delay)
                
        return success
    
    def paste_text(self, text):
        """Set clipboard and paste text"""
        if not text or not user32.IsWindow(self.hwnd):
            return False
            
        # Save original clipboard content
        original_clipboard = pyperclip.paste()
        
        try:
            # Set clipboard to desired text
            pyperclip.copy(text)
            
            if self.background_mode:
                # Try different approaches to paste
                # First approach: Direct Windows messages
                success = False
                
                # Try SendMessage for Ctrl+V
                try:
                    user32.SendMessageW(self.hwnd, WM_KEYDOWN, VK_CONTROL, 0)
                    user32.SendMessageW(self.hwnd, WM_KEYDOWN, ord('V'), 0)
                    user32.SendMessageW(self.hwnd, WM_KEYUP, ord('V'), 0)
                    user32.SendMessageW(self.hwnd, WM_KEYUP, VK_CONTROL, 0)
                    success = True
                    self.method_success_count["direct_send"] += 1
                except:
                    success = False
                
                # If that fails, try PostMessage for Ctrl+V
                if not success:
                    try:
                        user32.PostMessageW(self.hwnd, WM_KEYDOWN, VK_CONTROL, 0)
                        user32.PostMessageW(self.hwnd, WM_KEYDOWN, ord('V'), 0)
                        user32.PostMessageW(self.hwnd, WM_KEYUP, ord('V'), 0)
                        user32.PostMessageW(self.hwnd, WM_KEYUP, VK_CONTROL, 0)
                        success = True
                        self.method_success_count["direct_post"] += 1
                    except:
                        success = False
                
                # If all else fails, fall back to pyautogui
                if not success and self.ensure_window_focus():
                    pyautogui.hotkey('ctrl', 'v')
                    success = True
                    self.method_success_count["pyautogui"] += 1
            else:
                # Ensure window has focus
                if not self.ensure_window_focus():
                    return False
                    
                # Paste with keyboard shortcut
                pyautogui.hotkey('ctrl', 'v')
                success = True
                self.method_success_count["pyautogui"] += 1
                
            time.sleep(0.05)  # Brief pause to ensure paste completes
            
            return success
        finally:
            # Restore original clipboard
            pyperclip.copy(original_clipboard)
    
    def type_string_failsafe(self, text, delay=0.01):
        """Alternative typing method that tries individual characters and checks focus after each one"""
        if not text or not user32.IsWindow(self.hwnd):
            return False
            
        success = True
        for char in text:
            # Ensure focus for each character if not in background mode
            if not self.background_mode and not self.ensure_window_focus():
                return False
                
            # Type the character with all possible methods until one works
            if not self.type_char(char):
                success = False
                
            # Delay between characters
            if delay > 0:
                time.sleep(delay)

        return success

class TypingThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, text, delay, error_rate, punc_pause_prob, space_pause_prob, thinking_pause_prob, 
                 background_mode, notepad_mode=False):
        super().__init__()
        self.text = text
        self.delay = delay
        self.error_rate = error_rate
        self.punc_pause_prob = punc_pause_prob
        self.space_pause_prob = space_pause_prob
        self.thinking_pause_prob = thinking_pause_prob
        self.background_mode = background_mode
        self.notepad_mode = notepad_mode
        self.running = True
        self.target_window = None
        
    def run(self):
        try:
            self.error.emit("👆 Click in the target window now...")
            time.sleep(1)  # Brief pause
            self.error.emit("⌨️ Get ready to type in 1 second...")
            time.sleep(1)  # Second pause before starting
            
            # Get and store the active window handle
            self.target_window = user32.GetForegroundWindow()
            if not user32.IsWindow(self.target_window):
                self.error.emit("❌ Invalid target window selected. Please try again.")
                self.finished.emit()
                return
                
            # Get window title for better identification
            title_len = user32.GetWindowTextLengthW(self.target_window)
            buff = ctypes.create_unicode_buffer(title_len + 1)
            user32.GetWindowTextW(self.target_window, buff, title_len + 1)
            self.target_title = buff.value
            
            # Create diagnostic label for background mode
            bg_status = "enabled" if self.background_mode else "disabled"
            notepad_status = "enabled" if self.notepad_mode else "disabled"
            self.error.emit(f"✅ Typing into: {self.target_title} (Background: {bg_status}, Notepad: {notepad_status})")
            
            # Create direct typer
            typer = DirectWindowTyper(self.target_window, self.background_mode, self.notepad_mode)
            
            # First ensure window has focus before we start
            if not typer.ensure_window_focus():
                self.error.emit(f"Could not focus target window: {self.target_title}")
                self.finished.emit()
                return
                
            # Test typing with each method to identify what works with this window type
            self.error.emit("🧪 Testing typing methods...")
            
            # Try the direct send method
            direct_send_works = typer.try_direct_message("", "send")  # Try empty char to test without typing
            
            # Try the direct post method
            direct_post_works = typer.try_direct_message("", "post")  # Try empty char to test without typing
            
            # PyAutoGUI always works when window has focus
            pyautogui_works = True
            
            # Log the results
            self.error.emit(f"Compatible methods: DirectSend={direct_send_works}, DirectPost={direct_post_works}, PyAutoGUI={pyautogui_works}")
            
            # If we're in background mode but direct messaging won't work, warn the user
            if self.background_mode and not (direct_send_works or direct_post_works):
                self.error.emit("⚠️ Background mode may not work with this window type. Falling back to foreground typing.")
            
            total = len(self.text)
            i = 0
            current_line_indent = ''
            
            # Add rate limiting
            char_count = 0
            last_reset = time.time()
            last_focus_check = time.time()
            
            while i < total and self.running:
                try:
                    # Rate limiting - no more than 30 chars per second regardless of delay setting
                    char_count += 1
                    if char_count > 30:
                        now = time.time()
                        if now - last_reset < 1.0:
                            time.sleep(1.0 - (now - last_reset))
                        char_count = 0
                        last_reset = time.time()
                        
                    # Check window is still valid periodically
                    if not user32.IsWindow(self.target_window):
                        self.error.emit("Target window closed or became invalid during typing.")
                        break # Exit the loop
                    
                    # Check focus every 1 second to make sure we haven't lost it
                    now = time.time()
                    if now - last_focus_check > 1.0:
                        if not typer.ensure_window_focus():
                            self.error.emit("Lost focus on target window. Trying to refocus...")
                            if not typer.ensure_window_focus():  # Try one more time
                                self.error.emit("Could not refocus target window. Aborting.")
                                break
                        last_focus_check = now

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
                        
                        # Type newline
                        if not typer.type_char('\n'):
                            self.error.emit("Failed to type newline. Window may have lost focus.")
                            continue
                        time.sleep(self.delay)
                        
                        # Add indentation if needed
                        if current_line_indent:
                            success = typer.type_string_failsafe(current_line_indent, self.delay)
                            if not success:
                                self.error.emit("Warning: Failed to type indentation. Trying alternative method...")
                                # Try character by character as fallback
                                for indent_char in current_line_indent:
                                    if not typer.type_char(indent_char):
                                        self.error.emit("Failed to type indentation character.")
                                    time.sleep(self.delay)
                        
                        i += 1
                        self.progress.emit(int((i / total) * 100))
                        continue

                    # typo?
                    if ch.isalnum() and random.random() < self.error_rate:
                        if (nb := keyboard_neighbors.get(ch, [])):
                            typo = random.choice(nb)
                            if not typer.type_char(typo):
                                self.error.emit("Failed to type typo character. Checking window focus...")
                                if not typer.ensure_window_focus():
                                    self.error.emit("Lost focus and could not refocus. Aborting.")
                                    break
                            time.sleep(self.delay)
                            if not typer.type_char('\b'):  # backspace
                                self.error.emit("Failed to type backspace. Checking window focus...")
                                if not typer.ensure_window_focus():
                                    self.error.emit("Lost focus and could not refocus. Aborting.")
                                    break
                            time.sleep(self.delay)
                            
                    # type or emoji-paste
                    if emoji.is_emoji(ch):
                        # Emoji needs special handling - use paste
                        if not typer.paste_text(ch):
                            self.error.emit("Failed to paste emoji. Checking window focus...")
                            if not typer.ensure_window_focus():
                                self.error.emit("Lost focus and could not refocus. Aborting.")
                                break
                    else:
                        if not typer.type_char(ch):
                            self.error.emit("Failed to type character. Checking window focus...")
                            if not typer.ensure_window_focus():
                                self.error.emit("Lost focus and could not refocus. Aborting.")
                                break
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
            
            # At the end of typing, show diagnostics if there were any issues
            diagnostic_info = typer.get_diagnostic_info()
            self.error.emit(f"Typing complete. Methods used: {diagnostic_info}")
            
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
        
        # Background mode indicator
        self.bg_mode_label = QLabel()
        self.bg_mode_label.setObjectName("statusLabel")
        
        # Notepad mode indicator
        self.notepad_mode_label = QLabel()
        self.notepad_mode_label.setObjectName("statusLabel")
        
        layout.addWidget(self.speed_label)
        layout.addStretch()
        layout.addWidget(self.error_label)
        layout.addStretch()
        layout.addWidget(self.theme_label)
        layout.addStretch()
        layout.addWidget(self.bg_mode_label)
        layout.addStretch()
        layout.addWidget(self.notepad_mode_label)
        
        # Connect to checkbox changes
        if hasattr(parent, 'background_mode_check'):
            parent.background_mode_check.stateChanged.connect(self.update_status)
        if hasattr(parent, 'notepad_mode_check'):
            parent.notepad_mode_check.stateChanged.connect(self.update_status)
        
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
        
        # Update background mode
        if hasattr(self.parent, 'background_mode_check'):
            bg_mode = "Enabled" if self.parent.background_mode_check.isChecked() else "Disabled"
            self.bg_mode_label.setText(f"🖥️ Background: {bg_mode}")
            
        # Update notepad mode
        if hasattr(self.parent, 'notepad_mode_check'):
            notepad_mode = "Enabled" if self.parent.notepad_mode_check.isChecked() else "Disabled"
            self.notepad_mode_label.setText(f"📝 Notepad: {notepad_mode}")

class SplashScreen(QDialog):
    """A reliable splash screen shown at application startup"""
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setModal(True)
        self.setFixedSize(450, 300)
        
        # Center on screen
        screen_size = QApplication.primaryScreen().geometry()
        self.move((screen_size.width() - self.width()) // 2,
                  (screen_size.height() - self.height()) // 2)
        
        # Set up UI
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Eye image
        self.eye_label = QLabel()
        self.eye_label.setAlignment(Qt.AlignCenter)
        try:
            pixmap = QPixmap("assets/eyes.png").scaled(175, 175, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.eye_label.setPixmap(pixmap)
        except:
            # Fallback if image is missing
            self.eye_label.setText("👁️ 👁️")
            self.eye_label.setStyleSheet("font-size: 64px;")
        
        # Welcome text
        title = QLabel("Welcome to Eyetype4You")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #08d9d6;")
        
        subtitle = QLabel("The intelligent typing assistant")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #f8f8ff;")
        
        # Close button
        self.close_btn = QPushButton("Start Using Eyetype4You")
        self.close_btn.setFixedHeight(40)
        self.close_btn.clicked.connect(self.accept)
        
        # Add all widgets to layout
        layout.addWidget(self.eye_label)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.close_btn)
        
        # Set dark background
        self.setStyleSheet("""
            QDialog {
                background-color: #10101a;
                border: 2px solid #08d9d6;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #08d9d6;
                color: #1a1a2e;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #20e7e4;
            }
        """)
        
        # Auto-close after 5 seconds
        QTimer.singleShot(5000, self.accept)

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
        
        # Show splash screen
        splash = SplashScreen(self)
        splash.exec_()
    
    def setup_ui(self):
        # Bot image with reference
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
        
        # Background mode checkbox
        self.background_mode_check = QCheckBox("Background Typing Mode")
        self.background_mode_check.setToolTip("When enabled, typing continues in the target window<br>even if you're working in other windows.")
        
        # Notepad mode checkbox
        self.notepad_mode_check = QCheckBox("Notepad/Text Editor Mode")
        self.notepad_mode_check.setToolTip("Enable this when typing into Notepad, Notepad++, or other text editors.<br>Uses special methods that work better with these applications.")
        
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
        
        # Put buttons and checkbox in same row
        controls_row = QHBoxLayout()
        controls_row.addWidget(self.start_button)
        
        # Stack checkboxes vertically in a container
        checkbox_layout = QVBoxLayout()
        checkbox_layout.addWidget(self.background_mode_check)
        checkbox_layout.addWidget(self.notepad_mode_check)
        checkbox_container = QWidget()
        checkbox_container.setLayout(checkbox_layout)
        
        controls_row.addWidget(checkbox_container)
        controls_row.addWidget(self.close_button)
        controls_row.addStretch()
        controls_row.addLayout(progress_layout)
        
        self.main_layout.addLayout(controls_row)
        self.main_layout.addWidget(self.status_indicator)
        self.main_layout.addLayout(content_layout)
    
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
        
        # Check if special modes are enabled
        background_mode = self.background_mode_check.isChecked()
        notepad_mode = self.notepad_mode_check.isChecked()
        
        # Create instructions based on modes
        if background_mode:
            instructions = "Click into the target window within 2 seconds.\nYou can work in other windows while typing continues in the background."
        else:
            instructions = "Click into the target window within 2 seconds.\nThe typing will stay in that window even if you click elsewhere."
            
        if notepad_mode:
            instructions += "\nNotepad/Text Editor Mode is enabled for better compatibility."
            
        self.show_popup("Ready", instructions)
        
        # Start typing in a separate thread
        if self.typing_thread and self.typing_thread.isRunning():
            self.typing_thread.stop()
            self.typing_thread.wait()
        
        self.typing_thread = TypingThread(
            text, delay, self.error_rate, 
            self.punc_pause_prob, self.space_pause_prob, 
            self.thinking_pause_prob,
            background_mode,
            notepad_mode
        )
        self.typing_thread.progress.connect(self.update_progress)
        self.typing_thread.finished.connect(self.typing_finished)
        self.typing_thread.error.connect(self.handle_typing_error)
        self.typing_thread.start()
    
    def handle_typing_error(self, error_msg):
        """Handle errors from typing thread"""
        print(f"Error: {error_msg}")
        
        # Display critical errors as popups
        if any(critical in error_msg for critical in 
              ["Invalid target window", "Lost focus", "Failed to", "Aborting"]):
            # Use QTimer to ensure this runs on the main thread
            QTimer.singleShot(0, lambda: self.show_popup("Typing Error", error_msg, kind="warn"))
        
        # Let other errors just appear in the status message
    
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
