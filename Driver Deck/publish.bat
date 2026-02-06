@echo off
setlocal enabledelayedexpansion

:: Settings
set VERSION=v5.3.2
set APP_NAME=Driver_Deck
set EXE_PATH=dist\Driver Deck.exe

echo [1/3] Running Build...
call build.bat

echo [2/3] Checking GitHub CLI...
where gh >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: GitHub CLI (gh) is not installed. Please install it to use this script.
    exit /b 1
)

echo [3/3] Publishing to GitHub...
gh release create %APP_NAME%-%VERSION% "%EXE_PATH%" --title "%APP_NAME% %VERSION%" --notes "Automated release for %APP_NAME% %VERSION%"

if %ERRORLEVEL% equ 0 (
    echo SUCCESS: %APP_NAME% %VERSION% has been published!
) else (
    echo FAILED: Could not publish release. (Maybe the tag already exists?)
)

pause
