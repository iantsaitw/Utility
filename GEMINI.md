# Utility Suite - Master Status Record

## Repository Architecture Overview
This repository serves as a centralized suite for Windows internal tools, featuring a unified release and documentation framework.

## Global Infrastructure Updates (2026-02-06)

### 1. Unified Release Framework
- **Master Release System**: Implemented `release.bat` in each project to automate the entire lifecycle (Bump -> Log -> Sync -> Build -> Publish).
- **Safety-First Flow**: Reordered process to ensure successful `build.bat` before any Git commits or version bumps.
- **Versioning Strategy**: Adopted Semantic Versioning (v1.0.0 baseline) using a single-source `VERSION` file.
- **Automated Changelog**: Integrated `CHANGELOG.md` with automatic Git log extraction for GitHub Release Notes.

### 2. Documentation Standards
- **Professional READMEs**: Rewritten all documentation in English with technical highlights and visual formatting.
- **Interlinked History**: Root README now links to individual project changelogs.
- **GEMINI.md Consistency**: Standardized project status recording across sub-folders.

### 3. Maintenance & Cleanup
- **Global Gitignore**: Consolidated Python, IDE, and temporary file rules into the root `.gitignore`.
- **Junk Removal**: Automated filtering of `CONERR$`, `*.txt` logs, and build artifacts.

## Current Project Matrix
| Project | Version | Status | Last Update |
| :--- | :--- | :--- | :--- |
| Driver Deck | v1.0.0 | Stable / Automated | 2026-02-06 |
| ETL Weaver | v1.0.0 | Stable / Automated | 2026-02-06 |

---
*Last Updated: 2026-02-06*
