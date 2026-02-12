@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0.."
title Driver Deck - Light Build

echo [1/4] Killing old processes...
taskkill /F /IM "DriverDeck.exe" /T >nul 2>&1
taskkill /F /IM "Driver Deck.exe" /T >nul 2>&1
timeout /t 1 /nobreak >nul

echo [2/4] Detecting environment...
echo from config import APP_NAME; print(APP_NAME.replace(' ', '')) > .tmp.py
for /f "delims=" %%i in ('python .tmp.py') do set "A_NAME=%%i"
del .tmp.py

if "%A_NAME%"=="" set "A_NAME=DriverDeck"

echo [3/4] Cleaning old files...
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"
if exist "%A_NAME%.spec" del /f /q "%A_NAME%.spec"

echo [4/4] Building Single EXE...
python -m PyInstaller --noconfirm --onefile --windowed --noupx --name "%A_NAME%" ^
    --icon="icon.ico" ^
    --add-data "icon.ico;." ^
    --add-data "VERSION;." ^
    "main.py"

if %errorlevel% equ 0 (
    if exist "build" rd /s /q "build"
    if exist "%A_NAME%.spec" del /f /q "%A_NAME%.spec"
    echo Build Complete.
) else (
    echo ERROR: Build failed.
    pause
)