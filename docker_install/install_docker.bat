@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0.."

set ENV_FILE=.env

echo MediaSorter Docker setup
echo Enter absolute host paths for each directory (created if missing).
echo.

set DEFAULT_MEDIA_SRC=
set DEFAULT_PHOTO_DEST=
set DEFAULT_VIDEO_DEST=
set DEFAULT_INTERVAL=3600

if exist "%ENV_FILE%" (
    for /f "tokens=1,* delims==" %%A in ('findstr /b "MEDIA_SRC=" "%ENV_FILE%"') do set DEFAULT_MEDIA_SRC=%%B
    for /f "tokens=1,* delims==" %%A in ('findstr /b "PHOTO_DEST=" "%ENV_FILE%"') do set DEFAULT_PHOTO_DEST=%%B
    for /f "tokens=1,* delims==" %%A in ('findstr /b "VIDEO_DEST=" "%ENV_FILE%"') do set DEFAULT_VIDEO_DEST=%%B
    for /f "tokens=1,* delims==" %%A in ('findstr /b "RUN_INTERVAL_SECONDS=" "%ENV_FILE%"') do set DEFAULT_INTERVAL=%%B
)

set /p MEDIA_SRC=Media dump source folder [!DEFAULT_MEDIA_SRC!]:
if "!MEDIA_SRC!"=="" set MEDIA_SRC=!DEFAULT_MEDIA_SRC!
if "!MEDIA_SRC!"=="" (
    echo Error: MEDIA_SRC cannot be empty.
    exit /b 1
)
if not exist "!MEDIA_SRC!" mkdir "!MEDIA_SRC!"

set /p PHOTO_DEST=Photo destination folder [!DEFAULT_PHOTO_DEST!]:
if "!PHOTO_DEST!"=="" set PHOTO_DEST=!DEFAULT_PHOTO_DEST!
if "!PHOTO_DEST!"=="" (
    echo Error: PHOTO_DEST cannot be empty.
    exit /b 1
)
if not exist "!PHOTO_DEST!" mkdir "!PHOTO_DEST!"

set /p VIDEO_DEST=Video destination folder [!DEFAULT_VIDEO_DEST!]:
if "!VIDEO_DEST!"=="" set VIDEO_DEST=!DEFAULT_VIDEO_DEST!
if "!VIDEO_DEST!"=="" (
    echo Error: VIDEO_DEST cannot be empty.
    exit /b 1
)
if not exist "!VIDEO_DEST!" mkdir "!VIDEO_DEST!"

set /p RUN_INTERVAL_SECONDS=Run interval in seconds [!DEFAULT_INTERVAL!]:
if "!RUN_INTERVAL_SECONDS!"=="" set RUN_INTERVAL_SECONDS=!DEFAULT_INTERVAL!

set DEFAULT_PROOF_ENABLE=n
if exist "%ENV_FILE%" (
    findstr /b /c:"COMPOSE_PROFILES=proof" "%ENV_FILE%" >nul && set DEFAULT_PROOF_ENABLE=y
)
set /p PROOF_ENABLE=Enable proof generation service? [y/N] (default: %DEFAULT_PROOF_ENABLE%):
if "!PROOF_ENABLE!"=="" set PROOF_ENABLE=!DEFAULT_PROOF_ENABLE!

set COMPOSE_PROFILES=
set PROOF_INTERVAL_SECONDS=3600

if /i "!PROOF_ENABLE!"=="y" (
    set COMPOSE_PROFILES=proof
    set DEFAULT_PROOF_INTERVAL=3600
    if exist "%ENV_FILE%" (
        for /f "tokens=1,* delims==" %%A in ('findstr /b "PROOF_INTERVAL_SECONDS=" "%ENV_FILE%"') do set DEFAULT_PROOF_INTERVAL=%%B
    )
    set /p PROOF_INTERVAL_SECONDS=Proof interval in seconds [!DEFAULT_PROOF_INTERVAL!]:
    if "!PROOF_INTERVAL_SECONDS!"=="" set PROOF_INTERVAL_SECONDS=!DEFAULT_PROOF_INTERVAL!
)

(
    echo MEDIA_SRC=!MEDIA_SRC!
    echo PHOTO_DEST=!PHOTO_DEST!
    echo VIDEO_DEST=!VIDEO_DEST!
    echo RUN_INTERVAL_SECONDS=!RUN_INTERVAL_SECONDS!
    echo COMPOSE_PROFILES=!COMPOSE_PROFILES!
    echo PROOF_ENABLE=!PROOF_ENABLE!
    echo PROOF_INTERVAL_SECONDS=!PROOF_INTERVAL_SECONDS!
) > "%ENV_FILE%"

echo.
echo Wrote %ENV_FILE%
echo Building Docker image...
docker compose build

echo.
echo Done. Start the container with: docker compose up -d
