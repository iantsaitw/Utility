All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-02-12
### Fixed
- **Focus Lock Resolution**: Implemented a global Win32 click listener to break terminal focus and restore keyboard control to UI fields.
- **Smart Suffix Refresh**: Refined suffix logic to preserve custom text while automatically updating the date/time portion.
- **Backup Sorting**: Added modification time update (`os.utime`) to ensure new backups appear at the top of the list.
- **Dynamic Versioning**: Fixed an issue where the UI would incorrectly show version 1.0.0 after bundling.

### Changed
- **Modern Terminal**: Forced Windows Terminal (`wt.exe`) for the embedded view to ensure full color support in Administrator mode.
- **UI Alignment**: Refined terminal layout to perfectly align with the left-hand project tree.

## [1.1.0] - 2026-02-11
### Fixed
- **Config Restoration**: Restored missing `config.py` logic and UI constants to fix startup errors.
- **Path Resolution**: Corrected `TARGET_BATCH_FILE` path to ensure reliable project scanning.
- **Release Automation**: Updated `release.bat` to correctly locate build scripts and filter git logs.

### Changed
- **Terminal Stability**: Enhanced terminal embedding stability by reverting to a native CMD-based backend, resolving focus issues in VS 2022.

## [1.0.0] - 2026-02-06
### Added
- **Initial Release**: First professional release with automated build system.
- **UI Framework**: Modernized interface using `sv-ttk` and Win32 immersive styling.
- **Terminal Integration**: Embedded Win32 console for direct command execution.
- **Documentation**: Professional English README and automated CHANGELOG generation.
