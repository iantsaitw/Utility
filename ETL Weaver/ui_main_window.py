# ui_main_window.py
# Main application window, UI layout, and event handling.

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import tkinter.font as tkfont
import os
import sys
import threading
import platform
import ctypes
import queue
import re
import math

from tkinterdnd2 import DND_FILES, TkinterDnD
import psutil
import sv_ttk

# Import from our own modules
from config import (
    APP_VERSION, SHOW_SYSTEM_INFO, APP_TITLE, load_settings, save_settings
)
from utils import resource_path, get_executable_dir, format_size
import core_logic

class TextSplitterApp(TkinterDnD.Tk):
    def __init__(self, show_sys_info=SHOW_SYSTEM_INFO):
        if platform.system() == "Windows":
            myappid = f'mycompany.textsplitter.pro.{APP_VERSION}'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        super().__init__()
        
        # Load persisted settings
        self.settings = load_settings()
        
        self.show_sys_info = show_sys_info
        
        # UI Variables
        self.etl_path = tk.StringVar(value="")
        self.pdb_path = tk.StringVar(value="")
        self.txt_path = tk.StringVar(value="")
        self.original_size = tk.StringVar(value="N/A")
        self.split_size_value = tk.StringVar(value="30")
        self.split_size_unit = tk.StringVar(value="MB")
        self.estimated_files = tk.StringVar(value="N/A")
        self.status = tk.StringVar(value="Ready to process files")
        self.txt_postfix = tk.StringVar(value="")
        self.pdb_search_path = tk.StringVar()
        self.found_pdb_files = []
        
        if self.show_sys_info:
            self.cpu_details_text = tk.StringVar(value="0.0 %")
            self.mem_details_text = tk.StringVar(value="0.0 % (0.0 GB / 0.0 GB)")

        self.log_queue = queue.Queue()
        self.log_text = None 
        self.pdb_listbox = None

        # Set Theme
        sv_ttk.set_theme(self.settings["theme"])
        
        self.title(APP_TITLE)
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass
        
        self.initial_width = 950
        initial_height = 800
        self.geometry(f"{self.initial_width}x{initial_height}")
        self.resizable(True, True)
        self.minsize(800, 600)

        self.create_widgets()
        self.update_styles()
        self.after_idle(self._initialize_app)

    def _initialize_app(self):
        self._reset_pdb_path()
        if self.show_sys_info:
            self.update_system_info()
        self.process_log_queue()

    def update_styles(self):
        theme = self.settings["theme"]
        ui_font = (self.settings["ui_font_family"], self.settings["ui_font_size"])
        log_font = (self.settings["log_font_family"], self.settings["log_font_size"])
        
        style = ttk.Style()
        style.configure(".", font=ui_font)
        style.configure("TLabel", font=ui_font)
        style.configure("TButton", font=ui_font)
        style.configure("TEntry", font=ui_font)
        style.configure("TCombobox", font=ui_font)
        style.configure("TLabelframe.Label", font=(self.settings["ui_font_family"], self.settings["ui_font_size"], "bold"))
        
        if theme == "dark":
            style.configure("Card.TFrame", background="#2b2b2b", relief="solid", borderwidth=0)
            style.configure("Secondary.TFrame", background="#202020")
            style.configure("Secondary.TLabel", background="#202020", foreground="#aaaaaa")
        else:
            style.configure("Card.TFrame", background="#ffffff", relief="solid", borderwidth=0)
            style.configure("Secondary.TFrame", background="#f3f3f3")
            style.configure("Secondary.TLabel", background="#f3f3f3", foreground="#666666")
        
        if self.log_text:
            self.log_text.configure(font=log_font)
            if theme == "dark":
                self.log_text.configure(bg="#1c1c1c", fg="#e0e0e0", insertbackground="white")
            else:
                self.log_text.configure(bg="#ffffff", fg="#000000", insertbackground="black")

        if self.pdb_listbox:
            self.pdb_listbox.configure(font=ui_font)
            if theme == "dark":
                self.pdb_listbox.configure(bg="#2b2b2b", fg="#ffffff")
            else:
                self.pdb_listbox.configure(bg="#f5f5f5", fg="#000000")

    def refresh_ui(self):
        log_content = self.log_text.get("1.0", tk.END) if self.log_text else ""
        for widget in self.winfo_children():
            if isinstance(widget, tk.Toplevel): continue
            widget.destroy()
        self.create_widgets()
        self.update_styles()
        self._reset_pdb_path()
        if log_content.strip() and self.log_text:
            self.log_text.config(state="normal")
            self.log_text.insert(tk.END, log_content)
            self.log_text.config(state="disabled")

    def create_widgets(self):
        # 1. Status Bar (Fixed at Bottom)
        status_bar = ttk.Frame(self, padding=(12, 3), style="Secondary.TFrame")
        status_bar.pack(side="bottom", fill="x")
        ttk.Label(status_bar, textvariable=self.status, font=(self.settings["ui_font_family"], 8, "italic"), style="Secondary.TLabel").pack(side="left")
        ttk.Label(status_bar, text=f"v{APP_VERSION}", font=(self.settings["ui_font_family"], 8), style="Secondary.TLabel").pack(side="right")

        # 2. Main Scrollable Container (Fills middle)
        main_container = ttk.Frame(self, padding=(20, 10, 20, 10))
        main_container.pack(side="top", fill="both", expand=True)
        main_container.columnconfigure(0, weight=1)

        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(header_frame, text=APP_TITLE, font=(self.settings["ui_font_family"], 16, "bold")).pack(side="left")
        
        ttk.Button(header_frame, text="⚙ Settings", width=12, command=self.open_settings_dialog).pack(side="right", padx=(10, 0))
        
        if self.show_sys_info:
            sys_info_mini = ttk.Frame(header_frame)
            sys_info_mini.pack(side="right")
            ttk.Label(sys_info_mini, text="CPU:", font=(self.settings["ui_font_family"], 8)).pack(side="left", padx=(10, 2))
            ttk.Label(sys_info_mini, textvariable=self.cpu_details_text, font=(self.settings["ui_font_family"], 8, "bold")).pack(side="left")
            ttk.Label(sys_info_mini, text="RAM:", font=(self.settings["ui_font_family"], 8)).pack(side="left", padx=(10, 2))
            ttk.Label(sys_info_mini, textvariable=self.mem_details_text, font=(self.settings["ui_font_family"], 8, "bold")).pack(side="left")

        # Workspace
        workspace = ttk.Frame(main_container)
        workspace.grid(row=1, column=0, sticky="nsew")
        workspace.columnconfigure(0, weight=6)
        workspace.columnconfigure(1, weight=4)
        workspace.rowconfigure(0, weight=1)

        left_col = ttk.Frame(workspace)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_col.columnconfigure(0, weight=1)

        right_col = ttk.Frame(workspace)
        right_col.grid(row=0, column=1, sticky="nsew")
        right_col.columnconfigure(0, weight=1)
        right_col.rowconfigure(0, weight=1)

        self.create_drop_zone(left_col).grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.create_file_info_panel(left_col).grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.create_txt_settings_panel(left_col).grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.create_action_buttons(left_col).grid(row=3, column=0, sticky="ew", pady=(5, 0))

        self.create_pdb_browser_panel(right_col).grid(row=0, column=0, sticky="nsew")

        # Log
        self.create_log_panel(main_container).grid(row=2, column=0, sticky="nsew", pady=(15, 0))
        main_container.rowconfigure(2, weight=1)

    def create_drop_zone(self, parent):
        drop_card = ttk.Frame(parent, padding=1, style="Card.TFrame")
        drop_card.drop_target_register(DND_FILES)
        drop_card.dnd_bind('<<Drop>>', self.handle_drop)
        inner = ttk.Frame(drop_card, padding=15)
        inner.pack(fill="both", expand=True)
        inner.columnconfigure(1, weight=1)
        ttk.Label(inner, text="📂", font=("Segoe UI Symbol", 28)).grid(row=0, column=0, rowspan=2, padx=(0, 15))
        ttk.Label(inner, text="Drag & Drop files here", font=(self.settings["ui_font_family"], 11, "bold")).grid(row=0, column=1, sticky="w")
        ttk.Label(inner, text="Supports .etl, .pdb, and .txt files", font=(self.settings["ui_font_family"], 9)).grid(row=1, column=1, sticky="w")
        return drop_card

    def create_file_info_panel(self, parent):
        info_frame = ttk.LabelFrame(parent, text=" File Path Information ", padding=12)
        info_frame.columnconfigure(1, weight=1)
        labels = [("ETL:", self.etl_path), ("PDB:", self.pdb_path), ("TXT:", self.txt_path)]
        for i, (label, var) in enumerate(labels):
            ttk.Label(info_frame, text=label).grid(row=i, column=0, sticky="e", padx=(0, 8), pady=4)
            ttk.Entry(info_frame, textvariable=var, state="readonly").grid(row=i, column=1, sticky="ew", pady=4)
        return info_frame

    def create_txt_settings_panel(self, parent):
        sf = ttk.LabelFrame(parent, text=" TXT Setting ", padding=12)
        sf.columnconfigure((0, 1, 2, 3), weight=1)
        
        # --- Left Side: Rename & Info ---
        ttk.Label(sf, text="Postfix:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Entry(sf, textvariable=self.txt_postfix).grid(row=0, column=1, sticky="ew", pady=6, padx=(0, 20))

        ttk.Label(sf, text="Size:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(sf, textvariable=self.original_size, font=(self.settings["ui_font_family"], 9, "bold")).grid(row=1, column=1, sticky="w")
        
        # --- Right Side: Split Settings ---
        ttk.Label(sf, text="Split Size:").grid(row=0, column=2, sticky="e", padx=(0, 8), pady=6)
        si = ttk.Frame(sf)
        si.grid(row=0, column=3, sticky="w")
        ttk.Entry(si, textvariable=self.split_size_value, width=8).pack(side="left", padx=(0, 5))
        ucb = ttk.Combobox(si, textvariable=self.split_size_unit, values=["KB", "MB"], width=5, state="readonly")
        ucb.pack(side="left")
        ucb.bind("<<ComboboxSelected>>", self.update_estimated_files)
        
        ttk.Label(sf, text="Est. Parts:").grid(row=1, column=2, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(sf, textvariable=self.estimated_files, font=(self.settings["ui_font_family"], 9, "bold")).grid(row=1, column=3, sticky="w")
        return sf

    def create_pdb_browser_panel(self, parent):
        pf = ttk.LabelFrame(parent, text=" PDB Symbol Browser ", padding=12)
        pf.columnconfigure(0, weight=1)
        pf.rowconfigure(2, weight=1)
        ttk.Label(pf, text="Search Path:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        sr = ttk.Frame(pf)
        sr.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        sr.columnconfigure(0, weight=1)
        ttk.Entry(sr, textvariable=self.pdb_search_path).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(sr, text="Scan", width=6, command=self._scan_pdb_from_entry).grid(row=0, column=1)
        lc = ttk.Frame(pf)
        lc.grid(row=2, column=0, sticky="nsew")
        lc.columnconfigure(0, weight=1)
        lc.rowconfigure(0, weight=1)
        sb = ttk.Scrollbar(lc, orient="vertical")
        self.pdb_listbox = tk.Listbox(lc, yscrollcommand=sb.set, borderwidth=0, highlightthickness=0)
        self.pdb_listbox.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")
        sb.config(command=self.pdb_listbox.yview)
        self.pdb_listbox.bind("<Double-1>", self._on_pdb_select)
        ttk.Button(pf, text="Reset to Default Path", command=self._reset_pdb_path).grid(row=3, column=0, sticky="ew", pady=(10, 0))
        return pf

    def create_action_buttons(self, parent):
        af = ttk.Frame(parent)
        af.columnconfigure((0, 1, 2, 3), weight=1)
        
        self.convert_button = ttk.Button(af, text="Convert ETL", style="Accent.TButton", command=self.start_conversion_thread, state="disabled")
        self.convert_button.grid(row=0, column=0, sticky="ew", ipady=8, padx=(0, 5))
        
        self.split_button = ttk.Button(af, text="Split TXT", command=self.start_split_thread, state="disabled")
        self.split_button.grid(row=0, column=1, sticky="ew", ipady=8, padx=(5, 5))
        
        self.rename_button = ttk.Button(af, text="Rename TXT", command=self.rename_txt_file, state="disabled")
        self.rename_button.grid(row=0, column=2, sticky="ew", ipady=8, padx=(5, 5))
        
        self.open_folder_button = ttk.Button(af, text="Open Folder", command=self._open_txt_folder, state="disabled")
        self.open_folder_button.grid(row=0, column=3, sticky="ew", ipady=8, padx=(5, 0))
        return af

    def _update_button_states(self):
        tr = self.etl_path.get() and self.pdb_path.get()
        self.convert_button.config(state="normal" if tr else "disabled")
        sr = self.txt_path.get() and os.path.exists(self.txt_path.get())
        self.split_button.config(state="normal" if sr else "disabled")
        self.rename_button.config(state="normal" if sr else "disabled")
        self.open_folder_button.config(state="normal" if sr else "disabled")

    def create_log_panel(self, parent):
        lf = ttk.LabelFrame(parent, text=" Command Execution Log ", padding=12)
        lf.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)
        self.log_text = scrolledtext.ScrolledText(lf, wrap=tk.WORD, state="disabled", borderwidth=0, highlightthickness=0)
        self.log_text.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        br = ttk.Frame(lf)
        br.grid(row=1, column=0, sticky="e")
        ttk.Button(br, text="Save Log", command=self._save_log).pack(side="left", padx=5)
        ttk.Button(br, text="Clear Log", command=self.clear_log).pack(side="left")
        return lf

    def open_settings_dialog(self):
        sw = tk.Toplevel(self)
        sw.title("Settings")
        sw.geometry("480x480")
        sw.resizable(False, False)
        sw.transient(self)
        sw.grab_set()
        
        try:
            sw.iconbitmap(resource_path("icon.ico"))
        except: pass

        sw.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (sw.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (sw.winfo_height() // 2)
        sw.geometry(f"+{x}+{y}")

        container = ttk.Frame(sw, padding=20)
        container.pack(fill="both", expand=True)
        container.columnconfigure(1, weight=1)

        p = {"padx": 10, "pady": 8}
        ttk.Label(container, text="Theme:").grid(row=0, column=0, sticky="w", **p)
        tv = tk.StringVar(value=self.settings.get("theme", "dark"))
        ttk.Combobox(container, textvariable=tv, values=["dark", "light"], state="readonly").grid(row=0, column=1, sticky="ew", **p)
        
        fonts = sorted(tkfont.families())
        ttk.Label(container, text="UI Font Family:").grid(row=1, column=0, sticky="w", **p)
        fv = tk.StringVar(value=self.settings.get("ui_font_family", "Segoe UI"))
        ttk.Combobox(container, textvariable=fv, values=fonts, state="readonly").grid(row=1, column=1, sticky="ew", **p)
        
        ttk.Label(container, text="UI Font Size:").grid(row=2, column=0, sticky="w", **p)
        sv = tk.IntVar(value=self.settings.get("ui_font_size", 10))
        ttk.Spinbox(container, from_=8, to=24, textvariable=sv).grid(row=2, column=1, sticky="ew", **p)
        
        ttk.Label(container, text="Default PDB Path:").grid(row=3, column=0, sticky="w", **p)
        path_frame = ttk.Frame(container)
        path_frame.grid(row=3, column=1, sticky="ew", **p)
        path_frame.columnconfigure(0, weight=1)
        
        pv = tk.StringVar(value=self.settings.get("pdb_path", "C:\\"))
        ttk.Entry(path_frame, textvariable=pv).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        def b_pdb():
            path = filedialog.askdirectory(initialdir=pv.get())
            if path: pv.set(path)
        ttk.Button(path_frame, text="Browse", width=8, command=b_pdb).grid(row=0, column=1, sticky="e")
        
        def save():
            self.settings.update({
                "theme": tv.get(), 
                "ui_font_family": fv.get(), 
                "ui_font_size": sv.get(), 
                "pdb_path": pv.get()
            })
            save_settings(self.settings)
            sv_ttk.set_theme(self.settings["theme"])
            sw.destroy()
            self.refresh_ui()
            self.status.set("Settings applied.")
            
        br = ttk.Frame(container)
        br.grid(row=5, column=0, columnspan=2, pady=(30, 0))
        ttk.Button(br, text="Save Settings", style="Accent.TButton", command=save, width=15).pack(side="left", padx=5)
        ttk.Button(br, text="Cancel", command=sw.destroy, width=10).pack(side="left", padx=5)

    def _reset_pdb_path(self):
        dp = self.settings.get("pdb_path")
        if not dp or not os.path.isdir(dp):
            dp = os.path.join(get_executable_dir(), 'symbol')
        self.pdb_search_path.set(dp)
        self._scan_pdb_folder(dp)

    def _scan_pdb_from_entry(self):
        self._scan_pdb_folder(self.pdb_search_path.get())

    def _scan_pdb_folder(self, folder_path):
        if not self.pdb_listbox: return
        self.pdb_listbox.delete(0, tk.END)
        self.found_pdb_files.clear()
        if not os.path.isdir(folder_path):
            self.pdb_listbox.insert(tk.END, "Folder not found.")
            return
        try:
            for f in sorted(os.listdir(folder_path)):
                if f.lower().endswith(".pdb"):
                    self.pdb_listbox.insert(tk.END, f)
                    self.found_pdb_files.append(os.path.join(folder_path, f))
            if not self.found_pdb_files: self.pdb_listbox.insert(tk.END, "No .pdb found.")
        except Exception as e: self.pdb_listbox.insert(tk.END, f"Error: {e}")

    def _on_pdb_select(self, event):
        sel = self.pdb_listbox.curselection()
        if sel and 0 <= sel[0] < len(self.found_pdb_files):
            path = self.found_pdb_files[sel[0]]
            self.pdb_path.set(path)
            self.status.set(f"Selected PDB: {os.path.basename(path)}")
            self._update_button_states()

    def _open_txt_folder(self):
        tp = self.txt_path.get()
        if tp and os.path.exists(tp):
            try: os.startfile(os.path.dirname(tp))
            except Exception as e: self.show_message("Error", str(e))

    def _save_log(self):
        content = self.log_text.get("1.0", tk.END)
        if not content.strip(): return
        fp = filedialog.asksaveasfilename(defaultextension=".txt")
        if fp:
            try:
                with open(fp, 'w', encoding='utf-8') as f: f.write(content)
            except Exception as e: self.show_message("Error", str(e))

    def clear_log(self):
        if self.log_text:
            self.log_text.config(state="normal")
            self.log_text.delete('1.0', tk.END)
            self.log_text.config(state="disabled")

    def log_message(self, message): self.log_queue.put(message)

    def process_log_queue(self):
        if self.log_text:
            try:
                while True:
                    line = self.log_queue.get_nowait()
                    self.log_text.config(state="normal")
                    self.log_text.insert(tk.END, line)
                    self.log_text.see(tk.END)
                    self.log_text.config(state="disabled")
            except queue.Empty: pass
        self.after(100, self.process_log_queue)

    def start_conversion_thread(self):
        self.log_message("\n--- Starting ETL Conversion ---\n")
        self.convert_button.config(state="disabled")
        self.split_button.config(state="disabled")
        self.status.set("Converting...")
        cb = { 
            'log': self.log_message, 
            'status': lambda m: self.after(0, self.status.set, m), 
            'success': lambda p: self.after(0, self.process_txt_file, p), 
            'failure': lambda m: self.after(0, self.status.set, m) 
        }
        threading.Thread(target=core_logic.run_conversion, args=(self.etl_path.get(), self.pdb_path.get(), self.txt_postfix.get(), cb), daemon=True).start()

    def update_system_info(self):
        if not self.show_sys_info: return
        cpu = psutil.cpu_percent()
        self.cpu_details_text.set(f"{cpu:.1f} %")
        mem = psutil.virtual_memory()
        self.mem_details_text.set(f"{mem.percent:.1f} % ({format_size(mem.used)} / {format_size(mem.total)})")
        self.after(2000, self.update_system_info)

    def handle_drop(self, event):
        for path in self.tk.splitlist(event.data):
            if path.lower().endswith(".pdb"): self.pdb_path.set(path)
            elif path.lower().endswith(".txt"): self.process_txt_file(path)
            elif re.search(r'\.etl(\.\d+)?$', path, re.IGNORECASE): self.etl_path.set(path)
        self._update_button_states()

    def process_txt_file(self, path):
        self.txt_path.set(path)
        self.update_estimated_files()
        self._update_button_states()
        
    def update_estimated_files(self, event=None):
        tp = self.txt_path.get()
        if not tp or not os.path.exists(tp):
            self.original_size.set("N/A"); self.estimated_files.set("N/A")
            return
        try:
            sz = os.path.getsize(tp)
            self.original_size.set(format_size(sz))
            ssz = int(self.split_size_value.get())
            u = self.split_size_unit.get()
            sb = (ssz * 1024) if u == "KB" else (ssz * 1024 * 1024)
            self.estimated_files.set(str(math.ceil(sz / sb)) if sb > 0 else "N/A")
        except: self.estimated_files.set("N/A")

    def start_split_thread(self):
        self.split_button.config(state="disabled")
        self.status.set("Splitting...")
        cb = { 'log': self.log_message, 'status': lambda m: self.after(0, self.status.set, m), 'success': lambda m: self.show_message("Success", m), 'failure': lambda m: self.show_message("Error", m) }
        try:
            sv = int(self.split_size_value.get())
            ef = int(self.estimated_files.get()) if self.estimated_files.get().isdigit() else 1
            threading.Thread(target=core_logic.run_file_splitting, args=(self.txt_path.get(), sv, self.split_size_unit.get(), ef, self.txt_postfix.get(), cb), daemon=True).start()
        except: self.show_message("Error", "Invalid input")

    def rename_txt_file(self):
        old_path = self.txt_path.get()
        postfix = self.txt_postfix.get().strip()
        if not old_path or not os.path.exists(old_path): return
        if not postfix:
            self.show_message("Warning", "Please enter a postfix first.")
            return
            
        try:
            directory = os.path.dirname(old_path)
            base, ext = os.path.splitext(os.path.basename(old_path))
            if base.endswith(f"_{postfix}"):
                self.show_message("Info", "File already has this postfix.")
                return
            new_name = f"{base}_{postfix}{ext}"
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            self.txt_path.set(new_path)
            self.log_message(f"SUCCESS: Renamed to {new_name}\n")
            self.status.set("File renamed.")
        except Exception as e:
            self.show_message("Error", f"Rename failed: {e}")

    def show_message(self, title, message):
        if "error" in title.lower(): messagebox.showerror(title, message)
        else: messagebox.showinfo(title, message)
