# ETL Weaver

ETL Weaver is a modern GUI utility designed for viewing and converting Windows Event Trace Log (ETL) files. It streamlines the workflow of transforming raw ETL data into human-readable formats using established Windows debugging tools.

## Features

- **Modern UI**: Clean and intuitive interface built with Python and Tkinter, supporting theme customization (Dark/Light).
- **Stable Conversion**: Utilizes a bundled, stable version of `traceview.exe` to ensure data integrity and prevent common truncation or encoding issues.
- **Flexible Tooling**: Includes both legacy `traceview.exe` and modern `tracefmt.exe` (WDK 2025) to cater to different performance and compatibility needs.
- **Persistent Configuration**: Save your UI preferences (font, theme) and default PDB search paths across sessions.
- **Live UI Refresh**: Update application themes and fonts instantly without restarting the tool or losing your current logs.
- **Performance Optimized**: Conversion processes are executed with high priority to minimize wait times for large log files.

## Prerequisites

- **OS**: Windows 10/11
- **Python**: 3.10 or higher
- **Dependencies**: 
  ```bash
  pip install sv-ttk
  ```

## Usage

### Running from Source
```bash
python main.py
```

### Building the Executable
A `build.bat` script is provided for packaging the application with PyInstaller.
```bash
./build.bat
```

## Project Structure

- `main.py`: Entry point for the application.
- `ui_main_window.py`: Core UI logic including settings and conversion workflows.
- `core_logic.py`: Standardized ETL conversion logic using bundled tools.
- `config.py`: Management of configuration settings and JSON persistence.
- `trace_tools/`: Directory containing `traceview.exe`, `tracefmt.exe`, and documentation.

## License
Internal Tool - Realtek Semiconductor Corp.
