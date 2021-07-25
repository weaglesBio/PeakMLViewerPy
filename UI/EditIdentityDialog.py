import tkinter as tk
import tkinter.ttk as ttk
from UI.ViewerDialog import ViewerDialog

class EditIdentityDialog(ViewerDialog):
    def __init__(self, parent, title, id, prior, notes, ipa_imported):
        self.id = id
        self.prior = prior
        self.notes = notes
        self.ipa_imported = ipa_imported
        self.submit = False
        self.validate_prior_details = tk.StringVar()
        self.validate_notes_details = tk.StringVar()
        super().__init__(parent, title, width=260, height=260)
    
    def body(self, frame):

        # Register validation methods
        validate_prior = frame.register(self.confirm_prior_valid)

        self.lbl_id = tk.Label(frame, width=5, text="ID:")
        self.lbl_id.grid(row=0, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_id_val = tk.Label(frame, width=5, text=self.id)
        self.lbl_id_val.grid(row=0, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_prior = tk.Label(frame, width=5, text="Prior:")
        self.lbl_prior.grid(row=1, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.ent_prior = tk.Entry(frame, width=10)
        self.ent_prior.insert('end', self.prior)
        self.ent_prior.grid(row=1, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        # %P - on entry based on what change will result in.
        self.ent_prior.config(validate="key", validatecommand=(validate_prior,'%P'))

        self.lbl_prior_validate = tk.Label(frame, width=5, fg="#ff0000", textvariable = self.validate_prior_details)
        self.lbl_prior_validate.grid(row=2, column=1, padx=(0,0), pady=(0,5),sticky="NEWS")

        if not self.ipa_imported: 
            # Disable event prior if not 
            self.ent_prior['state'] = 'disabled'

            # Set message explaining that
            self.lbl_prior_validate.config(fg="#303030")
            self.validate_prior_details.set("Editable if IPA")
            
        self.lbl_notes = tk.Label(frame, width=5, text="Notes:")
        self.lbl_notes.grid(row=3, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.txt_notes_frame = tk.Frame(frame)

        self.txt_notes = tk.Text(self.txt_notes_frame, width=20, height=5)
        self.txt_notes.grid(row=0, column=0)
        self.txt_notes_vsb = ttk.Scrollbar(self.txt_notes_frame, orient="vertical", command=self.txt_notes.yview)
        self.txt_notes_vsb.grid(row=0, column=1, sticky="NEWS")
        self.txt_notes.insert('end', self.notes)
        
        self.txt_notes_frame.grid(row=3, column=1, padx=(2,2), pady=(2,2), sticky="NEWS")

        self.txt_notes.bind("<KeyRelease>", self.confirm_notes_length)

        self.lbl_notes_validate = tk.Label(frame, width=5, fg="#000000", textvariable = self.validate_notes_details)
        self.lbl_notes_validate.grid(row=4, column=1, padx=(0,0), pady=(0,5),sticky="NEWS")

        self.validate_notes_details.set(f"{len(self.txt_notes.get('1.0',tk.END))}/140")

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='Save', width=5, command=self.save_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.save_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def save_btn_clicked(self):
        self.prior = self.ent_prior.get()
        self.notes = self.txt_notes.get("1.0",tk.END)
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    # Validate prior entry to only two decimal place value between 1 and 0
    # Can also be blank
    def confirm_prior_valid(self, input):

        # Unset is valid entry
        if input == "":
            self.validate_prior_details.set("")
            return True

        try:
            float(input)     
        except ValueError:
            self.validate_prior_details.set("Must be a decimal")
            #print("Input must be a decimal")
            return False

        # Must be greater than or equal to 0
        if float(input) < 0:
            self.validate_prior_details.set("Must be >= 0")
            #print("Input must be greater than or equal to 0")
            return False

        # Must be less than or equal to 1
        if float(input) > 1:
            self.validate_prior_details.set("Must be <= 1")
            #print("Input must be less than or equal to 1")
            return False

        # Must be max 2 decimal places, so four characters long in total.
        if len(input) > 4:
            self.validate_prior_details.set("Max 2 decimal places")
            #print("Input must be max 2 decimal places, so four characters long in total.")
            return False

        #print("Input valid")

        # If passes all criteria
        self.validate_prior_details.set("")
        return True

    def confirm_notes_length(self, event):
        content = event.widget.get(1.0, "end-1c")
        current_char_count = len(content)
        self.validate_notes_details.set(f"{current_char_count}/140")

        #TODO Key press - is incorrect number
        # Key release potential for unacceptable length - need to handle one.


        if current_char_count > 140:
            self.lbl_notes_validate.config(fg="#ff0000")
            self.btn_ok["state"] = "disabled"
        else:
            self.lbl_notes_validate.config(fg="#000000")
            self.btn_ok["state"] = "normal"

            