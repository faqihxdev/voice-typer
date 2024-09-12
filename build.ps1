# Remove the ./build directory if it exists
if (Test-Path "./build") {
    Remove-Item "./build" -Recurse -Force
    Write-Host "Removed ./build directory"
}

# Remove the ./dist directory if it exists
if (Test-Path "./dist") {
    Remove-Item "./dist" -Recurse -Force
    Write-Host "Removed ./dist directory"
}

# Remove the ./VoiceTyper.spec file if it exists
if (Test-Path "./VoiceTyper.spec") {
    Remove-Item "./VoiceTyper.spec" -Force
    Write-Host "Removed ./VoiceTyper.spec file"
}

# Run PyInstaller to build the executable
pyinstaller --onefile --icon="assets/app.ico" --name="VoiceTyper" --add-data "assets;assets" --add-data "env/Lib/site-packages/whisper/assets;whisper/assets" --noconsole main.py
