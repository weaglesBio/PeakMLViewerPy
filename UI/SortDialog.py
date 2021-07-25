import tkinter as tk
from UI.ViewerDialog import ViewerDialog
class SortDialog(ViewerDialog):
    def __init__(self, parent):
        self.sort_type = None
        self.submit = False
        super().__init__(parent, "Sort")
    
    def body(self, frame):

        option_sort_list = ["mass ascending", "mass descending", "intensity ascending", "intensity descending", "retention-time ascending", "retention-time descending"]

        self.option_sort_selected = tk.StringVar(frame)
        self.option_sort_selected.set("mass ascending")

        self.lbl_sort = tk.Label(frame, width=15, text="Type:")
        self.option_sort = tk.OptionMenu(frame, self.option_sort_selected, *option_sort_list)
        self.lbl_sort.grid(row=0, column=0)
        self.option_sort.grid(row=0, column=1)

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.sort_type = self.option_sort_selected.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()