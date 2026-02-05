# project_tab.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import datetime
import subprocess
import config 
import driver_utils 
from ui_factory import UIFactory

class ProjectTab(ttk.Frame):
    """ 代表一個 Project 的分頁 """
    def __init__(self, master, project_path, app_root=None, **kwargs):
        super().__init__(master, padding=15, **kwargs) # 減少外邊距
        self.project_path = project_path
        self.app_root = app_root
        self.selected_driver_path = None
        self.cached_items = []
        self.file_data_cache = []
        
        self.filter_var = tk.StringVar(value=config.current_settings.get("filter_mode", "All"))
        
        self.setup_ui()
        
        self.after(500, self.restore_sash_pos)
        self.after(100, self.refresh_driver_list)

    def sync_filter_ui(self):
        global_mode = config.current_settings.get("filter_mode", "All")
        if self.filter_var.get() != global_mode:
            self.filter_var.set(global_mode)
            self.update_tree_view()

    def setup_ui(self):
        # 1. Top
        top_frame = UIFactory.create_frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10)) 
        
        UIFactory.create_header_label(top_frame, text=os.path.basename(self.project_path)).pack(side=tk.LEFT)
        UIFactory.create_secondary_button(top_frame, "📂 Explorer", self.open_project_folder).pack(side=tk.RIGHT)

        # 3. Bottom (Backup & Export)
        op_frame = ttk.Frame(self)
        op_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0))

        # Backup Area
        bf_frame = ttk.LabelFrame(op_frame, text=" Backup ", padding=10)
        bf_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        UIFactory.create_sub_label(bf_frame, "Suffix:").pack(side=tk.LEFT, padx=(0, 5))
        self.suffix_entry = UIFactory.create_entry(bf_frame, driver_utils.get_time_suffix())
        self.suffix_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        UIFactory.create_secondary_button(bf_frame, "Run Backup", self.do_backup).pack(side=tk.LEFT)

        # Export Area
        cp_frame = ttk.LabelFrame(op_frame, text=" Export ", padding=10)
        cp_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        self.dest_entry = UIFactory.create_entry(cp_frame, config.current_settings.get("export_dir", ""))
        self.dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        UIFactory.create_secondary_button(cp_frame, "...", self.browse_dest, width=4).pack(side=tk.LEFT, padx=(0, 5))
        
        UIFactory.create_secondary_button(cp_frame, "Folder", lambda: self.do_export("folder")).pack(side=tk.LEFT, padx=2)
        UIFactory.create_secondary_button(cp_frame, "Sys", lambda: self.do_export("sys")).pack(side=tk.LEFT, padx=2)

        # 2. Middle (Split View)
        self.paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.paned.bind("<ButtonRelease-1>", self.on_sash_release)

        # --- Driver Versions Pane ---
        driver_pane = ttk.LabelFrame(self.paned, text=" Driver Versions ", padding=10)
        self.paned.add(driver_pane, weight=1)

        d_toolbar = ttk.Frame(driver_pane)
        d_toolbar.pack(side=tk.TOP, fill=tk.X, pady=(0, 8)) 
        UIFactory.create_secondary_button(d_toolbar, "Refresh List", self.refresh_driver_list).pack(side=tk.RIGHT)

        modes = ["All", "PCIE", "USB"]
        for m in reversed(modes): 
            ttk.Radiobutton(d_toolbar, text=m, variable=self.filter_var, value=m, 
                            style="Toggle.TButton", command=self.on_filter_change).pack(side=tk.RIGHT, padx=4)

        d_list_frame = ttk.Frame(driver_pane)
        d_list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        cols = ("folder", "version", "date", "path")
        self.driver_list = UIFactory.create_treeview(d_list_frame, cols)
        
        self.driver_list.heading("folder", text="Folder", command=lambda: self.sort_driver_list("folder", False))
        self.driver_list.heading("version", text="Version", command=lambda: self.sort_driver_list("version", False))
        self.driver_list.heading("date", text="Date Modified", command=lambda: self.sort_driver_list("date", False))
        self.driver_list.heading("path", text="Path", command=lambda: self.sort_driver_list("path", False))
        
        self.driver_list.column("folder", width=160)
        self.driver_list.column("version", width=120)
        self.driver_list.column("date", width=140)
        self.driver_list.column("path", width=300)
        
        # 使用 <<TreeviewSelect>> 事件來觸發選取與同步
        self.driver_list.bind("<<TreeviewSelect>>", self.on_driver_select)

        d_scroll = ttk.Scrollbar(d_list_frame, orient="vertical", command=self.driver_list.yview)
        self.driver_list.configure(yscrollcommand=d_scroll.set)
        self.driver_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        d_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Files Pane ---
        file_pane = ttk.LabelFrame(self.paned, text=" Files ", padding=10)
        self.paned.add(file_pane, weight=1)

        f_toolbar = ttk.Frame(file_pane)
        f_toolbar.pack(side=tk.TOP, fill=tk.X, pady=(0, 8))
        
        self.btn_open_driver_folder = UIFactory.create_secondary_button(f_toolbar, "📂 Open Folder", self.open_driver_folder)
        self.btn_open_driver_folder.pack(side=tk.RIGHT)
        self.btn_open_driver_folder.state(["disabled"])
        
        self.btn_sign_driver = UIFactory.create_primary_button(f_toolbar, "✒ Sign Driver", self.do_sign_driver)
        self.btn_sign_driver.pack(side=tk.RIGHT, padx=10)
        self.btn_sign_driver.state(["disabled"])

        f_list_frame = ttk.Frame(file_pane)
        f_list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        f_cols = ("name", "version", "signature", "date", "size")
        self.file_list = UIFactory.create_treeview(f_list_frame, f_cols)
        
        self.file_list.heading("name", text="Name", anchor="center", command=lambda: self.sort_file_list("name", False))
        self.file_list.heading("version", text="Version", anchor="center", command=lambda: self.sort_file_list("version", False))
        self.file_list.heading("signature", text="Digital Signature", anchor="center", command=lambda: self.sort_file_list("signature", False))
        self.file_list.heading("date", text="Date Modified", anchor="center", command=lambda: self.sort_file_list("date", False))
        self.file_list.heading("size", text="Size", anchor="center", command=lambda: self.sort_file_list("size", False))

        self.file_list.column("name", width=150, minwidth=100, stretch=tk.YES)
        self.file_list.column("version", width=80, minwidth=80, stretch=tk.NO)
        self.file_list.column("signature", width=200, minwidth=150, stretch=tk.YES)
        self.file_list.column("date", width=130, minwidth=130, stretch=tk.NO)
        self.file_list.column("size", width=70, minwidth=70, stretch=tk.NO, anchor="e")

        self.file_list.bind("<Double-1>", self.on_file_double_click)

        f_scroll = ttk.Scrollbar(f_list_frame, orient="vertical", command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=f_scroll.set)
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        f_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # === Logic ===
    def on_sash_release(self, event):
        try:
            total_height = self.paned.winfo_height()
            if total_height <= 1: return
            current_sash = self.paned.sashpos(0)
            ratio = current_sash / total_height
            if ratio < 0.1: ratio = 0.1
            if ratio > 0.9: ratio = 0.9
            old_ratio = config.current_settings.get("split_ratio", 0.6)
            if abs(ratio - old_ratio) > 0.01: config.save_settings({"split_ratio": ratio})
        except: pass

    def restore_sash_pos(self):
        try:
            ratio = config.current_settings.get("split_ratio", 0.6)
            total_height = self.paned.winfo_height()
            if total_height > 50:
                new_pos = int(total_height * ratio)
                self.paned.sashpos(0, new_pos)
            else: self.after(200, self.restore_sash_pos)
        except: pass

    def refresh_export_path(self):
        new_path = config.current_settings.get("export_dir", "")
        current_val = self.dest_entry.get()
        if new_path != current_val:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, new_path)

    def on_filter_change(self):
        mode = self.filter_var.get()
        config.save_settings({"filter_mode": mode})
        self.update_tree_view()

    def sort_driver_list(self, col, reverse):
        col_map = {"folder": 0, "version": 1, "date": 2, "path": 3}
        idx = col_map.get(col, 0)
        self.cached_items.sort(key=lambda x: x[idx].lower(), reverse=reverse)
        for c in col_map: self.driver_list.heading(c, command=lambda _c=c: self.sort_driver_list(_c, False))
        self.driver_list.heading(col, command=lambda: self.sort_driver_list(col, not reverse))
        self.update_tree_view()

    def update_tree_view(self):
        for item in self.driver_list.get_children(): self.driver_list.delete(item)
        filter_mode = self.filter_var.get() 
        for item in self.cached_items:
            drv_type = item[4]
            if filter_mode == "All" or filter_mode == drv_type:
                display_values = (item[0], item[1], item[2], item[3])
                self.driver_list.insert("", "end", values=display_values)

    def refresh_driver_list(self):
        for item in self.driver_list.get_children(): self.driver_list.delete(item)
        for item in self.file_list.get_children(): self.file_list.delete(item)
        self.selected_driver_path = None
        self.btn_open_driver_folder.state(["disabled"])
        self.btn_sign_driver.state(["disabled"])
        self.cached_items = []
        for drv_type, subpaths in config.DRIVER_PATHS.items():
            for subpath in subpaths:
                base_path = os.path.join(self.project_path, subpath)
                if not os.path.exists(base_path): continue 
                for root, dirs, files in os.walk(base_path):
                    for d in dirs:
                        full_path = os.path.join(root, d)
                        rel_path = os.path.relpath(full_path, base_path)
                        if rel_path.lower() in ["win10", "win11"]: continue
                        ver_str = ""
                        date_str = ""
                        try:
                            mtime = os.path.getmtime(full_path)
                            date_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
                            sys_files = [f for f in os.listdir(full_path) if f.lower().endswith(".sys")]
                            if sys_files:
                                target_sys = os.path.join(full_path, sys_files[0])
                                ver_str = driver_utils.get_file_version(target_sys)
                        except: pass
                        self.cached_items.append((rel_path, ver_str, date_str, full_path, drv_type))
        self.cached_items.sort(key=lambda x: x[0].lower())
        self.update_tree_view()

    def on_driver_select(self, event):
        selection = self.driver_list.selection()
        if not selection: return
        item = self.driver_list.item(selection[0])
        full_path = item['values'][3] 
        self.selected_driver_path = full_path
        self.btn_open_driver_folder.state(["!disabled"])
        self.btn_sign_driver.state(["!disabled"])
        self.refresh_file_list(full_path)
        
        # 同步終端機目錄
        if self.app_root and hasattr(self.app_root, "sync_terminal_dir"):
            self.app_root.sync_terminal_dir(full_path)

    def sort_file_list(self, col, reverse):
        col_map = {"name": 0, "version": 1, "signature": 2, "date": 5, "size": 6} 
        idx = col_map.get(col, 0)
        self.file_data_cache.sort(key=lambda x: (not x[7], x[idx] if isinstance(x[idx], (int, float)) else x[idx].lower()), reverse=reverse)
        for c in col_map: self.file_list.heading(c, command=lambda _c=c: self.sort_file_list(_c, False))
        self.file_list.heading(col, command=lambda: self.sort_file_list(col, not reverse))
        self.update_file_list_view()

    def update_file_list_view(self):
        for item in self.file_list.get_children(): self.file_list.delete(item)
        for item in self.file_data_cache:
            display_values = (item[0], item[1], item[2], item[3], item[4])
            self.file_list.insert("", "end", values=display_values)

    def refresh_file_list(self, path):
        self.file_data_cache = []
        if path and os.path.exists(path):
            try:
                items = os.listdir(path)
                items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
                for f in items:
                    full_p = os.path.join(path, f)
                    mtime = os.path.getmtime(full_p)
                    date_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
                    version_str = ""
                    size_str = ""
                    sig_str = ""
                    size_bytes = 0
                    is_dir = False
                    if os.path.isfile(full_p):
                        size_bytes = os.path.getsize(full_p)
                        size_str = driver_utils.format_size(size_bytes)
                        ext = os.path.splitext(f)[1].lower()
                        if ext in ('.sys', '.exe', '.dll'): version_str = driver_utils.get_file_version(full_p)
                        if ext in ('.sys', '.exe', '.dll', '.cat'): sig_str = driver_utils.check_file_signature(full_p)
                    else:
                        is_dir = True
                        size_str = "<DIR>"
                        size_bytes = -1
                    self.file_data_cache.append((f, version_str, sig_str, date_str, size_str, mtime, size_bytes, is_dir, full_p))
            except: pass
        self.sort_file_list("name", False)

    def do_sign_driver(self):
        if not self.selected_driver_path: return
        pfx_path = config.current_settings.get("pfx_path", "")
        if not pfx_path or not os.path.exists(pfx_path):
            messagebox.showwarning("Warning", "PFX certificate not found!")
            return
        signtool_exe = config.current_settings.get("signtool_path", "")
        if not signtool_exe or not os.path.exists(signtool_exe): signtool_exe = driver_utils.find_signtool()
        if not signtool_exe:
            messagebox.showerror("Error", "SignTool.exe not found!")
            return
        target_extensions = {".sys", ".dll", ".cat", ".exe"}
        files_to_sign = []
        for f in os.listdir(self.selected_driver_path):
            if os.path.splitext(f)[1].lower() in target_extensions:
                files_to_sign.append(f'"{os.path.join(self.selected_driver_path, f)}"')
        if not files_to_sign: return
        cmd = f'"{signtool_exe}" sign /fd sha256 /f "{pfx_path}" {" ".join(files_to_sign)}'
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, shell=True)
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                messagebox.showinfo("Success", "Signing Completed!")
                self.refresh_file_list(self.selected_driver_path)
            else: messagebox.showerror("Sign Failed", f"Error Code: {process.returncode}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024: return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def open_project_folder(self):
        if os.path.exists(self.project_path): os.startfile(self.project_path)

    def open_driver_folder(self):
        if self.selected_driver_path and os.path.exists(self.selected_driver_path): os.startfile(self.selected_driver_path)

    def on_file_double_click(self, event):
        if not self.selected_driver_path: return
        selection = self.file_list.selection()
        if not selection: return
        filename = self.file_list.item(selection[0])['values'][0]
        full_path = os.path.join(self.selected_driver_path, filename)
        if os.path.exists(full_path): os.startfile(full_path)

    def do_backup(self):
        if not self.selected_driver_path: return
        src = self.selected_driver_path
        dest = os.path.join(os.path.dirname(src), f"{os.path.basename(src)}{self.suffix_entry.get()}")
        if os.path.exists(dest):
            if not messagebox.askyesno("Confirm", "Overwrite backup?"): return
            shutil.rmtree(dest)
        try:
            shutil.copytree(src, dest)
            messagebox.showinfo("Success", f"Backed up: {os.path.basename(dest)}")
            self.refresh_driver_list()
        except Exception as e: messagebox.showerror("Error", str(e))

    def browse_dest(self):
        d = filedialog.askdirectory()
        if d:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, d)
            config.save_settings({"export_dir": d})

    def do_export(self, mode):
        if not self.selected_driver_path: return
        src = self.selected_driver_path
        dest_root = self.dest_entry.get()
        if not src or not os.path.exists(dest_root): return
        try:
            if mode == "folder":
                final_dest = os.path.join(dest_root, os.path.basename(src))
                if os.path.exists(final_dest):
                    if not messagebox.askyesno("Confirm", "Overwrite?"): return
                    shutil.rmtree(final_dest)
                shutil.copytree(src, final_dest)
            elif mode == "sys":
                src_files = [f for f in os.listdir(src) if f.lower().endswith(".sys")]
                for f in src_files: shutil.copy2(os.path.join(src, f), os.path.join(dest_root, f))
            messagebox.showinfo("Success", "Copy Complete")
        except Exception as e: messagebox.showerror("Error", str(e))
