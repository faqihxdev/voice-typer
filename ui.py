import tkinter as tk
from tkinter import ttk
import keyboard

class STTUI:
    def __init__(self, root, toggle_stt_callback, close_app_callback):
        self.root = root
        self.root.title("STT Floating Mic")
        self.root.geometry("150x150")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        self.mic_button = ttk.Button(root, text="Record", command=toggle_stt_callback)
        self.mic_button.pack(expand=True)

        self.status_indicator = ttk.Label(root, text="Ready", background="gray")
        self.status_indicator.pack(side="bottom", fill="x")

        close_button = ttk.Button(root, text="Close", command=close_app_callback)
        close_button.pack(side="bottom")

        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)

        keyboard.add_hotkey('ctrl+shift+7', toggle_stt_callback)

        self._offsetx = 0
        self._offsety = 0

    def update_status(self, status):
        if status == "ready":
            self.status_indicator.config(text="Ready", background="gray")
        elif status == "recording":
            self.status_indicator.config(text="Recording", background="red")
        elif status == "transcribing":
            self.status_indicator.config(text="Transcribing", background="yellow")
        self.root.update()

    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def on_move(self, event):
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        self.root.geometry(f'+{x}+{y}')