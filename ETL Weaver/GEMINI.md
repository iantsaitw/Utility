# ETL Weaver - Project Status Record

## Current Version: 1.0.0 (Settings & Stability Update)
**Last Updated:** 2026-02-06

---

## 1. New Features
- **Persistent Settings:** Added a Settings dialog to customize UI font (family/size), application theme (Dark/Light), and default PDB search path. Settings are saved to `settings.json`.
- **UI Refresh Mechanism:** Implemented a non-destructive UI refresh that applies new settings live while preserving the current execution log.

## 2. Core Logic & Stability
- **Tool Consolidation:** Renamed `traceview` folder to `trace_tools` to reflect its multi-tool nature.
- **Traceview Restoration:** Reverted to the original, stable `traceview.exe` for ETL conversion to ensure data integrity (preventing truncation/encoding issues found in newer versions).
- **Tool Options:** Bundled both `traceview.exe` (legacy/stable) and `tracefmt.exe` (WDK 2025/fast) within the package.
- **Process Optimization:** Set high process priority for conversion tasks to improve performance.

## 3. Project Structure
- `main.py`: Entry point.
- `ui_main_window.py`: Modern UI with Settings support and stable conversion workflow.
- `core_logic.py`: Standardized conversion logic using bundled `traceview.exe`.
- `config.py`: Configuration management with JSON persistence.
- `utils.py`: Path and formatting helpers.
- `trace_tools/`: Contains `traceview.exe`, `tracefmt.exe`, and `TraceView.chm`.
- `test/`: Sample ETL and PDB for verification.

## Standardized Release Process (release.bat)
The project follows a safety-first automated release workflow consistent with Driver Deck:
1. **Version Detection**: Reads from `VERSION` file and sets `ETL_Weaver-v` prefix.
2. **Pre-release Build**: Automatically triggers `scripts\build.bat` to ensure binary integrity.
3. **Automated Changelog**: Extracts git logs since last tag and prepends to `CHANGELOG.md`.
4. **Git Synchronization**: Handles `git commit` (chore: release), `git tag`, and `git push` to origin master.
5. **GitHub Integration**: Creates a GitHub Release via `gh` CLI and uploads `dist\ETLWeaver.exe`.

---
*Status: Finalized and Stable.*