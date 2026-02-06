import os

# Application Info
APP_NAME = "Driver Deck"

# Read version from VERSION file
try:
    with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r") as f:
        APP_VERSION = f"v{f.read().strip()}"
except Exception:
    APP_VERSION = "v1.0.0"

# UI Colors
COLOR_BG = "#2b2b2b"
COLOR_FG = "#ffffff"
COLOR_ACCENT = "#0078d4"