# 🛠️ Windows Utility Suite
> A premium collection of high-performance internal tools for Windows Driver development and system analysis.

[![License](https://img.shields.io/badge/License-Internal-blue.svg?style=for-the-badge)](https://github.com/iantsaitw/Utility)
[![Master Build](https://img.shields.io/github/last-commit/iantsaitw/Utility?style=for-the-badge&color=orange)](https://github.com/iantsaitw/Utility/commits/master)
[![Platform](https://img.shields.io/badge/Platform-Win10%20%7C%20Win11-0078d4?style=for-the-badge&logo=windows)](https://www.microsoft.com/windows)

This repository serves as a centralized hub for engineering utilities designed to bridge the gap between legacy kernel debugging and modern GUI workflows. Every tool is built with a focus on **stability, speed, and immersive UX**.

---

## 🚀 Project Matrix

| Tool | Capability | Latest Release | Download | History |
| :--- | :--- | :--- | :--- | :--- |
| [**🚢 Driver Deck**](./Driver%20Deck) | Professional Driver Lifecycle Management | [![v1.2.1](https://img.shields.io/github/v/tag/iantsaitw/Utility?filter=Driver_Deck-v*&label=v1.2.1&color=green&style=flat-square)](https://github.com/iantsaitw/Utility/releases) | [📦 EXE](https://github.com/iantsaitw/Utility/releases) | [📜 Log](./Driver%20Deck/CHANGELOG.md) |
| [**🧶 ETL Weaver**](./ETL%20Weaver) | High-Speed ETL Analysis & Splitting | [![v1.1.0](https://img.shields.io/github/v/tag/iantsaitw/Utility?filter=ETL_Weaver-v*&label=v1.1.0&color=green&style=flat-square)](https://github.com/iantsaitw/Utility/releases) | [📦 EXE](https://github.com/iantsaitw/Utility/releases) | [📜 Log](./ETL%20Weaver/CHANGELOG.md) |

---

## 📂 Repository Anatomy

```text
Utility/
├── 🚢 Driver Deck/      # Flagship Driver management and build system
├── 🧶 ETL Weaver/       # High-speed diagnostic trace analysis engine
├── .gitignore           # Global exclude rules for build artifacts and backups
├── GEMINI.md            # Master status record and global release workflow
└── README.md            # Suite entrance and project matrix (this file)
```

## 🏗️ Architecture & Standards

- **[Unified Release System](./GEMINI.md)**: Standardized `release.bat` ensures 100% binary integrity and automated documentation.
- **Modern UI Architecture**: Built with `sv-ttk` for a native Windows 11 Fluent Design experience.
- **Industrial Stability**: Includes advanced Win32 focus management and high-process-priority execution.

---

## 🛠️ Global Requirements

- **OS**: Windows 10/11 (x64 Required).
- **Toolchain**: Visual Studio 2022 + WDK (for driver-related features).
- **Environment**: Python 3.10+ with `pip install sv-ttk tkinterdnd2 psutil`.

---

## 👨‍💻 Developer Guide
To deploy a new version of any component:
1. Commit your functional changes.
2. Navigate to the project's `scripts/` folder.
3. Run `release.bat`.

---
*Internal Engineering Toolset - Realtek Semiconductor Corp.*