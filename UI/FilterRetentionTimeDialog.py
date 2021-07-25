import tkinter as tk
import tkinter.ttk as ttk
from UI.ViewerDialog import ViewerDialog

class FilterRetentionTimeDialog(ViewerDialog):
    def __init__(self, parent, title, rt_min, rt_max):

        self.rt_min_sec = 0
        self.rt_min_minu = 0
        self.rt_max_sec = 0
        self.rt_max_minu = 0

        if rt_max:
            rt_max_split = rt_max.split(":")
            self.rt_max_sec = rt_max_split[1]
            self.rt_max_minu = rt_max_split[0]

        if rt_min:
            rt_min_split = rt_min.split(":")
            self.rt_min_sec = rt_min_split[1]
            self.rt_min_minu = rt_min_split[0]
            
        self.retention_time_min_sec = None
        self.retention_time_min_minu = None
        self.retention_time_max_sec = None
        self.retention_time_max_minu = None
        self.submit = False

        super().__init__(parent, title, width=200, height=160)

    def body(self, frame):

        self.lbl_mini = tk.Label(frame, width=10, text="Minimum:")
        self.lbl_max = tk.Label(frame, width=10, text="Maximum:")
        self.lbl_sec = tk.Label(frame, width=5, text="Second")
        self.lbl_minu = tk.Label(frame, width=5, text="Minute")

        self.val_mini_sec = tk.StringVar(frame, value=self.rt_min_sec)
        self.val_max_sec = tk.StringVar(frame, value=self.rt_max_sec)
        self.val_mini_min = tk.StringVar(frame, value=self.rt_min_minu)
        self.val_max_min = tk.StringVar(frame, value=self.rt_max_minu)

        self.spbx_mini_sec = ttk.Spinbox(frame, width=5, from_=0, to=59, state='readonly', textvariable=self.val_mini_sec)
        self.spbx_max_sec = ttk.Spinbox(frame, width=5, from_=0, to=59, state='readonly', textvariable=self.val_max_sec)
        self.spbx_mini_min = ttk.Spinbox(frame, width=5, from_=0, to=self.rt_max_minu, state='readonly',  textvariable=self.val_mini_min)
        self.spbx_max_min = ttk.Spinbox(frame, width=5, from_=0, to=self.rt_max_minu, state='readonly', textvariable=self.val_max_min)

        self.lbl_mini.grid(row=1, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_max.grid(row=2, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_minu.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_sec.grid(row=0, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.spbx_mini_min.grid(row=1, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_mini_sec.grid(row=1, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_max_min.grid(row=2, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_max_sec.grid(row=2, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.retention_time_min_sec = self.val_mini_sec.get()
        self.retention_time_max_sec = self.val_max_sec.get()
        self.retention_time_min_minu = self.val_mini_min.get()
        self.retention_time_max_minu = self.val_max_min.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()