# Utility Suite - Master Status Record

## 1. Repository Architecture Overview
A centralized suite for Windows internal tools featuring a unified release, documentation, and versioning framework.

## 2. Global Release Workflow (Standardized)
Every project follows this automated "Safety-First" lifecycle via `scripts/release.bat`:
1.  **Version Detection**: Reads from the local `VERSION` file.
2.  **README Audit (AI Rule)**: Gemini AI must scan source code for new features/settings and synchronize `README.md` before proceeding.
3.  **Safety Check**: If the Git Tag already exists, the release aborts.
4.  **Mandatory Build Test**: Automatically executes `scripts/build.bat`.
5.  **Local Archiving**: Backs up the binary to `release/<Tag_Name>/<Name>.exe`. (Ignored by Git).
6.  **Automated Changelog**: Extracts Git logs and prepends to `CHANGELOG.md`.
7.  **Git Synchronization**: Handles `chore(release)` commit, tagging, and pushing.
8.  **GitHub Publication**: Uses `gh` CLI to create a release and upload assets.
9.  **Editorial Rule**: Gemini AI humanizes logs into `### Added/Fixed` categories.

## 3. Engineering Standards & Best Practices
- **Executable Naming**: Use `ProjectName.exe` (Strictly NO spaces or dots in filenames).
- **Build Stability**: PyInstaller must use `--noupx` and `--noconfirm` to avoid Windows Defender locking issues on Win11.
- **Focus Recovery (Win32)**: When embedding child windows (like CMD), implement a global click listener using `SetForegroundWindow` and `SetFocus` to prevent keyboard focus lockups.
- **Frozen Versioning**: Bundle `VERSION` file as data and use `utils.resource_path` to ensure UI accuracy in compiled binaries.
- **Modern UI**: Mandatory High DPI awareness and Win11 immersive dark mode support.

## 4. Current Project Matrix
| Project | Version | Status | Highlights |
| :--- | :--- | :--- | :--- |
| **Driver Deck** | v1.2.1 | Stable | Focus Recovery, WT Integration, Suffix Logic |
| **ETL Weaver** | v1.1.0 | Stable | Postfix Rename, Refactored UI, Config Fix |

---
*Global Suite Status: Synchronized & Verified.*