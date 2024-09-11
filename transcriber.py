import whisper
import torch
import time
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# Check for CUDA
print(f"[CUDA] PyTorch version: {torch.__version__}")
print(f"[CUDA] CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"[CUDA] Version: {torch.version.cuda}, Current device: {torch.cuda.current_device()}, Device name: {torch.cuda.get_device_name(0)}")

class Transcriber:
    def __init__(self):
        self.model = self.load_whisper_model()

    def load_whisper_model(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model("large-v2", device=device)
        print(f"[LOG] Model loaded into {device}")

        return model

    def unload_model(self):
        print("[LOG] Unloading model")
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def transcribe_audio(self, audio_data):
        print("[LOG] Transcribing")
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
            print(f"[ERROR] [transcriber | transcribe_audio]: {e}")
            print(f"[ERROR] Error type: {type(e)}")
            print(f"[ERROR] Error args: {e.args}")
            return None
