import tkinter as tk
from tkinter import ttk
import utils

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.timezones = {"UTC":utils.utc_converter, "JST":utils.jst_converter, "ET":utils.et_converter, "CT":utils.ct_converter, "MT":utils.mt_converter, "PT":utils.pt_converter}
        self.app_name = "Time Zone Converter"

        self.SCR_WIDTH= self.winfo_screenwidth()
        self.SCR_HEIGHT= self.winfo_screenheight()
        self.geometry(f"350x250")
        self.title(self.app_name)
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.hr_reg = self.register(self.hour_filter)
        self.min_reg = self.register(self.minute_filter)

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
        self.hour.config(validate="key", validatecommand=(self.hr_reg, '%P'))
        self.hour.bind("<FocusOut>", lambda e: self.on_focusout(e) or self.display(e))
        self.hour.bind("<KeyRelease>", self.display)

        self.title_label = tk.Label(self.gen_frame, text=":")
        self.title_label.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.input_min = tk.StringVar()
        self.minute = tk.Entry(self.gen_frame, textvariable=self.input_min, width=5, justify="center")
        self.minute.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.minute.config(validate="key", validatecommand=(self.min_reg, '%P'))
        self.minute.bind("<FocusOut>", lambda e: self.on_focusout(e) or self.display(e))
        self.minute.bind("<KeyRelease>", self.display)

        self.timezone1_var = tk.StringVar()
        self.timezone1_var.set("-")
        self.timezone1 = ttk.Combobox(self.gen_frame, textvariable=self.timezone1_var, state="readonly")
        self.timezone1.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        self.conversion_frame = ttk.Frame(self.gen_frame)
        self.conversion_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        self.conversion_frame_col_count = 7
        self.conversion_frame.columnconfigure(self.conversion_frame_col_count)

        for i in range(self.conversion_frame_col_count):
            self.conversion_frame.grid_columnconfigure(i, weight=1)

        self.timezone2_var = tk.StringVar()
        self.timezone2_var.set("-")
        self.timezone2 = ttk.Combobox(self.conversion_frame, textvariable=self.timezone2_var, state="readonly")
        self.timezone2.grid(row=0, column=2, columnspan=3, sticky="ew", padx=5, pady=5)

        self.result_frame = ttk.Frame(self.conversion_frame, relief="groove")
        self.result_frame.grid(row=1, column=1, columnspan=5, sticky="nsew", padx=5, pady=5)

        self.result_frame.grid_columnconfigure(0, weight=1)

        self.result_text = tk.StringVar()
        self.result_text.set("00 : 00")
        self.result = tk.Label(self.result_frame, textvariable=self.result_text)
        self.result.grid(sticky="nsew", padx=10, pady=10)

        self.timezone1.config(postcommand=lambda :self.update_options(self.timezone1, self.timezone2))
        self.timezone2.config(postcommand=lambda :self.update_options(self.timezone2, self.timezone1))
        self.timezone1.bind("<FocusOut>", self.display)
        self.timezone2.bind("<FocusOut>", self.display)
        self.timezone1.bind("<<ComboboxSelected>>", self.display)
        self.timezone2.bind("<<ComboboxSelected>>", self.display)

    def update_options(self, w1, w2):
        w1_picked = w1.get()
        w2_picked = w2.get()

        timezones = self.timezones.keys()
        options = list(timezones)[:]

        if w1_picked in options:
            options.remove(w1_picked)

        if w2_picked in options:
            options.remove(w2_picked)

        options.insert(0, "-")

        if w1_picked == "-":
            options.remove("-")

        w1['values'] = options

    def on_focusout(self, event):
        widget = event.widget
        widget_text = widget.get()
        if len(widget_text) == 1:
            widget.delete(0, tk.END)
            widget.insert(0, f"{int(widget_text):02d}")

    @utils.time_filter
    def hour_filter(self, key):
        if int(key) <= 23:
            return True
        else:
            return False

    @utils.time_filter
    def minute_filter(self, key):
        if int(key) <= 59:
            return True
        else:
            return False
    
    def update_result(self, val1=None, val2=None, day=None):

        if val1 == "":
            val1 = "00"

        if val2 == "":
            val2 = "00"

        if val1 == None or val2 == None:
            result = "Error"
        else:
            result = f"{val1} : {val2} Day {day:+}"

        self.result_text.set(result)
        

    def display(self, event):
        value1 = self.hour.get()
        value2 = self.minute.get()

        time1 = self.timezone1_var.get()
        time2 = self.timezone2_var.get()

        try:
            timezone1 = self.timezones[time1]
            hour, minute = timezone1(value1, value2, reverse=True)

            timezone2 = self.timezones[time2]
            value1, value2, day = timezone2(hour, minute)
        except KeyError as ke:
            print(ke)
        
        except ValueError as ve:
            print(ve)

        print(time1, time2)
        print(value1, value2)

        if (self.timezone1.get() != "-") and (self.timezone2.get() != "-"):
            self.update_result(value1, value2, day=day)
        else:
            self.update_result()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
