# 🛳️ Driver Deck

**Driver Deck** is a high-performance GUI utility engineered for Windows PCIE/USB driver management. It centralizes project scanning, build orchestration, and digital signing into a single, cohesive interface.

---

## ✨ Key Capabilities

### 🖥️ Integrated Win32 Terminal
Unlike standard text-based terminals, Driver Deck implements low-level **Win32 window embedding**. It hosts an actual VS 2022 Developer Console directly within the Tkinter frame, providing:
- **Zero Latency**: Native shell performance.
- **Robust Focus**: Advanced `AttachThreadInput` logic for seamless keyboard handling.
- **Tab-Completion**: Full shell-level path completion support.

### 🏗️ Build & Signing Orchestration
- **Project Auto-Discovery**: Smart scanning of PCIE and USB driver directories.
- **WDK Integration**: Automated environment detection for Visual Studio 2022.
- **Security-First Signing**: Integrated `signtool.exe` workflow with PFX certificate management.

### 📦 Workflow Automation
- **Atomic Backups**: One-click timestamped source archival.
- **Direct Export**: Simplified extraction of `.sys` binaries and package folders.

---

## 🛠️ Technical Stack

- **Core**: Python 3.10+
- **UI Framework**: Tkinter + `sv-ttk` (Windows 11 Immersive Design)
- **APIs**: Win32 API (via `ctypes`) for window management and focus control.
- **Packaging**: Customized PyInstaller workflow with resource lock avoidance.

---

## 🚀 Quick Start

1. **Install Dependencies**:
   ```powershell
   pip install sv-ttk
   ```
2. **Launch**:
   ```powershell
   python main.py
   ```
3. **Build Binary**:
   Run `build.bat` for a production-ready executable.

---

## 📜 Version History
Detailed version history and changes are documented in [CHANGELOG.md](./CHANGELOG.md).

---
*License: Internal Tool - Realtek Semiconductor Corp.*