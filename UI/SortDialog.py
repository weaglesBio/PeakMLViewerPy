import tkinter as tk
from UI.ViewerDialog import ViewerDialog
class SortDialog(ViewerDialog):
    def __init__(self, parent, title):
        self.sort_type = None
        self.sort_direction = None
        self.submit = False
        super().__init__(parent, title, width=250, height=120)
    
    def body(self, frame):

        type_list = ["Mass", "Intensity", "Retention Time", "Sample Count"]
        direction_list = ["ASC", "DESC"]

        self.option_type_selected = tk.StringVar(frame)
        self.option_type_selected.set("Mass")
        self.option_direction_selected = tk.StringVar(frame)
        self.option_direction_selected.set("ASC")

        self.lbl_sort = tk.Label(frame, width=5, text="By:")
        self.option_type = tk.OptionMenu(frame, self.option_type_selected, *type_list)
        self.option_direction = tk.OptionMenu(frame, self.option_direction_selected, *direction_list)

        self.lbl_sort.grid(row=0, column=0)
        self.option_type.grid(row=0, column=1)
        self.option_direction.grid(row=0, column=2)

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.sort_type = self.option_type_selected.get()
        self.sort_direction = self.option_direction_selected.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()