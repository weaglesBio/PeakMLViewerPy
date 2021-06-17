import tkinter as tk

class FilterRetentionTimeDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.retention_time_min = None
        self.retention_time_max = None
        super().__init__(parent, title)

    def body(self, frame):
        self.lbl_retention_time_min = tk.Label(frame, width=15, text="Min:")
        self.lbl_retention_time_max = tk.Label(frame, width=15, text="Max:")
        self.ent_retention_time_min = tk.Entry(frame, width=15)
        self.ent_retention_time_max = tk.Entry(frame, width=15)

        self.lbl_retention_time_min.grid(row=0, column=0)
        self.lbl_retention_time_max.grid(row=1, column=0)
        self.ent_retention_time_min.grid(row=0, column=1)
        self.ent_retention_time_max.grid(row=1, column=1)

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right")
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.retention_time_min = self.ent_retention_time_min.get()
        self.retention_time_max = self.ent_retention_time_max.get()
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()