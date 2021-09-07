import tkinter as tk
from UI.ViewerDialog import ViewerDialog
class SortDialog(ViewerDialog):
    def __init__(self, parent, title):
        self.sort_type = None
        self.sort_direction = None
        self.submit = False
        self.option_type_selected = tk.StringVar()
        self.option_direction_selected = tk.StringVar()
        super().__init__(parent, title, width=260, height=100, take_focus=True, extendable=False)
    
    def body(self, frame):

        type_list = ["Mass", "Intensity", "Retention Time", "Sample Count"]
        direction_list = ["ASC", "DESC"]

        self._sort_frame = tk.Frame(frame, padx=5, pady=5)
        self._sort_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.lbl_sort = tk.Label(self._sort_frame, width=5, text="By:")
        self.option_type = tk.OptionMenu(self._sort_frame, self.option_type_selected, *type_list)
        self.option_direction = tk.OptionMenu(self._sort_frame, self.option_direction_selected, *direction_list)

        self.lbl_sort.grid(row=0, column=0)
        self.option_type.grid(row=0, column=1)
        self.option_direction.grid(row=0, column=2)

        self.option_type_selected.set("Mass")
        self.option_direction_selected.set("ASC")

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