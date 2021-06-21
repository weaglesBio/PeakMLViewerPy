import tkinter as tk

class FilterNumberDetectionsDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.number_detections = None
        self.submit = False
        super().__init__(parent, title)
    
    def body(self, frame):
        self.lbl_number_detections = tk.Label(frame, width=15, text="Min:")
        self.ent_number_detections = tk.Entry(frame, width=15)

        self.lbl_number_detections.grid(row=0, column=0)
        self.ent_number_detections.grid(row=0, column=1)

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.number_detections = self.ent_number_detections.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()