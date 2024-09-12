import os
import whisper
import torch
import time
import numpy as np
import warnings
from utils import send_notification

warnings.filterwarnings("ignore", category=FutureWarning)

# Check for CUDA
print(f"[CUDA] Torch {torch.__version__}")
if torch.cuda.is_available():
    print(f"[CUDA] Ver {torch.version.cuda} | Device {torch.cuda.current_device()} {torch.cuda.get_device_name(0)}")
else:
    print("[CUDA] Not Available")

class Transcriber:
    def __init__(self):
        self.model = self.load_whisper_model()

    def load_whisper_model(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        models_dir = os.path.join(os.getcwd(), "models")
        os.makedirs(models_dir, exist_ok=True)

        # Check if the model file exists before downloading
        model_file_path = os.path.join(models_dir, "medium.en.pt")  # The filename may vary depending on whisper's implementation

        if not os.path.exists(model_file_path):
            # Notify the user that the model is being downloaded
            send_notification(
                "Downloading Model",
                "Please wait around 5 min, you'll be notified once done."
            )
        
        # Load the model (downloads if not present)
        model = whisper.load_model("medium.en", device=device, download_root=models_dir)
        
        # If the model was downloaded, send another notification
        if not os.path.exists(model_file_path):
            send_notification(
                "Model Download Complete",
                "Model has been successfully downloaded."
            )

        print(f"[LOG] Model loaded into {'GPU' if device == 'cuda' else 'CPU'}")

        # Notify the user that the application is ready to record
        send_notification(
            "Ready to Record",
            "In a text input, hold ALT + X to start recording. Release to transcribe."
        )

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
