#!/bin/bash

# Remove the ./build directory if it exists
if [ -d "./build" ]; then
    rm -rf "./build"
    echo "Removed ./build directory"
fi

# Remove the ./dist directory if it exists
if [ -d "./dist" ]; then
    rm -rf "./dist"
    echo "Removed ./dist directory"
fi

# Remove the ./VoiceTyper.spec file if it exists
if [ -f "./VoiceTyper.spec" ]; then
    rm "./VoiceTyper.spec"
    echo "Removed ./VoiceTyper.spec file"
fi

# Run PyInstaller to build the executable
pyinstaller --onefile --icon="assets/app.ico" --name="VoiceTyper" \
    --add-data "assets:assets" \
    --add-data "env/Lib/site-packages/whisper/assets:whisper/assets" \
    --noconsole main.py