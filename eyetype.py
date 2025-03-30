import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from PIL import Image, ImageTk
import pyautogui, time

# 🧠 Multi-line input popup
class MultiLineInput(tk.Toplevel):
    def __init__(self, parent, title="Paste what should be typed:"):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x300")
        self.result = None

        self.text_widget = tk.Text(self, wrap=tk.WORD)
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        ok_btn = tk.Button(button_frame, text="OK", width=10, command=self.on_ok)
        ok_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(button_frame, text="Cancel", width=10, command=self.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

        self.text_widget.focus_set()
        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def on_ok(self):
        self.result = self.text_widget.get("1.0", tk.END).strip()
        self.destroy()


# 🕶️ Draggable floating eye window
class DraggableWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # No border or title bar
        self.attributes('-topmost', True)  # Always on top

        # Load eye image
        eye_img = Image.open("assets/eyes.png").resize((100, 100))
        self.eye_photo = ImageTk.PhotoImage(eye_img)
        eye_label = tk.Label(self, image=self.eye_photo)
        eye_label.pack()

        # Drag controls
        eye_label.bind('<ButtonPress-1>', self.start_move)
        eye_label.bind('<B1-Motion>', self.do_move)
        eye_label.bind('<Button-3>', self.show_menu)  # Right-click

        # Right-click menu
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Paste & Type", command=self.paste_and_type)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Exit", command=self.destroy)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        self.geometry(f'+{event.x_root - self.x}+{event.y_root - self.y}')

    def show_menu(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)

    def paste_and_type(self):
        text = MultiLineInput(self).result
        if text:
            wpm = simpledialog.askinteger("Speed", "Words per minute (WPM):", minvalue=10, maxvalue=300, initialvalue=60)
            if wpm:
                delay = 60 / (wpm * 5)
                messagebox.showinfo("Ready", "Click into the target window within 3 seconds.")
                self.withdraw()
                time.sleep(3)
                pyautogui.write(text, interval=delay)
                self.deiconify()

if __name__ == "__main__":
    app = DraggableWindow()
    app.mainloop()
