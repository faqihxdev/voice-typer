import tkinter as tk
from tkinter import ttk
import whisper
import sounddevice as sd
import numpy as np
import keyboard
import pyautogui
import threading
import torch

# Define the app class
class STTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STT Floating Mic")
        self.root.geometry("150x150")  # Set window size
        self.root.overrideredirect(True)  # No window decorations
        self.root.attributes("-topmost", True)  # Keep the window always on top

        # Load Whisper model on app start (this will load into GPU)
        self.model = self.load_whisper_model()

        # Create a mic button (this will trigger the STT function later)
        self.mic_button = ttk.Button(root, text="🎤", command=self.start_stt)
        self.mic_button.pack(expand=True)

        # Make the window movable by dragging
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)

        # Create a close button (this will hide the window, but STT will still be active via hotkey)
        close_button = ttk.Button(root, text="Close", command=self.close_app)
        close_button.pack(side="bottom")

        # Detect hotkey activation
        keyboard.add_hotkey('ctrl+shift+h', self.start_stt)

        # Variable for window dragging
        self._offsetx = 0
        self._offsety = 0

        # Audio variables
        self.is_recording = False
        self.samplerate = 16000  # Whisper prefers 16kHz
        self.silence_threshold = 0.02  # Silence detection threshold
        self.silence_duration = 1.5  # Time of silence to stop recording

    def load_whisper_model(self):
        print("Loading Whisper model into GPU...")
        model = whisper.load_model("base")
        return model

    def unload_whisper_model(self):
        print("Unloading Whisper model from GPU...")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def start_stt(self):
        if not self.is_recording:
            self.is_recording = True
            threading.Thread(target=self.record_audio).start()

    def record_audio(self):
        print("Recording started...")

        audio_data = []
        silent_chunks = 0

        def callback(indata, frames, time, status):
            nonlocal silent_chunks
            volume_norm = np.linalg.norm(indata) * 10
            audio_data.append(indata.copy())

            # Check for silence
            if volume_norm < self.silence_threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            # Stop recording after certain silence duration
            if silent_chunks > int(self.silence_duration * self.samplerate / frames):
                print("Silence detected, stopping recording.")
                raise sd.CallbackStop()

        with sd.InputStream(callback=callback, channels=1, samplerate=self.samplerate, dtype='float32'):
            sd.sleep(10000)  # Run the stream for 10 seconds max or until silence is detected

        self.is_recording = False

        audio_data = np.concatenate(audio_data, axis=0)
        threading.Thread(target=self.transcribe_audio, args=(audio_data,)).start()

    def transcribe_audio(self, audio_data):
        print("Transcribing...")

        audio_data = np.squeeze(audio_data)
        audio_data = whisper.pad_or_trim(audio_data)
        mel = whisper.log_mel_spectrogram(audio_data)

        result = self.model.transcribe(mel)
        transcription = result['text']
        print(f"Transcription: {transcription}")

        self.output_to_active_window(transcription)

    def output_to_active_window(self, text):
        pyautogui.write(text, interval=0.05)
        print(f"Typed: {text}")

    def start_move(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def on_move(self, event):
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        self.root.geometry(f'+{x}+{y}')

    def close_app(self):
        self.unload_whisper_model()  # Unload the model when the app is closed
        self.root.quit()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = STTApp(root)
    root.mainloop()
