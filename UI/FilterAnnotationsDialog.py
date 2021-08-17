import tkinter as tk
from UI.ViewerDialog import ViewerDialog
class FilterAnnotationsDialog(ViewerDialog):
    def __init__(self, parent, title):
        self.annotation_name = None
        self.annotation_relation = None
        self.annotation_value = None
        self.submit = False
        super().__init__(parent, title, width=200, height=200)
    
    def body(self, frame):
        option_annotation_relation_list = ["=", ">", "<", "like"]

        self.option_annotation_relation_selected = tk.StringVar(frame)
        self.option_annotation_relation_selected.set("=")

        self.lbl_annotation_name = tk.Label(frame, width=10, text="Label:")
        self.ent_annotation_name = tk.Entry(frame, width=15)

        self.lbl_annotation_relation = tk.Label(frame, width=10)
        self.option_annotation_relation = tk.OptionMenu(frame, self.option_annotation_relation_selected, *option_annotation_relation_list)

        self.lbl_annotation_value = tk.Label(frame, width=10, text="Value:")
        self.ent_annotation_value = tk.Entry(frame, width=15)

        self.lbl_annotation_name.grid(row=0, column=0)
        self.ent_annotation_name.grid(row=0, column=1)
        self.lbl_annotation_relation.grid(row=1, column=0)
        self.option_annotation_relation.grid(row=1, column=1)
        self.lbl_annotation_value.grid(row=2, column=0)
        self.ent_annotation_value.grid(row=2, column=1)

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.ent_annotation_name = self.ent_annotation_name.get()
        self.annotation_relation = self.option_annotation_relation_selected.get()
        self.ent_annotation_value = self.ent_annotation_value.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    def confirm_valid_annotation(self, input):

 
        # Like is not valid option for a number
        # 
        # Use 'like' for non-numbers


        try:
            float(input)     
        except ValueError:
            self.validate_intensity_min_details.set("Must be a decimal")
            return False

        is_valid = True

        try:
            float(input)     
        except ValueError:
            is_valid = False

        if is_valid:
            self.validate_intensity_min_details.set("")
            self.btn_ok["state"] = "normal"
        else:
            self.validate_intensity_min_details.set("Intensity must be a decimal")
            self.btn_ok["state"] = "disabled"

        # Required to update value in entry.
        return True