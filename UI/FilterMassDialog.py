import tkinter as tk
from UI.ViewerDialog import ViewerDialog

class FilterMassDialog(ViewerDialog):
    def __init__(self, parent, title, mass_min, mass_max):
        self.mass_min = mass_min
        self.mass_max = mass_max
        self.submit = False
        self.validate_mass_details = tk.StringVar()

        super().__init__(parent, title, width=170, height=150)

    def body(self, frame):

        # Register validation methods
        validate_mass = frame.register(self.confirm_valid_mass)

        self._mass_frame = tk.Frame(frame, padx=5, pady=5)
        self._mass_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.lbl_validate_mass = tk.Label(frame, fg="#ff0000", textvariable = self.validate_mass_details)
        self.lbl_validate_mass.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.lbl_mass_min = tk.Label(self._mass_frame, text="Min:")

        self.ent_mass_min = tk.Entry(self._mass_frame, width=10)
        self.ent_mass_min.insert('end', self.mass_min)

        self.lbl_mass_max = tk.Label(self._mass_frame, text="Max:")

        self.ent_mass_max = tk.Entry(self._mass_frame, width=10)
        self.ent_mass_max.insert('end', self.mass_max)

        self.lbl_mass_min.grid(row=0, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.ent_mass_min.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.lbl_mass_max.grid(row=1, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.ent_mass_max.grid(row=1, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")

        # %P - on entry based on what change will result in.
        self.ent_mass_min.config(validate="key", validatecommand=(validate_mass,'%P'))
        self.ent_mass_max.config(validate="key", validatecommand=(validate_mass,'%P'))

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

        self.update_validation_status(True, "")

    def ok_btn_clicked(self):
        self.mass_min = self.ent_mass_min.get()
        self.mass_max = self.ent_mass_max.get()

        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    def confirm_valid_mass(self, input: str):

        try:
            float(input)     
        except ValueError:
            self.update_validation_status(False, "Must be a decimal")
            return False

        self.update_validation_status(True, "")
        # Required to update value in entry.
        return True

    def update_validation_status(self, valid: bool, message: str):
        if valid:
            self.lbl_validate_mass.configure(foreground="#808080")
            self.validate_mass_details.set("") # Parameters are valid
            self.btn_ok["state"] = "normal"
        else:
            self.lbl_validate_mass.configure(foreground="#ff0000")
            self.validate_mass_details.set(message)
            self.btn_ok["state"] = "disabled"