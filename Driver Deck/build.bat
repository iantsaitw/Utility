@echo off
setlocal enabledelayedexpansion
echo [1/3] Killing old processes...
taskkill /F /IM "Driver Deck.exe" /T >nul 2>&1
taskkill /F /IM "DriverDeck_Pro.exe" /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/3] Cleaning folders...
if exist "build" rmdir /s /q "build"
timeout /t 1 /nobreak >nul

echo [3/3] Building EXE...
python -m PyInstaller --onefile --noconsole --clean --name "Driver Deck" --icon="icon.ico" --add-data "icon.ico;." "main.py"

if %errorlevel% equ 0 (
    echo Finalizing...
    
    :: Read base version from VERSION file
    set /p BASE_VER=<VERSION

    :: Generate version info for publish script (e.g., v1.0.0-20260206_1100)
    for /f "tokens=*" %%a in ('powershell -Command "Get-Date -Format 'yyyyMMdd_HHmm'"') do set TS=%%a
    echo v!BASE_VER!-!TS!> "dist\version.txt"

    if exist "build" rmdir /s /q "build"
    if exist "Driver Deck.spec" del "Driver Deck.spec"
    echo Done.
) else (
    echo Build Failed.
    exit /b 1
)
