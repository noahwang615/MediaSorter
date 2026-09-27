@echo off
setlocal
cd /d "%~dp0.."

echo Triggering MediaSorter manual sort in Docker...
docker compose exec mediasorter python scripts/mediasorter.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo Note: Container might not be running. Attempting one-shot container run...
    docker compose run --rm --entrypoint python mediasorter scripts/mediasorter.py
)

echo.
echo Manual sort complete.
pause
