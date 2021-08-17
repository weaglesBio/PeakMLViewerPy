import tkinter as tk
from UI.ViewerDialog import ViewerDialog

class FilterProbabilityDialog(ViewerDialog):
    def __init__(self, parent, title):
        self.submit = False
        self.validate_probability_details = tk.StringVar()

        super().__init__(parent, title, width=200, height=200)

    def body(self, frame):

        # Register validation methods
        validate_probability = frame.register(self.confirm_probability_valid)

        self.lbl_info_probability = tk.Label(frame, text="Filters to to entries with at least one identification of probability")
        self.lbl_info_probability.pack(fill=tk.BOTH, expand = tk.TRUE)

        self._figure_frame = tk.Frame(frame, padx=20, pady=20)
        self._figure_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.lbl_validate_probability = tk.Label(frame, fg="#ff0000", textvariable = self.validate_probability_details)
        self.lbl_validate_probability.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.lbl_mini = tk.Label(self._figure_frame, width=10, text="Minimum:")
        self.lbl_max = tk.Label(self._figure_frame, width=10, text="Maximum:")
        self.lbl_prior = tk.Label(self._figure_frame, width=5, text="Prior")
        self.lbl_post = tk.Label(self._figure_frame, width=5, text="Post")

        self.ent_prior_min = tk.Entry(self._figure_frame, width=5)
        self.ent_prior_max = tk.Entry(self._figure_frame, width=5)
        self.ent_post_min = tk.Entry(self._figure_frame, width=5)
        self.ent_post_max = tk.Entry(self._figure_frame, width=5)

        # %P - on entry based on what change will result in.
        self.ent_prior_min.config(validate="key", validatecommand=(validate_probability,'%P'))
        self.ent_prior_max.config(validate="key", validatecommand=(validate_probability,'%P'))
        self.ent_post_min.config(validate="key", validatecommand=(validate_probability,'%P'))
        self.ent_post_max.config(validate="key", validatecommand=(validate_probability,'%P'))

        self.lbl_mini.grid(row=1, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_max.grid(row=2, column=0, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_prior.grid(row=0, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.lbl_post.grid(row=0, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")

        self.ent_prior_min.grid(row=1, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.ent_prior_max.grid(row=2, column=1, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.ent_post_min.grid(row=1, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")
        self.ent_post_max.grid(row=2, column=2, padx=(2,2), pady=(5,5), sticky="NEWS")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.prior_min = self.ent_prior_min.get()
        self.prior_max = self.ent_prior_max.get()
        self.post_min = self.ent_post_min.get()
        self.post_max = self.ent_post_max.get()

        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

# Validate prior entry to only two decimal place value between 1 and 0
    # Can also be blank
    def confirm_probability_valid(self, input):

        # Unset is valid entry
        if input == "":
            self.validate_probability_details.set("")
            return True

        try:
            float(input)
        except ValueError:
            self.validate_probability_details.set("Must be a decimal")
            return False

        # Must be greater than or equal to 0
        if float(input) < 0:
            self.validate_probability_details.set("Must be >= 0")
            return False

        # Must be less than or equal to 1
        if float(input) > 1:
            self.validate_probability_details.set("Must be <= 1")
            return False

        # Must be max 2 decimal places, so four characters long in total.
        if len(input) > 4:
            self.validate_probability_details.set("Max 2 decimal places")
            return False

        # If passes all criteria
        self.validate_probability_details.set("")
        return True