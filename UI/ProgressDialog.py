import tkinter as tk
import tkinter.ttk as ttk

from UI.ViewerDialog import ViewerDialog

class ProgressDialog(ViewerDialog):
    def __init__(self, parent, progress_text, progress_val):
        self.parent = parent
        self.progress_text = progress_text
        self.progress_val = progress_val
        self.progress_text.trace("w", self.check_if_complete)

        super().__init__(parent=self.parent, title="Progress", width=400, height=100, take_focus=False)

    def body(self, parent):
        progress_frame = tk.Frame(parent, padx=10, pady=10)
        progress_frame.grid(row=0, column=1, columnspan=2, padx=(10,0))

        progress_lbl = tk.Label(progress_frame, textvariable = self.progress_text)
        progress_lbl.grid(row=0, column=0)

        # self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, mode='indeterminate', takefocus=True, length=300)
        # self.progress_bar.grid(row=1, column=0)

        self.progress_bar_track = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, mode='determinate', variable=self.progress_val, takefocus=True, length=300)
        self.progress_bar_track.grid(row=1, column=0)

        #progress_lbl = tk.Label(progress_frame, textvariable = self.progress_text)
        #progress_lbl.grid(row=0, column=0)

    def buttonbox(self):
        pass

    def ok_btn_clicked(self):
        pass

    def cancel_btn_clicked(self):
        pass

    def check_if_complete(self, *args):
        if self.progress_text.get() == "Completed":
            self.progress_stop()

    #def progress_start(self):
        #self.progress_bar.start()
    
    def progress_stop(self):
        #self.progress_bar.stop()
        #self.progress_bar.destroy()
        self.destroy()