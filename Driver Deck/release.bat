@echo off
setlocal enabledelayedexpansion
title Driver Deck - Master Release

echo [1/6] Detecting changes since last release...
:: Get current version
set /p OLD_VER=<VERSION
set TAG_PREFIX=Driver_Deck-v
set LAST_TAG=%TAG_PREFIX%%OLD_VER%

:: Bump Version (Patch +1)
for /f "tokens=1,2,3 delims=." %%a in ("%OLD_VER%") do (
    set /a PATCH=%%c+1
    set NEW_VER=%%a.%%b.!PATCH!
)
echo Current: %OLD_VER% -^> Next: %NEW_VER%

:: Get Git Logs (Filter out chore/docs if you want, or just get all)
echo [2/6] Extracting Git logs...
set LOG_FILE=release_logs.tmp
git log %LAST_TAG%..HEAD --oneline --pretty=format:"- %%s" > %LOG_FILE%
if %ERRORLEVEL% neq 0 (
    echo No previous tag found or no changes. using default log.
    echo - Minor updates and improvements > %LOG_FILE%
)

:: [3/6] Update VERSION file
echo %NEW_VER%> VERSION

:: [4/6] Update CHANGELOG.md
echo [4/6] Updating CHANGELOG.md...
set TEMP_CHG=changelog.tmp
echo ## [%NEW_VER%] - %date% > %TEMP_CHG%
type %LOG_FILE% >> %TEMP_CHG%
echo. >> %TEMP_CHG%
type CHANGELOG.md >> %TEMP_CHG%
:: Filter out the first few lines of the old changelog to avoid double header
powershell -Command "(Get-Content %TEMP_CHG%) | Select-Object -Skip 3 | Set-Content CHANGELOG.md"
del %LOG_FILE% %TEMP_CHG%

:: [5/6] Sync Source Code
echo [5/6] Committing version bump...
git add VERSION CHANGELOG.md
git commit -m "chore: bump version to v%NEW_VER%"
git push

:: [6/6] Build and Publish
echo [6/6] Executing Build and Publish...
call build.bat
call publish.bat

echo.
echo ==========================================
echo  RELEASE %NEW_VER% COMPLETE
echo ==========================================
pause
