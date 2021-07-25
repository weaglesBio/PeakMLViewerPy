import tkinter as tk
import Logger as lg
from UI.ViewerDialog import ViewerDialog
class LogDialog(ViewerDialog):
    def __init__(self, parent):
        self.submit = False
        super().__init__(parent, "View Log", width=200, height=200)
    
    def body(self, frame):
        self.log_text = tk.Text(frame)

        # Get contents of current log file.
        log_contents = lg.get_log()

        self.log_text.insert('end', log_contents)
        self.log_text.configure(state='disabled')

        self.log_text.pack(fill=tk.BOTH, expand = tk.TRUE)
        #self.log_text.grid(row=0, column=0, sticky="NEWS")

        self.resizable(width = True, height = True)

    def buttonbox(self):
        self.btn_close = tk.Button(self, text='Close', width=5, command=self.close_btn_clicked)
        self.btn_close.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.close_btn_clicked())
        self.bind("<Escape>", lambda event: self.close_btn_clicked())

    def close_btn_clicked(self):
        self.destroy()