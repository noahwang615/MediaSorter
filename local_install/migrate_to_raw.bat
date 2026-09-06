@echo off
setlocal

set "PROJECT_ROOT=%~dp0.."
cd /d "%PROJECT_ROOT%"

python scripts\migrate_to_raw.py %*
if errorlevel 1 exit /b %errorlevel%