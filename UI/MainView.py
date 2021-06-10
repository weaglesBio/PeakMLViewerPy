import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import ast

class MainView():

    def __init__(self, data):

        root = tk.Tk()

        root.title('PeakMLViewerPy')
        root.resizable(None, None)

        self.data = data
        self.menubar = tk.Menu(root)

        #Add 'File' category
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(label="Save as...", command=self.file_save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="Menu", menu=self.filemenu)

        #Main content container
        self.viewer_frame = tk.Frame(root)
        self.viewer_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        # Allow the second column and row to be resizable second column resizable
        self.viewer_frame.columnconfigure(1, weight = 1)
        self.viewer_frame.rowconfigure(1, weight = 1)

        #Split into three sections vertically, with the middle split into three horizontally.

        self.top_frame = tk.Frame(self.viewer_frame, width=1100, height=100, padx=5, pady=5)
        self.top_frame.grid(row=0, column=0, columnspan = 3, sticky = "NEWS")

        self.middle_left_frame = tk.LabelFrame(self.viewer_frame, width=250, height=750, padx=10, pady=10, text="Entries")
        self.middle_left_frame.grid(row=1, column=0, columnspan = 1, sticky="NEWS")

        self.middle_centre_frame = tk.LabelFrame(self.viewer_frame, width=750, height=750, padx=5, pady=5, text="Summary Plots")
        self.middle_centre_frame.grid(row=1, column=1, columnspan = 1, sticky="NEWS")

        self.middle_right_frame = tk.LabelFrame(self.viewer_frame, width=100, height=750, padx=10, pady=10, text="Sets")
        self.middle_right_frame.grid(row=1, column=2, columnspan = 1, sticky="NEWS")

        self.bottom_frame = tk.LabelFrame(self.viewer_frame, width=1100, height=150, padx=10, pady=10, text="Annotations")
        self.bottom_frame.grid(row=2, column=0, columnspan = 3,sticky="NEWS")

        # Allow middle centre to be resizable.
        self.middle_centre_frame.columnconfigure(0, weight = 1)
        self.middle_centre_frame.rowconfigure(1, weight = 1)

        self.tabs_plot = ttk.Notebook(self.middle_centre_frame)
        self.tab_peak = ttk.Frame(self.tabs_plot)
        self.tab_derivatives = ttk.Frame(self.tabs_plot)
        self.tab_intensity_pattern = ttk.Frame(self.tabs_plot)

        self.tabs_plot.add(self.tab_peak, text = "peak")
        self.tabs_plot.add(self.tab_derivatives, text = "derivatives")
        self.tabs_plot.add(self.tab_intensity_pattern, text = "intensity pattern")
        self.tabs_plot.pack(expand = 1, fill = "both")

        self.tabs_int = ttk.Notebook(self.tab_intensity_pattern)
        self.tab_int_all = ttk.Frame(self.tabs_int)
        self.tab_int_log = ttk.Frame(self.tabs_int)

        self.tabs_int.add(self.tab_int_all, text = "All")
        self.tabs_int.add(self.tab_int_log, text = "Log")
        self.tabs_int.pack(expand = 1, fill = "both")


        # Info View
        self.filename_text = tk.StringVar()
        self.peak_number_text = tk.StringVar()

        self.filename_label = tk.Label(self.top_frame, textvariable = self.filename_text, justify=tk.LEFT)
        self.filename_label.grid(row=0, column=0)

        self.peak_number_label = tk.Label(self.top_frame, textvariable = self.peak_number_text, justify=tk.LEFT)
        self.peak_number_label.grid(row=1, column=0)

        self.filename_text.set("Filename:")
        self.peak_number_text.set("Nr peaks:")

        # Entry View
        self.selected_id = tk.StringVar()

        self.entry_tree = ttk.Treeview(self.middle_left_frame, height = 30)
        self.entry_tree["columns"]=["RT","Mass", "Intensity", "Nr_peaks"]
        self.entry_tree.column("#0", width=10, stretch = tk.YES)
        self.entry_tree.column("#1", width=100, stretch = tk.YES)
        self.entry_tree.column("#2", width=100, stretch = tk.YES)
        self.entry_tree.column("#3", width=100, stretch = tk.YES)
        self.entry_tree.column("#4", width=100, stretch = tk.YES)

        self.entry_tree.heading("#0", text="")
        self.entry_tree.heading("#1", text="Retention time")
        self.entry_tree.heading("#2", text="Mass")
        self.entry_tree.heading("#3", text="Intensity")
        self.entry_tree.heading("#4", text="Sample Count")

        self.entry_tree.bind('<ButtonRelease-1>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Up>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Down>', self.select_entry)

        self.entry_tree.grid(row=0, column=0, sticky="NEWS")

        ## Graph View

        # Peak plot
        self.figure_peak = plt.Figure(figsize=(7,7))#figsize=(6,5),dpi=100
        self.axes_peak = self.figure_peak.add_subplot(111)
        canvas_peak = FigureCanvasTkAgg(self.figure_peak, self.tab_peak)
        toolbar_frame_peak = tk.Frame(self.tab_peak)
        toolbar_frame_peak.pack(side="top",fill ='x',expand=True)
        toolbar_peak = NavigationToolbar2Tk(canvas_peak,toolbar_frame_peak)
        canvas_peak.get_tk_widget().pack(side="top",fill ='both',expand=True)
        canvas_peak.draw()

        # Derivatives plot
        self.figure_derivatives = plt.Figure(figsize=(7,7))#figsize=(6,5),dpi=100
        self.axes_derivatives = self.figure_derivatives.add_subplot(111)
        canvas_derivatives = FigureCanvasTkAgg(self.figure_derivatives, self.tab_derivatives)
        toolbar_frame_derivatives = tk.Frame(self.tab_derivatives)
        toolbar_frame_derivatives.pack(side="top",fill ='x',expand=True)
        toolbar_derivatives = NavigationToolbar2Tk(canvas_derivatives,toolbar_frame_derivatives)
        canvas_derivatives.get_tk_widget().pack(side="top",fill ='both',expand=True)
        canvas_derivatives.draw()

        # Intensity pattern all plot
        self.figure_int_all = plt.Figure(figsize=(7,7))#figsize=(6,5),dpi=100
        self.axes_int_all = self.figure_int_all.add_subplot(111)
        canvas_int_all = FigureCanvasTkAgg(self.figure_int_all, self.tab_int_all)
        toolbar_frame_int_all = tk.Frame(self.tab_int_all)
        toolbar_frame_int_all.pack(side="top",fill ='x',expand=True)
        toolbar = NavigationToolbar2Tk(canvas_int_all,toolbar_frame_int_all)
        canvas_int_all.get_tk_widget().pack(side="top",fill ='both',expand=True)
        canvas_int_all.draw()

        # Intensity pattern log plot
        self.figure_int_log = plt.Figure(figsize=(7,7))#figsize=(6,5),dpi=100
        self.axes_int_log = self.figure_int_log.add_subplot(111)
        canvas_int_log = FigureCanvasTkAgg(self.figure_int_log, self.tab_int_log)
        toolbar_frame_int_log = tk.Frame(self.tab_int_log)
        toolbar_frame_int_log.pack(side="top",fill ='x',expand=True)
        toolbar_int_log = NavigationToolbar2Tk(canvas_int_log,toolbar_frame_int_log)
        canvas_int_log.get_tk_widget().pack(side="top",fill ='both',expand=True)
        canvas_int_log.draw()

        # Sets View
        self.sets_tree = ttk.Treeview(self.middle_right_frame)

        self.sets_tree["columns"]=["Name","Colour"]
        self.sets_tree.column("#0", width = 10, stretch = tk.YES)
        self.sets_tree.column("#1", width = 100, stretch = tk.YES)
        self.sets_tree.column("#2", width = 100, stretch = tk.YES)

        self.sets_tree.heading("#0", text="",)
        self.sets_tree.heading("#1", text="Name")
        self.sets_tree.heading("#2", text="Colour")

        self.sets_tree.grid(row=0, column=0, sticky="NEWS")

    #    self.details_tree = ttk.Treeview(parent_frame)

    #    self.details_tree["columns"]=["Name","Colour"]
    #    self.details_tree.column("#0", width = 10, stretch = tk.YES)
    #    self.details_tree.column("#1", width = 100, stretch = tk.YES)
    #    self.details_tree.column("#2", width = 100, stretch = tk.YES)

    #    self.details_tree.heading("#0", text="",)
    #    self.details_tree.heading("#1", text="Label")
    #    self.details_tree.heading("#2", text="Value")

    #    self.details_tree.grid(row=1, column=0, sticky="NEWS")

        # Annotation View
        self.annotation_tree = ttk.Treeview(self.bottom_frame)
        self.annotation_tree["columns"]=["ID", "Formula", "PPM", "Adduct", "Name", "Class", "Description"]
        self.annotation_tree.column("#0", width=10, minwidth=10, stretch = tk.NO)
        self.annotation_tree.column("#1", stretch = tk.YES)
        self.annotation_tree.column("#2", stretch = tk.YES)
        self.annotation_tree.column("#3", stretch = tk.YES)
        self.annotation_tree.column("#4",  stretch = tk.YES)
        self.annotation_tree.column("#5")
        self.annotation_tree.column("#6", stretch = tk.YES)
        self.annotation_tree.column("#7", stretch = tk.YES)

        self.annotation_tree.heading("#0", text="")
        self.annotation_tree.heading("#1", text="ID")
        self.annotation_tree.heading("#2", text="Formula")
        self.annotation_tree.heading("#3", text="PPM")
        self.annotation_tree.heading("#4", text="Adduct")
        self.annotation_tree.heading("#5", text="Name")
        self.annotation_tree.heading("#6", text="Class")
        self.annotation_tree.heading("#7", text="Description")

        self.annotation_tree.grid(row=0, column=0, columnspan = 3, sticky="NES")

        self.data.load_molecule_databases()
        #print(self.data.get_molecule_database())

        root.config(menu=self.menubar)
        # Run GUI until event occurs.
        root.mainloop()
 
        ## DEBUGGING LOGIC - PRESETTING THE FILENAME
        #self.data.import_from_filepath("C:\\Users\\willi\\OneDrive\\University\\RP2\\peakML\\Example_file.peakml")

    def import_file(self):
        try:
            filepath = self.get_filepath()

            if filepath:
                self.data.import_from_filepath(filepath)

                self.refresh_entry_view()
                #self.refresh_on_data_change()
        except Exception as err:
            print (err)

    def refresh_on_data_change(self):
        self.refresh_info_view()
        self.refresh_entry_view()
        self.refresh_graph_view()
        self.refresh_sets_view()
        self.refresh_identification_view()

    def refresh_on_selected_value_change(self):
        print("Not implemented")

    # Menu Methods

    def file_open(self):
        try:
            filepath = fd.askopenfilename()
            self.set_filepath(filepath)    
            self.import_file()
        except IOError:
            print("An error occurred")

    def file_save(self):
        print("Not Implemented")

    def file_save_as(self):
        print("Not Implemented")

    def get_filepath(self):
        return self.filepath

    def set_filepath(self,filepath):
        self.filepath = filepath

    def close_application(self):
        print("Not Implemented")

    # Info View Methods

    def refresh_info_view(self):
        self.filename_text.set("Filename: " + self.data.get_filename())
        self.peak_number_text.set("Nr peaks: " + self.data.get_nr_peaks()) 

    # Entry View Methods

    def refresh_entry_view(self):
        df_entry = self.data.get_entry_list()

        for i in range(len(df_entry)):
            selected_val = ""
            rt_val = df_entry.iloc[i]["RT"]
            mass_val = df_entry.iloc[i]["Mass"]
            inten_val = df_entry.iloc[i]["Intensity"]
            sc_val = df_entry.iloc[i]["Nrpeaks"]
            sha1sum_val = df_entry.iloc[i]["Sha1sum"]

            self.entry_tree.insert("",i,i, values=(rt_val,mass_val,inten_val,sc_val), tags=sha1sum_val)

    def select_entry(self, event):
        focused_row = self.entry_tree.focus()
        focused_entry = self.entry_tree.item(focused_row)
        focused_id = focused_entry["tags"][0]
        print(focused_id)
        self.selected_id.set(focused_id)
        self.data.set_selected_peak(focused_id)
        self.refresh_graph_view()
        self.refresh_identification_view()

    def refresh_identification_view(self):
        
        self.annotation_tree.delete(*self.annotation_tree.get_children())

        df_identifications = self.data.get_identification()

        for i in range(len(df_identifications)):
            id_val = df_identifications.iloc[i]["ID"]
            formula_val = df_identifications.iloc[i]["Formula"]
            ppm_val = df_identifications.iloc[i]["PPM"]
            adduct_val = df_identifications.iloc[i]["Adduct"]
            name_val = df_identifications.iloc[i]["Name"]
            class_val = df_identifications.iloc[i]["Class"]
            desc_val = df_identifications.iloc[i]["Description"]

            self.annotation_tree.insert("",i,i, values=(id_val,formula_val,ppm_val,adduct_val,name_val,class_val,desc_val))

    # Graph View Methods

    def refresh_graph_view(self):
        self.generate_plot_peak()
        self.generate_plot_derivatives()
        self.generate_plot_int_all()
        self.generate_plot_int_log()

    def generate_plot_peak(self):

        df = self.data.get_peak_plot()
        
        plot_count = len(df)

        plots = {}
        self.axes_peak.clear()
        for i in range(plot_count):

            RT_values_arr = df.iloc[i]['RT_values']
            Intensity_values_arr = df.iloc[i]['Intensity_values']
            plot_label = df.iloc[i]["Label"]

            #plots[row["Label"]] = pd.Dataframe({"RT_values": row["RT_values"], "Intensity_values": row["Intensity_values"]})
            #plot_data = pd.DataFrame({"RT_values": RT_values_arr, "Intensity_values": Intensity_values_arr})
            self.axes_peak.plot(RT_values_arr, Intensity_values_arr, marker='', color=self.set_plot_colour(plot_label), linewidth=0.5, label=plot_label)
            #self.gcf().autofmt_xdate()

        #self.axes_peak.tick_params(axis='x', labelrotation=90)
        self.axes_peak.set_xlabel("Retention Time")
        self.axes_peak.set_ylabel("Intensity")

        date_format = DateFormatter("%M:%S")
        self.axes_peak.xaxis.set_major_formatter(date_format)

        #If used needs to take into account range 
        #self.axes_peak.xaxis.set_major_locator(mdates.SecondLocator(interval=2))

        self.figure_peak.canvas.draw()

    def generate_plot_derivatives(self):
        df = self.data.get_derivatives_plot()
        self.axes_derivatives.clear()

        mass_values = df['Mass']
        intensity_values = df['Intensity']
        label_values = df['Description']

        self.axes_derivatives.stem(mass_values, intensity_values, markerfmt=None)

        for i in range(len(df)):
            self.axes_derivatives.annotate(label_values[i],(mass_values[i],intensity_values[i]))

        self.axes_derivatives.set_xlabel("Mass")
        self.axes_derivatives.set_ylabel("Intensity")
        self.figure_derivatives.canvas.draw()

    def generate_plot_int_all(self):
        print("Not Implemented")

    def generate_plot_int_log(self):
        print("Not Implemented")
 
    def set_plot_colour(self, label):
        if label == "A_01" or label == "B_01" or label == "C_01":
            return 'blue'
        elif label == "A_02" or label == "B_02" or label == "C_02":
            return 'green'
        elif label == "A_03" or label == "B_03" or label == "C_03":
            return 'red'

    # Sets View Methods

    def refresh_sets_view(self):
        df_sets = None

        for i in range(len(df_sets)):
            name_val = df_sets.iloc[i]["Name"]
            column_val = df_sets.iloc[i]["Colour"]

            self.sets_tree.insert("",i,i, values=(name_val,column_val))

    # Sets Annotations Methods
    
    def refresh_annotations_view(self):
        df_annotation = None

        for i in range(len(df_annotation)):
            id_val = df_annotation.iloc[i]["ID"]
            formula_val = df_annotation.iloc[i]["Formula"]
            ppm_val = df_annotation.iloc[i]["PPM"]
            adduct_val = df_annotation.iloc[i]["Adduct"]
            name_val = df_annotation.iloc[i]["Name"]
            class_val = df_annotation.iloc[i]["Class"]
            desc_val = df_annotation.iloc[i]["Description"]

            self.annotation_tree.insert("",i,i, values=(id_val,formula_val,ppm_val,adduct_val,name_val,class_val,desc_val))


        





