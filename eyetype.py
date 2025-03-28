import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import pyautogui, time

# Draggable window class
class DraggableWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # No border or title bar
        self.attributes('-topmost', True)  # Keep it on top always

        # Load and display your eyes image
        eye_img = Image.open("assets/eyes.png").resize((100, 100))
        self.eye_photo = ImageTk.PhotoImage(eye_img)
        eye_label = tk.Label(self, image=self.eye_photo)
        eye_label.pack()

        # Bind drag events to move the window around
        eye_label.bind('<ButtonPress-1>', self.start_move)
        eye_label.bind('<B1-Motion>', self.do_move)
        eye_label.bind('<Button-3>', self.show_menu)  # Right-click menu

        # Right-click popup menu
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
        text = simpledialog.askstring("Input", "Paste what should be typed:")
        if text:
            wpm = simpledialog.askinteger("Speed", "Words per minute (WPM):", minvalue=10, maxvalue=300, initialvalue=60)
            if wpm:
                delay = 60 / (wpm * 5)
                messagebox.showinfo("Ready", "Click into the target window within 3 seconds.")
                self.withdraw()  # Hide window while typing
                time.sleep(3)
                pyautogui.write(text, interval=delay)
                self.deiconify()  # Bring window back afterward

if __name__ == "__main__":
    app = DraggableWindow()
    app.mainloop()
