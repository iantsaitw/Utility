import ctypes
import os
import sys

# 啟用 DPI 意識
try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

import tkinter as tk
from tkinter import ttk, filedialog
from ctypes import c_int, byref, sizeof
import sv_ttk 
import config 
from project_tab import ProjectTab
from terminal_widget import TerminalFrame
from utils import resource_path
from settings_dialog import SettingsDialog 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        
        self.is_admin = self.check_admin()
        
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.APP_ID)
        except: pass

        self.title(f"{config.APP_NAME} {'(Administrator)' if self.is_admin else ''}")
        self.geometry("1400x850") 
        
        try:
            self.update()
            hwnd = ctypes.windll.user32.GetAncestor(self.winfo_id(), 2)
            value = c_int(2) 
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(value), sizeof(value))
        except: pass

        icon_file = resource_path("icon.ico")
        if os.path.exists(icon_file):
            try: self.iconbitmap(icon_file)
            except: pass

        self.root_dir = config.current_settings.get("root_dir", r"E:\Project")
        
        self.setup_theme()
        self.setup_ui()
        
        self.after(100, self._finalize_startup)

    def check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def _finalize_startup(self):
        # 6:4 比例 (1400 * 0.6 = 840)
        self.main_paned.sashpos(0, 840)
        self.scan_projects()
        self.deiconify()

    def setup_theme(self):
        mode = config.current_settings.get("theme_mode", "Dark").lower()
        sv_ttk.set_theme(mode)
        self.apply_font_styles()

    def apply_font_styles(self):
        font_fam = config.current_settings.get("font_family", "Segoe UI")
        font_size = 9
        self.style = ttk.Style()
        self.style.configure(".", font=(font_fam, font_size))
        self.style.configure("Treeview", rowheight=30, font=(font_fam, font_size))
        self.style.configure("Treeview.Heading", font=(font_fam, font_size, "bold"))
        self.style.configure("TButton", font=(font_fam, font_size))
        self.style.configure("TNotebook.Tab", font=(font_fam, font_size))
        self.style.configure("TLabelframe.Label", font=(font_fam, font_size, "bold"))
        self.style.configure("Bold.TLabel", font=(font_fam, font_size, "bold"))

    def setup_ui(self):
        self.top_bar = ttk.Frame(self, padding=20)
        self.top_bar.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(self.top_bar, text="Root Path:", style="Bold.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        self.root_entry = ttk.Entry(self.top_bar)
        self.root_entry.insert(0, self.root_dir)
        self.root_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        ttk.Button(self.top_bar, text="Browse", command=self.browse_root).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(self.top_bar, text="Scan Projects", command=self.scan_projects).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.top_bar, text="Settings", command=self.open_settings).pack(side=tk.LEFT, padx=5)

        self.status_bar = ttk.Frame(self, padding=(10, 5))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Label(self.status_bar, text=f"{config.APP_VERSION}").pack(side=tk.RIGHT)
        self.status_msg = tk.StringVar(value="Ready")
        ttk.Label(self.status_bar, textvariable=self.status_msg).pack(side=tk.LEFT)

        self.main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # 左側：專案分頁區塊
        self.notebook = ttk.Notebook(self.main_paned)
        self.main_paned.add(self.notebook, weight=6)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # 右側：終端機區塊
        term_container = ttk.Frame(self.main_paned)
        self.main_paned.add(term_container, weight=4)
        
        # [修改] 終端機初始目錄直接使用 Root Path
        term_dir = self.root_dir if os.path.exists(self.root_dir) else os.getcwd()
        self.terminal = TerminalFrame(term_container, term_dir)
        self.terminal.pack(fill=tk.BOTH, expand=True)

    def sync_terminal_dir(self, path):
        """ 移除同步切換邏輯，僅更新狀態列 """
        if os.path.exists(path):
            self.status_msg.set(f"Selected: {os.path.basename(path)}")

    def on_tab_changed(self, event):
        try:
            selected_tab_id = self.notebook.select()
            if not selected_tab_id: return
            tab_text = self.notebook.tab(selected_tab_id, "text")
            config.save_settings({"last_tab": tab_text})
            widget = self.nametowidget(selected_tab_id)
            if hasattr(widget, "refresh_export_path"): widget.refresh_export_path()
            if hasattr(widget, "sync_filter_ui"): widget.sync_filter_ui()
        except: pass

    def browse_root(self):
        d = filedialog.askdirectory()
        if d:
            self.root_entry.delete(0, tk.END)
            self.root_entry.insert(0, d)
            config.save_settings({"root_dir": d})
            self.root_dir = d # 更新記憶體中的路徑
            self.scan_projects()

    def open_settings(self):
        SettingsDialog(self, callback=self.reload_ui)

    def reload_ui(self):
        config.load_settings()
        self.setup_theme()
        self.scan_projects()
        self.status_msg.set("Settings applied.")

    def scan_projects(self):
        root_path = self.root_entry.get()
        if not root_path or not os.path.exists(root_path): return
        for tab in self.notebook.tabs(): self.notebook.forget(tab)
        self.status_msg.set(f"Scanning {root_path}...")
        self.update_idletasks()
        count = 0
        last_tab = config.current_settings.get("last_tab", "")
        try:
            items = os.listdir(root_path)
            items.sort()
            for item in items:
                full_path = os.path.join(root_path, item)
                if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, config.TARGET_BATCH_FILE)):
                    tab = ProjectTab(self.notebook, full_path, app_root=self)
                    self.notebook.add(tab, text=item)
                    count += 1
        except: pass
        self.status_msg.set(f"Found {count} projects.")
        if last_tab:
            for tab_id in self.notebook.tabs():
                if self.notebook.tab(tab_id, "text") == last_tab:
                    self.notebook.select(tab_id)
                    break
        
        # 啟動終端機 (如果尚未啟動)
        if not self.terminal.cmd_hwnd:
            self.terminal.start_embedded_cmd()

if __name__ == "__main__":
    app = App()
    app.mainloop()