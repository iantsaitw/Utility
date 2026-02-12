import tkinter as tk
from tkinter import ttk
import os
import subprocess
import ctypes
import time
import threading
import config

# Win32 APIs and Constants
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
GWL_STYLE = -16
WS_CAPTION = 0x00C00000
WS_THICKFRAME = 0x00040000
WS_CHILD = 0x40000000
WS_POPUP = 0x80000000
SWP_NOZORDER = 0x0004
SWP_SHOWWINDOW = 0x0040
SWP_FRAMECHANGED = 0x0020
SWP_NOACTIVATE = 0x0010
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001

def find_vs2022_bat():
    """ Try to locate VS 2022 Developer Command Prompt batch file """
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        vswhere = r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
        if os.path.exists(vswhere):
            cmd = [vswhere, "-version", "[17.0,18.0)", "-products", "*", "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64", "-property", "installationPath"]
            path = subprocess.check_output(cmd, startupinfo=startupinfo).decode().strip()
            if path:
                bat = os.path.join(path, "Common7", "Tools", "VsDevCmd.bat")
                if os.path.exists(bat): return bat
    except: pass
    editions = ["Professional", "Community", "Enterprise"]
    for ed in editions:
        p = rf"C:\Program Files\Microsoft Visual Studio\2022\{ed}\Common7\Tools\VsDevCmd.bat"
        if os.path.exists(p): return p
    return None

class TerminalFrame(ttk.Frame):
    """ A Frame that embeds a Win32 CMD window """
    def __init__(self, master, work_dir, **kwargs):
        super().__init__(master, **kwargs)
        self.work_dir = work_dir
        self.cmd_hwnd = None
        self.is_embedding = False
        
        self.configure(takefocus=0)
        
        self.container = tk.Frame(self, bg="black", takefocus=0)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.container.bind("<Configure>", self.on_resize)

        # Place the Restart button at the bottom-right corner as an overlay-like button
        self.btn_restart = ttk.Button(self, text="🔄 Restart", width=10, command=self.restart_terminal)
        self.btn_restart.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")
        
        # Focus recovery bindings: ONLY on hard click
        self.container.bind("<Button-1>", self.force_focus)

    def force_focus(self, event=None):
        """ Forcefully give keyboard focus to the embedded Win32 window """
        if self.cmd_hwnd:
            gui_thread = kernel32.GetCurrentThreadId()
            cmd_thread = user32.GetWindowThreadProcessId(self.cmd_hwnd, None)
            if gui_thread != cmd_thread:
                user32.AttachThreadInput(gui_thread, cmd_thread, True)
                user32.SetFocus(self.cmd_hwnd)
                # Removed SetActiveWindow(self.cmd_hwnd) as it steals global focus
                user32.AttachThreadInput(gui_thread, cmd_thread, False)
            else:
                user32.SetFocus(self.cmd_hwnd)

    def restart_terminal(self, new_dir=None):
        """ Close current terminal and start a new one in the specified directory """
        if self.is_embedding: return
        
        if new_dir and new_dir == self.work_dir and self.cmd_hwnd:
            return

        if new_dir:
            self.work_dir = new_dir

        self.btn_restart.configure(text="🔄 Starting...", state="disabled")
        
        if self.cmd_hwnd:
            try: user32.PostMessageW(self.cmd_hwnd, 0x0010, 0, 0)
            except: pass
            time.sleep(0.2)
        
        self.cmd_hwnd = None
        self.start_embedded_cmd()

    def start_embedded_cmd(self):
        """ Spawn a new CMD process with a unique title for embedding """
        if self.is_embedding: return
        self.is_embedding = True
        
        vs_bat = find_vs2022_bat()
        unique_id = f"{int(time.time() * 1000) % 1000000:06d}"
        unique_title = f"DriverDeck_{unique_id}"
        
        # Prepare the internal command string
        if vs_bat:
            inner_cmd = f'title {unique_title} && cd /d "{self.work_dir}" && call "{vs_bat}"'
        else:
            inner_cmd = f'title {unique_title} && cd /d "{self.work_dir}"'
            
        try:
            # Using a list with shell=False is the most reliable way to handle quotes in Windows
            # Python will handle the necessary escaping for the underlying CreateProcess call
            args = ["wt.exe", "-p", "Windows PowerShell", "cmd.exe", "/k", inner_cmd]
            subprocess.Popen(args, shell=False, cwd=self.work_dir)
        except:
            # Fallback to traditional CMD if WT is missing
            fallback_args = ["cmd.exe", "/c", "start", unique_title, "cmd.exe", "/k", inner_cmd]
            subprocess.Popen(fallback_args, shell=False, cwd=self.work_dir)

        threading.Thread(target=self.wait_and_embed, args=(unique_title,), daemon=True).start()

    def wait_and_embed(self, title):
        """ Search for the window by title and reparent it to the Tkinter frame """
        try:
            hwnd = 0
            for i in range(100):
                hwnd = user32.FindWindowW(None, title)
                if hwnd: break
                
                # Fallback: Enum windows if FindWindow fails
                found_hwnds = []
                def enum_cb(h, l_ptr):
                    buf = ctypes.create_unicode_buffer(512)
                    user32.GetWindowTextW(h, buf, 512)
                    if title in buf.value:
                        found_hwnds.append(h)
                        return False
                    return True
                WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
                user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
                if found_hwnds:
                    hwnd = found_hwnds[0]
                    break
                time.sleep(0.1)

            if hwnd:
                self.cmd_hwnd = hwnd
                parent_hwnd = 0
                for _ in range(20):
                    try:
                        parent_hwnd = self.container.winfo_id()
                        if parent_hwnd != 0: break
                    except: pass
                    time.sleep(0.05)
                
                if parent_hwnd:
                    user32.ShowWindow(self.cmd_hwnd, 1)
                    # Modify style: remove caption/border, add child attribute
                    style = user32.GetWindowLongW(self.cmd_hwnd, GWL_STYLE)
                    user32.SetWindowLongW(self.cmd_hwnd, GWL_STYLE, (style & ~WS_CAPTION & ~WS_THICKFRAME & ~WS_POPUP) | WS_CHILD)
                    user32.SetParent(self.cmd_hwnd, parent_hwnd)
                    user32.SetWindowPos(self.cmd_hwnd, 0, 0, 0, 0, 0, SWP_NOZORDER | SWP_NOMOVE | SWP_NOSIZE | SWP_FRAMECHANGED)
                    self.on_resize(is_first=True)
                    # Removed self.after(100, self.force_focus) to avoid stealing focus on start
        except: pass
        self.after(0, self._finalize_ui_state)

    def _finalize_ui_state(self):
        self.btn_restart.configure(text="🔄 Restart", state="normal")
        self.is_embedding = False

    def on_resize(self, event=None, is_first=False):
        """ Keep embedded window size synced with the Tkinter frame """
        if self.cmd_hwnd:
            if not user32.IsWindow(self.cmd_hwnd):
                self.cmd_hwnd = None
                return
            w = self.container.winfo_width()
            h = self.container.winfo_height()
            if w > 10 and h > 10:
                flags = SWP_NOZORDER | SWP_SHOWWINDOW
                if not is_first: flags |= SWP_NOACTIVATE
                user32.SetWindowPos(self.cmd_hwnd, 0, 0, 0, w, h, flags)

    def __del__(self):
        if self.cmd_hwnd:
            try: user32.PostMessageW(self.cmd_hwnd, 0x0010, 0, 0)
            except: pass