# Utility Suite - Master Status Record

## 1. Repository Architecture Overview
A centralized suite for Windows internal tools featuring a unified release, documentation, and versioning framework.

## 2. Global Release Workflow (Standardized)
Every project follows this automated "Safety-First" lifecycle via `scripts/release.bat`:
1.  **Version Detection**: Reads from the local `VERSION` file.
2.  **Safety Check (Abort-on-Exists)**: If the Git Tag already exists, the release aborts to prevent overwriting history.
3.  **Mandatory Build Test**: Automatically executes `scripts/build.bat`. Must pass to proceed.
4.  **Local Archiving**: Backs up the binary to `release/<Tag_Name>/<Name>.exe`. (Ignored by Git).
5.  **Automated Changelog**: Extracts Git logs since the last tag and prepends to `CHANGELOG.md`.
6.  **Git Synchronization**: Handles `chore(release)` commit, tagging, and pushing to origin master.
7.  **GitHub Publication**: Uses `gh` CLI to create a release and upload assets.
8.  **Editorial Rule (AI README Audit)**: During every release, Gemini AI must scan the source code and README.md. If descriptions, feature lists, or folder structures are outdated, the AI must automatically correct them before the final commit.
9.  **Log Refinement**: Gemini AI is responsible for "Humanizing" logs into `### Added/Fixed` categories.

## 3. Engineering Standards
- **Binary Naming**: Standardized `ProjectName.exe` (no spaces, no dots).
- **Frozen Versioning**: All tools must bundle `VERSION` into the EXE and use `utils.resource_path` for accurate UI display.
- **Build Flags**: PyInstaller must use `--noupx` and `--noconfirm` for stability on Windows 11.
- **DPI awareness**: Mandatory High DPI awareness and Win11 immersive dark mode.

## 4. Current Project Matrix
| Project | Version | Status | Highlights |
| :--- | :--- | :--- | :--- |
| **Driver Deck** | v1.2.1 | Stable | Focus Recovery, WT Integration, Suffix Logic |
| **ETL Weaver** | v1.1.0 | Stable | Postfix Rename, Refactored UI, Config Fix |

---
*Global Suite Status: Synchronized & Verified.*