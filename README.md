# Driver Deck

Driver Deck is a modern GUI utility designed for managing and building Windows PCIE/USB drivers. It provides a unified interface to scan driver projects, integrate with the VS 2022 build environment, and handle digital signatures.

## Features

- **Modern UI**: Built with Python and Tkinter, featuring the `sv-ttk` theme for a Windows 11 look and feel (supporting Dark/Light modes).
- **Integrated Terminal**: Built-in VS 2022 Developer Console with Win32-level embedding and robust focus management.
- **Project Management**: Automatic scanning of driver projects with categorized views (PCIE/USB).
- **Digital Signing**: Seamless integration with `signtool.exe` using PFX certificates.
- **Workflow Tools**: One-click backup with timestamps and easy export of folders or `.sys` files.
- **Persistent Settings**: Local storage of configurations like PFX paths and root directories.

## Prerequisites

- **OS**: Windows 10/11
- **Python**: 3.10 or higher
- **Build Tools**: Visual Studio 2022 (Professional/Community/Enterprise) with C++ build components.
- **Dependencies**: 
  ```bash
  pip install sv-ttk
  ```

## Usage

### Running from Source
To start the application in a development environment:
```bash
python main.py
```

### Building the Executable
A provided `build.bat` script handles the PyInstaller packaging process. It uses a temporary-rename strategy to bypass Windows file locks and ensures resources (manifests/icons) are correctly embedded.
```bash
./build.bat
```
The output will be located in the `dist/` directory.

## Project Structure

- `main.py`: Application entry point and layout management.
- `terminal_widget.py`: Win32 logic for embedding the CMD window and handling keyboard focus.
- `project_tab.py`: Logic for project tabs, file lists, and driver operations.
- `driver_utils.py`: Helpers for file versions, signatures, and environment pathing.
- `config.py`: Global constants, color definitions, and settings persistence.
- `ui_factory.py`: Standardized widget creation engine.

## License
Internal Tool - Realtek Semiconductor Corp.
