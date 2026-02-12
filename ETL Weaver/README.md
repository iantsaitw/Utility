# 🧶 ETL Weaver
> High-precision diagnostic engine for Windows Event Trace Log analysis.

[![Version](https://img.shields.io/github/v/tag/iantsaitw/Utility?filter=ETL_Weaver-v*&label=stable&color=green&style=for-the-badge)](https://github.com/iantsaitw/Utility/releases)
[![Core](https://img.shields.io/badge/Engine-TraceView%20Stable-blue?style=for-the-badge)](./trace_tools/)
[![Feature](https://img.shields.io/badge/New-Postfix%20Support-orange?style=for-the-badge)](./CHANGELOG.md)

**ETL Weaver** is a high-speed diagnostic utility designed to transform raw ETL traces into structured analysis. It focuses on data integrity, bypassing common truncation bugs found in modern tools.

---

## 💎 Features

### 🛡️ Legacy Stability, Modern Power
- **Reliable Core**: Bundles verified Microsoft `traceview.exe` to ensure zero data loss.
- **Drag & Drop**: Native integration for lightning-fast ETL and PDB loading.
- **High Priority**: Executes conversion tasks with elevated process priority.

### 📝 Smart TXT Management
- **Postfix Engine**: Add custom suffixes to outputs automatically.
- **Instant Rename**: Dedicated logic to apply postfix renaming to existing logs.
- **Dual-Column Settings**: Balanced UI for fine-grained splitting control.

---

## 📂 Project Architecture

```text
ETL Weaver/
├── scripts/             # Automation hub (build.bat, release.bat)
├── trace_tools/         # Bundled verified MS trace binaries
├── dist/                # Production binaries (ETLWeaver.exe)
├── release/             # Local versioned archives (Git ignored)
├── main.py              # Application entry point
├── ui_main_window.py    # Win11 Fluent UI and logic orchestration
├── core_logic.py        # Conversion, Splitting, and Renaming algorithms
├── config.py            # App settings and dynamic VERSION handling
├── utils.py             # Path helpers and data formatting
├── VERSION              # Version source of truth
└── icon.ico             # Application branding
```

---

## 🚀 Quick Start

### 📦 For Users (Portable EXE)
1. Download `ETLWeaver.exe` from [Latest Releases](https://github.com/iantsaitw/Utility/releases).
2. Load your **ETL** and corresponding **PDB** files.
3. Click **Convert** to generate analyzed output.

### ⌨️ For Developers (Source)
```powershell
pip install sv-ttk tkinterdnd2 psutil
python main.py
```

---

## 📜 Roadmap & History
View the complete history of feature additions in [CHANGELOG.md](./CHANGELOG.md).

---
*Status: Production Ready | v1.1.0*