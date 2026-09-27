@echo off
setlocal
cd /d "%~dp0.."

echo Triggering MediaSorter manual proof generation in Docker...
docker compose run --rm --entrypoint python mediasorter scripts/make_proofs.py

echo.
echo Manual proof generation complete.
pause
