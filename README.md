# 🛠️ Windows Utility Suite

[![License](https://img.shields.io/badge/License-Internal-blue.svg)](https://github.com/iantsaitw/Utility)
[![GitHub Releases](https://img.shields.io/github/v/release/iantsaitw/Utility?include_prereleases&label=Latest%20Release)](https://github.com/iantsaitw/Utility/releases)

A curated collection of high-performance internal tools engineered for Windows driver development, system debugging, and ETL log analysis. This suite bridges legacy command-line utilities with modern, efficient GUI workflows.

---

## 🚀 Project Matrix

| Tool Name | Purpose | Latest Version | Direct Download | History |
| :--- | :--- | :--- | :--- | :--- |
| [**Driver Deck**](./Driver%20Deck) | Professional Driver Management & Build System | ![Version](https://img.shields.io/badge/version-1.0.0-green) | [📦 Download EXE](https://github.com/iantsaitw/Utility/releases) | [📜 Changelog](./Driver%20Deck/CHANGELOG.md) |
| [**ETL Weaver**](./ETL%20Weaver) | Modern ETL Analysis & Conversion Engine | ![Version](https://img.shields.io/badge/version-1.0.0-green) | [📦 Download EXE](https://github.com/iantsaitw/Utility/releases) | [📜 Changelog](./ETL%20Weaver/CHANGELOG.md) |

---

## 🏗️ Architecture & Standards

- **[Master Release System](./GEMINI.md)**: Every project follows a "Safety-First" automated release workflow via `release.bat`.
- **Integrated Tooling**: Seamlessly bundles essential WDK and debugging utilities.
- **Modern UI/UX**: All tools feature Windows 11 immersive design and DPI awareness.

## 🛠️ Global Requirements

- **OS**: Windows 10 / 11 (x64)
- **Environment**: Visual Studio 2022 / Windows Driver Kit (WDK) for build operations.
- **Dependencies**: 
  ```powershell
  pip install sv-ttk tkinterdnd2 psutil
  ```

---

## 👨‍💻 Developer Guide

To release a new version of any tool:
1. Complete your changes and commit them.
2. Navigate to the tool's directory (e.g., `cd "Driver Deck"`).
3. Run `release.bat`.

The system will automatically bump the version, update the changelog, sync with Git, and publish to GitHub Releases.

---
*Internal Engineering Toolset - Realtek Semiconductor Corp.*