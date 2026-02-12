# 🧶 ETL Weaver
> High-precision diagnostic engine for Windows Event Trace Log analysis.

[![Version](https://img.shields.io/github/v/tag/iantsaitw/Utility?filter=ETL_Weaver-v*&label=stable&color=green&style=for-the-badge)](https://github.com/iantsaitw/Utility/releases)
[![Core](https://img.shields.io/badge/Engine-TraceView%20Stable-blue?style=for-the-badge)](./trace_tools/)
[![Feature](https://img.shields.io/badge/New-Postfix%20Support-orange?style=for-the-badge)](./CHANGELOG.md)

**ETL Weaver** is a high-speed diagnostic utility designed to transform raw ETL traces into structured analysis. It focuses on data integrity, bypassing common truncation bugs found in modern tools.

---

## 📸 Screenshots
*(Showcase the conversion feedback and the side-by-side settings panel)*

---

## 💎 Features

### 🛡️ Legacy Stability, Modern Power
- **Reliable Core**: Bundles verified Microsoft `traceview.exe` to ensure zero data loss.
- **Drag & Drop**: Native integration for ETL, PDB, and TXT files.
- **High Priority**: Executes conversion tasks with elevated process priority.

### 📝 Smart TXT Management
- **Postfix Engine**: Add custom suffixes to outputs automatically.
- **Instant Rename**: Apply postfix renaming to existing logs with one click.
- **Precision Splitting**: Split massive TXT files into manageable chunks.

---

## 🔍 Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **Conversion Error** | Ensure the **PDB** matches the exact version of the ETL trace. |
| **Garbled Text** | The tool uses UTF-8; ensure your viewer supports it (e.g., VS Code). |
| **Empty Log List** | Use the "Scan" button to refresh the PDB Symbol Browser. |
| **App won't start** | Install dependencies: `pip install sv-ttk tkinterdnd2 psutil`. |

---

## 📂 Project Architecture

```text
ETL Weaver/
├── scripts/             # Automation hub (build.bat, release.bat)
├── trace_tools/         # Bundled verified MS trace binaries (TraceView, TraceFmt)
├── dist/                # Production binaries (ETLWeaver.exe)
├── release/             # Local versioned archives (Git ignored)
├── main.py              # Application entry point
├── ui_main_window.py    # Win11 Fluent UI and logic orchestration
├── core_logic.py        # Conversion, Splitting, and Renaming algorithms
├── config.py            # App settings and dynamic VERSION handling
├── utils.py             # Path helpers and data formatting
├── VERSION              # Version source of truth (Bump this for release)
└── icon.ico             # Application branding
```

---

## 🚀 Quick Start

### 📦 For Users (Portable EXE)
1. Download `ETLWeaver.exe` from [Latest Releases](https://github.com/iantsaitw/Utility/releases).
2. Load your **ETL** and corresponding **PDB** files via drag & drop.
3. Click **Convert** to generate analyzed output.

---
*Status: Production Ready | v1.1.0*