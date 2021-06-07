from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
#from pandastablepip

class MainViewer():
    
    def file_open(self):
        print("Not Implemented")

    def file_save(self):
        print("Not Implemented")

    def file_save_as(self):
        print("Not Implemented")
        
    def close_application(self):
        print("Not Implemented")

    def label_filename_update(self, filename):
        self.lblFileName.text = "Filename: " + filename 

    def set_plot_colour(self,label):

        if label == "A_01" or label == "B_01" or label == "C_01":
            return 'blue'
        elif label == "A_02" or label == "B_02" or label == "C_02":
            return 'green'
        elif label == "A_03" or label == "B_03" or label == "C_03":
            return 'red'

    def __init__(self, root, data_obj):
        root.title('PeakMLViewerPy')

        self.data_obj = data_obj

        self.menubar = Menu(root)
        self.viewer_container = Frame(root, highlightbackground="black", highlightthickness = 1)
        self.viewer_container.pack()

        self.top_container = Frame(self.viewer_container, background="blue", borderwidth = 5, height = 100, width = 200)
        self.top_container.pack(side = TOP)

        self.middle_container = Frame(self.viewer_container)
        self.middle_container.pack(side = TOP)

        self.middle_left_container = Frame(self.middle_container, background="green", borderwidth = 5, height = 100, width = 100)
        self.middle_left_container.pack(side = LEFT, fill = BOTH, expand = YES)

        self.middle_right_container = Frame(self.middle_container, background="yellow", borderwidth = 5, height = 100, width = 100)
        self.middle_right_container.pack(side = RIGHT, fill = BOTH, expand = YES)

        self.bottom_container = Frame(self.viewer_container, background="red", borderwidth = 5, height = 100, width = 200)
        self.bottom_container.pack(side = TOP)

        self.info_container = Frame(self.top_container, highlightbackground="black", highlightthickness = 1)
        self.info_container.pack()

        self.entry_container = Frame(self.middle_left_container, highlightbackground="black", highlightthickness = 1)
        self.entry_container.pack()

        self.graph_container = Frame(self.middle_container, highlightbackground="black", highlightthickness = 1)
        self.graph_container.pack()

        self.annotation_container = Frame(self.bottom_container, highlightbackground="black", highlightthickness = 1)
        self.annotation_container.pack()
        
        #Add 'File' category
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(label="Save as...", command=self.file_save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="Menu", menu=self.filemenu)

        # add widgets (controls)
        self.lblFileName = Label(self.info_container, text = "Filename:")
        self.lblPeakNumber = Label(self.info_container, text = "Nr peaks:")

        #self.phEntry = Label(self.entry_container, text = "Placeholder for Entry View")
        #self.phGraph = Label(self.graph_container, text = "Placeholder for Graph View")
        #self.phAnnotation = Label(self.annotation_container, text = "Placeholder for Annotation View")

        # .pack method adds widget to window
        #self.lblFileName.pack()
        #self.lblPeakNumber.pack()

        #self.phEntry.pack()
        #self.phGraph.pack()
        #self.phAnnotation.pack()

        data_obj.get_entry_list()






        f = plt.Figure(figsize=(6,5),dpi=100)
        a = f.add_subplot(111)
        df = data_obj.get_peak_graph_data_by_scanid("NhQMcJnK5Riv89yGGPg9zgN87bk=")

        plot_count = len(df)

        plots = {}
        plot_count = 1
        for i in range(plot_count):

            df.iloc[i]['RT_values']
            RT_values_arr = df.iloc[i]['RT_values']
            Intensity_values_arr = df.iloc[i]['Intensity_values']
            plot_label = df.iloc[i]["Label"]


            #plots[row["Label"]] = pd.Dataframe({"RT_values": row["RT_values"], "Intensity_values": row["Intensity_values"]})
            plot_data = pd.DataFrame({"RT_values": RT_values_arr, "Intensity_values": Intensity_values_arr})
            a.plot("RT_values", "Intensity_values", data=plot_data, marker='', color=self.set_plot_colour(plot_label), linewidth=0.5, label=plot_label)

        a.tick_params(axis='x', labelrotation=90)
        a.set_xlabel("Retention Time")
        a.set_ylabel("Intensity")


        canvas = FigureCanvasTkAgg(f, self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)

        toolbar = NavigationToolbar2Tk(canvas,self.graph_container)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)


        # Run GUI until event occurs.
        root.config(menu=self.menubar)




