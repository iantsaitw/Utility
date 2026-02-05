# ui_main_window.py
# Main application window, UI layout, and event handling.
# This version adds support for multi-part ETL file naming (e.g., .etl.001).

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import os
import sys
import threading
import platform
import ctypes
import queue
import re # Import regular expressions module

from tkinterdnd2 import DND_FILES, TkinterDnD
import psutil
import sv_ttk

# Import from our own modules
from config import APP_VERSION, SHOW_SYSTEM_INFO, APP_TITLE, UI_FONT_FAMILY, UI_FONT_SIZE, LOG_FONT_FAMILY, LOG_FONT_SIZE
from utils import resource_path, get_executable_dir, format_size
import core_logic

class TextSplitterApp(TkinterDnD.Tk):
    def __init__(self, show_sys_info=SHOW_SYSTEM_INFO):
        if platform.system() == "Windows":
            myappid = f'mycompany.textsplitter.pro.{APP_VERSION}'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        super().__init__()
        
        self.show_sys_info = show_sys_info
        self.default_font = (UI_FONT_FAMILY, UI_FONT_SIZE)
        self.log_font = (LOG_FONT_FAMILY, LOG_FONT_SIZE)

        # Force Dark Theme
        theme = "dark"
        sv_ttk.set_theme(theme)
        
        style = ttk.Style()
        style.configure(".", font=self.default_font)
        style.configure("TLabel", font=self.default_font)
        style.configure("TButton", font=self.default_font)
        
        # --- Modern Custom Styles ---
        # Card style for sections
        if theme == "dark":
            style.configure("Card.TFrame", background="#2b2b2b", relief="solid", borderwidth=0)
            style.configure("Secondary.TFrame", background="#202020")
            style.configure("Secondary.TLabel", background="#202020", foreground="#aaaaaa")
        else:
            style.configure("Card.TFrame", background="#ffffff", relief="solid", borderwidth=0)
            style.configure("Secondary.TFrame", background="#f3f3f3")
            style.configure("Secondary.TLabel", background="#f3f3f3", foreground="#666666")
        
        self.title(APP_TITLE)
        
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass
        
        # Tool-centric compact size
        self.initial_width = 950
        initial_height = 800
        self.geometry(f"{self.initial_width}x{initial_height}")
        self.resizable(True, True)
        self.minsize(800, 600)

        # (Variable definitions)
        self.etl_path = tk.StringVar(value="")
        self.pdb_path = tk.StringVar(value="")
        self.txt_path = tk.StringVar(value="")
        self.original_size = tk.StringVar(value="N/A")
        self.split_size_value = tk.StringVar(value="30")
        self.split_size_unit = tk.StringVar(value="MB")
        self.estimated_files = tk.StringVar(value="N/A")
        self.status = tk.StringVar(value="Ready to process files")
        self.pdb_search_path = tk.StringVar()
        self.found_pdb_files = []
        
        if self.show_sys_info:
            self.cpu_details_text = tk.StringVar(value="0.0 %")
            self.mem_details_text = tk.StringVar(value="0.0 % (0.0 GB / 0.0 GB)")

        self.log_queue = queue.Queue()
        self.log_text = None 
        
        self.create_widgets()
        self.after_idle(self._initialize_app)

    def _initialize_app(self):
        self._reset_pdb_path()
        if self.show_sys_info:
            self.update_system_info()
        
        self.process_log_queue()

    def create_widgets(self):
        # Main Scrollable Container
        main_container = ttk.Frame(self, padding=(20, 10, 20, 10))
        main_container.pack(fill="both", expand=True)
        main_container.columnconfigure(0, weight=1)

        # 1. Header Area (Compact)
        header_frame = ttk.Frame(main_container)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(header_frame, text=APP_TITLE, font=(UI_FONT_FAMILY, 16, "bold")).pack(side="left")
        
        if self.show_sys_info:
            sys_info_mini = ttk.Frame(header_frame)
            sys_info_mini.pack(side="right")
            ttk.Label(sys_info_mini, text="CPU:", font=(UI_FONT_FAMILY, 8)).pack(side="left", padx=(10, 2))
            ttk.Label(sys_info_mini, textvariable=self.cpu_details_text, font=(UI_FONT_FAMILY, 8, "bold")).pack(side="left")
            ttk.Label(sys_info_mini, text="RAM:", font=(UI_FONT_FAMILY, 8)).pack(side="left", padx=(10, 2))
            ttk.Label(sys_info_mini, textvariable=self.mem_details_text, font=(UI_FONT_FAMILY, 8, "bold")).pack(side="left")

        # 2. Main Workspace (Split into two columns)
        workspace = ttk.Frame(main_container)
        workspace.grid(row=1, column=0, sticky="nsew")
        workspace.columnconfigure(0, weight=6) # Left for core flow
        workspace.columnconfigure(1, weight=4) # Right for PDB selection
        workspace.rowconfigure(0, weight=1)

        left_column = ttk.Frame(workspace)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_column.columnconfigure(0, weight=1)

        right_column = ttk.Frame(workspace)
        right_column.grid(row=0, column=1, sticky="nsew")
        right_column.columnconfigure(0, weight=1)
        right_column.rowconfigure(0, weight=1)

        # --- Left Side: Workflow ---
        # Drop Zone
        self.create_drop_zone(left_column).grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # File Info Card
        self.create_file_info_panel(left_column).grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Split Settings Card
        self.create_split_settings_panel(left_column).grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        # Action Buttons
        self.create_action_buttons(left_column).grid(row=3, column=0, sticky="ew", pady=(5, 0))

        # --- Right Side: PDB Browser ---
        self.create_pdb_browser_panel(right_column).grid(row=0, column=0, sticky="nsew")

        # 3. Log Panel (Bottom)
        self.create_log_panel(main_container).grid(row=2, column=0, sticky="nsew", pady=(15, 0))
        main_container.rowconfigure(2, weight=1)

        # 4. Status Bar
        status_bar = ttk.Frame(self, padding=(12, 3), style="Secondary.TFrame")
        status_bar.pack(side="bottom", fill="x")
        ttk.Label(status_bar, textvariable=self.status, font=(UI_FONT_FAMILY, 8, "italic"), style="Secondary.TLabel").pack(side="left")
        ttk.Label(status_bar, text=f"v{APP_VERSION}", font=(UI_FONT_FAMILY, 8), style="Secondary.TLabel").pack(side="right")

    def create_drop_zone(self, parent):
        drop_card = ttk.Frame(parent, padding=1, style="Card.TFrame")
        drop_card.drop_target_register(DND_FILES)
        drop_card.dnd_bind('<<Drop>>', self.handle_drop)
        
        inner = ttk.Frame(drop_card, padding=15)
        inner.pack(fill="both", expand=True)
        inner.columnconfigure(1, weight=1)
        
        ttk.Label(inner, text="📂", font=("Segoe UI Symbol", 28)).grid(row=0, column=0, rowspan=2, padx=(0, 15))
        ttk.Label(inner, text="Drag & Drop files here", font=(UI_FONT_FAMILY, 11, "bold")).grid(row=0, column=1, sticky="w")
        ttk.Label(inner, text="Supports .etl, .pdb, and .txt files", font=(UI_FONT_FAMILY, 9)).grid(row=1, column=1, sticky="w")
        
        return drop_card

    def _create_sys_info_panel(self, parent):
        sys_info_frame = ttk.LabelFrame(parent, text=" System Monitor ", padding=12)
        sys_info_frame.columnconfigure(0, weight=1)
        
        # CPU
        cpu_row = ttk.Frame(sys_info_frame)
        cpu_row.pack(fill="x", pady=(0, 8))
        ttk.Label(cpu_row, text="CPU Load", font=(UI_FONT_FAMILY, 9)).pack(side="left")
        ttk.Label(cpu_row, textvariable=self.cpu_details_text, font=(UI_FONT_FAMILY, 9, "bold")).pack(side="right")
        self.cpu_progressbar = ttk.Progressbar(sys_info_frame, mode='determinate')
        self.cpu_progressbar.pack(fill="x", pady=(0, 5))
        
        # Memory
        mem_row = ttk.Frame(sys_info_frame)
        mem_row.pack(fill="x", pady=(8, 8))
        ttk.Label(mem_row, text="Memory Usage", font=(UI_FONT_FAMILY, 9)).pack(side="left")
        ttk.Label(mem_row, textvariable=self.mem_details_text, font=(UI_FONT_FAMILY, 9, "bold")).pack(side="right")
        self.mem_progressbar = ttk.Progressbar(sys_info_frame, mode='determinate')
        self.mem_progressbar.pack(fill="x")
        
        return sys_info_frame

    def create_file_info_panel(self, parent):
        info_frame = ttk.LabelFrame(parent, text=" File Information ", padding=12)
        info_frame.columnconfigure(1, weight=1)
        
        labels = [("ETL Path:", self.etl_path), ("PDB Path:", self.pdb_path), ("TXT Path:", self.txt_path)]
        for i, (label, var) in enumerate(labels):
            ttk.Label(info_frame, text=label).grid(row=i, column=0, sticky="e", padx=(0, 8), pady=4)
            entry = ttk.Entry(info_frame, textvariable=var, state="readonly")
            entry.grid(row=i, column=1, sticky="ew", pady=4)
            
        return info_frame

    def create_split_settings_panel(self, parent):
        settings_frame = ttk.LabelFrame(parent, text=" TXT Split Settings ", padding=12)
        settings_frame.columnconfigure(1, weight=1)
        
        ttk.Label(settings_frame, text="Original Size:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(settings_frame, textvariable=self.original_size, font=(UI_FONT_FAMILY, 9, "bold")).grid(row=0, column=1, sticky="w")
        
        ttk.Label(settings_frame, text="Split Size:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=6)
        size_input = ttk.Frame(settings_frame)
        size_input.grid(row=1, column=1, sticky="w")
        ttk.Entry(size_input, textvariable=self.split_size_value, width=8).pack(side="left", padx=(0, 5))
        unit_cb = ttk.Combobox(size_input, textvariable=self.split_size_unit, values=["KB", "MB"], width=5, state="readonly")
        unit_cb.pack(side="left")
        unit_cb.bind("<<ComboboxSelected>>", self.update_estimated_files)
        
        ttk.Label(settings_frame, text="Estimated Files:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(settings_frame, textvariable=self.estimated_files, font=(UI_FONT_FAMILY, 9, "bold")).grid(row=2, column=1, sticky="w")
        
        return settings_frame

    def create_pdb_browser_panel(self, parent):
        pdb_frame = ttk.LabelFrame(parent, text=" PDB Symbol Browser ", padding=12)
        pdb_frame.columnconfigure(0, weight=1)
        pdb_frame.rowconfigure(2, weight=1)
        
        # Search area
        ttk.Label(pdb_frame, text="Search Path:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        search_row = ttk.Frame(pdb_frame)
        search_row.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        search_row.columnconfigure(0, weight=1)
        ttk.Entry(search_row, textvariable=self.pdb_search_path).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(search_row, text="Scan", width=6, command=self._scan_pdb_from_entry).grid(row=0, column=1)
        
        # Listbox area
        list_container = ttk.Frame(pdb_frame)
        list_container.grid(row=2, column=0, sticky="nsew")
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)
        
        sb = ttk.Scrollbar(list_container, orient="vertical")
        self.pdb_listbox = tk.Listbox(list_container, yscrollcommand=sb.set, font=self.default_font, 
                                     borderwidth=0, highlightthickness=0, bg="#2b2b2b" if theme=="dark" else "#f5f5f5",
                                     fg="#ffffff" if theme=="dark" else "#000000")
        self.pdb_listbox.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")
        sb.config(command=self.pdb_listbox.yview)
        
        self.pdb_listbox.bind("<Double-1>", self._on_pdb_select)
        
        ttk.Button(pdb_frame, text="Reset to Default", command=self._reset_pdb_path).grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        return pdb_frame

    def create_action_buttons(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.columnconfigure((0, 1, 2), weight=1)
        
        self.traceview_button = ttk.Button(action_frame, text="Traceview Convert", style="Accent.TButton", command=self.start_traceview_thread, state="disabled")
        self.traceview_button.grid(row=0, column=0, sticky="ew", ipady=8, padx=(0, 5))
        
        self.split_button = ttk.Button(action_frame, text="Split TXT File", command=self.start_split_thread, state="disabled")
        self.split_button.grid(row=0, column=1, sticky="ew", ipady=8, padx=(5, 5))
        
        self.open_folder_button = ttk.Button(action_frame, text="Open Output Folder", command=self._open_txt_folder, state="disabled")
        self.open_folder_button.grid(row=0, column=2, sticky="ew", ipady=8, padx=(5, 0))
        
        return action_frame

    def create_log_panel(self, parent):
        log_frame = ttk.LabelFrame(parent, text=" Execution Log Output ", padding=12)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state="disabled", font=self.log_font,
                                                borderwidth=0, highlightthickness=0)
        self.log_text.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        btn_row = ttk.Frame(log_frame)
        btn_row.grid(row=1, column=0, sticky="e")
        ttk.Button(btn_row, text="Save Log", command=self._save_log).pack(side="left", padx=5)
        ttk.Button(btn_row, text="Clear Log", command=self.clear_log).pack(side="left")
        
        return log_frame

    def _create_sys_info_panel(self, parent):
        sys_info_frame = ttk.LabelFrame(parent, text=" System Monitor ", padding=12)
        sys_info_frame.columnconfigure(0, weight=1)
        
        # CPU
        cpu_row = ttk.Frame(sys_info_frame)
        cpu_row.pack(fill="x", pady=(0, 8))
        ttk.Label(cpu_row, text="CPU Load", font=(UI_FONT_FAMILY, 9)).pack(side="left")
        ttk.Label(cpu_row, textvariable=self.cpu_details_text, font=(UI_FONT_FAMILY, 9, "bold")).pack(side="right")
        self.cpu_progressbar = ttk.Progressbar(sys_info_frame, mode='determinate')
        self.cpu_progressbar.pack(fill="x", pady=(0, 5))
        
        # Memory
        mem_row = ttk.Frame(sys_info_frame)
        mem_row.pack(fill="x", pady=(8, 8))
        ttk.Label(mem_row, text="Memory Usage", font=(UI_FONT_FAMILY, 9)).pack(side="left")
        ttk.Label(mem_row, textvariable=self.mem_details_text, font=(UI_FONT_FAMILY, 9, "bold")).pack(side="right")
        self.mem_progressbar = ttk.Progressbar(sys_info_frame, mode='determinate')
        self.mem_progressbar.pack(fill="x")
        
        return sys_info_frame

    def create_file_info_panel(self, parent):
        info_frame = ttk.LabelFrame(parent, text=" File Path Information ", padding=12)
        info_frame.columnconfigure(1, weight=1)
        
        labels = [("ETL:", self.etl_path), ("PDB:", self.pdb_path), ("TXT:", self.txt_path)]
        for i, (label, var) in enumerate(labels):
            ttk.Label(info_frame, text=label).grid(row=i, column=0, sticky="e", padx=(0, 8), pady=4)
            entry = ttk.Entry(info_frame, textvariable=var, state="readonly")
            entry.grid(row=i, column=1, sticky="ew", pady=4)
            
        return info_frame

    def create_split_settings_panel(self, parent):
        settings_frame = ttk.LabelFrame(parent, text=" TXT Split Settings ", padding=12)
        settings_frame.columnconfigure(1, weight=1)
        
        ttk.Label(settings_frame, text="Original Size:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(settings_frame, textvariable=self.original_size, font=(UI_FONT_FAMILY, 9, "bold")).grid(row=0, column=1, sticky="w")
        
        ttk.Label(settings_frame, text="Split Size:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=6)
        size_input = ttk.Frame(settings_frame)
        size_input.grid(row=1, column=1, sticky="w")
        ttk.Entry(size_input, textvariable=self.split_size_value, width=8).pack(side="left", padx=(0, 5))
        unit_cb = ttk.Combobox(size_input, textvariable=self.split_size_unit, values=["KB", "MB"], width=5, state="readonly")
        unit_cb.pack(side="left")
        unit_cb.bind("<<ComboboxSelected>>", self.update_estimated_files)
        
        ttk.Label(settings_frame, text="Est. Parts:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=6)
        ttk.Label(settings_frame, textvariable=self.estimated_files, font=(UI_FONT_FAMILY, 9, "bold")).grid(row=2, column=1, sticky="w")
        
        return settings_frame

    def create_pdb_browser_panel(self, parent):
        pdb_frame = ttk.LabelFrame(parent, text=" PDB Symbol Browser ", padding=12)
        pdb_frame.columnconfigure(0, weight=1)
        pdb_frame.rowconfigure(2, weight=1)
        
        # Search area
        ttk.Label(pdb_frame, text="Search Path:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        search_row = ttk.Frame(pdb_frame)
        search_row.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        search_row.columnconfigure(0, weight=1)
        ttk.Entry(search_row, textvariable=self.pdb_search_path).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(search_row, text="Scan", width=6, command=self._scan_pdb_from_entry).grid(row=0, column=1)
        
        # Listbox area
        list_container = ttk.Frame(pdb_frame)
        list_container.grid(row=2, column=0, sticky="nsew")
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)
        
        sb = ttk.Scrollbar(list_container, orient="vertical")
        self.pdb_listbox = tk.Listbox(list_container, yscrollcommand=sb.set, font=self.default_font, 
                                     borderwidth=0, highlightthickness=0, bg="#2b2b2b" if sv_ttk.get_theme()=="dark" else "#f5f5f5",
                                     fg="#ffffff" if sv_ttk.get_theme()=="dark" else "#000000")
        self.pdb_listbox.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")
        sb.config(command=self.pdb_listbox.yview)
        
        self.pdb_listbox.bind("<Double-1>", self._on_pdb_select)
        
        ttk.Button(pdb_frame, text="Reset to Default Path", command=self._reset_pdb_path).grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        return pdb_frame

    def create_action_buttons(self, parent):
        action_frame = ttk.Frame(parent)
        action_frame.columnconfigure((0, 1, 2), weight=1)
        
        # Enhance buttons with taller padding (ipady)
        self.traceview_button = ttk.Button(action_frame, text="Convert ETL", style="Accent.TButton", command=self.start_traceview_thread, state="disabled")
        self.traceview_button.grid(row=0, column=0, sticky="ew", ipady=8, padx=(0, 5))
        
        self.split_button = ttk.Button(action_frame, text="Split TXT", command=self.start_split_thread, state="disabled")
        self.split_button.grid(row=0, column=1, sticky="ew", ipady=8, padx=(5, 5))
        
        self.open_folder_button = ttk.Button(action_frame, text="Open Folder", command=self._open_txt_folder, state="disabled")
        self.open_folder_button.grid(row=0, column=2, sticky="ew", ipady=8, padx=(5, 0))
        
        return action_frame

    def create_log_panel(self, parent):
        log_frame = ttk.LabelFrame(parent, text=" Command Execution Log ", padding=12)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state="disabled", font=self.log_font,
                                                borderwidth=0, highlightthickness=0)
        self.log_text.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        btn_row = ttk.Frame(log_frame)
        btn_row.grid(row=1, column=0, sticky="e")
        ttk.Button(btn_row, text="Save Log", command=self._save_log).pack(side="left", padx=5)
        ttk.Button(btn_row, text="Clear Log", command=self.clear_log).pack(side="left")
        
        return log_frame
    
    def _reset_pdb_path(self):
        default_path = os.path.join(get_executable_dir(), 'symbol')
        self.pdb_search_path.set(default_path)
        self._scan_pdb_folder(default_path)
        
    def _save_log(self):
        log_content = self.log_text.get("1.0", tk.END)
        if not log_content.strip():
            self.show_message("Info", "Log is empty, nothing to save.")
            return
        filepath = filedialog.asksaveasfilename(
            title="Save Log As", initialfile="trace_splitter_log.txt", defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath: return
        try:
            with open(filepath, 'w', encoding='utf-8') as f: f.write(log_content)
            self.status.set(f"Log successfully saved to {os.path.basename(filepath)}")
        except Exception as e:
            self.show_message("Error", f"Failed to save log file:\n{e}")
            
    def _scan_pdb_from_entry(self):
        path = self.pdb_search_path.get()
        self._scan_pdb_folder(path)

    def _scan_pdb_folder(self, folder_path):
        self.pdb_listbox.delete(0, tk.END)
        self.found_pdb_files.clear()
        if not os.path.isdir(folder_path):
            self.pdb_listbox.insert(tk.END, "Folder not found or is not a directory.")
            return
        try:
            for filename in sorted(os.listdir(folder_path)):
                if filename.lower().endswith(".pdb"):
                    self.pdb_listbox.insert(tk.END, filename)
                    self.found_pdb_files.append(os.path.join(folder_path, filename))
            if not self.found_pdb_files:
                self.pdb_listbox.insert(tk.END, "No .pdb files found in this folder.")
        except Exception as e:
            self.pdb_listbox.insert(tk.END, f"Error scanning folder: {e}")

    def _on_pdb_select(self, event):
        selected_indices = self.pdb_listbox.curselection()
        if not selected_indices: return
        selected_index = selected_indices[0]
        if 0 <= selected_index < len(self.found_pdb_files):
            full_path = self.found_pdb_files[selected_index]
            self.pdb_path.set(full_path)
            self.status.set(f"Selected PDB: {os.path.basename(full_path)}")
            self._update_button_states()

    def _open_txt_folder(self):
        txt_path = self.txt_path.get()
        if txt_path and os.path.exists(txt_path):
            folder = os.path.dirname(txt_path)
            try:
                os.startfile(folder)
            except Exception as e:
                self.show_message("Error", f"Could not open folder:\n{e}")

    def clear_log(self):
        if not self.log_text: return
        self.log_text.config(state="normal")
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state="disabled")

    def log_message(self, message):
        self.log_queue.put(message)

    def process_log_queue(self):
        if not self.log_text:
            self.after(100, self.process_log_queue)
            return
        try:
            while True:
                line = self.log_queue.get_nowait()
                self.log_text.config(state="normal")
                self.log_text.insert(tk.END, line)
                self.log_text.see(tk.END)
                self.log_text.config(state="disabled")
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_log_queue)

    def start_traceview_thread(self):
        self.log_message("\n" + "="*80 + "\n")
        self.log_message("--- Starting New Traceview Conversion ---\n")
        self.traceview_button.config(state="disabled")
        self.split_button.config(state="disabled")
        self.status.set("Starting Traceview conversion...")
        callbacks = { 'log': self.log_message, 'status': lambda msg: self.after(0, self.status.set, msg), 'success': lambda path: self.after(0, self.process_txt_file, path), 'failure': lambda msg: self.after(0, self.status.set, msg) }
        thread = threading.Thread(target=core_logic.run_traceview_conversion, args=(self.etl_path.get(), self.pdb_path.get(), callbacks), daemon=True)
        thread.start()

    def update_system_info(self):
        if not self.show_sys_info: return
        
        # cpu_percent with interval=None depends on the previous call. 
        # On the very first call it will return 0.0.
        cpu_percent = psutil.cpu_percent()
        self.cpu_details_text.set(f"{cpu_percent:.1f} %")
        
        # Update progress bars only if they exist
        if hasattr(self, 'cpu_progressbar'):
            self.cpu_progressbar['value'] = cpu_percent
            
        mem_info = psutil.virtual_memory()
        used_mem = format_size(mem_info.used)
        total_mem = format_size(mem_info.total)
        self.mem_details_text.set(f"{mem_info.percent:.1f} % ({used_mem} / {total_mem})")
        
        if hasattr(self, 'mem_progressbar'):
            self.mem_progressbar['value'] = mem_info.percent
            
        self.after(2000, self.update_system_info)

    def handle_drop(self, event):
        filepaths = self.tk.splitlist(event.data)
        for path in filepaths:
            # --- MODIFIED: Regex to handle .etl and .etl.xxx files ---
            if path.lower().endswith(".pdb"):
                self.pdb_path.set(path)
                self.status.set(f"Loaded PDB: {os.path.basename(path)}")
            elif path.lower().endswith(".txt"):
                self.process_txt_file(path)
            elif re.search(r'\.etl(\.\d+)?$', path, re.IGNORECASE):
                self.etl_path.set(path)
                self.status.set(f"Loaded ETL: {os.path.basename(path)}")
            else:
                self.show_message("Unsupported File", f"File type not supported:\n{os.path.basename(path)}")
        self._update_button_states()

    def process_txt_file(self, path):
        self.txt_path.set(path)
        #self.etl_path.set("")
        #self.pdb_path.set("")
        try:
            self.update_estimated_files()
        except Exception as e:
            self.show_message("Error", f"Failed to process TXT file:\n{e}")
            self.reset_txt_fields()
        self._update_button_states()
        
    def _update_button_states(self):
        traceview_ready = self.etl_path.get() and self.pdb_path.get()
        self.traceview_button.config(state="normal" if traceview_ready else "disabled")
        split_ready = self.txt_path.get() and os.path.exists(self.txt_path.get())
        self.split_button.config(state="normal" if split_ready else "disabled")
        self.open_folder_button.config(state="normal" if split_ready else "disabled")

    def reset_txt_fields(self):
        self.txt_path.set("")
        self.original_size.set("N/A")
        self.estimated_files.set("N/A")
        
    def update_estimated_files(self, event=None):
        txt_path = self.txt_path.get()
        if not txt_path or not os.path.exists(txt_path):
            self.original_size.set("N/A")
            self.estimated_files.set("N/A")
            return
        try:
            size_in_bytes = os.path.getsize(txt_path)
            self.original_size.set(format_size(size_in_bytes))
            split_size = int(self.split_size_value.get())
            unit = self.split_size_unit.get()
            split_bytes = (split_size * 1024) if unit == "KB" else (split_size * 1024 * 1024)
            if split_bytes > 0: self.estimated_files.set(str(math.ceil(size_in_bytes / split_bytes)))
            else: self.estimated_files.set("N/A")
        except (ValueError, FileNotFoundError): self.estimated_files.set("N/A")
        except ZeroDivisionError: self.estimated_files.set("Infinite")

    def _on_split_success(self, message):
        """Handles successful split operation."""
        self.show_message("Success", message)
        self._update_button_states()

    def _on_split_failure(self, message):
        """Handles failed split operation."""
        self.show_message("Runtime Error", message)
        self._update_button_states()

    def start_split_thread(self):
        self.split_button.config(state="disabled")
        self.traceview_button.config(state="disabled")
        self.status.set("Preparing to split...")
        # 將 'success' 和 'failure' 的回呼改為我們的新函式
        callbacks = { 
            'log': self.log_message, 
            'status': lambda msg: self.after(0, self.status.set, msg), 
            'success': self._on_split_success, 
            'failure': self._on_split_failure 
        }
        try:
            split_size_val = int(self.split_size_value.get())
            estimated_files_val = int(self.estimated_files.get()) if self.estimated_files.get().isdigit() else 1
        except ValueError:
            self.show_message("Input Error", "Invalid split size or estimated file count.")
            return
        thread = threading.Thread( target=core_logic.run_file_splitting, args=( self.txt_path.get(), split_size_val, self.split_size_unit.get(), estimated_files_val, callbacks ), daemon=True )
        thread.start()

    def show_message(self, title, message):
        if title.lower() in ["error", "runtime error", "input error", "fatal error"]: messagebox.showerror(title, message)
        elif title.lower() == "warning": messagebox.showwarning(title, message)
        else: messagebox.showinfo(title, message)
