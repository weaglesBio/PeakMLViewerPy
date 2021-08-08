import tkinter as tk
import tkinter.ttk as ttk
from UI.ViewerDialog import ViewerDialog

class PeakSplitDialog(ViewerDialog):
    def __init__(self, parent, title, rt):

        self.rt_sec = 0
        self.rt_min = 0

        if rt:
            rt_split = rt.split(":")
            self.rt_sec = rt_split[1]
            self.rt_min = rt_split[0]
            
        self.retention_time_sec = None
        self.retention_time_min = None
        self.submit = False

        super().__init__(parent, title, width=200, height=160)

    def body(self, frame):

        self.lbl_sec = tk.Label(frame, width=5, text="Sec")
        self.lbl_min = tk.Label(frame, width=5, text="Min")

        self.val_sec = tk.StringVar(frame, value=self.rt_sec)
        self.val_min = tk.StringVar(frame, value=self.rt_min)

        self.spbx_sec = ttk.Spinbox(frame, width=5, from_=0, to=59, state='readonly', textvariable=self.val_sec)
        self.spbx_min = ttk.Spinbox(frame, width=5, from_=0, to_=100, state='readonly',  textvariable=self.val_min)

        self.lbl_min.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_sec.grid(row=0, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.spbx_min.grid(row=1, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_sec.grid(row=1, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.retention_time_sec = self.val_sec.get()
        self.retention_time_min = self.val_min.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()