## [1.2.0] - 2026-02-13
### Added
- **Smart Persistence**: Split size and unit settings are now automatically saved in the background whenever changed.
- **Editable Paths**: File path fields are now editable, allowing manual name adjustments without re-dragging.

### Changed
- **Compact Layout**: Refactored UI to a top-aligned compact design, providing more vertical space for the log panel.
- **Themed UI**: Integrated modern themed scrollbars into the Command Execution Log.

### Fixed
- **Bundle Reliability**: Fixed ModuleNotFoundError issues in the standalone executable by optimizing internal search paths.

## [1.1.1] - 2026-02-12
### Fixed
- **UI Consistency**: Replaced legacy scrollbars in the Execution Log with modern themed ttk.Scrollbars for a unified look.
- **Admin Limitations**: Verified stability across various privilege levels.

### Added
- **Visual Assets**: Included the initial application screenshots in the project documentation.

## [1.1.0] - 2026-02-12
### Added
- **Postfix Support**: Added Postfix field to specify custom suffixes for converted and split files.
- **Rename TXT**: New dedicated button to immediately apply postfix to the loaded TXT file.
- **Side-by-Side UI**: Refactored the TXT Setting panel into a more ergonomic two-column layout.

### Fixed
- **Critical ImportError**: Resolved config.py issues that prevented the application from launching.
- **Class Structure**: Repaired UI window method nesting and indentation for improved stability.
- **Settings Dialog**: Improved centering, icon support, and fixed the PDB path entry field layout.
- **Version Bundling**: VERSION file is now correctly embedded in the EXE for accurate UI display.

### Changed
- **Asset Naming**: Standardized executable name to ETLWeaver.exe (no spaces/dots).

# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-06
### Added
- **Initial Release**: First professional release with stable ETL conversion engine.
- **Settings UI**: Added persistent settings for Theme (Dark/Light) and Font customization.
- **Conversion Core**: Bundled reliable `traceview.exe` to prevent data truncation issues.
- **Automation**: Implemented `build.bat` and `release.bat` for one-click deployment.

### Changed
- **Asset Naming**: Standardized executable name to `ETLWeaver.exe` (aligned with Driver Deck).



