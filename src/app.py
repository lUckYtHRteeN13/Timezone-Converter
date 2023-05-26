import tkinter as tk
from tkinter import ttk
import utils

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__() 
        self.iconbitmap(utils.ICON_IMG)
        self.btn_img = tk.PhotoImage(file=utils.SWITCH_IMG)
        self.btn_img = self.btn_img.subsample(3,3)
        self.timezones = utils.TIMEZONE
        self.app_name = "Time Zone Converter"

        self.SCR_WIDTH= self.winfo_screenwidth()
        self.SCR_HEIGHT= self.winfo_screenheight()
        self.geometry(f"410x270")
        self.title(self.app_name)
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.hr_reg = self.register(self.hour_filter)
        self.min_reg = self.register(self.minute_filter)
        
        self.menu = tk.Menu(self)
        self.settings = tk.Menu(self.menu, tearoff=0)
        self.time_format = tk.StringVar()
        self.settings.add_radiobutton(label="24-hour Format", variable=self.time_format, value=24, command=self.change_time_format)
        self.settings.add_radiobutton(label="12-hour Format", variable=self.time_format, value=12, command=self.change_time_format)
        self.time_format.set(utils.time_format)

        self.settings.add_separator()
        self.settings.add_command(label="About")
        self.menu.add_cascade(label="Settings", menu=self.settings)

        self.gen_frame = ttk.Frame(self, relief="groove")
        self.gen_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=40)
        for i in range(6):
            self.gen_frame.grid_columnconfigure(i, weight=1)
        self.gen_frame.grid_rowconfigure(1, weight=1)
        self.gen_frame.grid_rowconfigure(0, weight=1)

        self.title_label = tk.Label(self, text=self.app_name)
        self.title_label.grid(row=0, sticky="nsew", padx=10, pady=10)

        self.input_hr = tk.StringVar()
        self.hour = tk.Entry(self.gen_frame, textvariable=self.input_hr, width=5, justify="center")
        self.hour.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.hour.config(validate="key", validatecommand=(self.hr_reg, '%P'))
        self.input_hr.set("00")

        self.title_label = tk.Label(self.gen_frame, text=":")
        self.title_label.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.input_min = tk.StringVar()
        self.minute = tk.Entry(self.gen_frame, textvariable=self.input_min, width=5, justify="center")
        self.minute.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.input_min.set("00")

        self.am_btn = tk.Button(self.gen_frame, text="AM", width=2, command=lambda e=1:self.set_day_type(e))
        self.am_btn.grid(row=0, column=3, sticky="ew", padx=3, pady=3)
        self.pm_btn = tk.Button(self.gen_frame, text="PM", width=2, command=lambda e=0:self.set_day_type(e))
        self.pm_btn.grid(row=0, column=4, sticky="ew", padx=3, pady=3)

        self.timezone1_var = tk.StringVar()
        self.timezone1_var.set("-")
        self.timezone1 = ttk.Combobox(self.gen_frame, textvariable=self.timezone1_var, state="readonly")
        self.timezone1.grid(row=0, column=5, sticky="ew", padx=5, pady=5)

        self.conversion_frame = ttk.Frame(self.gen_frame)
        self.conversion_frame.grid(row=2, column=0, columnspan=6, sticky="nsew", padx=5, pady=5)
        self.conversion_frame_col_count = 7

        for i in range(self.conversion_frame_col_count):
            self.conversion_frame.grid_columnconfigure(i, weight=1)

        self.timezone2_var = tk.StringVar()
        self.timezone2_var.set("-")
        self.timezone2 = ttk.Combobox(self.conversion_frame, textvariable=self.timezone2_var, state="readonly")
        self.timezone2.grid(row=0, column=2, columnspan=2, sticky="ew", padx=5, pady=5)

        self.switch = tk.Button(self.conversion_frame, image=self.btn_img, command=self.switch)
        self.switch.grid(row=0, column=4, padx=5, pady=5)

        self.result_frame = ttk.Frame(self.conversion_frame, relief="groove")
        self.result_frame.grid(row=1, column=1, columnspan=5, sticky="nsew", padx=5, pady=5)

        self.result_frame.grid_columnconfigure(0, weight=1)

        self.result_text = tk.StringVar()
        self.result = tk.Label(self.result_frame, textvariable=self.result_text)
        self.result.grid(sticky="nsew", padx=10, pady=10)

        self._config()

    def _config(self):
        self.config(menu=self.menu)
        self.change_time_format()

        self.hour.bind("<FocusOut>", lambda e: self.on_focusout(e) or self.display(e))
        self.hour.bind("<KeyRelease>", self.display)
        self.minute.config(validate="key", validatecommand=(self.min_reg, '%P'))
        self.minute.bind("<FocusOut>", lambda e: self.on_focusout(e) or self.display(e))
        self.minute.bind("<KeyRelease>", self.display)
        self.conversion_frame.columnconfigure(self.conversion_frame_col_count)
        self.timezone1.config(postcommand=lambda :self.update_options(self.timezone1, self.timezone2))
        self.timezone2.config(postcommand=lambda :self.update_options(self.timezone2, self.timezone1))
        self.timezone1.bind("<FocusOut>", self.display)
        self.timezone2.bind("<FocusOut>", self.display)
        self.timezone1.bind("<<ComboboxSelected>>", self.display)
        self.timezone2.bind("<<ComboboxSelected>>", self.display)

    def set_day_type(self, widget):
        if widget:
            self.am_btn.configure(relief=tk.SUNKEN)
            self.pm_btn.configure(relief=tk.RAISED)
        else:
            self.pm_btn.configure(relief=tk.SUNKEN)
            self.am_btn.configure(relief=tk.RAISED)

        utils.set_day_type(widget)
        print(utils.day_type)

    def change_time_format(self):
        utils.set_time_format(int(self.time_format.get()))
        if utils.time_format == 24:
            self.pm_btn.configure(relief=tk.RAISED)
            self.am_btn.configure(relief=tk.RAISED)
            self.am_btn.configure(state=tk.DISABLED)
            self.pm_btn.configure(state=tk.DISABLED)
            self.input_hr.set("00")
            self.input_min.set("00")
        else:
            self.input_hr.set("12")
            self.input_min.set("00")
            self.am_btn.configure(state=tk.NORMAL)
            self.pm_btn.configure(state=tk.NORMAL)

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
        if utils.time_format == 24:
            time =  utils.time_format-1
            if int(key) <= time:
                return True
            else:
                return False
        else:
            time = utils.time_format
            if 0 < int(key) <= time:
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

        if val2 == None:
            result = "Error"
        
        elif val1 != "" and val2 != "":
            result = f"{val1:02} : {val2:02} Day {day:+}"       
        else:
            result = f"{val1:02} : {val2:02}"

        self.result_text.set(result)

    def display(self, event):
        day = 0
        day_type = None
        value1 = self.hour.get()
        value2 = self.minute.get()

        time1 = self.timezone1_var.get()
        time2 = self.timezone2_var.get()

        try:
            diff1 = self.timezones[time1]
            hour, minute = utils.convert(value1, value2, diff1, reverse=True)

            diff2 = self.timezones[time2]
            value1, value2, day = utils.convert(hour, minute, diff2)

        except KeyError as ke:
            print(ke)
        
        except ValueError as ve:
            print(ve)

        if (self.timezone1.get() != "-"):
            self.update_result(value1, value2, day=day)
                
        else:
            self.update_result()

    def switch(self):
        time1 = self.timezone1_var.get()
        time2 = self.timezone2_var.get()

        self.timezone1_var.set(time2)
        self.timezone2_var.set(time1)

        self.display(None)
    
    def update(self):
        self.display(None)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
