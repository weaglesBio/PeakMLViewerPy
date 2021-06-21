import tkinter as tk

class FilterMassDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.mass_min = None
        self.mass_max = None
        self.formula = None
        self.formula_ppm = None
        self.charge = None
        self.filter_option = None
        self.submit = False

        super().__init__(parent, title)
    
    def body(self, frame):

        #|----------|------------|----------------|----------------|----------------------|
        #| radio A  | mass label | mass min entry | mass max entry |                      |
        #|----------|------------|----------------|----------------|----------------------|
        #| radio B  | formula lbl| formula entry  | formula ppm ent| formula charge entry |
        #|----------|------------|----------------|----------------|----------------------|
        self.selected_option = tk.StringVar()
        self.selected_option.set("mass")

        self.radio_option_mass = tk.Radiobutton(frame, width=5, text="", variable=self.selected_option, value='mass', command=self.select_filter)
        self.radio_option_formula = tk.Radiobutton(frame, width=5, text="", variable=self.selected_option, value='formula', command=self.select_filter)

        self.mass_label = tk.Label(frame, width=15, text="Mass range")
        self.ent_mass_min = tk.Entry(frame, width=15)
        self.ent_mass_max = tk.Entry(frame, width=15)

        self.formula_label = tk.Label(frame, width=15, text="Formula")
        self.ent_formula = tk.Entry(frame, width=15)
        self.ent_formula_ppm = tk.Entry(frame, width=15)
        self.ent_formula_charge = tk.Entry(frame, width=5)

        self.ent_formula_charge.insert(tk.END, '1')

        self.radio_option_mass.grid(row=0, column=0)
        self.radio_option_formula.grid(row=1, column=0)
        self.mass_label.grid(row=0, column=1)
        self.ent_mass_min.grid(row=0, column=2)
        self.ent_mass_max.grid(row=0, column=3)
        self.formula_label.grid(row=1, column=1)
        self.ent_formula.grid(row=1, column=2)
        self.ent_formula_ppm.grid(row=1, column=3)
        self.ent_formula_charge.grid(row=1, column=4)

        self.ent_mass_min.config(state='normal')
        self.ent_mass_max.config(state='normal')
        self.ent_formula.config(state='disabled')
        self.ent_formula_ppm.config(state='disabled')
        self.ent_formula_charge.config(state='disabled')

    def select_filter(self):
        if self.selected_option.get() == "mass":
            self.ent_mass_min.config(state='normal')
            self.ent_mass_max.config(state='normal')
            self.ent_formula.config(state='disabled')
            self.ent_formula_ppm.config(state='disabled')
            self.ent_formula_charge.config(state='disabled')

        elif self.selected_option.get() == "formula":
            self.ent_mass_min.config(state='disabled')
            self.ent_mass_max.config(state='disabled')
            self.ent_formula.config(state='normal')
            self.ent_formula_ppm.config(state='normal')
            self.ent_formula_charge.config(state='normal')

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
        self.mass_formula = self.ent_formula.get()
        self.mass_formula_ppm = self.ent_formula_ppm.get()
        self.mass_charge = self.ent_formula_charge.get()
        self.filter_option = self.selected_option.get()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()