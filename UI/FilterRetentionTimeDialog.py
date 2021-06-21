import tkinter as tk
import tkinter.ttk as ttk

class FilterRetentionTimeDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.retention_time_min_hr = None
        self.retention_time_min_minu = None
        self.retention_time_max_hr = None
        self.retention_time_max_minu = None
        self.submit = False
        super().__init__(parent, title)

    def body(self, frame):

        self.lbl_mini = tk.Label(self.frame, width=15, text="Minimum:")
        self.lbl_max = tk.Label(self.frame, width=15, text="Maximum:")
        self.lbl_hour = tk.Label(self.frame, width=15, text="Hour")
        self.lbl_minu = tk.Label(self.frame, width=15, text="Minute")

        self.val_mini_hr = tk.StringVar()
        self.val_max_hr = tk.StringVar()
        self.val_mini_min = tk.StringVar()
        self.val_max_min = tk.StringVar()

        self.spbx_mini_hr = ttk.Spinbox(self.frame, width=15, from_=0, to=23, textvariable=self.val_mini_hr)
        self.spbx_max_hr = ttk.Spinbox(self.frame, width=15, from_=0, to=23, textvariable=self.val_max_hr)
        self.spbx_mini_min = ttk.Spinbox(self.frame, width=15, from_=0, to=59, textvariable=self.val_mini_min)
        self.spbx_max_min = ttk.Spinbox(self.frame, width=15, from_=0, to=59, textvariable=self.val_max_min)

        self.lbl_mini.grid(row=1, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_max.grid(row=2, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_hour.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_minu.grid(row=0, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_mini_hr.grid(row=1, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_max_hr.grid(row=2, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_mini_min.grid(row=1, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_max_min.grid(row=2, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.retention_time_min_hr = self.val_mini_hr.get()
        self.retention_time_max_hr = self.val_max_hr.get()
        self.retention_time_min_minu = self.val_mini_min.get()
        self.retention_time_max_minu = self.val_max_min.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()