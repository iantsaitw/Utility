@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0.."
title ETL Weaver - Master Release (Safety First)

echo [1/6] Calculating next version...
if not exist "VERSION" echo 1.0.0> VERSION
set /p OLD_VER=<VERSION
set TAG_PREFIX=ETL_Weaver-v

for /f "tokens=1,2,3 delims=." %%a in ("%OLD_VER%") do (
    set /a PATCH=%%c+1
    set NEW_VER=%%a.%%b.!PATCH!
)
set LAST_TAG=%TAG_PREFIX%%OLD_VER%
echo Current: %OLD_VER% -^> Next: %NEW_VER%

echo [2/6] Executing Build Test...
call build.bat
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] ERROR: Build failed. Release aborted.
    pause
    exit /b 1
)

echo [3/6] Extracting logs and updating files...
set LOG_FILE=release_logs.tmp
git log %LAST_TAG%..HEAD --oneline --pretty=format:"- %%s" > %LOG_FILE%
if %ERRORLEVEL% neq 0 (
    echo - Minor updates and improvements > %LOG_FILE%
)

echo %NEW_VER%> VERSION
set TEMP_CHG=changelog.tmp
echo ## [%NEW_VER%] - %date% > %TEMP_CHG%
type %LOG_FILE% >> %TEMP_CHG%
echo. >> %TEMP_CHG%
if exist CHANGELOG.md (
    type CHANGELOG.md >> %TEMP_CHG%
    powershell -Command "(Get-Content %TEMP_CHG%) | Select-Object -Skip 3 | Set-Content CHANGELOG.md"
) else (
    move /y %TEMP_CHG% CHANGELOG.md >nul
)

echo [4/6] Syncing Source Code (Git Push)...
git add VERSION CHANGELOG.md
git commit -m "chore: bump version to v%NEW_VER%"
git push

echo [5/6] Publishing to GitHub Release...
set TAG_NAME=%TAG_PREFIX%%NEW_VER%
powershell -Command "$v = '%NEW_VER%'; $c = Get-Content CHANGELOG.md -Raw; if ($c -match \"## \[$v\](.*?)(?=\n## |$)\") { $matches[1].Trim() | Out-File -Encoding utf8 notes.tmp } else { 'New release' | Out-File -Encoding utf8 notes.tmp }"

gh release create %TAG_NAME% "dist\ETL Weaver.exe" --title "ETL Weaver v%NEW_VER%" --notes-file notes.tmp

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