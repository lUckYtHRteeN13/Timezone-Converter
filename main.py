import tkinter as tk
from tkinter import ttk
import utils

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.timezones = []
        self.app_name = "Time Zone Converter"

        self.SCR_WIDTH= self.winfo_screenwidth()
        self.SCR_HEIGHT= self.winfo_screenheight()
        self.geometry(f"350x250")
        self.title(self.app_name)
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.reg = self.register(self.filter)

        self.gen_frame = ttk.Frame(self, relief="groove")
        self.gen_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=40)
        self.gen_frame.grid_columnconfigure(0, weight=1)
        self.gen_frame.grid_columnconfigure(1, weight=1)
        self.gen_frame.grid_columnconfigure(2, weight=1)
        self.gen_frame.grid_columnconfigure(3, weight=1)
        self.gen_frame.grid_rowconfigure(1, weight=1)
        self.gen_frame.grid_rowconfigure(0, weight=1)

        self.title_label = tk.Label(self, text=self.app_name)
        self.title_label.grid(row=0, sticky="nsew", padx=10, pady=10)

        self.input_hr = tk.StringVar()
        self.hour = tk.Entry(self.gen_frame, textvariable=self.input_hr, width=5, justify="center")
        self.hour.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.hour.config(validate="key", validatecommand=(self.reg, '%P'))

        self.title_label = tk.Label(self.gen_frame, text=":")
        self.title_label.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.input_min = tk.StringVar()
        self.minute = tk.Entry(self.gen_frame, textvariable=self.input_min, width=5, justify="center")
        self.minute.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.minute.config(validate="key", validatecommand=(self.reg, '%P'))

        self.timezone1 = ttk.Combobox(self.gen_frame, values=self.timezones, state="readonly")
        self.timezone1.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        self.conversion_frame = ttk.Frame(self.gen_frame)
        self.conversion_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        self.conversion_frame_col_count = 7
        self.conversion_frame.columnconfigure(self.conversion_frame_col_count)

        for i in range(self.conversion_frame_col_count):
            self.conversion_frame.grid_columnconfigure(i, weight=1)

        self.timezone2 = ttk.Combobox(self.conversion_frame, values=self.timezones, state="readonly")
        self.timezone2.grid(row=0, column=2, columnspan=3, sticky="ew", padx=5, pady=5)

        self.result_frame = ttk.Frame(self.conversion_frame, relief="groove")
        self.result_frame.grid(row=1, column=1, columnspan=5, sticky="nsew", padx=5, pady=5)

        self.result_frame.grid_columnconfigure(0, weight=1)

        self.result = tk.Label(self.result_frame, text="Hello")
        self.result.grid(sticky="nsew", padx=10, pady=10)

    def filter(self, key):
        if key.isdigit() and len(key) <= 2:
            return True

        elif key is "":
            return True

        else:
            return False

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()