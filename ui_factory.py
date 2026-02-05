# ui_factory.py
import tkinter as tk
from tkinter import ttk
import config  # [新增] 匯入設定檔

class UIFactory:
    """
    Modular UI Engine: 負責生產統一風格的元件
    符合 Windows 11 Design Guideline，並支援使用者自訂字體
    """
    
    # Helper: 取得當前字體設定
    @staticmethod
    def get_font(size=9, weight="normal"):
        family = config.current_settings.get("font_family", "Segoe UI")
        return (family, size, weight)

    @staticmethod
    def create_frame(parent, **kwargs):
        """ 建立標準容器 """
        return ttk.Frame(parent, **kwargs)

    @staticmethod
    def create_header_label(parent, text):
        """ 大標題文字 (Size 20, Bold) """
        return ttk.Label(parent, text=text, font=UIFactory.get_font(20, "bold"))

    @staticmethod
    def create_sub_label(parent, text):
        """ 副標題/一般文字 (Size 10) """
        return ttk.Label(parent, text=text, font=UIFactory.get_font(10))

    @staticmethod
    def create_primary_button(parent, text, command, width=None):
        """ 主要按鈕 (Accent Color) """
        # 按鈕字體通常由 Style 控制，但也可以這裡強制覆蓋，暫時保持 Style 控制
        btn = ttk.Button(parent, text=text, command=command, style="Accent.TButton")
        if width: btn.configure(width=width)
        return btn

    @staticmethod
    def create_secondary_button(parent, text, command, width=None):
        """ 次要按鈕 (標準樣式) """
        btn = ttk.Button(parent, text=text, command=command)
        if width: btn.configure(width=width)
        return btn
    
    @staticmethod
    def create_entry(parent, initial_value=""):
        """ 輸入框 """
        entry = ttk.Entry(parent, font=UIFactory.get_font(9))
        if initial_value:
            entry.delete(0, tk.END)
            entry.insert(0, str(initial_value))
        return entry

    @staticmethod
    def create_treeview(parent, columns):
        """ 列表視圖 """
        # Treeview 的內容字體由 Style "Treeview" 控制 (在 main.py 設定)
        # 這裡只負責結構
        tree = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col.title(), anchor="center")
        return tree