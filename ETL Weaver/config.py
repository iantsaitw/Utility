import os

# Application Info
APP_NAME = "ETL Weaver"

# Read version from VERSION file
try:
    with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r") as f:
        APP_VERSION = f.read().strip()
except Exception:
    APP_VERSION = "1.0.0"

# Theme
THEME_DEFAULT = "dark"
PDB_PATH_DEFAULT = "C:\\"
