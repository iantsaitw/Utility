# Driver Deck - Project Status Record

## Project Overview
Driver Deck is a GUI tool specifically designed for managing and building Windows drivers, built with Python, Tkinter, and sv-ttk.

## Current Version Features (v1.0.0 - UI Optimized)

### 1. UI Layout
- **Layout Swap**: Moved "Project Management Tab" to the left and "Terminal" to the right to optimize visual focus.
- **Window Size**: Default geometry set to `1400x850`.
- **Column Optimization**: Optimized the width of the "Files" list columns. Set `Name` and `Digital Signature` to auto-expand to prevent columns from being squeezed at startup.
- **Button Simplification**: Simplified the button text in the Export area from "Export Folder/Sys" to "Folder/Sys".
- **Theme Style**: Uses `sv-ttk` for dark mode and enables Windows 11 immersive title bar via Win32 API.

### 2. Integrated Terminal (Terminal Widget)
- **Win32 Embedding**: Seamlessly embedded the CMD window into Tkinter via `SetParent` and style modifications.
- **Robust Focus Management**:
    - Implemented `AttachThreadInput` technology to ensure keyboard input is immediately directed to the embedded CMD when clicking or entering the terminal area.
    - Support for `Tab` key cycling: Intercepts Tkinter's Tab focus switching and passes the Tab key to CMD for path completion.
- **Default Directory**: The terminal consistently opens at the configured "Root Path" (e.g., `E:\Project`) to ensure startup stability.

### 3. Settings Persistence
- **Absolute Path Fix**: Corrected the storage path of `settings.json` to the EXE directory, ensuring that settings like PFX are correctly preserved regardless of how the app is launched.

### 4. Build System
- **Direct Build**: `build.bat` now builds the executable directly as `Driver Deck.exe`.
- **Version Tracking**: Automatically generates a `version.txt` with timestamp in the `dist` folder during build for automated publishing.

## Key File Descriptions
- `main.py`: Application entry point, handles layout, DPI awareness, and core component initialization.
- `terminal_widget.py`: Core Win32 window operations, handling embedding, focus management, and Tab key passing.
- `config.py`: Global settings, color definitions, and absolute path handling for `settings.json`.
- `project_tab.py`: Driver list logic, file list rendering, and backup/export functions.
- `build.bat`: Stable PyInstaller packaging script.

## Development Notes
- **Administrator Privileges**: In Administrator mode, the Windows kernel limits some UI rendering (e.g., scrollbar color). Current strategy prioritizes functional stability.
- **Event Mechanism**: List selection uses the `<<TreeviewSelect>>` event.

---
*Last Updated: 2026-02-05*