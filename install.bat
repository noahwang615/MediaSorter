@echo off
setlocal

set "SCRIPT_DIR=%~dp0"

if not exist "%SCRIPT_DIR%data\mediadump" mkdir "%SCRIPT_DIR%data\mediadump"
if not exist "%SCRIPT_DIR%data\photos" mkdir "%SCRIPT_DIR%data\photos"
if not exist "%SCRIPT_DIR%data\videos" mkdir "%SCRIPT_DIR%data\videos"

echo MediaSorter installer
echo 1^) Local install
echo 2^) Docker install
set /p "CHOICE=Choose an option [1/2]: "

if "%CHOICE%"=="1" (
    call "%SCRIPT_DIR%local_install\install_local.bat"
    exit /b %ERRORLEVEL%
)
if "%CHOICE%"=="2" (
    call "%SCRIPT_DIR%docker_install\install_docker.bat"
    exit /b %ERRORLEVEL%
)

echo Invalid choice.
exit /b 1
