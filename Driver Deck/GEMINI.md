# Driver Deck - Project Status Record

## 1. Project Overview
A professional GUI tool for Windows Driver management and build operations.

## 2. Current Version: v1.1.0
**Status:** Stable / UX Optimized
**Last Updated:** 2026-02-11

### 🚀 Key Features
- **Project Tree**: Automatic scanning of PCIE/USB driver projects.
- **Modern Terminal**: Embedded Windows Terminal (WT) with full ANSI color support.
- **Smart Management**: Automated backup with timestamping and symbol filtering (All/Symbol/No Symbol).
- **One-Click Signing**: Digital signature integration via SignTool.

### 🛠️ Technical Implementation (Modular Fixes)
- **Focus Lock Resolution**: Uses a global Win32 click listener (`SetForegroundWindow` & `SetFocus`) to break terminal focus and return keyboard control to Python UI.
- **Terminal Integration**: Forced `wt.exe` via list-based `subprocess.Popen` to solve quoting issues with paths containing spaces (e.g., `C:\Program Files`).
- **Filesystem Hooks**: Applied `os.utime` post-backup to force directory sorting priority.
- **Regex Logic**: Suffix auto-refresh uses `^(_\d{8}_\d{4})(.*)$` to selectively update time while preserving manual text.

## 3. Standardized Release Process
1. **Validation**: Mandatory `build.bat` check (Aligned with ETL Weaver, includes `--noupx`).
2. **Changelog**: Manual Notepad editing of Git logs before publish.
3. **Deployment**: Automated tagging and GitHub Release upload.

---
*Status: Finalized and Stable.*