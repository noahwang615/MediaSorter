@echo off
REM install_local.bat - setup script for MediaSort project on Windows

SET SCRIPT_DIR=%~dp0
SET PROJECT_BASE=%SCRIPT_DIR%..

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
pip install -r "%PROJECT_BASE%\scripts\requirements.txt"

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
set ENV_FILE=%PROJECT_BASE%\.env
set DEFAULT_MEDIA_SRC=%PROJECT_BASE%\data\mediadump
set DEFAULT_PHOTO_DEST=%PROJECT_BASE%\data\photos
set DEFAULT_VIDEO_DEST=%PROJECT_BASE%\data\videos

if exist "%ENV_FILE%" (
    for /f "tokens=1,* delims==" %%A in ('findstr /b "MEDIA_SRC=" "%ENV_FILE%"') do set DEFAULT_MEDIA_SRC=%%B
    for /f "tokens=1,* delims==" %%A in ('findstr /b "PHOTO_DEST=" "%ENV_FILE%"') do set DEFAULT_PHOTO_DEST=%%B
    for /f "tokens=1,* delims==" %%A in ('findstr /b "VIDEO_DEST=" "%ENV_FILE%"') do set DEFAULT_VIDEO_DEST=%%B
)

echo.
echo Configuring MediaSorter paths (used by mediasorter.py via .env)
set /p MEDIA_SRC=Media dump source folder [!DEFAULT_MEDIA_SRC!]:
if "!MEDIA_SRC!"=="" set MEDIA_SRC=!DEFAULT_MEDIA_SRC!
if "!MEDIA_SRC!"=="" exit /b 1
if not exist "!MEDIA_SRC!" mkdir "!MEDIA_SRC!"

set /p PHOTO_DEST=Photo destination folder [!DEFAULT_PHOTO_DEST!]:
if "!PHOTO_DEST!"=="" set PHOTO_DEST=!DEFAULT_PHOTO_DEST!
if "!PHOTO_DEST!"=="" exit /b 1
if not exist "!PHOTO_DEST!" mkdir "!PHOTO_DEST!"

set /p VIDEO_DEST=Video destination folder [!DEFAULT_VIDEO_DEST!]:
if "!VIDEO_DEST!"=="" set VIDEO_DEST=!DEFAULT_VIDEO_DEST!
if "!VIDEO_DEST!"=="" exit /b 1
if not exist "!VIDEO_DEST!" mkdir "!VIDEO_DEST!"

(
    echo MEDIA_SRC=!MEDIA_SRC!
    echo PHOTO_DEST=!PHOTO_DEST!
    echo VIDEO_DEST=!VIDEO_DEST!
    echo RUN_INTERVAL_SECONDS=3600
) > "%ENV_FILE%"

echo Wrote %ENV_FILE%
echo You are ready to run the script.
pause
