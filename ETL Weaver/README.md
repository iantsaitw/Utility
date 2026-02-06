# 🧶 ETL Weaver

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

1. **Environment**: Ensure Python 3.10+ is installed.
2. **Library**:
   ```powershell
   pip install sv-ttk
   ```
3. **Run**:
   ```powershell
   python main.py
   ```

---
*License: Internal Tool - Realtek Semiconductor Corp.*