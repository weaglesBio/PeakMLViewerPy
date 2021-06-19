import tkinter as tk
import tkinter.ttk as ttk
import threading
#https://gist.github.com/MattWoodhead/c7c51cd2beaea33e1b8f5057f7a7d78a
class ProgressBar():
    def __init__(self, parent, row, column):
        self.maximum = 100
        self.interval = 10

        self.progress_bar = ttk.Progressbar(parent, orient=tk.HORIZONTAL, mode='indeterminate', maximum=self.maximum)
        self.progress_bar.grid(row=row, column=column, sticky="we")

        self.thread = threading.Thread()
        self.thread.__init__(target=self.progress_bar.start(self.interval), args=())
        self.thread.start()

    def progress_stop(self):
        if not self.thread.is_alive():
            val = self.progress_bar["value"]
            self.progress_bar.stop()
            self.progress_bar["value"] = val

    def progress_start(self):
        if not self.thread.is_alive():
            val = self.progress_bar["value"]
            self.progress_bar.configure(mode="indeterminate", maximum=self.maximum, value=val)
            self.progress_bar.start(self.interval)

    def progress_clear(self):
        if not self.thread.is_alive():
            self.progress_bar.stop()
            self.progress_bar.configure(mode = "determinate", value=0)

    def progress_complete(self):
        if not self.thread.is_alive():
            self.progress_bar.stop()
            self.progress_bar.configure(mode = "determinate", maximum=self.maximum, value=self.maximum)


    #def start(self):
    #    self.progress.start()

   # def close(self):
    #    self.destroy()

    #def close(self, event = None):
        #if self.progress['value'] == self.maximum:
        #    print('Process Completed')
        #else:
        #    print('Process Cancelled')
    #    self.master.focus_set()
    #    self.destroy()

        