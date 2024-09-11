import tkinter as tk
from ui import STTUI
from recorder import AudioRecorder
from transcriber import Transcriber
from typer import OutputHandler

class STTApp:
    def __init__(self, root):
        self.ui = STTUI(root, self.toggle_stt, self.close_app)
        self.transcriber = Transcriber()
        self.output_handler = OutputHandler()
        self.audio_recorder = AudioRecorder(self.transcribe_and_output)

    def toggle_stt(self):
        if not self.audio_recorder.is_recording:
            self.start_stt()
        else:
            self.stop_stt()

    def start_stt(self):
        if not self.audio_recorder.is_recording:
            self.ui.update_status("recording")
            self.audio_recorder.start_recording()

    def stop_stt(self):
        if self.audio_recorder.is_recording:
            self.ui.update_status("ready")
            self.audio_recorder.stop_recording()

    def transcribe_and_output(self, audio_data):
        self.ui.update_status("transcribing")
        transcription = self.transcriber.transcribe_audio(audio_data)
        if transcription:
            self.output_handler.output_to_active_window(transcription)
        self.ui.update_status("recording")

    def close_app(self):
        self.transcriber.unload_model()
        self.ui.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = STTApp(root)
    root.mainloop()