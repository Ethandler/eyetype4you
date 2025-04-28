import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyautogui
pyautogui.PAUSE = 0  # Remove default pause between actions for max speed
import threading
import random
import time
import json
import os
from typing import Dict, List
import string
import math
import regex as re  # Use the 'regex' module for Unicode emoji support

keyboard_neighbors: Dict[str, List[str]] = {
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

SPECIAL_KEYS = {
    'enter': 'enter',
    'shift+enter': ['shift', 'enter'],
    'tab': 'tab',
    'capslock': 'capslock',
    'numlock': 'numlock',
    'esc': 'esc',
    'escape': 'esc',
    'backspace': 'backspace',
    'delete': 'delete',
    'end': 'end',
    'home': 'home',
    'pageup': 'pageup',
    'pagedown': 'pagedown',
    'up': 'up',
    'down': 'down',
    'left': 'left',
    'right': 'right',
    'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4', 'f5': 'f5', 'f6': 'f6',
    'f7': 'f7', 'f8': 'f8', 'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12',
    'numpad0': 'num0', 'numpad1': 'num1', 'numpad2': 'num2', 'numpad3': 'num3',
    'numpad4': 'num4', 'numpad5': 'num5', 'numpad6': 'num6', 'numpad7': 'num7',
    'numpad8': 'num8', 'numpad9': 'num9', 'numpad.': 'decimal',
    'numpad+': 'add', 'numpad-': 'subtract', 'numpad*': 'multiply', 'numpad/': 'divide',
    'numpad_enter': 'enter',
    '~': '`',
    'win': 'win',
    'ctrl': 'ctrl',
    'alt': 'alt',
    # Add more as needed
}

class TypingBot(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Eyetype4You Bot")
        self.geometry("700x800")
        self.configure(bg="#997287")
        self.word_memory: Dict = self.load_memory()

        bot_img = Image.open("assets/eyes.png").resize((150, 150))
        self.bot_photo = ImageTk.PhotoImage(bot_img)
        tk.Label(self, image=self.bot_photo, bg="#997287").pack(pady=10)

        menu_frame = tk.Frame(self, bg="#997287")
        menu_frame.pack(pady=5)

        self.start_btn = tk.Button(menu_frame, text="▶️ Start Typing", width=20, command=self.start_typing)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.close_btn = tk.Button(menu_frame, text="❌ Close", width=10, command=self.destroy)
        self.close_btn.pack(side=tk.LEFT, padx=5)

        self.text_widget = tk.Text(self, wrap=tk.WORD, font=("Courier", 12))
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, padx=10, pady=5)

        speed_frame = tk.Frame(self, bg="#997287")
        speed_frame.pack(pady=5)
        tk.Label(speed_frame, text="Typing Speed:", fg="white", bg="#997287").pack(side=tk.LEFT, padx=5)

        self.speed_var = tk.StringVar(value="Medium")
        speed_options = ["Slow", "Medium", "Fast", "Faster"]
        self.speed_menu = tk.OptionMenu(speed_frame, self.speed_var, *speed_options)
        self.speed_menu.config(bg="#997287", fg="white", highlightthickness=0)
        self.speed_menu["menu"].config(bg="#997287", fg="white")
        self.speed_menu.pack(side=tk.LEFT)

    def load_memory(self) -> Dict:
        try:
            with open("word_memory.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_memory(self) -> None:
        with open("word_memory.json", "w", encoding="utf-8") as f:
            json.dump(self.word_memory, f, indent=2)

    def start_typing(self) -> None:
        text = self.text_widget.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "You need to enter some text first!")
            return

        speed_map = {
            "Slow": 0.20,
            "Medium": 0.12,
            "Fast": 0.08,
            "Faster": 0.05
        }
        delay = speed_map.get(self.speed_var.get(), 0.12)

        # Randomize start delay for stealth
        start_delay = random.uniform(3, 7)
        messagebox.showinfo("Ready", f"Click into the target window within {int(start_delay)} seconds.")
        time.sleep(start_delay)

        threading.Thread(target=self.simulate_typing, args=(text, delay), daemon=True).start()

    def load_emoji_keyword_map(self):
        # Loads emoji to keyword mapping from emoji_annotations.json
        try:
            with open("emoji_annotations.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            mapping = {}
            annotations = data.get("annotations", {}).get("annotations", {})
            for emoji, info in annotations.items():
                keywords = info.get("default", [])
                # Only map if there is at least one keyword and the emoji is not a single ASCII symbol
                if keywords and not (len(emoji) == 1 and ord(emoji) < 128):
                    mapping[emoji] = keywords[0]  # Use the first keyword as the search term
            return mapping
        except Exception as e:
            print("Failed to load emoji annotations:", e)
            return {}

    def insert_emoji_via_picker(self, search_term: str):
        pyautogui.hotkey('win', '.')
        time.sleep(0.3)
        pyautogui.typewrite(search_term, interval=0.05)
        time.sleep(0.1)
        pyautogui.press('enter')
        time.sleep(0.1)
        pyautogui.press('esc')  # Close the picker
        time.sleep(0.1)

    def wait_for_window_focus(self):
        # Placeholder: waits a short time, can be improved with window detection
        time.sleep(0.3)

    def simulate_typing(self, text: str, delay: float) -> None:
        """
        Simulates human-like typing with adjustable speed and error rate.
        Now also detects emoji characters and inserts them using the emoji picker.
        """
        total_chars = len(text)
        base_interval = 0.13
        error_probability = 1 / 83
        punctuation_pause_prob = 0.18
        space_pause_prob = 0.08
        thinking_pause_prob = 0.005
        stutter_prob = 0.008
        shift_slip_prob = 0.002
        long_word_pause_prob = 0.10
        distraction_pause_prob = 0.01
        punctuation_pause_range = (0.10, 0.25)
        space_pause_range = (0.07, 0.18)
        thinking_pause_range = (0.7, 1.5)
        stutter_pause_range = (0.05, 0.12)
        long_word_pause_range = (0.15, 0.35)
        distraction_pause_range = (1.5, 3.0)
        def _random_hold_time():
            return max(0.025, min(random.gauss(0.04, 0.01), 0.06))
        def _random_between_keys():
            return max(0.05, min(random.gauss(base_interval, 0.03), 0.18))
        last_pause = 0
        word_buffer = []
        emoji_map = getattr(self, "_emoji_map", None)
        if emoji_map is None:
            emoji_map = self.load_emoji_keyword_map()
            self._emoji_map = emoji_map
        # Build a set of all emoji keys, sorted by length (longest first)
        emoji_keys = sorted(emoji_map.keys(), key=len, reverse=True)
        emoji_pattern = re.compile('|'.join(re.escape(e) for e in emoji_keys))
        i = 0
        total_chars = len(text)
        while i < total_chars:
            # Try to match an emoji at the current position
            match = emoji_pattern.match(text, i)
            if match:
                emoji = match.group(0)
                self.insert_emoji_via_picker(emoji_map[emoji])
                self.wait_for_window_focus()
                i += len(emoji)
                continue
            char = text[i]
            base_char = char.lower()
            # Replace unsupported unicode with dash or space
            if ord(char) > 126 and char not in {"’", "'"}:
                char = '-' if char == '—' else ' '
            # Build word buffer for long word pause
            if char.isalnum():
                word_buffer.append(char)
            else:
                word_buffer = []
            # Simulate typo with small probability (matches 94% accuracy)
            neighbors = keyboard_neighbors.get(base_char)
            if neighbors and random.random() < error_probability:
                typo_char = random.choice(neighbors)
                self.simulate_typo_correction(typo_char, base_interval)
                time.sleep(_random_between_keys())
            # Random pause after punctuation
            if char in ".!?," and random.random() < punctuation_pause_prob:
                time.sleep(random.uniform(*punctuation_pause_range))
            # Random pause after space
            elif char == " " and random.random() < space_pause_prob:
                time.sleep(random.uniform(*space_pause_range))
            # Rare thinking pause
            if random.random() < thinking_pause_prob:
                time.sleep(random.uniform(*thinking_pause_range))
            # Rare double-tap (stutter) and correction
            if random.random() < stutter_prob:
                self.simulate_typo_correction(char, base_interval)
                time.sleep(random.uniform(*stutter_pause_range))
            # Pause after long word
            if len(word_buffer) > 7 and char == " " and random.random() < long_word_pause_prob:
                time.sleep(random.uniform(*long_word_pause_range))
            # Rare shift slip (wrong case, then correct)
            if char.isalpha() and random.random() < shift_slip_prob:
                wrong_case = char.swapcase()
                self.simulate_typo_correction(wrong_case, base_interval)
                time.sleep(_random_between_keys())
            # Main keypress with random hold time
            self.simulate_keypress(char, _random_hold_time())
            # Random interval between keystrokes
            time.sleep(_random_between_keys())
            self.update_progress(i + 1, total_chars)
            # Occasionally pause for a few seconds (simulate distraction)
            if i - last_pause > random.randint(60, 120) and random.random() < distraction_pause_prob:
                time.sleep(random.uniform(*distraction_pause_range))
                last_pause = i
            i += 1
        self.progress['value'] = 0
        messagebox.showinfo("Done", "Typing complete!")
        self.save_memory()

    def _random_hold_time(self, base: float) -> float:
        # Gaussian distribution for hold time, clipped to human-like range
        return max(0.025, min(random.gauss(base, base * 0.38), 0.19))

    def _random_between_keys(self, base: float) -> float:
        # Gaussian distribution for between-key interval, clipped
        return max(0.012, min(random.gauss(base, base * 0.52), 0.27))

    def simulate_keypress(self, char: str, hold_time: float) -> None:
        # Handles special keys and combos
        if char.lower() in SPECIAL_KEYS:
            key = SPECIAL_KEYS[char.lower()]
            if isinstance(key, list):
                for k in key:
                    pyautogui.keyDown(k)
                time.sleep(hold_time)
                for k in reversed(key):
                    pyautogui.keyUp(k)
            else:
                self._press_key_with_delay(key, hold_time)
                pyautogui.keyUp(key)
            return
        # Handles shift for uppercase and symbols
        needs_shift = False
        key = char

        if char in string.ascii_uppercase:
            needs_shift = True
            key = char.lower()
        shift_symbols = {
            '~': '`', '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
            '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
            '_': '-', '+': '=', '{': '[', '}': ']', '|': '\\',
            ':': ';', '"': "'", '<': ',', '>': '.', '?': '/'
        }
        if char in shift_symbols:
            needs_shift = True
            key = shift_symbols[char]

        if needs_shift:
            pyautogui.keyDown('shift')
        pyautogui.keyDown(key)
        time.sleep(hold_time)
        pyautogui.keyUp(key)
        if needs_shift:
            pyautogui.keyUp('shift')

    def update_progress(self, current: int, total: int) -> None:
        self.progress['value'] = (current / total) * 100
        self.update_idletasks()

    def simulate_typo_correction(self, char: str, base_interval: float) -> None:
        """Simulates a typo and its correction."""
        self.simulate_keypress(char, self._random_hold_time(base_interval))
        pyautogui.press('backspace')

    def simulate_mouse_action(self, action: str, x: int = None, y: int = None):
        if action == 'move' and x is not None and y is not None:
            pyautogui.moveTo(x, y)
        elif action == 'click':
            pyautogui.click()
        elif action == 'right_click':
            pyautogui.rightClick()
        elif action == 'double_click':
            pyautogui.doubleClick()
        # Add more as needed

    def open_emoji_picker(self):
        # Wait for coordinates from user to finish this method
        # Example: pyautogui.hotkey('win', '.')
        pass

if __name__ == "__main__":
    app = TypingBot()
    app.mainloop()

