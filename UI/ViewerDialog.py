import tkinter as tk

#https://github.com/python/cpython/blob/3.9/Lib/tkinter/simpledialog.py

class ViewerDialog(tk.Toplevel):
    def __init__(self, parent, title, width, height, take_focus: bool = True):
        self.parent = parent
        #self.title = title
        self.width = width
        self.height = height

        master = parent
        if not master:
            master = tk._get_default_root('create dialog window')

        super().__init__(self.parent, height=height, width=width)

        self.withdraw() # Keep dialog invisible.
        
        if self.parent is not None and self.parent.winfo_viewable(): # Make transient
            self.transient(self.parent)

        self.title(title)

        if self._windowingsystem == "aqua":
            self.tk.call("::tk::unsupported::MacWindowStyle", "style", self, "moveableModal", "")
        elif self._windowingsystem == "x11":
            self.wm_attributes("-type", "dialog")

        #self.parent = parent

        self.result = None
        
        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry(f'{width}x{height}+{self.parent.winfo_x()+int((self.parent.winfo_width()/2)-(width/2))}+{self.parent.winfo_y()+int((self.parent.winfo_height()/2)-(height/2))}')

        self.deiconify() # Set visible

        self.initial_focus.focus_set()


        if take_focus:
            self.wait_visibility()
            self.grab_set()
            self.wait_window()
        else:
            #self.wait_visibility()
            self.grab_set()
            #self.wait_window()

    def body(self, parent):
        pass

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok())
        self.bind("<Escape>", lambda event: self.cancel())
    
    def destroy(self):
        self.initial_focus = None
        tk.Toplevel.destroy(self)

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

        #self.destroy()

    def cancel(self, event=None):
        if self.parent is not None:
            self.parent.focus_set()

        #self.withdraw()
        self.destroy()

    def validate(self):
        return 1

    def apply(self):
        pass