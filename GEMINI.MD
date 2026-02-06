# ETL Weaver - Project Status Record

## Current Version: 25.0905 (Settings & Stability Update)
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

---
*Status: Finalized and Stable.*