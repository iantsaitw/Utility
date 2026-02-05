# config.py
import os
import json

# ==========================================
# [使用者設定區]
# ==========================================
APP_NAME = "Driver Deck"
APP_VERSION = "v5.3.1 (Clean Config)"

APP_ID = f"mycompany.tools.{APP_NAME.replace(' ', '').lower()}.v5_3"

SETTINGS_FILE = "settings.json"
TARGET_BATCH_FILE = "setenv-for-windows-msbuild-system.bat"

# 定義分類與路徑
DRIVER_PATHS = {
    "PCIE": [
        "RTLWlanE_WindowsDriver_(WithSymbol)",
        "RTLWlanE_WindowsDriver_"
    ],
    "USB": [
        "RTLWlanU_WindowsDriver_(WithSymbol)",
        "RTLWlanU_WindowsDriver_"
    ]
}

DEFAULT_SETTINGS = {
    "theme_mode": "Dark",
    "font_family": "Segoe UI",
    "accent_color": "#4db6ac",
    "root_dir": r"E:\Project",
    "export_dir": "",
    "pfx_path": "",
    "signtool_path": "",
    "last_tab": "",
    "filter_mode": "All",
    "split_ratio": 0.6  # [新增] 預設分割比例 (0.6 代表上方佔 60%)
}

current_settings = DEFAULT_SETTINGS.copy()

# === 全域變數 ===
COLOR_BG_DARK = "#1e1e1e"
COLOR_BG_LIGHT = "#252526"
COLOR_FG = "#d4d4d4"
COLOR_BTN_TEXT = "#ffffff"
COLOR_BTN_BG = "#3c3c3c"
COLOR_HEADER_BG = "#333333"
COLOR_HEADER_FG = "#ffffff"
COLOR_HEADER_BORDER = "#2d2d2d"

COLOR_SCROLL_BG = "#3e3e42"
COLOR_SCROLL_BG_HOVER = "#686868"
COLOR_SCROLL_TROUGH = "#1e1e1e"
COLOR_SCROLL_ARROW = "#999999"

COLOR_ACCENT = "#4db6ac"
COLOR_ACCENT_HOVER = "#80cbc4"

FONT_UI = ("Segoe UI", 9)
FONT_BOLD = ("Segoe UI", 9, "bold")
FONT_LARGE = ("Segoe UI", 11, "bold")

def load_settings():
    global current_settings
    global COLOR_BG_DARK, COLOR_BG_LIGHT, COLOR_FG
    global COLOR_BTN_TEXT, COLOR_BTN_BG
    global COLOR_HEADER_BG, COLOR_HEADER_FG, COLOR_HEADER_BORDER
    global COLOR_SCROLL_BG, COLOR_SCROLL_BG_HOVER, COLOR_SCROLL_TROUGH, COLOR_SCROLL_ARROW
    global COLOR_ACCENT, COLOR_ACCENT_HOVER
    global FONT_UI, FONT_BOLD, FONT_LARGE

    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                current_settings.update(data)
                
                if "last_scan_mode" in current_settings:
                    del current_settings["last_scan_mode"]
                    
        except: pass

    for key, value in DEFAULT_SETTINGS.items():
        if key not in current_settings:
            current_settings[key] = value

    if current_settings["theme_mode"] == "Light":
        COLOR_BG_DARK = "#f0f0f0"
        COLOR_BG_LIGHT = "#ffffff"
        COLOR_FG = "#333333"
        COLOR_BTN_TEXT = "#333333"
        COLOR_BTN_BG = "#e0e0e0"
        
        COLOR_HEADER_BG = "#e1e1e1"
        COLOR_HEADER_FG = "#000000"
        COLOR_HEADER_BORDER = "#cccccc"
        
        COLOR_SCROLL_BG = "#cdcdcd"
        COLOR_SCROLL_BG_HOVER = "#a6a6a6"
        COLOR_SCROLL_TROUGH = "#f0f0f0"
        COLOR_SCROLL_ARROW = "#666666"
    else:
        COLOR_BG_DARK = "#1e1e1e"
        COLOR_BG_LIGHT = "#252526"
        COLOR_FG = "#d4d4d4"
        COLOR_BTN_TEXT = "#ffffff"
        COLOR_BTN_BG = "#333333"
        
        COLOR_HEADER_BG = "#111111"
        COLOR_HEADER_FG = "#cccccc"
        COLOR_HEADER_BORDER = "#2d2d2d"
        
        COLOR_SCROLL_BG = "#424242"
        COLOR_SCROLL_BG_HOVER = "#4f4f4f"
        COLOR_SCROLL_TROUGH = "#252526"
        COLOR_SCROLL_ARROW = "#d4d4d4"

    COLOR_ACCENT = current_settings["accent_color"]
    COLOR_ACCENT_HOVER = COLOR_ACCENT 

    font_fam = current_settings["font_family"]
    FONT_UI = (font_fam, 9)
    FONT_BOLD = (font_fam, 9, "bold")
    FONT_LARGE = (font_fam, 11, "bold")

def save_settings(new_settings):
    global current_settings
    current_settings.update(new_settings)
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(current_settings, f, indent=4)
    except: pass
    load_settings()

load_settings()