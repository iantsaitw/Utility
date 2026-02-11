# ETL Weaver - Project Status Record

## Current Version: 1.0.0 (Settings & Stability Update)
**Last Updated:** 2026-02-11

---

## 1. Feature Highlights
- **Persistent Settings:** Custom UI font and theme (Dark/Light) saved to `settings.json`.
- **Conversion Core:** Bundled stable `traceview.exe` to ensure ETL data integrity.
- **Naming Alignment:** Standardized executable name to `ETLWeaver.exe` to match the suite's style.

## 2. Standardized Release Process (release.bat)
Consistent with the Utility Suite's workflow:
1. **Build Integrity**: Mandatory `build.bat` check before release.
2. **Humanized Logging**: Opens **Notepad** for manual refinement of release notes (convert Git logs to ### Added/Fixed).
3. **Automated Deployment**: One-click Git push, Tagging, and GitHub Release.
4. **Asset Management**: Automatically uploads `dist\ETLWeaver.exe`.

## 3. Project Structure
- `main.py`: Entry point.
- `ui_main_window.py`: Modern UI with `sv-ttk` support.
- `trace_tools/`: Multi-tool bundle (`traceview.exe`, `tracefmt.exe`).
- `scripts/`: Centralized `build.bat` and `release.bat`.

---
*Status: Finalized and Stable.*