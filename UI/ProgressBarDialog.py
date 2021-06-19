import tkinter as tk
import tkinter.ttk as ttk

class ProgressBarDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title)

    def body(self, frame):
        #self.focus_set()
        #self.grab_set()
        #self.transient(self.master)
        #self.resizable(False, False)
        #self.bind('<Escape>', self.close)

        self.progress = ttk.Progressbar(frame, maximum=100, orient='horizontal', mode='indeterminate')
        self.progress.pack(padx=10, pady=10)

        self.progress.start()

    def progress_stop(self):
        if not self.thread.isAlive():
            val = self.progressbar["value"]
            self.progressbar.stop()
            self.progressbar["value"] = val

    def progress_start(self):
        if not self.thread.isAlive():
            val = self.progressbar["value"]
            self.progressbar.configure(mode="intermediate", maximum=self.maximum, value=val)
            self.progressbar.start(self.interval)

    def progress_clear(self):
        if not self.thread.isAlive():
            self.progressbar.stop()
            self.progressbar.configure(mode = "deteminate", value=0)

    def progress_complete(self):
        if not self.thread.isAlive():
            self.progressbar.stop()
            self.progressbar.configure(mode = "deteminate", maximum=self.maximum, value=self.maximum)


    #def start(self):
    #    self.progress.start()

    def close(self):
        self.destroy()

    #def close(self, event = None):
        #if self.progress['value'] == self.maximum:
        #    print('Process Completed')
        #else:
        #    print('Process Cancelled')
    #    self.master.focus_set()
    #    self.destroy()

        