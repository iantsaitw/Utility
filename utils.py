import os
import sys

def resource_path(relative_path):
    """ 
    Get the absolute path to a resource.
    Supports both standard development environments and frozen PyInstaller executables (_MEIPASS).
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
