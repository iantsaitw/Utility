@echo off
setlocal enabledelayedexpansion
title ETL Weaver - Master Release

echo [1/6] Detecting changes since last release...
set /p OLD_VER=<VERSION
set TAG_PREFIX=ETL_Weaver-v
set LAST_TAG=%TAG_PREFIX%%OLD_VER%

for /f "tokens=1,2,3 delims=." %%a in ("%OLD_VER%") do (
    set /a PATCH=%%c+1
    set NEW_VER=%%a.%%b.!PATCH!
)
echo Current: %OLD_VER% -^> Next: %NEW_VER%

echo [2/6] Extracting Git logs...
set LOG_FILE=release_logs.tmp
git log %LAST_TAG%..HEAD --oneline --pretty=format:"- %%s" > %LOG_FILE%
if %ERRORLEVEL% neq 0 (
    echo No previous tag found. using default log.
    echo - Minor updates and improvements > %LOG_FILE%
)

echo %NEW_VER%> VERSION

echo [4/6] Updating CHANGELOG.md...
set TEMP_CHG=changelog.tmp
echo ## [%NEW_VER%] - %date% > %TEMP_CHG%
type %LOG_FILE% >> %TEMP_CHG%
echo. >> %TEMP_CHG%
type CHANGELOG.md >> %TEMP_CHG%
powershell -Command "(Get-Content %TEMP_CHG%) | Select-Object -Skip 3 | Set-Content CHANGELOG.md"
del %LOG_FILE% %TEMP_CHG%

echo [5/6] Committing version bump...
git add VERSION CHANGELOG.md
git commit -m "chore: bump version to v%NEW_VER%"
git push

echo [6/6] Build and Publish...
call build.bat
call publish.bat

echo.
echo ==========================================
echo  RELEASE %NEW_VER% COMPLETE
echo ==========================================
pause
