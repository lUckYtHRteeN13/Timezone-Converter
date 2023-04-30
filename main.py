import tkinter as tk
from tkinter import ttk
import utils

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_name = None

        self.SCR_WIDTH= self.winfo_screenwidth()
        self.SCR_HEIGHT= self.winfo_screenheight()
        self.geometry(f"300x300")
        self.title(self.app_name)
        
        # self.wm_attributes("-topmost", 1)
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(3, weight=1)

class CustomFrame(ttk.Frame):
    def __init__(self, master, **options):
        super().__init__(master, **options)

    def show(self):
        self.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()