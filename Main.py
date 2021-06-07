
from tkinter import *
from  UI.Viewer import MainViewer
import Data.PeakMLData as Data

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():

    data_obj = Data.PeakMLData()

    #Before file selection logic
    data_obj.import_file_to_data_object("C:\\Users\\willi\\OneDrive\\University\\RP2\\peakML\\Example_file.peakml")

    #Creates main window
    root = Tk()
    MainViewer(root, data_obj)

    root.mainloop()

if __name__ == "__main__":
    main()
