#This file creates custom, pre-styled UI widgets (buttons and labels) for your dashboard
#Instead of telling Tkinter what color and font to use every single time
#Not used in this project
import tkinter as tk
from config import Config

class StyledButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            font=("Arial", 10, "bold"),
            bg=Config.ACCENT_COLOR,
            fg="black",
            relief=tk.FLAT,
            padx=10
        )

class InfoLabel(tk.Label):
    def __init__(self, master, text, **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.config(
            bg=Config.PANEL_COLOR,
            fg=Config.TEXT_COLOR,
            font=("Arial", 11, "italic")
        )