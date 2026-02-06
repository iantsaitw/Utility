import tkinter as tk
from tkinter import ttk
import config

class UIFactory:
    """
    Modular UI Engine: Responsible for producing widgets with a unified style
    following Windows 11 Design Guidelines.
    """
    
    @staticmethod
    def get_font(size=9, weight="normal"):
        """ Helper to retrieve the current font family from settings """
        family = config.current_settings.get("font_family", "Segoe UI")
        return (family, size, weight)

    @staticmethod
    def create_frame(parent, **kwargs):
        """ Create a standard themed container """
        return ttk.Frame(parent, **kwargs)

    @staticmethod
    def create_header_label(parent, text):
        """ Create a large header label """
        return ttk.Label(parent, text=text, font=UIFactory.get_font(20, "bold"))

    @staticmethod
    def create_sub_label(parent, text):
        """ Create a standard sub-label or body text """
        return ttk.Label(parent, text=text, font=UIFactory.get_font(10))

    @staticmethod
    def create_primary_button(parent, text, command, width=None):
        """ Create an accent-colored button """
        btn = ttk.Button(parent, text=text, command=command, style="Accent.TButton")
        if width: btn.configure(width=width)
        return btn

    @staticmethod
    def create_secondary_button(parent, text, command, width=None):
        """ Create a standard secondary button """
        btn = ttk.Button(parent, text=text, command=command)
        if width: btn.configure(width=width)
        return btn
    
    @staticmethod
    def create_entry(parent, initial_value=""):
        """ Create a standard text entry """
        entry = ttk.Entry(parent, font=UIFactory.get_font(9))
        if initial_value:
            entry.delete(0, tk.END)
            entry.insert(0, str(initial_value))
        return entry

    @staticmethod
    def create_treeview(parent, columns):
        """ Create a standard data grid (Treeview) """
        tree = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            tree.heading(col, text=col.title(), anchor="center")
        return tree
