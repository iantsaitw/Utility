# Utility Suite - Master Status Record

## Repository Architecture Overview
This repository serves as a centralized suite for Windows internal tools, featuring a unified release and documentation framework.

## Global Infrastructure Updates (2026-02-06)

### 1. Unified Release Framework
- **Master Release System**: Implemented `scripts/release.bat` in each project to automate the entire lifecycle (Bump -> Log -> Sync -> Build -> Publish).
- **Safety-First Flow**: Reordered process to ensure successful `build.bat` before any Git commits or version bumps.
- **Localized Logging**: Modified `git log` extraction to target project-specific directories (`-- .`), preventing commit mixing in Monorepo.
- **Versioning Strategy**: Adopted Semantic Versioning (v1.0.0 baseline) using a single-source `VERSION` file.
- **Automated Changelog**: Integrated `CHANGELOG.md` with automatic Git log extraction for GitHub Release Notes.

### 2. Structural & UI Optimization
- **Script Reorganization**: Moved all maintenance scripts (`build.bat`, `release.bat`) into a dedicated `scripts/` folder for a cleaner root directory.
- **UI Version Sync**: Updated Python `config.py` in both projects to dynamically read the `VERSION` file, ensuring UI display matches the release baseline.
- **DPI & UX Highlights**: Confirmed DPI Awareness for high-res displays and added Drag-and-Drop support details to READMEs.

### 3. Documentation Standards
- **Professional READMEs**: Rewritten all documentation in English with dynamic GitHub badges.
- **Interlinked History**: Root README now links to individual project changelogs.
- **Public Repo Optimization**: Optimized badge links for public visibility and individual project tag tracking.

### 4. Maintenance & Cleanup
- **Global Gitignore**: Consolidated Python, IDE, and temporary file rules into the root `.gitignore`.
- **Junk Removal**: Automated filtering of `CONERR$`, `*.txt` logs, and build artifacts.

## Current Project Matrix
| Project | Version | Status | Scripts Path |
| :--- | :--- | :--- | :--- |
| Driver Deck | v1.1.0 | Stable / Automated | `scripts/` |
| ETL Weaver | v1.0.0 | Stable / Automated | `scripts/` |

---
*Last Updated: 2026-02-11*
