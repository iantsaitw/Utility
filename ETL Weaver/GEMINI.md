# ETL Weaver - Project Status Record

## Current Version: 1.0.0 (Feature & Stability Update)
**Last Updated:** 2026-02-11

---

## 1. Feature Highlights
- **TXT Setting & Postfix**: Added a "Postfix" input field. Both ETL conversion and splitting now support custom filename suffixes.
- **Rename TXT**: New dedicated button to apply the current Postfix to the loaded TXT file immediately.
- **UI Refactoring**: 
    - "TXT Setting" is now a clean two-column layout.
    - Improved "Settings" dialog with centering, application icon, and fixed PDB path input.
- **Stability**: Fixed major `config.py` ImportError and class structure issues in `ui_main_window.py`.

## 2. Standardized Release Process (release.bat)
Consistent with the Utility Suite's workflow:
1. **Build Integrity**: Mandatory `build.bat` check before release.
2. **Humanized Logging**: Opens Notepad for manual log refinement.
3. **Automated Deployment**: One-click Git push, Tagging, and GitHub Release.

---
*Status: Feature Enhanced & Stable.*