# Voice Typer

A locally run Speech-To-Text voice typer enabled with hotkeys and floating interface for effortless voice typing, powered by the publicly available OpenAI Whisper model.

## 📸 Screenshot

<img src=".github/demo.png" alt="Screenshot" style="width: 100%; display: block; margin: 0 auto;">

## ❓ Why?

I created this because I couldn't find a free solution that uses a locally run Whisper model (or any speech-to-text model) with a hotkey activation for easy interaction. Even if a solution exists, this was a cool project to work on. A hotkey, like holding Alt+X to record and release to transcribe, is an efficient way to control a speech-to-text model! It can type on any input, so as long as your cursor can access it, you can use VoiceTyper on it. With all the typing we do for LLMs, sometimes we want to explain things in detail, but typing it all out can feel long and tedious. Using voice is faster and more interactive. Now, the next few projects will be built even faster. Let's gooo!

P.S. I've been using it ALOT, maybe too much, hopefully I still remember how to type with a keyboard.

## ✨ Features

- Floating, draggable, minimal mic/close app interface
- Speech-to-text transcription using OpenAI's Whisper model
- Automatic output of transcribed text to the active window
- Global hotkey hold (Alt+X) to start/stop recording
- Press the "X" button on the floating window to quit

## 💻 Requirements

- Microphone
- Windows 10 or later
- At least 4GB of VRAM (for GPU acceleration)
- Note: Hardware will determine the transcription performance.

## 📥 Installation for Users

* I've only tested it on Windows 11. For others, you're free to try if it works.
* Since the exe file is > 2GB, github's release limit, it's split into 2.
* (1) VoiceTyper.7z.001, and (2) VoiceTyper.7z.002

1. Go to [Releases Page](https://github.com/faqihxdev/Voice-Typer/releases) & Download all files.
2. Install 7-Zip from [www.7-zip.org](http://www.7-zip.org) if you haven't already.
3. Right-click on VoiceTyper.7z.001 > Select 7-Zip > Extract Here.
4. Run the VoiceTyper.exe file
5. Wait startup & model download, there'll be notifications
   1. Startup (~5-30s)
   2. Model Download (For first time users) (~1m-5m)
   3. Waiting times will vary between hardwares & internet connections
6. In any text field, hold Alt+X to start/stop recording
7. Press the "X" button on the floating window to quit

## 👨‍💻 For Developers

### 🛠️ Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv env`
3. Activate the virtual environment:
   - Windows: `.\env\Scripts\activate`
   - Unix/MacOS: `source env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

### 🚀 Running the Application

- Use `.\run.sh` to run the application in development mode

### 📦 Building the Executable

1. Ensure you have PyInstaller installed: `pip install pyinstaller`
2. Run the build script: `.\build.sh`
3. The executable will be created in the `dist` folder

### 📁 Project Structure

- `main.py`: Entry point of the application
- `ui.py`: User interface implementation
- `recorder.py`: Audio recording functionality
- `transcriber.py`: Speech-to-text transcription using Whisper
- `typer.py`: Handles text output to the active window
- `utils.py`: Utility functions

## ⚠️ Issues

* The hot keys (ALT+X), which is the ideal way to use it works. However, clicking on the record button removes focus from the input the cursor was at. This causes the program to enter characters into the unknown. For now, it's just used as a recording indicator.

## 👨‍💻 Author

Made with ❤️ by [@faqihxdev](https://github.com/faqihxdev)
