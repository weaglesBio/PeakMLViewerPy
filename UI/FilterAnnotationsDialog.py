import tkinter as tk

class FilterAnnotationsDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.annotation_name = None
        self.annotation_relation = None
        self.annotation_value = None
        super().__init__(parent, title)
    
    def body(self, frame):
        option_annotation_relation_list = ["=", ">", "<", "like"]

        self.option_annotation_relation_selected = tk.StringVar(frame)
        self.option_annotation_relation_selected.set("=")

        self.lbl_annotation_name = tk.Label(frame, width=15, text="Name:")
        self.ent_annotation_name = tk.Entry(frame, width=15)

        self.lbl_annotation_relation = tk.Label(frame, width=15, text="Relation:")
        self.option_annotation_relation = tk.OptionMenu(frame, self.option_annotation_relation_selected, *option_annotation_relation_list)

        self.lbl_annotation_value = tk.Label(frame, width=15, text="Value:")
        self.ent_annotation_value = tk.Entry(frame, width=15)

        self.lbl_annotation_name.grid(row=0, column=0)
        self.ent_annotation_name.grid(row=0, column=1)
        self.lbl_annotation_relation.grid(row=1, column=0)
        self.option_annotation_relation.grid(row=1, column=1)
        self.lbl_annotation_value.grid(row=2, column=0)
        self.ent_annotation_value.grid(row=2, column=1)

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right")
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.ent_annotation_name = self.ent_annotation_name.get()
        self.annotation_relation = self.option_annotation_relation_selected.get()
        self.ent_annotation_value = self.ent_annotation_value.get()
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()