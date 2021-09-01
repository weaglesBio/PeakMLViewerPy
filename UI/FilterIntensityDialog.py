import tkinter as tk
from UI.ViewerDialog import ViewerDialog
##Relative and percentage not implemented in Java version

class FilterIntensityDialog(ViewerDialog):
    def __init__(self, parent, title, intensity_min):
        self.intensity_min = intensity_min
        self.submit = False
        self.validate_intensity_min_details = tk.StringVar()
        
        super().__init__(parent, title, width=200, height=130)
    
    def body(self, frame):
        
        # Register validation methods
        validate_min_intensity = frame.register(self.confirm_valid_min_intensity)

        self._intensity_frame = tk.Frame(frame, padx=5, pady=5)
        self._intensity_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.lbl_validate_intensity_min = tk.Label(frame, fg="#ff0000", textvariable = self.validate_intensity_min_details)
        self.lbl_validate_intensity_min.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.lbl_intensity_min = tk.Label(self._intensity_frame, text="Min:")

        self.ent_intensity_min = tk.Entry(self._intensity_frame, width=10)
        self.ent_intensity_min.insert('end', self.intensity_min)

        # %P - on entry based on what change will result in.
        self.ent_intensity_min.config(validate="key", validatecommand=(validate_min_intensity,'%P'))

        self.lbl_intensity_min.grid(row=0, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        
        self.ent_intensity_min.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side=tk.RIGHT, padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side=tk.RIGHT, padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

        self.update_validation_status(True, "")

    def ok_btn_clicked(self):
        self.intensity_min = self.ent_intensity_min.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    def confirm_valid_min_intensity(self, input):

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
            self.lbl_validate_intensity_min.configure(foreground="#808080")
            self.validate_intensity_min_details.set("") # Parameters are valid
            self.btn_ok["state"] = "normal"
        else:
            self.lbl_validate_intensity_min.configure(foreground="#ff0000")
            self.validate_intensity_min_details.set(message)
            self.btn_ok["state"] = "disabled"