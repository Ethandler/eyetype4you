import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyautogui
import threading
import time
import json
from typing import Dict, List
import emoji  # pip install emoji
import pyperclip
import random

pyautogui.PAUSE = 0  # Remove default pause between actions for max speed

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

class TypingBot(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Eyetype4You Bot")
        self.geometry("800x600")
        self.configure(bg="#2e2e2e")  

        # Load memory
        self.word_memory: Dict = self.load_memory()

        # Bot image
        bot_img = Image.open("assets/eyes.png").resize((175, 175))
        self.bot_photo = ImageTk.PhotoImage(bot_img)
        tk.Label(self, image=self.bot_photo, bg="#2e2e2e").pack(pady=10)

        # Controls frame
        ctrl_frame = tk.Frame(self, bg="#2e2e2e")
        ctrl_frame.pack(fill=tk.X, padx=10, pady=5)

        # Accent color for buttons
        self.btn_color = "#0099FF"
        self.btn_active = "#33BFFF"
        self.btn_fg = "#fff"
        self.btn_font = ("Segoe UI", 14, "bold")
        self.btn_size = {"width": 14, "height": 2}  # ~120x40 px

        self.start_btn = tk.Button(ctrl_frame, text="▶️ Start Typing", command=self.start_typing,
                                  bg=self.btn_color, activebackground=self.btn_active, fg=self.btn_fg,
                                  font=self.btn_font, **self.btn_size, bd=0, relief=tk.FLAT, cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self._add_flash_effect(self.start_btn)

        self.close_btn = tk.Button(ctrl_frame, text="❌ Close", command=self.destroy,
                                  bg=self.btn_color, activebackground=self.btn_active, fg=self.btn_fg,
                                  font=self.btn_font, **self.btn_size, bd=0, relief=tk.FLAT, cursor="hand2")
        self.close_btn.pack(side=tk.LEFT, padx=5)
        self._add_flash_effect(self.close_btn)

        # Speed slider and progress circle at the top right
        speed_frame = tk.Frame(ctrl_frame, bg="#2e2e2e")
        speed_frame.pack(side=tk.RIGHT, padx=5)
        tk.Label(speed_frame, text="Speed:", fg="#e0e0e0", bg="#2e2e2e", font=("Segoe UI", 14, "bold")).pack()
        self.speed_scale = tk.Scale(speed_frame, from_=0.05, to=0.3, resolution=0.005, orient="vertical",
                                   bg="#2e2e2e", fg="#e0e0e0", troughcolor="#444", font=("Segoe UI", 12),
                                   highlightthickness=0, length=140)
        self.speed_scale.set(0.12)
        self.speed_scale.pack()
        # Progress circle next to speed slider
        self.progress_canvas = tk.Canvas(speed_frame, width=60, height=60, bg="#2e2e2e", highlightthickness=0)
        self.progress_canvas.pack(pady=5)
        # Draw faint background circle
        self.progress_bg = self.progress_canvas.create_arc(5, 5, 55, 55, start=0, extent=359.9, style=tk.ARC, width=7, outline="#444")
        self.progress_arc = self.progress_canvas.create_arc(5, 5, 55, 55, start=90, extent=0, style=tk.ARC, width=7, outline="#0099FF")

        # Menubar & Settings
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="⚙️ Settings", menu=settings_menu)
        settings_menu.add_command(label="Preferences…", command=self.open_settings)

        # Adjustable parameters
        self.error_rate = 1/83
        self.punc_pause_prob = 0.18
        self.space_pause_prob = 0.08
        self.thinking_pause_prob = 0.025
        self.dark_mode = True  # Default to dark mode

        # Text widget with high-contrast dark mode
        self.text_widget = tk.Text(self, wrap=tk.WORD, font=("Consolas", 18),
                                   bg="#2e2e2e", fg="#e0e0e0", insertbackground="#e0e0e0")
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def load_memory(self) -> Dict:
        try:
            with open("word_memory.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_memory(self) -> None:
        with open("word_memory.json", "w", encoding="utf-8") as f:
            json.dump(self.word_memory, f, indent=2)

    def open_settings(self):
        win = tk.Toplevel(self)
        win.title("Preferences")
        win.geometry("300x200")
        win.configure(bg="#2e2e2e")
        label = tk.Label(win, text="Error rate (%)", bg="#2e2e2e", fg="#e0e0e0", font=("Segoe UI", 14, "bold"))
        label.pack(pady=(10,0))
        err_scale = tk.Scale(win, from_=0, to=20, orient="horizontal",
                            command=lambda v: setattr(self, "error_rate", float(v)/100),
                            bg="#2e2e2e", fg="#e0e0e0", troughcolor="#444", font=("Segoe UI", 12),
                            highlightthickness=0, length=200)
        err_scale.set(self.error_rate * 100)
        err_scale.pack(fill="x", padx=20)
        dm_var = tk.BooleanVar(value=self.dark_mode)
        def toggle_dark():
            self.dark_mode = dm_var.get()
            bg, fg = ("#2e2e2e", "white") if self.dark_mode else ("#e0e0e0", "#222")
            self.text_widget.config(bg=bg, fg=fg, insertbackground=fg)
        chk = tk.Checkbutton(win, text="Color mode editor: Light or Dark?", variable=dm_var, command=toggle_dark,
                            bg="#2e2e2e", fg="#e0e0e0", selectcolor="#0099FF", font=("Segoe UI", 12))
        chk.pack(pady=10)
        close_btn = tk.Button(win, text="Close", command=win.destroy,
                            bg="#0099FF", activebackground="#33BFFF", fg="#fff",
                            font=("Segoe UI", 14, "bold"), width=14, height=2, bd=0, relief=tk.FLAT, cursor="hand2")
        close_btn.pack(pady=(20,0))
        self._add_flash_effect(close_btn)

    def show_popup(self, title, message, kind="info"):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.configure(bg="#222")
        popup.geometry("420x180")
        popup.grab_set()
        popup.transient(self)
        tk.Label(popup, text=title, bg="#222", fg="#0099FF", font=("Segoe UI", 20, "bold")).pack(pady=(18, 6))
        tk.Label(popup, text=message, bg="#222", fg="#e0e0e0", font=("Segoe UI", 16), wraplength=380, justify="center").pack(pady=(0, 18))
        btn_color = "#0099FF" if kind == "info" else "#FF8800"
        btn = tk.Button(popup, text="OK", command=popup.destroy, bg=btn_color, fg="#fff", font=("Segoe UI", 16, "bold"), width=12, height=2, bd=0, relief=tk.FLAT, activebackground="#33BFFF", cursor="hand2")
        btn.pack()
        self._add_flash_effect(btn)
        popup.wait_window()

    def start_typing(self) -> None:
        text = self.text_widget.get("1.0", tk.END).strip()
        if not text:
            self.show_popup("Warning", "Enter text first!", kind="warn")
            return
        delay = self.speed_scale.get()
        self.show_popup("Ready", "Click into target window within 4 seconds.")
        threading.Thread(target=self._delayed_typing, args=(text, delay), daemon=True).start()

    def _delayed_typing(self, text: str, delay: float):
        time.sleep(4)
        self.simulate_typing(text, delay)

    def smart_type(self, ch: str, delay: float = 0.05):
        if emoji.is_emoji(ch):
            pyperclip.copy(ch)
            pyautogui.hotkey('ctrl', 'v')
        else:
            pyautogui.typewrite(ch)
        time.sleep(delay)

    def simulate_typing(self, text: str, delay: float) -> None:
        total = len(text)
        i = 0
        while i < total:
            ch = text[i]
            # typo?
            if ch.isalnum() and random.random() < self.error_rate:
                if (nb := keyboard_neighbors.get(ch, [])):
                    typo = random.choice(nb)
                    pyautogui.typewrite(typo)
                    time.sleep(delay)
                    pyautogui.press("backspace")
                    time.sleep(delay)
            # type or emoji-paste
            if emoji.is_emoji(ch):
                pyperclip.copy(ch)
                pyautogui.hotkey("ctrl", "v")
            else:
                pyautogui.typewrite(ch)
            time.sleep(delay)
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
            self.update_progress_circle((i / total) * 100)
        self.update_progress_circle(0)
        self.show_popup("Done", "Typing complete!")
        self.save_memory()

    def update_progress_circle(self, percent):
        # percent: 0-100
        extent = percent * 3.6  # 360 degrees max
        self.progress_canvas.itemconfig(self.progress_arc, extent=-extent)  # negative for clockwise
        self.progress_canvas.update_idletasks()

    def _add_flash_effect(self, btn):
        def on_press(event):
            btn.config(bg=self.btn_active)
        def on_release(event):
            btn.config(bg=self.btn_color)
        btn.bind('<ButtonPress-1>', on_press)
        btn.bind('<ButtonRelease-1>', on_release)

if __name__ == "__main__":
    TypingBot().mainloop()

# Packaging instructions:
# 1. pip install pyinstaller
# 2. pyinstaller --onefile --windowed main.py
# This creates a user-friendly EXE without opening VSCode.
