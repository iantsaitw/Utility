# utils.py
# Helper functions for path management and data formatting.

import os
import sys
import math

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_executable_dir():
    """ Get the directory of the executable, works for dev and for PyInstaller. """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.abspath(".")

def format_size(size_bytes):
    """ Formats a size in bytes to a human-readable string. """
    if size_bytes == 0: return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB")
    i = int(math.floor(math.log(size_bytes, 1024))) if size_bytes > 0 else 0
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    unit = size_name[i] if i < len(size_name) else 'PB'
    return f"{s} {unit}"