import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pyautogui, threading, random, time

class TypingBot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Eyetype4You Bot")
        self.geometry("500x600")
        self.configure(bg="#2B2B2B")

        # Transparent bot image
        bot_img = Image.open("assets/eyes.png").resize((150, 150))
        self.bot_photo = ImageTk.PhotoImage(bot_img)
        tk.Label(self, image=self.bot_photo, bg="#2B2B2B").pack(pady=10)

        # Main menu buttons
        menu_frame = tk.Frame(self, bg="#2B2B2B")
        menu_frame.pack(pady=5)

        self.start_btn = tk.Button(menu_frame, text="▶️ Start Typing", width=20, command=self.start_typing)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.close_btn = tk.Button(menu_frame, text="❌ Close", width=10, command=self.destroy)
        self.close_btn.pack(side=tk.LEFT, padx=5)

        # Typing text box
        self.text_widget = tk.Text(self, wrap=tk.WORD, font=("Courier", 12))
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, padx=10, pady=5)

        # Typing speed slider
        slider_frame = tk.Frame(self, bg="#2B2B2B")
        slider_frame.pack(pady=5)
        tk.Label(slider_frame, text="Typing Speed (WPM):", fg="white", bg="#2B2B2B").pack(side=tk.LEFT, padx=5)
        self.wpm_slider = tk.Scale(slider_frame, from_=10, to=369, orient="horizontal", bg="#2B2B2B", fg="white", highlightthickness=0)
        self.wpm_slider.set(120)
        self.wpm_slider.pack(side=tk.LEFT)

    def start_typing(self):
        text = self.text_widget.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "You need to enter some text first!")
            return

        wpm = self.wpm_slider.get()
        delay = 60 / (wpm * 5)

        messagebox.showinfo("Ready", "Click into the target window within 5 seconds.")
        time.sleep(5)

        typing_thread = threading.Thread(target=self.simulate_typing, args=(text, delay))
        typing_thread.start()

    def simulate_typing(self, text, delay):
        total_chars = len(text)
        chars_typed = 0

        for char in text:
            if ord(char) > 126:
                char = '-' if char == '—' else ' '

            if random.random() < 0.03 and char.isalpha():
                typo_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                pyautogui.write(typo_char, interval=delay / 2)
                pyautogui.press('backspace')

            pyautogui.write(char, interval=delay / 2)
            chars_typed += 1

            self.update_progress(chars_typed, total_chars)

        self.progress['value'] = 0
        messagebox.showinfo("Done", "Typing complete!")

    def update_progress(self, current, total):
        percent = (current / total) * 100
        self.progress['value'] = percent
        self.update_idletasks()

if __name__ == "__main__":
    app = TypingBot()
    app.mainloop()
