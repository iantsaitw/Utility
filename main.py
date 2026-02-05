# main.py
import tkinter as tk
from tkinter import ttk, filedialog
import ctypes
from ctypes import c_int, byref, sizeof
import os
import sys
import sv_ttk 
import config 
from project_tab import ProjectTab
from utils import resource_path
from settings_dialog import SettingsDialog 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.APP_ID)
        except: pass

        self.title(config.APP_NAME)
        # [修改] 視窗高度設為 950
        self.geometry("1000x850") 
        
        # [Win11] Immersive Dark Mode
        try:
            self.update()
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = c_int(2) 
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, byref(value), sizeof(value))
        except: pass

        icon_file = resource_path("icon.ico")
        if os.path.exists(icon_file):
            try: self.iconbitmap(icon_file)
            except: pass

        self.root_dir = config.current_settings.get("root_dir", r"E:\Project")
        
        # 初始化主題與字體
        self.setup_theme()
        
        self.setup_ui()
        self.after(200, self.scan_projects)

    def setup_theme(self):
        # 1. 套用 sv-ttk 主題
        mode = config.current_settings.get("theme_mode", "Dark").lower()
        sv_ttk.set_theme(mode)
        
        # 2. 套用使用者自訂字體到 Style
        self.apply_font_styles()

    def apply_font_styles(self):
        """ 將 config 中的字體套用到 ttk.Style """
        font_fam = config.current_settings.get("font_family", "Segoe UI")
        self.style = ttk.Style()
        
        # 設定全域字體
        self.style.configure(".", font=(font_fam, 9))
        
        # 設定 Treeview 列表字體與行高
        self.style.configure("Treeview", rowheight=30, font=(font_fam, 9))
        self.style.configure("Treeview.Heading", font=(font_fam, 9, "bold"))
        
        # 設定按鈕字體
        self.style.configure("TButton", font=(font_fam, 9))
        self.style.configure("Accent.TButton", font=(font_fam, 9, "bold"))
        
        # 設定 LabelFrame 標題字體
        self.style.configure("TLabelframe.Label", font=(font_fam, 9, "bold"))

        # [字體修正] 設定 Tab 分頁標籤的字體
        self.style.configure("TNotebook.Tab", font=(font_fam, 9))

        # [字體修正] 設定粗體 Label 樣式 (給 Root Path 用)
        self.style.configure("Bold.TLabel", font=(font_fam, 9, "bold"))

    def setup_ui(self):
        # 1. Top Bar
        self.top_bar = ttk.Frame(self, padding=20)
        self.top_bar.pack(side=tk.TOP, fill=tk.X)
        
        # [字體修正] 套用 Bold.TLabel 樣式
        ttk.Label(self.top_bar, text="Root Path:", style="Bold.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        
        self.root_entry = ttk.Entry(self.top_bar)
        self.root_entry.insert(0, self.root_dir)
        self.root_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        
        ttk.Button(self.top_bar, text="Browse", command=self.browse_root).pack(side=tk.LEFT, padx=(10, 5))
        
        # [按鈕修正] 移除 style="Accent.TButton"，改回預設灰色按鈕
        ttk.Button(self.top_bar, text="Scan Projects", command=self.scan_projects).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.top_bar, text="Settings", command=self.open_settings).pack(side=tk.LEFT, padx=5)

        self.status_bar = ttk.Frame(self, padding=(10, 5))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        ttk.Label(self.status_bar, text=f"{config.APP_VERSION}").pack(side=tk.RIGHT)
        self.status_msg = tk.StringVar(value="Ready")
        ttk.Label(self.status_bar, textvariable=self.status_msg).pack(side=tk.LEFT)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

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
        if not os.path.exists(root_path):
            self.status_msg.set(f"Path not found: {root_path}")
            return

        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
            
        self.status_msg.set(f"Scanning {root_path}...")
        self.update_idletasks()
        
        count = 0
        last_tab = config.current_settings.get("last_tab", "")
        
        try:
            items = os.listdir(root_path)
            items.sort()
            for item in items:
                full_path = os.path.join(root_path, item)
                if os.path.isdir(full_path):
                    target_file = os.path.join(full_path, config.TARGET_BATCH_FILE)
                    if os.path.exists(target_file):
                        tab = ProjectTab(self.notebook, full_path)
                        self.notebook.add(tab, text=item)
                        count += 1
        except Exception as e:
            self.status_msg.set(f"Error: {e}")
            return

        if count == 0:
            self.status_msg.set("No projects found.")
        else:
            self.status_msg.set(f"Found {count} projects.")
            if last_tab:
                for tab_id in self.notebook.tabs():
                    if self.notebook.tab(tab_id, "text") == last_tab:
                        self.notebook.select(tab_id)
                        break

if __name__ == "__main__":
    app = App()
    app.mainloop()