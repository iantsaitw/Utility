# ETL Weaver - Project Status Record

## Current Version: 25.0905 (Refined)
**Last Updated:** 2026-02-05

---

## 1. UI & UX Refinement (Driver Deck Style)
- **Layout:** Transitioned from a sidebar-based layout to a more compact, single-panel workspace with grouped cards.
- **Theme:** Forced **Dark Mode** for a professional look.
- **Language:** Fully translated to **English** (all buttons, labels, and status messages).
- **System Monitoring:** Real-time CPU Load and RAM Usage displayed in the header (Auto-updating every 2 seconds).
- **Workspace:** 
  - Left: Core workflow (Drop Zone, File Information, Split Settings, Action Buttons).
  - Right: PDB Symbol Browser for quick selection.
  - Bottom: Expandable Command Execution Log.

## 2. Core Logic & Features
- **Traceview Integration:** Bundled `traceview.exe` for ETL to TXT conversion.
- **File Splitting:** Supports splitting large text files by KB/MB with estimated part counting.
- **Drag & Drop:** Fully supported for .etl, .pdb, and .txt files via `tkinterdnd2`.
- **Multi-part ETL:** Recognized and handled via regex (e.g., `.etl.001`).

## 3. Build & Distribution System
- **Unified Build Script (`build.bat`):** 
  - **Auto-Detection:** Automatically finds `tkinterdnd2` and `APP_NAME`.
  - **Release Mode (Single EXE):** Default mode, produces a clean, standalone EXE in `dist/`.
  - **Performance:** Used `--noupx` to significantly speed up the build process.
  - **Size Optimization:** Excluded the heavy `symbol/` folder from the EXE bundle to keep the size around 15MB.
- **Clean Environment:** Post-build auto-cleanup of `.spec` and `build/` folders.

## 4. Project Structure
- `main.py`: Entry point.
- `ui_main_window.py`: Refined modern UI logic.
- `core_logic.py`: Conversion and splitting logic.
- `config.py`: App constants and fonts.
- `utils.py`: Path and formatting helpers.
- `traceview/`: Bundled external tools.
- `symbol/`: External PDB storage (Excluded from build).

---
*Status: Stable and Optimized.*
