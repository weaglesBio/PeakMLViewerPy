import tkinter as tk
from UI.ViewerDialog import ViewerDialog
class FilterAnnotationsDialog(ViewerDialog):
    def __init__(self, parent, title):
        self.annotation_name = None
        self.annotation_relation = None
        self.annotation_value = None
        self.submit = False
        self.option_annotation_relation_selected = tk.StringVar()
        self.validate_annotation_details = tk.StringVar()

        super().__init__(parent, title, width=180, height=150, take_focus=True, extendable=False)
    
    def body(self, frame):

        # Register validation methods
        validate_annotation = frame.register(self.update_to_valid_relation_option)

        option_annotation_relation_list = ["=", ">", "<", "like"]

        self._figure_frame = tk.Frame(frame, padx=5, pady=5)
        self._figure_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.lbl_annotation_name = tk.Label(self._figure_frame, width=7, text="Label:")
        self.ent_annotation_name = tk.Entry(self._figure_frame, width=15)

        self.lbl_annotation_relation = tk.Label(self._figure_frame, width=5)
        self.option_annotation_relation = tk.OptionMenu(self._figure_frame, self.option_annotation_relation_selected, *option_annotation_relation_list)

        self.lbl_annotation_value = tk.Label(self._figure_frame, width=7, text="Value:")
        self.ent_annotation_value = tk.Entry(self._figure_frame, width=15)

        self.lbl_annotation_name.grid(row=0, column=0)
        self.ent_annotation_name.grid(row=0, column=1)
        self.lbl_annotation_relation.grid(row=1, column=0)
        self.option_annotation_relation.grid(row=1, column=1)
        self.lbl_annotation_value.grid(row=2, column=0)
        self.ent_annotation_value.grid(row=2, column=1)

        # %P - on entry based on what change will result in.
        self.ent_annotation_value.config(validate="key", validatecommand=(validate_annotation,'%P'))

        self.option_annotation_relation_selected.set("=")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.annotation_name = self.ent_annotation_name.get()
        self.annotation_relation = self.option_annotation_relation_selected.get()
        self.annotation_value = self.ent_annotation_value.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    def update_to_valid_relation_option(self, input):

        # Like is not valid option for a number
        # Use 'like' for non-numbers

        try:
            float(input)     
        except ValueError:
            self.option_annotation_relation_selected.set("like")

        # Required to update value in entry.
        return True
