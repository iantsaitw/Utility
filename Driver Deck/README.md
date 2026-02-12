# 🚢 Driver Deck
> Industrial-grade Windows Driver management and build orchestration.

[![Version](https://img.shields.io/github/v/tag/iantsaitw/Utility?filter=Driver_Deck-v*&label=stable&color=green&style=for-the-badge)](https://github.com/iantsaitw/Utility/releases)
[![Build](https://img.shields.io/badge/Build-Optimized-blue?style=for-the-badge&logo=python)](./scripts/build.bat)
[![UI](https://img.shields.io/badge/Design-Win11%20Fluent-0078d4?style=for-the-badge&logo=windows11)](https://github.com/rdbende/Sun-Valley-ttk)

**Driver Deck** is a high-performance GUI utility engineered for kernel developers. It centralizes project scanning, environment setup, and signing into a single, cohesive workflow.

---

## 📸 Screenshots
*(Add your latest UI screenshots here to showcase the Windows 11 design)*

---

## ✨ Key Capabilities

### 🖥️ Immersive Terminal (Win32 Embedded)
*The heart of Driver Deck.* It hosts an actual VS 2022 Developer Console directly within the UI:
- **Zero Latency**: Real-time native shell performance.
- **Color Support**: Powered by `wt.exe` for full ANSI rendering.
- **Focus Guard**: Proprietary Win32 focus recovery prevents terminal lock-ups.

### 🏗️ Build & Environment
- **Project Intelligence**: Auto-scans and categorizes PCIE/USB driver trees.
- **One-Click Signing**: Seamless integration with `signtool.exe` and PFX management.
- **Category Filter**: Instant toggle between PCIE, USB, and Symbol/No Symbol views.

---

## 🔍 Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **Terminal is blank/empty** | Ensure you run the application as **Administrator**. |
| **Cannot type in Suffix box** | Click anywhere on the UI to break the terminal's focus lock. |
| **Missing VS Environment** | Ensure Visual Studio 2022 is installed in the default directory. |
| **SignTool not found** | Install the Windows SDK or specify the path in `settings.json`. |

---

## 📂 Project Architecture

```text
Driver Deck/
├── scripts/             # Automation hub (build.bat, release.bat)
├── dist/                # Production binaries (DriverDeck.exe)
├── release/             # Local versioned archives (Git ignored)
├── main.py              # Application entry and window orchestration
├── terminal_widget.py   # Low-level Win32 window embedding & focus logic
├── project_tab.py       # Driver lifecycle logic and UI tab management
├── config.py            # Dynamic settings and versioning (VERSION sync)
├── driver_utils.py      # Win32 versioning and SignTool helpers
├── ui_factory.py        # Modular Win11-themed widget factory
├── VERSION              # Single source of truth for versioning (Bump this for release)
└── icon.ico             # High-DPI application branding
```

---

## 🚀 Quick Start

### 📦 For Users (Portable EXE)
1. Download `DriverDeck.exe` from [Latest Releases](https://github.com/iantsaitw/Utility/releases).
2. **Run as Administrator** (Required for terminal and driver access).

### ⌨️ For Developers (Source)
```powershell
# Clone and install
pip install sv-ttk

# Launch
python main.py
```

---
*Status: Production Ready | v1.2.1*