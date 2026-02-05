@echo off
echo Closing Windows Explorer...
taskkill /f /im explorer.exe

echo Cleaning Icon Cache...
cd /d %userprofile%\AppData\Local\Microsoft\Windows\Explorer
del iconcache*

echo Cleaning Thumbnails...
del thumbcache*

echo Restarting Windows Explorer...
start explorer.exe

echo Done! Icon cache cleared.
pause