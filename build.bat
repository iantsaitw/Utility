@echo off
setlocal enabledelayedexpansion

:: ================= 設定區 =================
:: 這裡設定產生的 EXE 檔名 (建議跟 Python 裡的名稱一樣)
set "APP_NAME=Driver Deck"
set "MAIN_FILE=main.py"
set "ICON_FILE=icon.ico"
:: ==========================================

echo [Init] Killing old process...
taskkill /F /IM "%APP_NAME%.exe" /T >nul 2>&1

where python >nul 2>&1
if %errorlevel% equ 0 ( set PY_CMD=python ) else ( set PY_CMD=py )

if not exist "%ICON_FILE%" (
    echo [Error] icon.ico not found! Please place an icon file in this folder.
    pause
    exit /b
)

echo [Build] Building %APP_NAME%...
%PY_CMD% -m PyInstaller --onefile --noconsole --clean --name "%APP_NAME%" --icon="%ICON_FILE%" --add-data "%ICON_FILE%;." "%MAIN_FILE%"

if %errorlevel% equ 0 (
    echo [Success] Done.
    if exist "%APP_NAME%.spec" del "%APP_NAME%.spec"
    if exist "build" rmdir /s /q "build"
    explorer dist
) else (
    echo [Error] Build Failed.
)
pause