import tkinter as tk
from UI.ViewerDialog import ViewerDialog
from molmass import Formula, FormulaError


class FilterMassDialog(ViewerDialog):
    def __init__(self, parent, title, mass_min, mass_max):
        self.mass_min = mass_min
        self.mass_max = mass_max
        self.submit = False
        self.validate_mass_details = tk.StringVar()
        self.val_charge = tk.StringVar()
        self.radio_var = tk.IntVar()
        self.val_charge.set("1")
        self.radio_var.set(1)

        super().__init__(parent, title, width=220, height=350, take_focus=True, extendable=False)

    def body(self, frame):

        # Register validation methods
        validate_decimal = frame.register(self.confirm_valid_decimal)

        self._radio_frame = tk.Frame(frame, padx=5, pady=5)
        self._radio_frame.pack(fill=tk.BOTH, expand = tk.FALSE)    

        # Add radio buttons at top.
        self._mass_radio_range = tk.Radiobutton(self._radio_frame, text="Range", variable=self.radio_var, value=1)        
        self._mass_radio_range.grid(row=0, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self._mass_radio_formula = tk.Radiobutton(self._radio_frame, text="Formula", variable=self.radio_var, value=2)
        self._mass_radio_formula.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")

        self._options_frame = tk.Frame(frame, padx=5, pady=5)
        self._options_frame.pack(fill=tk.BOTH, expand = tk.FALSE)

        self._mass_frame = tk.LabelFrame(self._options_frame, padx=5, pady=5, text="Range")
        self._mass_frame.pack(fill=tk.BOTH, expand = tk.FALSE)

        self._formula_frame = tk.LabelFrame(self._options_frame, padx=5, pady=5, text="Formula")
        self._formula_frame.pack(fill=tk.BOTH, expand = tk.FALSE)

        # Mass range frame

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

        # Formula frame

        self.lbl_formula = tk.Label(self._formula_frame, text="Formula:")
        self.ent_formula = tk.Entry(self._formula_frame, width=20)

        self.lbl_ppm = tk.Label(self._formula_frame, text="PPM:")
        self.ent_ppm = tk.Entry(self._formula_frame, width=5)
        self.ent_ppm.insert('end', 0)

        self.lbl_charge = tk.Label(self._formula_frame, text="Charge:")
        self.spbx_charge = tk.Spinbox(self._formula_frame, width=5, from_=0, to=9, state='readonly', textvariable=self.val_charge)

        self.lbl_formula.grid(row=0, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.ent_formula.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_ppm.grid(row=1, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.ent_ppm.grid(row=1, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_charge.grid(row=2, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.spbx_charge.grid(row=2, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        
        # Add validation label below frame.

        self.lbl_validate_mass = tk.Label(frame, fg="#ff0000", textvariable = self.validate_mass_details)
        self.lbl_validate_mass.pack(fill=tk.BOTH, expand = tk.FALSE)


        # %P - on entry based on what change will result in.
        self.ent_mass_min.config(validate="key", validatecommand=(validate_decimal,'%P'))
        self.ent_mass_max.config(validate="key", validatecommand=(validate_decimal,'%P'))
        self.ent_ppm.config(validate="key", validatecommand=(validate_decimal,'%P'))

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

        self.update_validation_status(True, "")

    def ok_btn_clicked(self):

        if self.radio_var.get() == 2:
            #get monoisotopic mass from chemical formula
            try:
                f = Formula(self.ent_formula.get())
                mass = f.isotope.mass
                formula_valid = True
            except FormulaError:
                formula_valid = False

            if formula_valid:

                divided_mass = mass / int(self.val_charge.get())

                #calculate delta
                delta = float(self.ent_ppm.get()) * (0.000001*divided_mass)

                #set minmass and maxmass
                self.mass_min = mass - delta
                self.mass_max = mass + delta

                self.submit = True
                self.destroy()

            else:
                self.update_validation_status(False, "Formula is invalid")

        else:
            self.mass_min = self.ent_mass_min.get()
            self.mass_max = self.ent_mass_max.get()

            self.submit = True
            self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    def confirm_valid_decimal(self, input: str):

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
        else:
            self.lbl_validate_mass.configure(foreground="#ff0000")
            self.validate_mass_details.set(message)

