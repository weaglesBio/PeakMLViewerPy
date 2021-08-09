import tkinter as tk
from UI.ViewerDialog import ViewerDialog

class FilterMassDialog(ViewerDialog):
    def __init__(self, parent, title, mass_min, mass_max):
        self.mass_min = mass_min
        self.mass_max = mass_max

        self.submit = False

        self.validate_mass_min_details = tk.StringVar()
        self.validate_mass_max_details = tk.StringVar()

        super().__init__(parent, title, width=200, height=200)

    def body(self, frame):

        # Register validation methods
        validate_mass_min = frame.register(self.confirm_valid_mass_min)
        validate_mass_max = frame.register(self.confirm_valid_mass_max)

        self.lbl_mass_min = tk.Label(frame, text="Min:")
        self.lbl_mass_min.grid(row=0, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.ent_mass_min = tk.Entry(frame, width=10)
        self.ent_mass_min.insert('end', self.mass_min)
        self.ent_mass_min.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")

        # %P - on entry based on what change will result in.
        self.ent_mass_min.config(validate="key", validatecommand=(validate_mass_min,'%P'))

        self.lbl_validate_mass_min = tk.Label(frame, fg="#ff0000", textvariable = self.validate_mass_min_details)
        self.lbl_validate_mass_min.grid(row=1, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.lbl_mass_max = tk.Label(frame, text="Max:")
        self.lbl_mass_max.grid(row=2, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.ent_mass_max = tk.Entry(frame, width=10)
        self.ent_mass_max.insert('end', self.mass_max)
        self.ent_mass_max.grid(row=2, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")

        # %P - on entry based on what change will result in.
        self.ent_mass_max.config(validate="key", validatecommand=(validate_mass_max,'%P'))

        self.lbl_validate_mass_max = tk.Label(frame, fg="#ff0000", textvariable = self.validate_mass_max_details)
        self.lbl_validate_mass_max.grid(row=3, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")


    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.mass_min = self.ent_mass_min.get()
        self.mass_max = self.ent_mass_max.get()

        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    def confirm_valid_mass_min(self, input):
        is_valid = True

        try:
            float(input)     
        except ValueError:
            is_valid = False

        if is_valid:
            self.validate_mass_max_details.set("")
            self.btn_ok["state"] = "normal"
        else:
            self.validate_mass_max_details.set("Must be a decimal")
            self.btn_ok["state"] = "disabled"

        # Required to update value in entry.
        return True

    def confirm_valid_mass_max(self, input):
        is_valid = True

        try:
            float(input)     
        except ValueError:
            is_valid = False

        if is_valid:
            self.validate_mass_max_details.set("")
            self.btn_ok["state"] = "normal"
        else:
            self.validate_mass_max_details.set("Must be a decimal")
            self.btn_ok["state"] = "disabled"

        # Required to update value in entry.
        return True