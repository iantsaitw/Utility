@echo off
setlocal enabledelayedexpansion
title Driver Deck - Master Release

echo [1/6] Detecting changes since last release...
:: Get current version
if not exist "VERSION" echo 1.0.0> VERSION
set /p OLD_VER=<VERSION
set TAG_PREFIX=Driver_Deck-v
set LAST_TAG=%TAG_PREFIX%%OLD_VER%

:: Bump Version (Patch +1)
for /f "tokens=1,2,3 delims=." %%a in ("%OLD_VER%") do (
    set /a PATCH=%%c+1
    set NEW_VER=%%a.%%b.!PATCH!
)
echo Current: %OLD_VER% -^> Next: %NEW_VER%

:: Get Git Logs
echo [2/6] Extracting Git logs...
set LOG_FILE=release_logs.tmp
git log %LAST_TAG%..HEAD --oneline --pretty=format:"- %%s" > %LOG_FILE%
if %ERRORLEVEL% neq 0 (
    echo No previous tag found. using default log.
    echo - Minor updates and improvements > %LOG_FILE%
)

:: Update VERSION file
echo %NEW_VER%> VERSION

:: Update CHANGELOG.md
echo [3/6] Updating CHANGELOG.md...
set TEMP_CHG=changelog.tmp
echo ## [%NEW_VER%] - %date% > %TEMP_CHG%
type %LOG_FILE% >> %TEMP_CHG%
echo. >> %TEMP_CHG%
if exist CHANGELOG.md (
    type CHANGELOG.md >> %TEMP_CHG%
    :: Skip the first few lines of the old changelog headers
    powershell -Command "(Get-Content %TEMP_CHG%) | Select-Object -Skip 3 | Set-Content CHANGELOG.md"
) else (
    move /y %TEMP_CHG% CHANGELOG.md >nul
)

:: Sync Source Code
echo [4/6] Committing version bump to Git...
git add VERSION CHANGELOG.md
git commit -m "chore: bump version to v%NEW_VER%"
git push

:: Build
echo [5/6] Executing Build...
call build.bat

:: Publish to GitHub
echo [6/6] Publishing to GitHub Release...
set APP_NAME=Driver_Deck
if exist "dist\version.txt" (
    set /p FULL_VER=<"dist\version.txt"
) else (
    set FULL_VER=v%NEW_VER%
)

:: Extract specific notes for this version
powershell -Command "$v = '%NEW_VER%'; $c = Get-Content CHANGELOG.md -Raw; if ($c -match \"## \[$v\](.*?)(?=\n## |$)\") { $matches[1].Trim() | Out-File -Encoding utf8 notes.tmp } else { 'New release' | Out-File -Encoding utf8 notes.tmp }"

gh release create %APP_NAME%-%FULL_VER% "dist\Driver Deck.exe" --title "%APP_NAME% %FULL_VER%" --notes-file notes.tmp

if %ERRORLEVEL% equ 0 (
    echo SUCCESS: %APP_NAME% %FULL_VER% is LIVE!
) else (
    echo FAILED: Could not publish to GitHub.
)

:: Cleanup
if exist notes.tmp del notes.tmp
if exist %LOG_FILE% del %LOG_FILE%
if exist %TEMP_CHG% del %TEMP_CHG%

echo.
echo ==========================================
echo  RELEASE %FULL_VER% COMPLETE
echo ==========================================
pause