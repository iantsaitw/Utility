@echo off
setlocal enabledelayedexpansion

:: Auto-extract version from GEMINI.md (looks for something like v5.3.2)
for /f "tokens=*" %%a in ('powershell -Command "if ((Get-Content GEMINI.md -Raw) -match '(v\d+\.\d+\.\d+)') { $matches[1] } else { 'v1.0.0' }"') do set VERSION=%%a

set APP_NAME=Driver_Deck
set EXE_PATH=dist\Driver Deck.exe

echo [1/4] Detected Version: %VERSION%
echo [2/4] Running Build...
call build.bat

echo [3/4] Checking GitHub CLI...
where gh >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: GitHub CLI (gh) is not installed.
    exit /b 1
)

echo [4/4] Publishing %APP_NAME% %VERSION% to GitHub...
gh release create %APP_NAME%-%VERSION% "%EXE_PATH%" --title "%APP_NAME% %VERSION%" --notes-file GEMINI.md

if %ERRORLEVEL% equ 0 (
    echo SUCCESS: Published to GitHub!
) else (
    echo FAILED: Could not publish.
)

pause