import sounddevice as sd
import numpy as np
import threading

class AudioRecorder:
    def __init__(self, transcribe_callback):
        self.is_recording = False
        self.samplerate = 16000
        self.chunk_size = 1024
        self.transcribe_callback = transcribe_callback

    def start_recording(self):
        if not self.is_recording:
            print("Starting recording...")
            self.is_recording = True
            threading.Thread(target=self._record_audio).start()

    def stop_recording(self):
        if self.is_recording:
            print("Stopping recording...")
            self.is_recording = False

    def _record_audio(self):
        print("Recording started...")
        audio_data = []
        np_audio_data = np.array([])

        def callback(indata, frames, time, status):
            nonlocal np_audio_data, audio_data

            if not self.is_recording:
                raise sd.CallbackStop()
            
            audio_data.append(indata.copy())
            
            print(f"T: {len(audio_data) * frames / self.samplerate}")

            if len(audio_data) * frames / self.samplerate > 3:
                np_audio_data = np.concatenate(audio_data, axis=0)
                audio_data = []
                threading.Thread(target=self.transcribe_callback, args=(np_audio_data,)).start()

        with sd.InputStream(callback=callback, channels=1, samplerate=self.samplerate, blocksize=self.chunk_size, dtype='float32'):
            while self.is_recording:
                sd.sleep(100)