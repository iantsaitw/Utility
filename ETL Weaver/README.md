# 🧶 ETL Weaver

[![Version](https://img.shields.io/github/v/tag/iantsaitw/Utility?filter=ETL_Weaver-v*&label=version&color=green)](https://github.com/iantsaitw/Utility/releases)
[![License](https://img.shields.io/badge/License-Internal-blue.svg)](https://github.com/iantsaitw/Utility)
[![Download](https://img.shields.io/badge/Download-EXE-orange.svg)](https://github.com/iantsaitw/Utility/releases)

**ETL Weaver** is a specialized diagnostic utility designed to transform raw Windows Event Trace Logs (ETL) into human-readable analysis. It focuses on data integrity, high-speed conversion, and a modern user experience.

---

## 💎 Features

### 🛡️ Rock-Solid Reliability
- **Legacy Stability**: Bundles a verified version of `traceview.exe` to bypass truncation and encoding bugs found in newer WDK versions.
- **Hybrid Engine**: Supports both stable legacy conversion and high-speed modern `tracefmt.exe` (WDK 2025) workflows.

### 🎨 Modern Analytical UI
- **Live Theming**: Instant switching between Dark and Light modes using the `sv-ttk` engine.
- **Personalized Workspace**: Persistent configuration for typography and default PDB symbol paths.
- **Thread-Safe Logging**: Real-time conversion feedback without UI freezing.

### ⚡ Performance Optimized
- **Process Elevation**: Automatically executes conversion tasks with high process priority.
- **Streamlined Workflow**: Minimizes manual steps from raw trace to formatted log.

---

## 📂 Project Architecture

- `ui_main_window.py`: Orchestrates the complex UI state and event loop.
- `core_logic.py`: Manages the lifecycle of external WDK tool processes.
- `trace_tools/`: A curated collection of stable and experimental Microsoft trace utilities.
- `config.py`: JSON-based settings management with live-apply capabilities.

---

## 🛠️ Setup

### For Users (Binary)
1. Download the latest `ETL Weaver.exe` from [Releases](https://github.com/iantsaitw/Utility/releases).
2. Ensure you have the necessary PDB files for symbol resolution.

### For Developers (Source)
1. **Environment**: Ensure Python 3.10+ is installed.
2. **Library**:
   ```powershell
   pip install sv-ttk tkinterdnd2 psutil
   ```
3. **Run**:
   ```powershell
   python main.py
   ```

---

## 📜 Version History
Detailed version history and changes are documented in [CHANGELOG.md](./CHANGELOG.md).

---
*License: Internal Tool - Realtek Semiconductor Corp.*
