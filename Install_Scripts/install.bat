@echo off
REM install.bat - setup script for MediaSort project on Windows

echo Checking for Python installation...

python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.6 or newer from https://python.org/downloads/ and ensure 'python' command is available in your PATH.
    pause
    exit /b 1
)

echo Python found:
python --version

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing required Python packages from requirements.txt...
pip install -r requirements.txt

echo Checking for ffprobe (FFmpeg tool) installation...

where ffprobe >nul 2>&1
IF ERRORLEVEL 1 (
    echo ffprobe not found in PATH.
    echo Please install FFmpeg and make sure ffprobe is added to your system PATH.
    echo Download from: https://ffmpeg.org/download.html
    pause
    exit /b 1
)

echo All dependencies installed successfully!
echo You are ready to run the script.
pause
