import tkinter as tk
from UI.ViewerDialog import ViewerDialog
import copy

class FilterNumberDetectionsDialog(ViewerDialog):
    def __init__(self, parent, title, sample_count_min, sample_count_max):
        self.sample_count_min = sample_count_min
        self.sample_count_max = sample_count_max

        # copy required so can assign same value rather than bind together by reference
        self.sample_count = copy.copy(self.sample_count_min)
        self.val_sample_count = tk.StringVar(value=self.sample_count)

        self.submit = False

        super().__init__(parent, title, width=200, height=120)
    
    def body(self, frame):

        self.lbl_sample_count = tk.Label(frame, text="Count:")
        self.spbx_sample_count = tk.Spinbox(frame, width=5, from_=self.sample_count_min, to=self.sample_count_max, state='readonly', textvariable=self.val_sample_count)

        self.lbl_sample_count.grid(row=0, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_sample_count.grid(row=1, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.sample_count = self.val_sample_count.get()
        self.submit = True
        self.ok()
        #self.destroy()

    def cancel_btn_clicked(self):
        self.cancel()
        #self.destroy()