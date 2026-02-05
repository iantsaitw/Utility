# settings_dialog.py
import tkinter as tk
from tkinter import ttk, colorchooser, font, filedialog
import os
import config
from utils import resource_path

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Settings")
        self.geometry("450x520") # 再拉高一點
        self.resizable(False, False)
        
        icon_file = resource_path("icon.ico")
        if os.path.exists(icon_file):
            try: self.iconbitmap(icon_file)
            except: pass
        
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        self.load_current_values()
        
        self.center_window(parent)

    def center_window(self, parent):
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (450 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (520 // 2)
        self.geometry(f"+{x}+{y}")

    def setup_ui(self):
        self.configure(bg=config.COLOR_BG_DARK)
        
        main_frame = ttk.Frame(self, padding=25) 
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_font = (config.FONT_UI[0], 11, "bold")
        normal_font = config.FONT_UI
        
        # 1. UI Theme
        ttk.Label(main_frame, text="Theme Mode", font=title_font).pack(anchor="w", pady=(0, 5))
        self.theme_var = tk.StringVar()
        self.theme_combo = ttk.Combobox(main_frame, textvariable=self.theme_var, values=["Dark", "Light"], state="readonly", font=normal_font)
        self.theme_combo.pack(fill=tk.X, pady=(0, 15))

        # 2. Font
        ttk.Label(main_frame, text="Font Family", font=title_font).pack(anchor="w", pady=(0, 5))
        self.font_var = tk.StringVar()
        try: fonts = sorted(list(font.families()))
        except: fonts = ["Segoe UI", "Arial", "Consolas"]
        self.font_combo = ttk.Combobox(main_frame, textvariable=self.font_var, values=fonts, state="readonly", font=normal_font)
        self.font_combo.pack(fill=tk.X, pady=(0, 15))

        # 3. Accent Color
        ttk.Label(main_frame, text="Accent Color", font=title_font).pack(anchor="w", pady=(0, 5))
        color_frame = ttk.Frame(main_frame)
        color_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.color_entry = ttk.Entry(color_frame, font=normal_font)
        self.color_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=3)
        self.pick_btn = ttk.Button(color_frame, text="Pick", width=6, command=self.pick_color)
        self.pick_btn.pack(side=tk.LEFT)

        # 4. PFX Path
        ttk.Label(main_frame, text="PFX Certificate Path", font=title_font).pack(anchor="w", pady=(0, 5))
        pfx_frame = ttk.Frame(main_frame)
        pfx_frame.pack(fill=tk.X, pady=(0, 15))
        self.pfx_entry = ttk.Entry(pfx_frame, font=normal_font)
        self.pfx_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=3)
        self.pfx_browse_btn = ttk.Button(pfx_frame, text="Browse", width=8, command=self.browse_pfx)
        self.pfx_browse_btn.pack(side=tk.LEFT)

        # 5. [新增] SignTool Path
        ttk.Label(main_frame, text="SignTool.exe Path (Optional)", font=title_font).pack(anchor="w", pady=(0, 5))
        st_frame = ttk.Frame(main_frame)
        st_frame.pack(fill=tk.X, pady=(0, 15))
        self.st_entry = ttk.Entry(st_frame, font=normal_font)
        self.st_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=3)
        self.st_browse_btn = ttk.Button(st_frame, text="Browse", width=8, command=self.browse_signtool)
        self.st_browse_btn.pack(side=tk.LEFT)

        # Bottom
        spacer = ttk.Frame(main_frame)
        spacer.pack(fill=tk.Y, expand=True)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        ttk.Button(btn_frame, text="Apply & Save", style="Accent.TButton", command=self.save_and_close).pack(side=tk.RIGHT)

    def load_current_values(self):
        self.theme_var.set(config.current_settings.get("theme_mode", "Dark"))
        self.font_var.set(config.current_settings.get("font_family", "Segoe UI"))
        self.color_entry.delete(0, tk.END)
        self.color_entry.insert(0, config.current_settings.get("accent_color", "#4db6ac"))
        
        self.pfx_entry.delete(0, tk.END)
        self.pfx_entry.insert(0, config.current_settings.get("pfx_path", ""))
        
        # Load SignTool
        self.st_entry.delete(0, tk.END)
        self.st_entry.insert(0, config.current_settings.get("signtool_path", ""))

    def pick_color(self):
        color = colorchooser.askcolor(initialcolor=self.color_entry.get(), parent=self)
        if color[1]:
            self.color_entry.delete(0, tk.END)
            self.color_entry.insert(0, color[1])
            self.focus_force()

    def browse_pfx(self):
        f = filedialog.askopenfilename(filetypes=[("PFX Files", "*.pfx"), ("All Files", "*.*")])
        if f:
            self.pfx_entry.delete(0, tk.END)
            self.pfx_entry.insert(0, f)
            self.focus_force()

    def browse_signtool(self):
        f = filedialog.askopenfilename(filetypes=[("Executable", "signtool.exe"), ("All Files", "*.*")])
        if f:
            self.st_entry.delete(0, tk.END)
            self.st_entry.insert(0, f)
            self.focus_force()

    def save_and_close(self):
        new_settings = {
            "theme_mode": self.theme_var.get(),
            "font_family": self.font_var.get(),
            "accent_color": self.color_entry.get(),
            "pfx_path": self.pfx_entry.get(),
            "signtool_path": self.st_entry.get()
        }
        config.save_settings(new_settings)
        if self.callback:
            self.callback()
        self.destroy()