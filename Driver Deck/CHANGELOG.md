All notable changes to this project will be documented in this file.

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
