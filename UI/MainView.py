import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import ttkwidgets as ttkw

import matplotlib.pyplot as plt
import tkinter.simpledialog as sd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import statistics as stats
from PIL import ImageTk, Image

from UI.FilterMassDialog import FilterMassDialog
from UI.FilterIntensityDialog import FilterIntensityDialog
from UI.FilterRetentionTimeDialog import FilterRetentionTimeDialog
from UI.FilterNumberDetectionsDialog import FilterNumberDetectionsDialog
from UI.FilterAnnotationsDialog import FilterAnnotationsDialog
from UI.SortDialog import SortDialog
from UI.SortTimeSeriesDialog import SortTimeSeriesDialog

import Utilities as Utils

class MainView():

    def __init__(self, data):

        self.root = tk.Tk()

        self.root.title('PeakMLViewerPy')
        self.root.resizable(None, None)

        self.style = ttk.Style()
        self.style.map('Treeview', foreground = self.fixed_map('foreground'), background = self.fixed_map('background'))
        self.style.map('Treeview', background=[('selected', 'blue')])

        self.data = data
        self.menubar = tk.Menu(self.root)

        #self.img_checked = ImageTk.PhotoImage(Image.open("checked.png"))
        #self.img_unchecked = ImageTk.PhotoImage(Image.open("checked.png"))

        #Add 'File' category
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(label="Save as...", command=self.file_save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="Menu", menu=self.filemenu)

        #Main content container
        self.viewer_frame = tk.Frame(self.root)
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

        self.filename_label = tk.Label(self.top_frame, textvariable = self.filename_text, anchor="w")
        self.filename_label.grid(row=0, column=0)

        self.peak_number_label = tk.Label(self.top_frame, textvariable = self.peak_number_text, anchor="w")
        self.peak_number_label.grid(row=1, column=0)

        self.filename_text.set("Filename:")
        self.peak_number_text.set("Nr peaks:")

        # Entry View
        self.selected_id = tk.StringVar()

        self.entry_tree = ttkw.CheckboxTreeview(self.middle_left_frame, height = 25, show=("headings","tree"), selectmode="browse")
        self.entry_tree["columns"]=["RT","Mass", "Intensity", "Nr_peaks"]
        self.entry_tree.column("#0", width=40, stretch = tk.YES)
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

        self.entry_tree.tag_configure("has_ann", foreground="black")
        self.entry_tree.tag_configure("no_ann", foreground="grey")
        self.entry_tree.tag_configure("is_focus", background="lightblue")
        #self.entry_tree.tag_configure("checked", image=self.img_checked)
        #self.entry_tree.tag_configure("unchecked", image=self.img_unchecked)

        self.entry_tree.grid(row=0, column=0, sticky="NEWS")

        self.filter_tree = ttk.Treeview(self.middle_left_frame, height = 6)

        self.filter_tree["columns"]=["Type","Settings"]
        self.filter_tree.column("#0", width = 10, stretch = tk.YES)
        self.filter_tree.column("#1", width = 100, stretch = tk.YES)
        self.filter_tree.column("#2", width = 100, stretch = tk.YES)

        self.filter_tree.heading("#0", text="",)
        self.filter_tree.heading("#1", text="Type")
        self.filter_tree.heading("#2", text="Settings")

        self.filter_tree.grid(row=1, column=0, sticky="NEWS")

        option_list = ["Filter Mass", "Filter Intensity", "Filter Retention Time", "Filter Number Detections", "Filter Annotations", "Sort", "Sort time-series"]

        self.filter_frame = ttk.Frame(self.middle_left_frame)

        self.filter_option_selected = tk.StringVar(self.root)
        self.filter_option_selected.set("Select Filter...")

        self.filter_option = tk.OptionMenu(self.filter_frame, self.filter_option_selected, *option_list)
        self.filter_add = tk.Button(self.filter_frame, text="Add", command=self.add_filter)
        self.filter_remove = tk.Button(self.filter_frame, text="Remove", command=self.remove_filter)

        self.filter_option.grid(row=0, column=0)
        self.filter_add.grid(row=0, column=1)
        self.filter_remove.grid(row=0, column=2)
        self.filter_frame.grid(row=2, column=0, sticky="NEWS")

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
        self.sets_tree = ttkw.CheckboxTreeview(self.middle_right_frame, height = 25, show=("headings","tree"))

        self.sets_tree["columns"]=["Name"]
        self.sets_tree.column("#0", width = 10, stretch = tk.YES)
        self.sets_tree.column("#1", width = 50, stretch = tk.YES)

        self.sets_tree.heading("#0", text="",)
        self.sets_tree.heading("#1", text="Name")

        self.sets_tree.bind('<ButtonRelease-1>', self.update_sets_view)
        
        self.sets_tree.grid(row=0, column=0, sticky="NEWS")

        self.details_tree = ttk.Treeview(self.middle_right_frame)

        self.details_tree["columns"]=["Label","Value"]
        self.details_tree.column("#0", width = 10, stretch = tk.YES)
        self.details_tree.column("#1", width = 100, stretch = tk.YES)
        self.details_tree.column("#2", width = 100, stretch = tk.YES)

        self.details_tree.heading("#0", text="",)
        self.details_tree.heading("#1", text="Label")
        self.details_tree.heading("#2", text="Value")

        self.details_tree.grid(row=1, column=0, sticky="NEWS")

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

        self.root.config(menu=self.menubar)
        # Run GUI until event occurs.
        self.root.mainloop()
 
        ## DEBUGGING LOGIC - PRESETTING THE FILENAME
        #self.data.import_from_filepath("C:\\Users\\willi\\OneDrive\\University\\RP2\\peakML\\Example_file.peakml")

    # Fix to bug with tkinter
    def fixed_map(self, option):
        return [elm for elm in self.style.map("Treeview", query_opt=option) 
                if elm[:2] != ("!disabled","!selected")]

    def import_file(self):
        try:
            filepath = self.get_filepath()

            if filepath:
                self.data.import_from_filepath(filepath)

                self.refresh_views(True)
                #self.refresh_on_data_change()
        except Exception as err:
            print (err)

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
        self.peak_number_text.set("Nr peaks: " + self.data.get_nr_peaks() + " (" + str(self.data.get_total_nr_peaks()) + ")") 

    # Entry View Methods

    def refresh_entry_view(self, reload_entries):

        focused_row_id = self.selected_id.get()
        self.entry_tree.delete(*self.entry_tree.get_children())    

        if reload_entries:
            self.df_entry = self.data.get_entry_list()

        for i in range(len(self.df_entry)):

            entry_row = self.df_entry.iloc[i]

            if focused_row_id == entry_row["Sha1sum"]:
                focus = "is_focus"
            elif focused_row_id is None and i == 0:
                focus = "is_focus"
            else:
                focus = "not_focus"

            self.entry_tree.insert("",i,i, values=(entry_row["RT"], entry_row["Mass"], entry_row["Intensity"], int(entry_row["Nrpeaks"])), tags=(entry_row["Sha1sum"], "has_ann" if entry_row["HasAnnotation"] else "no_ann", focus)) 

    def select_entry(self, event):
        self.refresh_entry_selected(False)

    def refresh_entry_selected(self, reload_entries):

        if reload_entries:
            self.entry_tree.focus(self.entry_tree.get_children()[0])
        
        focused_entry = self.entry_tree.item(self.entry_tree.focus())
        focused_id = focused_entry["tags"][0]    
        self.selected_id.set(focused_id)
        self.data.set_selected_peak(focused_id)

        self.refresh_entry_view(False)
        Utils.trace("ref3")
        self.refresh_graph_view()
        Utils.trace("ref4")
        self.refresh_identification_view()
        Utils.trace("ref5")
        self.refresh_sets_view()
        Utils.trace("ref6")
        self.refresh_details_view()
        Utils.trace("ref7")
        self.refresh_filters_view()
        Utils.trace("ref8")

    def refresh_views(self, reload_entries):
        Utils.trace("ref0")
        self.refresh_info_view()
        Utils.trace("ref1")
        self.refresh_entry_view(reload_entries)
        Utils.trace("ref2")
        self.refresh_entry_selected(reload_entries)
        Utils.trace("ref3")
        self.refresh_graph_view()
        Utils.trace("ref4")
        self.refresh_identification_view()
        Utils.trace("ref5")
        self.refresh_sets_view()
        Utils.trace("ref6")
        self.refresh_details_view()
        Utils.trace("ref7")
        self.refresh_filters_view()
        Utils.trace("ref8")

    def update_sets_view(self, event):
        # Save check status of each list
        for item in self.sets_tree.get_children():
            for child_item in self.sets_tree.get_children(item):
                name = self.sets_tree.item(child_item)["values"][0]
                selected_status = True
                if self.sets_tree.item(child_item)["tags"][1] == "unchecked":
                    selected_status = False

                self.data.update_set_selection(name, selected_status)
        # Refresh grid
        self.refresh_graph_view()

    def refresh_identification_view(self):
        
        self.annotation_tree.delete(*self.annotation_tree.get_children())
        df_identifications = self.data.get_identification()

        if df_identifications is not None:
            for i in range(len(df_identifications)):
                identification_row = df_identifications.iloc[i]
                self.annotation_tree.insert("",i,i, values=(identification_row["ID"],identification_row["Formula"],identification_row["PPM"],identification_row["Adduct"],identification_row["Name"],identification_row["Class"],identification_row["Description"]))

    def refresh_sets_view(self):
        
        self.sets_tree.delete(*self.sets_tree.get_children())
        df_sets = self.data.get_sets()
        if df_sets is not None:
            df_sets_parent = df_sets.loc[df_sets['Parent'].isnull()]

            if df_sets_parent is not None:
                for i in range(len(df_sets_parent)):
                    set_parent_row = df_sets_parent.iloc[i]    
                    name_parent = set_parent_row["Name"]

                    select_parent = "checked" if set_parent_row["Selected"] else "unchecked"

                    colour_tag = "colour_" + name_parent
                    self.sets_tree.tag_configure(colour_tag, foreground=set_parent_row["Color"])
                    folder = self.sets_tree.insert("", i, name_parent, values=(name_parent), tags=(select_parent, colour_tag))
                    
                    df_sets_child = df_sets.loc[df_sets['Parent'] == name_parent]

                    if df_sets_child is not None:

                        for j in range(len(df_sets_child)):
                            set_child_row = df_sets_child.iloc[j]    
                            select_child = "checked" if set_child_row["Selected"] else "unchecked"

                            self.sets_tree.insert(folder, "end", set_child_row["Name"], values=(set_child_row["Name"]), tags=(select_child, colour_tag))

    def refresh_details_view(self):
        
        self.details_tree.delete(*self.details_tree.get_children())
        df_details = self.data.get_details()

        if df_details is not None:
            for i in range(len(df_details)):
                detail_row = df_details.iloc[i]
                self.details_tree.insert("", i, i, values=(detail_row["Label"], detail_row["Value"]))

    def refresh_filters_view(self):

        self.filter_tree.delete(*self.filter_tree.get_children())
        df_filters = self.data.get_filters_list()

        if df_filters is not None:
            for i in range(len(df_filters)):
                filter_row = df_filters.iloc[i]
                self.filter_tree.insert("", i, i, values=(filter_row["Type"], filter_row["Settings"]), tags=(filter_row["ID"]))

    # Graph View Methods

    def refresh_graph_view(self):
        self.generate_plot_peak()
        self.generate_plot_derivatives()
        self.generate_plots_int()

    def generate_plot_peak(self):

        df = self.data.get_peak_plot()
        
        plot_count = len(df)

        plots = {}
        self.axes_peak.clear()
        for i in range(plot_count):

            RT_values_arr = df.iloc[i]['RT_values']
            Intensity_values_arr = df.iloc[i]['Intensity_values']
            plot_label = df.iloc[i]["Label"]
            colour = df.iloc[i]["Colour"]
            selected = df.iloc[i]["Selected"]

            if selected:
                self.axes_peak.plot(RT_values_arr, Intensity_values_arr, marker='', color=colour, linewidth=0.5, label=plot_label)

        self.axes_peak.set_xlabel("Retention Time")
        self.axes_peak.set_ylabel("Intensity")

        date_format = DateFormatter("%M:%S")
        self.axes_peak.xaxis.set_major_formatter(date_format)    

        #If used needs to take into account range 
        #self.axes_peak.xaxis.set_major_locator(mdates.SecondLocator(interval=2))

        self.figure_peak.canvas.draw()
        self.figure_peak.tight_layout()

    def set_plot_colour(self, plot_label):
        colour = self.data.get_peak_colour_by_sampleid(plot_label)
        return colour

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
        self.figure_derivatives.tight_layout()

    def generate_plots_int(self):
        df = self.data.get_intensity_plot()
        self.generate_plot_int_all(df)
        self.generate_plot_int_log(df)

    def generate_plot_int_all(self, data):
        self.axes_int_all.clear()
        Set_ID_arr = []
        Intensities_arr = []
        for i in range(len(data)):

            SetID = data.iloc[i]['SetID']
            Intensities = data.iloc[i]['Intensities']
        
            for j in range(len(Intensities)):

                Set_ID_val = str(SetID) + "-" + str(j + 1)
                Set_ID_arr.append(Set_ID_val)
                Intensities_arr.append(float(Intensities[j]))

        self.axes_int_all.plot(Set_ID_arr, Intensities_arr, marker='', linewidth=0.5)

        self.axes_int_all.set_xlabel("Set")
        self.axes_int_all.set_ylabel("Intensity")
        self.figure_int_all.canvas.draw()
        self.figure_int_all.tight_layout()

    def generate_plot_int_log(self, data):
        self.axes_int_log.clear()
 
        Intensities_float = []
        Set_ID_arr = []
        Intensity_mean_arr = []
        Intensity_neg_arr = []
        Intensity_pos_arr = []
        for i in range(len(data)):

            SetID = data.iloc[i]['SetID']
            Intensities = data.iloc[i]['Intensities']

            for i in range(len(Intensities)):
                Intensities_float.append(float(Intensities[i]))

            Intensity_mean = stats.mean(Intensities_float)
            Intensity_max = max(Intensities_float)
            Intensity_min = min(Intensities_float)
            Intensity_pos = Intensity_max - Intensity_mean
            Intensity_neg = Intensity_mean - Intensity_min

            Set_ID_arr.append(SetID)
            Intensity_mean_arr.append(Intensity_mean)
            Intensity_neg_arr.append(Intensity_neg)
            Intensity_pos_arr.append(Intensity_pos)

        self.axes_int_log.errorbar(Set_ID_arr, Intensity_mean_arr, yerr=[Intensity_neg_arr,Intensity_pos_arr])

        self.axes_int_log.set_xlabel("Set")
        self.axes_int_log.set_ylabel("Intensity")
        self.figure_int_log.canvas.draw()
        self.figure_int_log.tight_layout()

    def add_filter(self):
        option = self.filter_option_selected.get()
        if option == "Filter Mass":
            self.filter_mass_dialog()
        elif option == "Filter Intensity":
            self.filter_intensity_dialog()
        elif option == "Filter Retention Time":
            self.filter_retention_time_dialog()
        elif option == "Filter Number Detections":
            self.filter_number_detections_dialog()
        elif option == "Filter Annotations":
            self.filter_annotations_dialog()
        elif option == "Sort":
            self.filter_sort_dialog()
        elif option == "Sort time-series":
            self.filter_sort_time_series_dialog()
        self.refresh_views(True)

    def remove_filter(self):
        focused_filter = self.filter_tree.item(self.filter_tree.focus())
        self.data.remove_filter_by_id(focused_filter["tags"][0])
        self.refresh_views(True)

    def filter_mass_dialog(self):
        dlg = FilterMassDialog(self.root,"Filter mass")
        self.data.add_filter_mass(dlg.mass_min, dlg.mass_max, dlg.formula, dlg.formula_ppm, dlg.mass_charge, dlg.filter_option)

    def filter_intensity_dialog(self):
        dlg = FilterIntensityDialog(self.root,"Filter intensity")
        self.data.add_filter_intensity(dlg.intensity_min, dlg.intensity_unit)

    def filter_retention_time_dialog(self):
        dlg = FilterRetentionTimeDialog(self.root,"Filter retention-time")
        self.data.add_filter_retention_time(dlg.range_min, dlg.range_max)

    def filter_number_detections_dialog(self):
        dlg = FilterNumberDetectionsDialog(self.root,"Filter number of detections")
        self.data.add_filter_number_detections(dlg.detection_number)

    def filter_annotations_dialog(self):
        dlg = FilterAnnotationsDialog(self.root,"Filter annotations")
        self.data.add_filter_annotations(dlg.annotation_name, dlg.annotation_relation, dlg.annotation_value)

    def filter_sort_dialog(self):
        dlg = SortDialog(self.root,"Sort")
        self.data.add_filter_sort()

    def filter_sort_time_series_dialog(self):
        dlg = SortTimeSeriesDialog(self.root,"Sort time series")
        self.data.add_filter_sort_times_series()