@echo off
setlocal enabledelayedexpansion
title ETL Weaver - Light Build

echo [1/4] Killing existing processes...
taskkill /F /IM "ETL Weaver.exe" /T >nul 2>&1
timeout /t 1 /nobreak >nul

echo [2/4] Detecting environment...
echo import tkinterdnd2, os; print(os.path.dirname(tkinterdnd2.__file__)) > .tmp.py
for /f "delims=" %%i in ('python .tmp.py') do set "TK_PATH=%%i"
echo from config import APP_NAME; print(APP_NAME) > .tmp2.py
for /f "delims=" %%i in ('python .tmp2.py') do set "A_NAME=%%i"
del .tmp.py .tmp2.py

if "%A_NAME%"=="" set "A_NAME=ETL Weaver"

echo [3/4] Cleaning old files...
if exist "build" rd /s /q "build"
if exist "dist" rd /s /q "dist"
if exist "%A_NAME%.spec" del "%A_NAME%.spec"

echo [4/4] Building Single EXE...
python -m PyInstaller --noconfirm --onefile --windowed --noupx --name "%A_NAME%" ^
    --icon="icon.ico" ^
    --add-data "icon.ico;." ^
    --add-data "trace_tools;trace_tools" ^
    --add-data "%TK_PATH%;tkinterdnd2" ^
    --hidden-import "tkinterdnd2" ^
    -p . main.py

if errorlevel 0 (
    if exist "build" rd /s /q "build"
    if exist "%A_NAME%.spec" del "%A_NAME%.spec"
    echo Build Complete.
) else (
    echo ERROR: Build failed.
    pause
)