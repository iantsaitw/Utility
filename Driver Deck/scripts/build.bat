@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0.."
echo [1/3] Killing old processes...
taskkill /F /IM "Driver Deck.exe" /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/3] Cleaning folders...
if exist "build" rmdir /s /q "build"
timeout /t 1 /nobreak >nul

echo [3/3] Building EXE...
python -m PyInstaller --onefile --noconsole --clean --name "Driver Deck" --icon="icon.ico" --add-data "icon.ico;." "main.py"

if %errorlevel% equ 0 (
    echo Finalizing...
    if exist "build" rmdir /s /q "build"
    if exist "Driver Deck.spec" del "Driver Deck.spec"
    echo Done.
) else (
    echo Build Failed.
    exit /b 1
)