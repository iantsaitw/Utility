# Driver Deck - Project Status Record

## Project Overview
Driver Deck is a GUI tool specifically designed for managing and building Windows drivers, built with Python, Tkinter, and sv-ttk.

## Current Version: v1.1.0 (Terminal & Stability Update)
**Last Updated:** 2026-02-11

### 1. Key Updates in v1.1.0
- **Terminal Stability**: Reverted to a native CMD-based backend for the embedded terminal to resolve focus issues.
- **Path Resolution**: Fixed issues with `TARGET_BATCH_FILE` scanning and configuration restoration.
- **Naming Alignment**: Standardized executable name to `DriverDeck.exe` (no spaces/dots).

### 2. Integrated Terminal (Terminal Widget)
- **Win32 Embedding**: Seamlessly embedded the CMD window into Tkinter via `SetParent`.
- **Focus Management**: Implemented `AttachThreadInput` to ensure keyboard input is directed correctly.
- **Tab Key Support**: Intercepts Tkinter's Tab and passes it to CMD for path completion.

### 3. Standardized Release Process (release.bat)
The project follows a safety-first automated workflow:
1. **Version Detection**: Reads from `VERSION` file.
2. **Build Test**: Triggers `scripts\build.bat`.
3. **Humanized Logging**: Automatically opens **Notepad** for the user to refine Git logs into professional release notes.
4. **Git Sync**: Handles commit, tagging, and pushing to origin master.
5. **GitHub Release**: Uses `gh` CLI to publish assets (`dist\DriverDeck.exe`).

## Key File Descriptions
- `main.py`: Application entry point.
- `terminal_widget.py`: Win32 window operations for terminal embedding.
- `config.py`: Global settings and UI constants.
- `build.bat`: PyInstaller packaging script.

---
*Status: Finalized and Stable.*