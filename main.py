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

pyautogui.PAUSE = 0  # Remove default pause between actions for max speed

# (Keyboard neighbors and SPECIAL_KEYS remain unchanged)

class TypingBot(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Eyetype4You Bot")
        self.geometry("800x600")
        self.configure(bg="#2e2e2e")  # Dark background

        # Load memory
        self.word_memory: Dict = self.load_memory()

        # Bot image
        bot_img = Image.open("assets/eyes.png").resize((100, 100))
        self.bot_photo = ImageTk.PhotoImage(bot_img)
        tk.Label(self, image=self.bot_photo, bg="#2e2e2e").pack(pady=10)

        # Controls frame
        ctrl_frame = tk.Frame(self, bg="#2e2e2e")
        ctrl_frame.pack(fill=tk.X, padx=10, pady=5)

        self.start_btn = tk.Button(ctrl_frame, text="▶️ Start Typing", width=15, command=self.start_typing)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.close_btn = tk.Button(ctrl_frame, text="❌ Close", width=10, command=self.destroy)
        self.close_btn.pack(side=tk.LEFT, padx=5)

        # Speed slider
        slider_frame = tk.Frame(ctrl_frame, bg="#2e2e2e")
        slider_frame.pack(side=tk.RIGHT, padx=5)
        tk.Label(slider_frame, text="Speed", fg="white", bg="#2e2e2e").pack()
        self.speed_slider = ttk.Scale(slider_frame, from_=0.30, to=0.01, orient=tk.VERTICAL, length=150)
        self.speed_slider.set(0.12)  # Default medium speed
        self.speed_slider.pack()

        # Text widget with dark background
        self.text_widget = tk.Text(self, wrap=tk.WORD, font=("Courier", 12),
                                   bg="#1e1e1e", fg="white", insertbackground="white")
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, padx=10, pady=5)

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
            messagebox.showwarning("Warning", "Enter text first!")
            return

        delay = float(self.speed_slider.get())
        messagebox.showinfo("Ready", "Click into target window within 4 seconds.")
        threading.Thread(target=self.simulate_typing, args=(text, delay), daemon=True).start()

    def smart_type(self, ch: str, delay: float = 0.05):
        if emoji.is_emoji(ch):
            pyperclip.copy(ch)
            pyautogui.hotkey('ctrl', 'v')
        else:
            pyautogui.typewrite(ch)
        time.sleep(delay)

    def simulate_typing(self, text: str, delay: float) -> None:
        total = len(text)
        time.sleep(4)
        for i, ch in enumerate(text):
            self.smart_type(ch, delay)
            self.progress['value'] = (i + 1) / total * 100
            self.update_idletasks()
        self.progress['value'] = 0
        messagebox.showinfo("Done", "Typing complete!")
        self.save_memory()

if __name__ == "__main__":
    TypingBot().mainloop()

# Packaging instructions:
# 1. pip install pyinstaller
# 2. pyinstaller --onefile --windowed main.py
# This creates a user-friendly EXE without opening VSCode.
