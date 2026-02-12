@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0.."
title ETL Weaver - Master Release (Safety First)

echo [1/6] Calculating next version...
if not exist "VERSION" echo 1.0.0> VERSION
set /p NEW_VER=<VERSION
set TAG_PREFIX=ETL_Weaver-v
set TAG_NAME=%TAG_PREFIX%%NEW_VER%

echo Target Version: %NEW_VER%
echo Tag Name: %TAG_NAME%

:: README Check Prompt
echo.
set /p CONFIRM_README="[?] Have you updated README.md for this release? (Y/N): "
if /i "%CONFIRM_README%" neq "Y" (
    echo.
    echo [!] Release aborted. Please update README.md first.
    pause
    exit /b 1
)

:: Check if Tag already exists
git rev-parse %TAG_NAME% >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo.
    echo [!] ERROR: Tag %TAG_NAME% already exists.
    echo     Please bump the version in 'VERSION' file before releasing.
    pause
    exit /b 1
)

echo [2/6] Executing Build Test...
call scripts\build.bat
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] ERROR: Build failed. Release aborted.
    pause
    exit /b 1
)

:: Local Release Archiving
echo [2.5/6] Archiving to local release folder...
set RELEASE_DIR=release\%TAG_NAME%
if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"
copy /y "dist\ETLWeaver.exe" "%RELEASE_DIR%\"

echo [3/6] Extracting logs and updating files...
set LOG_FILE=release_logs.tmp
set LAST_TAG=
for /f "tokens=*" %%i in ('git describe --tags --abbrev^=0 --match "%TAG_PREFIX%*" 2^>nul') do set LAST_TAG=%%i

if "%LAST_TAG%"=="" (
    echo - Initial release > %LOG_FILE%
) else (
    echo Comparing with: %LAST_TAG%
    git log %LAST_TAG%..HEAD --oneline --pretty=format:"- %%s" -- . > %LOG_FILE%
    if !ERRORLEVEL! neq 0 echo - Minor updates and improvements > %LOG_FILE%
)

:: Update CHANGELOG.md
set TEMP_CHG=changelog.tmp
echo ## [%NEW_VER%] - %date% > %TEMP_CHG%
type %LOG_FILE% >> %TEMP_CHG%
echo. >> %TEMP_CHG%
if exist CHANGELOG.md (
    type CHANGELOG.md >> %TEMP_CHG%
    powershell -Command "(Get-Content %TEMP_CHG%) | Select-Object -First 100 | Set-Content CHANGELOG.md"
) else (
    move /y %TEMP_CHG% CHANGELOG.md >nul
)

echo [4/6] Syncing Source Code (Git Push)...
git add VERSION CHANGELOG.md
git commit -m "chore(release): ETL Weaver v%NEW_VER%"
git tag -a %TAG_NAME% -m "Release v%NEW_VER%"
git push origin master
git push origin %TAG_NAME%

echo [5/6] Publishing to GitHub Release...
type %LOG_FILE% > notes.tmp

gh release create %TAG_NAME% "dist\ETLWeaver.exe" --title "ETL Weaver v%NEW_VER%" --notes-file notes.tmp

if %ERRORLEVEL% equ 0 (
    echo SUCCESS: ETL Weaver v%NEW_VER% is LIVE!
) else (
    echo FAILED: Could not publish.
)

echo [6/6] Cleaning up...
if exist notes.tmp del notes.tmp
if exist %LOG_FILE% del %LOG_FILE%
if exist %TEMP_CHG% del %TEMP_CHG%

echo.
echo ==========================================
echo  RELEASE v%NEW_VER% COMPLETE
echo ==========================================
pause