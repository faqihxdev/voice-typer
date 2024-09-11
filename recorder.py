import sounddevice as sd
import numpy as np
import threading
import time

class AudioRecorder:
    def __init__(self, transcribe_callback):
        self.is_recording = False
        self.samplerate = 16000
        self.chunk_size = 1024
        self.transcribe_callback = transcribe_callback
        self.audio_data = []

    def record(self):
        print("[LOG] Recording Started")
        self.audio_data = []

        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.audio_data.append(indata.copy())

        with sd.InputStream(callback=callback, channels=1, samplerate=self.samplerate, blocksize=self.chunk_size):
            while self.is_recording:
                sd.sleep(100)

    def start_recording(self):
        if not self.is_recording:
            print("[LOG] Starting Recording")
            self.is_recording = True
            threading.Thread(target=self.record).start()

    def stop_recording(self):
        if self.is_recording:
            print("[LOG] Stopping Recording")
            self.is_recording = False
            np_audio_data = np.concatenate(self.audio_data, axis=0)
            threading.Thread(target=self.transcribe_callback, args=(np_audio_data,)).start()
