# ETL Weaver - Project Status Record

## 1. Project Overview
High-performance ETL analysis engine with stable traceview conversion and TXT splitting.

## 2. Current Version: 1.0.0 (Feature Update)
**Status:** Feature Enhanced
**Last Updated:** 2026-02-11

### 🚀 Key Features
- **Conversion Core**: Reliable ETL to TXT conversion using bundled `traceview.exe`.
- **TXT Setting & Postfix**: Support for custom filename suffixes in both conversion and splitting.
- **Rename Logic**: Dedicated button to apply postfix immediately to the current file.
- **Side-by-Side UI**: Refactored settings panel into a two-column layout for better ergonomics.

### 🛠️ Technical Implementation (Modular Fixes)
- **Import Resolution**: Fixed `config.py` ImportError by restoring missing system constants (`SHOW_SYSTEM_INFO`, etc.).
- **Class Structure**: Repaired `ui_main_window.py` indentation and nested function errors.
- **Dialog Alignment**: Fixed Settings window centering and icon inheritance.
- **Process Management**: Build script now forcefully kills `ETLWeaver.exe` to prevent file access denied errors.

## 3. Standardized Release Process
1. **Validation**: Mandatory `build.bat` check (Aligned with Driver Deck).
2. **Changelog**: Manual Notepad editing of Git logs before publish.
3. **Deployment**: Automated tagging and GitHub Release upload.

---
*Status: Feature Enhanced & Stable.*