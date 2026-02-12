# Driver Deck - Project Status Record

## Project Overview
Driver Deck is a GUI tool specifically designed for managing and building Windows drivers, built with Python, Tkinter, and sv-ttk.

## Current Version: v1.1.0 (Terminal Focus & UI Optimization)
**Last Updated:** 2026-02-11

### 1. Key Updates & Stability Fixes
- **Global Focus Recovery (Critical Fix)**: Solved the issue where the embedded terminal would "lock" the keyboard input. 
    - *Mechanism*: Implemented a global `<Button-1>` listener in the main app. Clicking any non-terminal widget triggers Win32 `SetForegroundWindow` and `SetFocus`, forcefully breaking the CMD thread's input hook and returning control to Python.
- **Modern Terminal (WT Integration)**: Forced the use of Windows Terminal (`wt.exe`) via `subprocess.Popen` (list-based) to ensure full ANSI color support and modern font rendering even in Administrator mode.
- **Smart Suffix Refresh**: Backup suffix now auto-updates the date/time portion during "Refresh List" using regex (`^(_\d{8}_\d{4})(.*)$`), while preserving any custom text manually appended by the user.
- **Backup Sorting Logic**: Applied `os.utime(dest, None)` after backup to ensure the new folder is timestamped as 'now', causing it to correctly appear at the top of the list.
- **Symbol Filtering**: Added "All / Symbol / No Symbol" buttons with state persistence in `settings.json`.

### 2. UI Layout & UX
- **Header Alignment**: Removed redundant titles. The "Restart" button is now a discreet overlay at the bottom-right of the terminal.
- **Visual Consistency**: Terminal top edge is now perfectly aligned with the left-hand project tree.
- **Build System**: Aligned `build.bat` with ETL Weaver (added `--noupx` and dynamic name detection) to bypass Windows Defender file-locking warnings on Windows 11.

### 3. Standardized Release Process (release.bat)
1. **Build Integrity**: Mandatory `build.bat` check.
2. **Humanized Logging**: Opens Notepad for manual log refinement.
3. **Automated Deployment**: One-click Git sync and GitHub Release.

---
*Status: Stable, UX Optimized & Focus issues resolved.*