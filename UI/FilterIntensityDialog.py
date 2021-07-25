import tkinter as tk
from UI.ViewerDialog import ViewerDialog
##Relative and percentage not implemented in Java version

class FilterIntensityDialog(ViewerDialog):
    def __init__(self, parent, title, intensity_min):
        self.intensity_min = intensity_min

        self.submit = False

        self.validate_intensity_min_details = tk.StringVar()
        
        super().__init__(parent, title, width=200, height=150)
    
    def body(self, frame):
        
        # Register validation methods
        validate_min_intensity = frame.register(self.confirm_valid_min_intensity)

        self.intensity_min_frame = tk.Frame(frame)

        self.lbl_intensity_min = tk.Label(self.intensity_min_frame, text="Min:")

        self.ent_intensity_min = tk.Entry(self.intensity_min_frame)
        self.ent_intensity_min.insert('end', self.intensity_min)

        # %P - on entry based on what change will result in.
        self.ent_intensity_min.config(validate="key", validatecommand=(validate_min_intensity,'%P'))

        self.lbl_validate_intensity_min = tk.Label(self.intensity_min_frame, fg="#ff0000", textvariable = self.validate_intensity_min_details)

        self.lbl_intensity_min.grid(row=0, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.ent_intensity_min.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_validate_intensity_min.grid(row=1, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.intensity_min_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side=tk.RIGHT, padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side=tk.RIGHT, padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

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