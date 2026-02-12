# ETL Weaver - Project Status Record

## 1. Project Overview
High-performance ETL analysis engine with stable traceview conversion and TXT splitting.

## 2. Current Version: v1.1.0
**Status:** Feature Enhanced
**Last Updated:** 2026-02-12

### 🚀 Key Features
- **Conversion Core**: Reliable ETL to TXT conversion using bundled `traceview.exe`.
- **TXT Setting & Postfix**: Support for custom filename suffixes in both conversion and splitting.
- **Rename Logic**: Dedicated button to apply postfix immediately to the current file.
- **Side-by-Side UI**: Refactored the settings panel into a two-column layout for better ergonomics.

### 🛠️ Technical Implementation (Modular Fixes)
- **Import Resolution**: Fixed `config.py` ImportError by restoring missing system constants (`SHOW_SYSTEM_INFO`, etc.).
- **Class Structure**: Repaired `ui_main_window.py` indentation and nested function errors.
- **Dialog Alignment**: Fixed Settings window centering and icon inheritance.
- **Version Embedding**: Bundles `VERSION` file into PyInstaller package for accurate UI versioning.

---
*Status: Feature Enhanced & Stable.*