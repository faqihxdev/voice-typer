from PIL import Image, ImageTk
import tkinter as tk
import keyboard

class STTUI:
    def __init__(self, root, toggle_stt_callback, close_app_callback):
        self.root = root
        self.root.title("STT Floating Mic")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.wm_attributes("-transparent", "black")

        # Load and resize images
        self.window_img = ImageTk.PhotoImage(Image.open("./assets/window.png"))

        # Resize button images to fit the button dimensions (36x36)
        button_img_size = (36, 36)
        self.button_grey_img = ImageTk.PhotoImage(Image.open("./assets/button-grey.png").resize(button_img_size, Image.Resampling.LANCZOS))
        self.button_blue_img = ImageTk.PhotoImage(Image.open("./assets/button-blue.png").resize(button_img_size, Image.Resampling.LANCZOS))

        # Resize mic and settings icons to fit within buttons (e.g., 20x20 or adjust accordingly)
        icon_size = (20, 20)
        self.mic_icon = ImageTk.PhotoImage(Image.open("./assets/mic.png").resize(icon_size, Image.Resampling.LANCZOS))
        self.settings_icon = ImageTk.PhotoImage(Image.open("./assets/settings.png").resize(icon_size, Image.Resampling.LANCZOS))

        # Adjust window size
        window_width = 56  # 36px button + 10px padding on each side
        window_height = 102  # 36px * 2 buttons + 10px padding top/bottom + 10px between buttons
        self.root.geometry(f"{window_width}x{window_height}")

        # Create window background
        self.background = tk.Label(root, bd=0, image=self.window_img, width=window_width, height=window_height, background='black')
        self.background.pack(fill="both", expand=True)

        # Mic button
        self.mic_button = tk.Button(
            self.background,
            image=self.button_grey_img,
            bd=0,
            background='#0E0E0E',
            highlightthickness=0,
            width=36,
            height=36,
            command=toggle_stt_callback
        )
        
        self.mic_button.place(x=10, y=10)
        
        self.mic_icon_label = tk.Button(
            self.mic_button,
            image=self.mic_icon,
            bd=0,
            bg='#2c2c2c',
            command=toggle_stt_callback
        )
        
        self.mic_icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Settings button
        self.settings_button = tk.Button(
            self.background,
            image=self.button_grey_img,
            bd=0,
            background='#0E0E0E',
            highlightthickness=0,
            width=36,
            height=36,
            command=close_app_callback
        )
        
        self.settings_button.place(x=10, y=56)  # 10px from bottom (102 - 36 - 10)
        
        self.settings_icon_label = tk.Button(
            self.settings_button,
            image=self.settings_icon,
            bd=0,
            bg='#2c2c2c',
            command=close_app_callback
        )
        
        self.settings_icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Bind mouse events for window dragging
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)

        # Add hotkey
        keyboard.add_hotkey('ctrl+shift+7', toggle_stt_callback)

        self._offsetx = 0
        self._offsety = 0

    def update_status(self, status):
        if status == "ready":
            self.mic_button.config(image=self.button_grey_img)
            self.mic_icon_label.config(bg='#2c2c2c')
        elif status == "recording":
            self.mic_button.config(image=self.button_blue_img)
            self.mic_icon_label.config(bg='#007ACC')
        self.root.update()

    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def on_move(self, event):
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        self.root.geometry(f'+{x}+{y}')
