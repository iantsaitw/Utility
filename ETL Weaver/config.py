import os
import json
import sys

# Application Info
APP_NAME = "ETLWeaver"
APP_TITLE = "ETL Weaver"
SHOW_SYSTEM_INFO = True

# Read version from VERSION file
try:
    with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r") as f:
        APP_VERSION = f.read().strip()
except Exception:
    APP_VERSION = "1.0.0"

def get_settings_path():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "settings.json")

DEFAULT_SETTINGS = {
    "theme": "dark",
    "ui_font_family": "Segoe UI",
    "ui_font_size": 10,
    "log_font_family": "Consolas",
    "log_font_size": 10,
    "pdb_path": "C:\\"
}

def load_settings():
    path = get_settings_path()
    settings = DEFAULT_SETTINGS.copy()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                settings.update(data)
        except Exception:
            pass
    return settings

def save_settings(settings):
    path = get_settings_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Failed to save settings: {e}")
