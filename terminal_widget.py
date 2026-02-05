# terminal_widget.py
import tkinter as tk
from tkinter import ttk
import os
import subprocess
import threading
import queue
import glob
from config import *

class DarkInteractiveConsole(tk.Text):
    def __init__(self, master, work_dir, prompt_callback=None, initial_cmd=None, **kwargs):
        super().__init__(master, **kwargs)
        self.work_dir = work_dir
        self.prompt_callback = prompt_callback
        
        # 狀態變數
        self.history = []           # 指令歷史
        self.history_index = 0
        self.current_input_start = "1.0" # 雖然 Persistent Shell 很難精確定位，但我們用行來判斷
        
        # Tab 循環變數
        self.is_tab_cycling = False
        self.tab_matches = []
        self.tab_index = 0
        
        # UI 設定
        self.configure(bg=COLOR_TERM_BG, fg=COLOR_TERM_FG, insertbackground="white", 
                       font=FONT_TERM, undo=False, wrap=tk.WORD, borderwidth=0, relief="flat")
        
        self.tag_configure("output", foreground=COLOR_TERM_FG)
        self.tag_configure("error", foreground=COLOR_ERROR)
        self.tag_configure("system", foreground=COLOR_SYSTEM)
        self.tag_configure("input", foreground=COLOR_INPUT, font=(FONT_TERM[0], FONT_TERM[1], "bold"))

        # 事件綁定
        self.bind("<Return>", self.on_enter)
        self.bind("<Key>", self.on_key_press)
        self.bind("<Tab>", self.on_tab)       # [修復] Tab 鍵
        self.bind("<Up>", self.on_up)         # [修復] 上鍵
        self.bind("<Down>", self.on_down)     # [修復] 下鍵
        self.bind("<Button-1>", self.on_click)
        
        # 佇列用於線程通訊
        self.queue = queue.Queue()
        self.update_interval = 50
        
        # 啟動持久化 CMD
        self.start_persistent_shell(initial_cmd)
        
        # 確保有焦點
        self.focus_set()
        
        # 開始更新迴圈
        self.process_queue()

    def start_persistent_shell(self, initial_cmd):
        """ 啟動一個長駐的 cmd.exe """
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            self.process = subprocess.Popen(
                "cmd.exe", 
                cwd=self.work_dir,
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                shell=True, 
                bufsize=0, 
                startupinfo=startupinfo
            )
            
            threading.Thread(target=self.read_from_process, daemon=True).start()
            
            if initial_cmd:
                # 這裡不顯示在 UI，只在背景執行，避免混淆
                self.send_command(initial_cmd, show_in_ui=False)
                self.queue.put(("system", f"[System] Initializing Environment...\n"))

        except Exception as e:
            self.insert(tk.END, f"Failed to start shell: {e}\n", "error")

    def read_from_process(self):
        while True:
            if self.process.poll() is not None: break
            try:
                char = self.process.stdout.read(1)
                if char: self.queue.put(("output", char))
            except: break

    def process_queue(self):
        while not self.queue.empty():
            try:
                msg_type, content = self.queue.get_nowait()
                
                if msg_type == "output":
                    try: text = content.decode('cp950', errors='ignore')
                    except: text = content.decode('utf-8', errors='ignore')
                    self.insert(tk.END, text, "output")
                
                elif msg_type == "system":
                    self.insert(tk.END, content, "system")
                
                self.see(tk.END)
                # 每次有輸出，更新輸入起點標記 (簡單認定最後就是起點)
                self.mark_set("insert", tk.END)
            except queue.Empty: break
        
        self.after(self.update_interval, self.process_queue)

    def on_click(self, event):
        self.focus_set()
        # 允許點擊複製，但輸入時會跳回最後
        return None 

    def on_key_press(self, event):
        # 重置 Tab 循環狀態 (除非按的是 Tab 或修飾鍵)
        if event.keysym not in ("Tab", "Shift_L", "Shift_R", "Control_L", "Control_R"):
            self.is_tab_cycling = False
            
        if (event.state & 4) and (event.keysym.lower() == 'c'): return None
        if (event.state & 4) and (event.keysym.lower() == 'v'): return None
        
        # 強制輸入只能在最後
        self.mark_set("insert", tk.END)
        return None

    def get_current_line_input(self):
        """ 取得目前最後一行的使用者輸入 (去除 Prompt) """
        # 抓取最後一行的所有文字
        full_content = self.get("1.0", tk.END)
        # 找最後一個換行符號
        last_newline = full_content.rfind('\n', 0, len(full_content)-1)
        if last_newline == -1: last_newline = 0
        
        last_line = full_content[last_newline:].strip()
        
        # 去除 Prompt (例如 E:\Project> )
        if '>' in last_line:
            return last_line.split('>', 1)[1].lstrip()
        return last_line

    def delete_current_line_input(self):
        """ 刪除最後一行的使用者輸入 (用於 History 或 Tab 替換) """
        # 我們不能刪除 prompt，所以要小心
        # 策略：找到最後一個 '>'，刪除後面的所有字
        line_idx = int(self.index("end-1c").split('.')[0])
        line_text = self.get(f"{line_idx}.0", "end-1c")
        
        prompt_idx = line_text.rfind('>')
        if prompt_idx != -1:
            start_pos = f"{line_idx}.{prompt_idx + 1}"
            self.delete(start_pos, tk.END)
        else:
            # 找不到 prompt，可能是互動輸入，刪除整行
            self.delete(f"{line_idx}.0", tk.END)

    def on_enter(self, event):
        cmd = self.get_current_line_input()
        self.insert(tk.END, "\n") # UI 換行
        self.is_tab_cycling = False
        
        if cmd:
            self.history.append(cmd)
            self.history_index = len(self.history)
            self.send_command(cmd)
            
            # 本地處理 cd 同步
            if cmd.lower().startswith("cd "):
                try:
                    target = cmd.split(" ", 1)[1].strip()
                    if target == "..":
                        new_path = os.path.dirname(self.work_dir)
                    else:
                        new_path = os.path.abspath(os.path.join(self.work_dir, target))
                    
                    if os.path.exists(new_path):
                        self.work_dir = new_path
                        if self.prompt_callback: self.prompt_callback(self.work_dir)
                except: pass
        else:
            self.send_command("") # 送出空行
            
        return "break"

    def send_command(self, cmd, show_in_ui=False):
        if show_in_ui:
            self.insert(tk.END, cmd + "\n", "input")
            
        if self.process and self.process.stdin:
            try:
                cmd_bytes = (cmd + "\n").encode('cp950')
                self.process.stdin.write(cmd_bytes)
                self.process.stdin.flush()
            except Exception as e:
                self.insert(tk.END, f"\nError: {e}\n", "error")

    # === [修復] 歷史紀錄功能 ===
    def on_up(self, event):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            cmd = self.history[self.history_index]
            self.delete_current_line_input()
            self.insert(tk.END, " " + cmd) # 加一個空白避免貼在 > 上
        return "break"

    def on_down(self, event):
        if self.history and self.history_index < len(self.history):
            self.history_index += 1
            self.delete_current_line_input()
            if self.history_index < len(self.history):
                cmd = self.history[self.history_index]
                self.insert(tk.END, " " + cmd)
        return "break"

    # === [修復] Tab 自動完成 ===
    def on_tab(self, event):
        if not self.is_tab_cycling:
            # 1. 抓取目前輸入
            current_text = self.get_current_line_input().strip()
            
            # 2. 分析最後一個字 (Prefix)
            if " " in current_text:
                prefix = current_text.split(" ")[-1]
                base_cmd = current_text.rsplit(" ", 1)[0]
            else:
                prefix = current_text
                base_cmd = ""
            
            # 3. 搜尋檔案
            search_pattern = os.path.join(self.work_dir, prefix + "*")
            matches = glob.glob(search_pattern)
            
            # 4. 準備循環列表
            self.tab_matches = [os.path.basename(p) for p in matches]
            # 如果是資料夾，不加斜線（Windows cmd 習慣）
            self.tab_index = 0
            self.is_tab_cycling = True
            self.tab_base_cmd = base_cmd # 記住前面的指令

        if self.tab_matches:
            match = self.tab_matches[self.tab_index]
            
            # 刪除並替換
            self.delete_current_line_input()
            
            # 組合回去
            if self.tab_base_cmd:
                new_line = f" {self.tab_base_cmd} {match}"
            else:
                new_line = f" {match}"
                
            self.insert(tk.END, new_line)
            
            self.tab_index = (self.tab_index + 1) % len(self.tab_matches)
        
        return "break"

class TerminalFrame(ttk.Frame):
    def __init__(self, master, work_dir, callback, initial_cmd=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.header_frame = ttk.Frame(self)
        self.header_frame.pack(fill=tk.X, pady=(0, 2))
        
        ttk.Label(self.header_frame, text=" TERMINAL: ", foreground="#888888", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.lbl_full_path = ttk.Label(self.header_frame, text=work_dir, foreground=COLOR_ACCENT, font=("Segoe UI", 9))
        self.lbl_full_path.pack(side=tk.LEFT, fill=tk.X, padx=5)

        container = ttk.Frame(self, padding=1) 
        container.pack(fill=tk.BOTH, expand=True)
        
        self.console = DarkInteractiveConsole(container, work_dir, self.on_dir_change, initial_cmd=initial_cmd)
        self.console.pack(fill=tk.BOTH, expand=True)
        
        self.external_callback = callback

    def on_dir_change(self, new_dir):
        self.lbl_full_path.config(text=new_dir)
        if self.external_callback:
            self.external_callback(new_dir)