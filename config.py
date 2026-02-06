# config.py
# Application configuration settings with persistence support.

import json
import os

APP_VERSION = "25.0905"
SHOW_SYSTEM_INFO = True
APP_TITLE = "ETL Weaver"
APP_NAME = "ETL Weaver"

# --- Default Configuration ---
DEFAULT_SETTINGS = {
    "ui_font_family": "Segoe UI",
    "ui_font_size": 9,
    "log_font_family": "Consolas",
    "log_font_size": 9,
    "theme": "dark",
    "default_pdb_path": ""  # If empty, use 'symbol' folder in app dir
}

SETTINGS_FILE = "settings.json"

def get_settings_path():
    """Returns the path to the settings file in the application directory."""
    from utils import get_executable_dir
    return os.path.join(get_executable_dir(), SETTINGS_FILE)

def load_settings():
    """Loads settings from the JSON file or returns defaults."""
    path = get_settings_path()
    settings = DEFAULT_SETTINGS.copy()
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                settings.update(loaded)
        except Exception:
            pass
    return settings

def save_settings(settings):
    """Saves the settings to the JSON file."""
    path = get_settings_path()
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4)
    except Exception:
        pass

# Initial load of settings
current_settings = load_settings()

# --- Exported Configuration Variables ---
UI_FONT_FAMILY = current_settings.get("ui_font_family")
UI_FONT_SIZE = current_settings.get("ui_font_size")
LOG_FONT_FAMILY = current_settings.get("log_font_family")
LOG_FONT_SIZE = current_settings.get("log_font_size")
THEME = current_settings.get("theme")
DEFAULT_PDB_PATH = current_settings.get("default_pdb_path")