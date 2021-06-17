import tkinter as tk

##Relative and percentage not implemented in Java version

class FilterIntensityDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.intensity_min = None
        self.intensity_unit = None
        super().__init__(parent, title)
    
    def body(self, frame):

        self.lbl_intensity_min = tk.Label(frame, width=15, text="Minimum intensity:")
        self.lbl_intensity_min.grid(row=0, column=0)

        self.ent_intensity_min = tk.Entry(frame, width=15)
        self.ent_intensity_min.grid(row=0, column=1)

        #option_intensity_unit_list = ["Absolute", "Relative", "Percentage"]

        #self.option_intensity_unit_selected = tk.StringVar(frame)
        #self.option_intensity_unit_selected.set("Absolute")

        #self.option_intensity_unit = tk.OptionMenu(frame, self.option_intensity_unit_selected, *option_intensity_unit_list)
        #self.option_intensity_unit.grid(row=0, column=2)

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right")
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.intensity_min = self.ent_intensity_min.get()
        #self.intensity_unit = self.option_intensity_unit_selected.get()
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()