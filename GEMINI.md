# Utility Suite - Master Status Record

## 1. Repository Architecture Overview
A centralized suite for Windows internal tools featuring a unified release, documentation, and versioning framework.

## 2. Infrastructure Standards (Last Updated: 2026-02-11)
- **Unified Release System**: Every project uses `scripts/release.bat` with automated log extraction and manual refinement (via Notepad).
- **Build Consistency**: Aligned PyInstaller parameters (e.g., `--noupx`) across all tools to improve stability on Windows 11.
- **Naming Convention**: Standarized executable naming (e.g., `DriverDeck.exe`, `ETLWeaver.exe`) without spaces or dots.
- **DPI & UI**: Mandatory High DPI awareness and Win11 immersive dark mode support.

## 3. Current Project Matrix
| Project | Version | Status | Highlights |
| :--- | :--- | :--- | :--- |
| **Driver Deck** | v1.1.0 | Stable | Terminal Focus Fix, WT Integration |
| **ETL Weaver** | v1.0.0 | Stable | Postfix Rename, Refactored UI |

---
*Global Suite Status: Synchronized & Verified.*