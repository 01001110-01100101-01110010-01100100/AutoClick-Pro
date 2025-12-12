# components.py
import tkinter as tk
from styles import CORES, FONT_MAIN

class ModernButton(tk.Button):
    def __init__(self, master, hover_color=CORES["btn_hover"], **kwargs):
        kwargs.setdefault("bg", CORES["btn_bg"])
        kwargs.setdefault("fg", CORES["fg"])
        kwargs.setdefault("bd", 0)
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("font", FONT_MAIN)
        kwargs.setdefault("activebackground", CORES["btn_press"])
        kwargs.setdefault("activeforeground", CORES["fg"])
        kwargs.setdefault("cursor", "hand2")
        
        super().__init__(master, **kwargs)
        self.default_bg = kwargs["bg"]
        self.hover_color = hover_color
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e): self.config(bg=self.hover_color)
    def on_leave(self, e): self.config(bg=self.default_bg)

class ModernEntry(tk.Entry):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("bg", "#404040")
        kwargs.setdefault("fg", "white")
        kwargs.setdefault("insertbackground", "white")
        kwargs.setdefault("bd", 0)
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("font", FONT_MAIN)
        super().__init__(master, **kwargs)