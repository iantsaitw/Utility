# main.py
# Main entry point for the application.

import sys
import os

# Ensure the directory containing this script is in the search path
# This helps PyInstaller find bundled modules correctly.
if getattr(sys, 'frozen', False):
    current_dir = sys._MEIPASS
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from ui_main_window import TextSplitterApp

if __name__ == "__main__":
    app = TextSplitterApp()
    app.mainloop()
