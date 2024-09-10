import whisper
import torch
import time
import numpy as np

# Check for CUDA
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Current CUDA device: {torch.cuda.current_device()}")
    print(f"CUDA device name: {torch.cuda.get_device_name(0)}")

class Transcriber:
    def __init__(self):
        self.model = self.load_whisper_model()

    def load_whisper_model(self):
        if torch.cuda.is_available():
            print("Loading model into GPU...")
            model = whisper.load_model("medium.en", device="cuda")
        else:
            print("Loading model into CPU...")
            model = whisper.load_model("medium.en", device="cpu")
        return model

    def unload_model(self):
        print("Unloading Whisper model from GPU...")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def transcribe_audio(self, audio_data):
        print("Transcribing...")
        audio_data = np.squeeze(audio_data)

        try:
            start_time = time.time()
            result = self.model.transcribe(audio_data)
            transcription = result['text']
            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"[LOG] [{elapsed_time:.2f}s] {transcription}")

            return transcription
        except Exception as e:
            print(f"[ERR] [transcriber | transcribe_audio]: {e}")
            print(f"Error type: {type(e)}")
            print(f"Error args: {e.args}")
            return None