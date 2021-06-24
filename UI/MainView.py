import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import ttkwidgets as ttkw
#If package only available as pip, install with anaconda prompt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.dates import DateFormatter
import pandas as pd
import statistics as stats
from PIL import ImageTk, Image
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import inchi

from UI.FilterMassDialog import FilterMassDialog
from UI.FilterIntensityDialog import FilterIntensityDialog
from UI.FilterRetentionTimeDialog import FilterRetentionTimeDialog
from UI.FilterNumberDetectionsDialog import FilterNumberDetectionsDialog
from UI.FilterAnnotationsDialog import FilterAnnotationsDialog
from UI.SortDialog import SortDialog
from UI.SortTimeSeriesDialog import SortTimeSeriesDialog
from UI.PreferencesDialog import PreferencesDialog

import Utilities as Utils

import threading

class MainView():

    def __init__(self, data):

        self.df_entry = pd.DataFrame(columns=['UID','Type','Selected','RT','Mass','Intensity','Nrpeaks','HasAnnotation','Checked'])

        self.root = tk.Tk()

        self.root.title('PeakMLViewerPy')
        self.root.resizable(None, None)

        self.style = ttk.Style()
        self.style.map('Treeview', foreground = self.fixed_map('foreground'), background = self.fixed_map('background'))
        self.style.map('Treeview', background=[('selected', 'blue')])

        self.data = data
        self.menubar = tk.Menu(self.root)

        #Add 'File' category
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(label="Save as...", command=self.file_save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Preferences", command=self.edit_preferences)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        #Main content container
        self.viewer_frame = tk.Frame(self.root)
        self.viewer_frame.pack(fill=tk.BOTH, expand = tk.TRUE, padx=(5,5), pady=(5,5))

        # Allow the second column and row to be resizable second column resizable
        self.viewer_frame.columnconfigure(1, weight = 1)
        self.viewer_frame.rowconfigure(1, weight = 1)

        #Split into three sections vertically, with the middle split into three horizontally.

        self.top_frame = tk.Frame(self.viewer_frame, width=1100, height=100, padx=5, pady=5)
        self.top_frame.grid(row=0, column=0, columnspan = 3, sticky = "NEWS")

        self.middle_left_frame = tk.Frame(self.viewer_frame, width=250, height=750, padx=10, pady=0)
        self.middle_left_frame.grid(row=1, column=0, columnspan = 1, sticky="NEWS")

        self.middle_centre_frame = tk.LabelFrame(self.viewer_frame, width=750, height=750, padx=5, pady=5, text="Summary Plots")
        self.middle_centre_frame.grid(row=1, column=1, columnspan = 1, sticky="NEWS")

        self.middle_right_frame = tk.Frame(self.viewer_frame, width=100, height=750, padx=10, pady=0)
        self.middle_right_frame.grid(row=1, column=2, columnspan = 1, sticky="NEWS")

        self.bottom_frame = tk.Frame(self.viewer_frame, width=1100, height=100, padx=10, pady=10)
        self.bottom_frame.grid(row=2, column=0, columnspan = 3, sticky="NEWS")
        
        # Allow middle centre to be resizable.
        self.middle_centre_frame.columnconfigure(0, weight = 1)
        self.middle_centre_frame.rowconfigure(1, weight = 1)

        self.tabs_plot = ttk.Notebook(self.middle_centre_frame)
        self.tab_peak = ttk.Frame(self.tabs_plot)
        self.tab_derivatives = ttk.Frame(self.tabs_plot)
        self.tab_intensity_pattern = ttk.Frame(self.tabs_plot)

        self.tabs_plot.add(self.tab_peak, text = "Peak")
        self.tabs_plot.add(self.tab_derivatives, text = "Derivatives")
        self.tabs_plot.add(self.tab_intensity_pattern, text = "Intensity Pattern")
        self.tabs_plot.pack(expand = 1, fill = "both")

        self.tabs_der = ttk.Notebook(self.tab_derivatives)
        self.tab_der_all = ttk.Frame(self.tabs_der)
        self.tab_der_log = ttk.Frame(self.tabs_der)

        self.tabs_der.add(self.tab_der_all, text = "All")
        self.tabs_der.add(self.tab_der_log, text = "Log")
        self.tabs_der.pack(expand = 1, fill = "both")

        self.tabs_int = ttk.Notebook(self.tab_intensity_pattern)
        self.tab_int_all = ttk.Frame(self.tabs_int)
        self.tab_int_log = ttk.Frame(self.tabs_int)

        self.tabs_int.add(self.tab_int_all, text = "All")
        self.tabs_int.add(self.tab_int_log, text = "Log")
        self.tabs_int.pack(expand = 1, fill = "both")

        # Info View
        self.info_frame = tk.LabelFrame(self.top_frame, padx=10, pady=10, text="Info")

        self.filename_text = tk.StringVar()
        self.peak_number_text = tk.StringVar()

        self.filename_label = tk.Label(self.info_frame, text = "Filename:")
        self.filename_label.grid(row=0, column=0)

        self.peak_number_label = tk.Label(self.info_frame, text = "Nr peaks:")
        self.peak_number_label.grid(row=1, column=0)

        self.filename_val_label = tk.Label(self.info_frame, textvariable = self.filename_text)
        self.filename_val_label.grid(row=0, column=1)

        self.peak_number_val_label = tk.Label(self.info_frame, textvariable = self.peak_number_text)
        self.peak_number_val_label.grid(row=1, column=1)
        
        self.info_frame.grid(row=0, column=0, columnspan = 1)
        
        self.progress_frame = tk.LabelFrame(self.top_frame, padx=10, pady=10, text="Progress")
        self.progress_details_text = tk.StringVar()
        self.progress_details_label = tk.Label(self.progress_frame, textvariable = self.progress_details_text)
        self.progress_details_label.grid(row=0, column=0)
        self.progress_frame.grid(row=0, column=1, columnspan = 1, padx=(10,0))

        self.progress_details_text.set("No file imported.")
        
        # Entry View
        self.selected_id = tk.StringVar()

        self.entry_grid_frame = tk.LabelFrame(self.middle_left_frame, padx=10, pady=10, text="Entries")

        self.entry_tree = ttkw.CheckboxTreeview(self.entry_grid_frame, height = 20, show=("headings","tree"), selectmode="browse")
        self.entry_tree["columns"]=["RT","Mass", "Intensity", "Nr_peaks"]
        self.entry_tree.column("#0", width=40, stretch = tk.YES)
        self.entry_tree.column("#1", width=100, stretch = tk.YES)
        self.entry_tree.column("#2", width=80, stretch = tk.YES)
        self.entry_tree.column("#3", width=80, stretch = tk.YES)
        self.entry_tree.column("#4", width=50, stretch = tk.YES)
        self.entry_tree.heading("#0", text="")
        self.entry_tree.heading("#1", text="Retention time")
        self.entry_tree.heading("#2", text="Mass")
        self.entry_tree.heading("#3", text="Intensity")
        self.entry_tree.heading("#4", text="Samples")
        self.entry_tree.bind('<ButtonRelease-1>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Up>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Down>', self.select_entry)
        self.entry_tree.tag_configure("has_ann_not_focus", foreground="black")
        self.entry_tree.tag_configure("no_ann_not_focus", foreground="grey")
        self.entry_tree.tag_configure("has_ann_is_focus", foreground="white", background="blue")
        self.entry_tree.tag_configure("no_ann_is_focus", foreground="white", background="blue")

        self.entry_tree.grid(row=0, column=0, sticky="NEWS")

        self.entry_tree_vsb = ttk.Scrollbar(self.entry_grid_frame, orient="vertical", command=self.entry_tree.yview)
        self.entry_tree_vsb.grid(row=0, column=1, sticky="NEWS")
        self.entry_tree_hsb = ttk.Scrollbar(self.entry_grid_frame, orient="horizontal", command=self.entry_tree.xview)
        self.entry_tree_hsb.grid(row=1, column=0, sticky="NEWS")
        self.entry_tree.configure(yscrollcommand=self.entry_tree_vsb.set, xscrollcommand=self.entry_tree_hsb.set)

        self.entry_grid_frame.grid(row=0, column=0, sticky="NEWS")

        self.filter_frame = tk.LabelFrame(self.middle_left_frame, padx=10, pady=10, text="Filters")

        self.filter_grid_frame = tk.Frame(self.filter_frame)

        self.filter_tree = ttk.Treeview(self.filter_grid_frame, height = 5)
        self.filter_tree["columns"]=["Type","Settings"]
        self.filter_tree.column("#0", width = 10, stretch = tk.YES)
        self.filter_tree.column("#1", width = 100, stretch = tk.YES)
        self.filter_tree.column("#2", width = 100, stretch = tk.YES)
        self.filter_tree.heading("#0", text="",)
        self.filter_tree.heading("#1", text="Type")
        self.filter_tree.heading("#2", text="Settings")
        self.filter_tree.grid(row=0, column=0)

        self.filter_tree_vsb = ttk.Scrollbar(self.filter_grid_frame, orient="vertical", command=self.filter_tree.yview)
        self.filter_tree_vsb.grid(row=0, column=1, sticky="NEWS")
        self.filter_tree_hsb = ttk.Scrollbar(self.filter_grid_frame, orient="horizontal", command=self.filter_tree.xview)
        self.filter_tree_hsb.grid(row=1, column=0, sticky="NEWS")
        self.filter_tree.configure(yscrollcommand=self.filter_tree_vsb.set, xscrollcommand=self.filter_tree_hsb.set)

        self.filter_grid_frame.grid(row=0, column=0, sticky="NEWS")

        self.filter_control_frame = tk.Frame(self.filter_frame)

        #option_list = ["Filter Mass", "Filter Intensity", "Filter Retention Time", "Filter Number Detections", "Filter Annotations", "Sort", "Sort time-series"]
        option_list = ["Filter Mass", "Filter Intensity", "Filter Retention Time", "Filter Number Detections", "Sort"]

        self.filter_option_selected = tk.StringVar(self.root)
        self.filter_option_selected.set("Select Filter...")

        self.filter_option = tk.OptionMenu(self.filter_control_frame, self.filter_option_selected, *option_list)
        self.filter_add = tk.Button(self.filter_control_frame, text="Add", command=self.add_filter)
        self.filter_remove = tk.Button(self.filter_control_frame, text="Remove", command=self.remove_filter)

        self.filter_option.grid(row=0, column=0)
        self.filter_add.grid(row=0, column=1)
        self.filter_remove.grid(row=0, column=2)

        self.filter_control_frame.grid(row=1, column=0, sticky="NEWS")
        self.filter_frame.grid(row=1, column=0, sticky="NEWS")

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

        # Derivatives all plot
        self.figure_der_all = plt.Figure(figsize=(7,7))#figsize=(6,5),dpi=100
        self.axes_der_all = self.figure_der_all.add_subplot(111)
        canvas_der_all = FigureCanvasTkAgg(self.figure_der_all, self.tab_der_all)
        toolbar_frame_der_all = tk.Frame(self.tab_der_all)
        toolbar_frame_der_all.pack(side="top",fill ='x',expand=True)
        toolbar_der_all = NavigationToolbar2Tk(canvas_der_all,toolbar_frame_der_all)
        canvas_der_all.get_tk_widget().pack(side="top",fill ='both',expand=True)
        canvas_der_all.draw()

        # Derivatives log plot
        self.figure_der_log = plt.Figure(figsize=(7,7))#figsize=(6,5),dpi=100
        self.axes_der_log = self.figure_der_log.add_subplot(111)
        canvas_der_log = FigureCanvasTkAgg(self.figure_der_log, self.tab_der_log)
        toolbar_frame_der_log = tk.Frame(self.tab_der_log)
        toolbar_frame_der_log.pack(side="top",fill ='x',expand=True)
        toolbar_der_log = NavigationToolbar2Tk(canvas_der_log,toolbar_frame_der_log)
        canvas_der_log.get_tk_widget().pack(side="top",fill ='both',expand=True)
        canvas_der_log.draw()

        # Intensity pattern all plot
        self.figure_int_all = plt.Figure(figsize=(7,7))#figsize=(6,5),dpi=100
        self.axes_int_all = self.figure_int_all.add_subplot(111)
        canvas_int_all = FigureCanvasTkAgg(self.figure_int_all, self.tab_int_all)
        toolbar_frame_int_all = tk.Frame(self.tab_int_all)
        toolbar_frame_int_all.pack(side="top",fill ='x',expand=True)
        toolbar_int_all = NavigationToolbar2Tk(canvas_int_all,toolbar_frame_int_all)
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
        self.set_grid_frame = tk.LabelFrame(self.middle_right_frame, padx=10, pady=10, text="Sets")

        self.set_tree = ttkw.CheckboxTreeview(self.set_grid_frame, height = 15, show=("headings","tree"), selectmode="browse")
        self.set_tree["columns"]=["Name"]
        self.set_tree.column("#0", width = 60, stretch = tk.YES)
        self.set_tree.column("#1", width = 150, stretch = tk.YES)
        self.set_tree.heading("#0", text="",)
        self.set_tree.heading("#1", text="Name")
        self.set_tree.bind('<ButtonRelease-1>', self.update_sets_view)
        self.set_tree.grid(row=0, column=0)

        self.set_tree_vsb = ttk.Scrollbar(self.set_grid_frame, orient="vertical", command=self.set_tree.yview)
        self.set_tree_vsb.grid(row=0, column=1, sticky="NEWS")
        self.set_tree_hsb = ttk.Scrollbar(self.set_grid_frame, orient="horizontal", command=self.set_tree.xview)
        self.set_tree_hsb.grid(row=1, column=0, sticky="NEWS")
        self.set_tree.configure(yscrollcommand=self.set_tree_vsb.set, xscrollcommand=self.set_tree_hsb.set)

        self.set_grid_frame.grid(row=0, column=0, sticky="NEWS")

        self.annotation_grid_frame = tk.LabelFrame(self.middle_right_frame, padx=10, pady=10, text="Details")

        self.annotation_tree = ttk.Treeview(self.annotation_grid_frame)
        self.annotation_tree["columns"]=["Label","Value"]
        self.annotation_tree.column("#0", width = 10, stretch = tk.YES)
        self.annotation_tree.column("#1", width = 80, stretch = tk.YES)
        self.annotation_tree.column("#2", width = 120, stretch = tk.YES)
        self.annotation_tree.heading("#0", text="",)
        self.annotation_tree.heading("#1", text="Label")
        self.annotation_tree.heading("#2", text="Value")
        self.annotation_tree.grid(row=0, column=0)

        self.annotation_tree_vsb = ttk.Scrollbar(self.annotation_grid_frame, orient="vertical", command=self.annotation_tree.yview)
        self.annotation_tree_vsb.grid(row=0, column=1, sticky="NEWS")
        self.annotation_tree_hsb = ttk.Scrollbar(self.annotation_grid_frame, orient="horizontal", command=self.annotation_tree.xview)
        self.annotation_tree_hsb.grid(row=1, column=0, sticky="NEWS")
        self.annotation_tree.configure(yscrollcommand=self.annotation_tree_vsb.set, xscrollcommand=self.annotation_tree_hsb.set)

        self.annotation_grid_frame.grid(row=1, column=0, sticky="NEWS")

        # Identification View

        self.identification_grid_frame = tk.LabelFrame(self.bottom_frame, padx=10, pady=10, text="Annotations")

        self.identification_tree = ttk.Treeview(self.identification_grid_frame, height = 8)
        self.identification_tree["columns"]=["ID", "Formula", "PPM", "Adduct", "Name", "Class", "Description"]
        self.identification_tree.column("#0", width=10, minwidth=10, stretch = tk.NO)
        self.identification_tree.column("#1", width = 100, stretch = tk.YES)
        self.identification_tree.column("#2", width = 200, stretch = tk.YES)
        self.identification_tree.column("#3", width = 100, stretch = tk.YES)
        self.identification_tree.column("#4", width = 200, stretch = tk.YES)
        self.identification_tree.column("#5", width = 200)
        self.identification_tree.column("#6", width = 200, stretch = tk.YES)
        self.identification_tree.column("#7", width = 200, stretch = tk.YES)
        self.identification_tree.heading("#0", text="")
        self.identification_tree.heading("#1", text="ID")
        self.identification_tree.heading("#2", text="Formula")
        self.identification_tree.heading("#3", text="PPM")
        self.identification_tree.heading("#4", text="Adduct")
        self.identification_tree.heading("#5", text="Name")
        self.identification_tree.heading("#6", text="Class")
        self.identification_tree.heading("#7", text="Description")
        self.identification_tree.grid(row=0, column=0)

        self.identification_tree_vsb = ttk.Scrollbar(self.identification_grid_frame, orient="vertical", command=self.identification_tree.yview)
        self.identification_tree_vsb.grid(row=0, column=1, sticky="NEWS")
        self.identification_tree_hsb = ttk.Scrollbar(self.identification_grid_frame, orient="horizontal", command=self.identification_tree.xview)
        self.identification_tree_hsb.grid(row=1, column=0, sticky="NEWS")
        self.identification_tree.configure(yscrollcommand=self.identification_tree_vsb.set, xscrollcommand=self.identification_tree_hsb.set)

        self.identification_grid_frame.grid(row=0, column=0)

        # Molecule View
        self.molecule_canvas_frame = tk.LabelFrame(self.bottom_frame, padx=10, pady=10, text="Molecule View")
        self.molecule_canvas = tk.Canvas(self.molecule_canvas_frame, bg="white", height=200, width=300)
        self.molecule_canvas.grid(row=0, column=0, sticky="NEWS")
        self.molecule_canvas_frame.grid(row=0, column=1, padx=(10,0))

        self.data.load_molecule_databases()

        self.root.config(menu=self.menubar)
        # Run GUI until event occurs.
        self.root.mainloop()

    # Fix to bug with tkinter
    def fixed_map(self, option):
        return [elm for elm in self.style.map("Treeview", query_opt=option) 
                if elm[:2] != ("!disabled","!selected")]

    def check_progress(self):
        if self.thread.is_alive():
            self.root.after(100, self.check_progress)
        else:
            self.show_progressbar(False)

    def show_progressbar(self, start):
        if start:
            self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, mode='indeterminate', takefocus=True)
            self.progress_bar.grid(row=1, column=0)
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.destroy()

    def import_peakml_file_with_progress(self):
        self.show_progressbar(True)

        self.thread = threading.Thread(target=self.import_peakml_file, args=())
        self.thread.daemon = True
        self.thread.start()

        self.check_progress()

    def export_peakml_file_with_progress(self):
        self.show_progressbar(True)

        self.thread = threading.Thread(target=self.export_peakml_file, args=())
        self.thread.daemon = True
        self.thread.start()

        self.check_progress()

    def refresh_entry_selected_with_progress(self):
        self.show_progressbar(True)

        self.thread = threading.Thread(target=self.refresh_entry_selected, args=())
        self.thread.daemon = True
        self.thread.start()

        self.check_progress()

    def refresh_entry_view_with_progress(self):
        self.show_progressbar(True)

        self.thread = threading.Thread(target=self.refresh_entry_view_with_reload, args=())
        self.thread.daemon = True
        self.thread.start()

        self.check_progress()

    def import_peakml_file(self):
        self.progress_details_text.set("Importing file...")

        try:
            filepath = self.get_filepath()

            if filepath:
                self.data.import_from_filepath(filepath)
                self.refresh_info_view()
                self.refresh_entry_view(True)
        except Exception as err:
            print("Error while importing file")
            print(err)
            self.progress_details_text.set("File import failed.")

        self.progress_details_text.set("File imported.")

    def export_peakml_file(self):
        self.progress_details_text.set("Exporting file...")

        try:
            filepath = self.get_filepath()

            if filepath:
                self.data.export_data_object_to_file(filepath)
        except Exception as err:
            print("Error while exporting file")
            print(err)
        
        self.progress_details_text.set("File exported.")

    # Menu Methods

    def file_open(self):
        try:
            filepath = fd.askopenfilename()
            if filepath:
                self.set_filepath(filepath)    
                self.import_peakml_file_with_progress()
        except IOError as ioerr:
            print("An IO error occurred")
            print(ioerr)
        except Exception as err:
            print("An error occurred")
            print(err)

    def file_save(self):
        # Ask 'Are you sure you want to update the imported file '<filename>'?
        try:
            self.export_peakml_file_with_progress()
        except IOError as ioerr:
            print("An error occurred")
            print(ioerr)
        except Exception as err:
            print("An error occurred")
            print(err)

    def file_save_as(self):
        try:
            filepath = fd.asksaveasfilename(defaultextension=".peakml")
            if filepath:
                self.set_filepath(filepath)    
                self.export_peakml_file_with_progress()
        except IOError as ioerr:
            print("An IO error occurred")
            print(ioerr)
        except Exception as err:
            print("An error occurred")
            print(err)

    def get_filepath(self):
        return self.filepath

    def set_filepath(self,filepath):
        self.filepath = filepath

    def get_min_max_retention_time(self):
        rt_list = self.df_entry["RT"].tolist()
        rt_list.sort()
        return rt_list[0], rt_list[-1]

    def edit_preferences(self):
        self.preferences_dialog()

    # Info View Methods

    def refresh_info_view(self):
        self.filename_text.set(self.data.get_filename())
        self.peak_number_text.set(self.data.get_nr_peaks() + " (" + str(self.data.get_total_nr_peaks()) + ")") 

    # Entry View Methods

    def refresh_entry_view_with_reload(self):
        self.refresh_entry_view(True)

    def refresh_entry_view(self, reload_entries):
        #Utils.trace("ref1")
        self.progress_details_text.set("Loading entry view...")

        focused_row_id = self.selected_id.get()
        self.entry_tree.delete(*self.entry_tree.get_children())    

        #Utils.trace("ref2")

        if reload_entries:
            self.data.update_entry_dataframe()
            self.df_entry = self.data.get_entry_view()
            focused_row_id = ''

        #Utils.trace("ref3")

        if self.df_entry is not None:
            for i in range(len(self.df_entry)):
                entry_row = self.df_entry.iloc[i]
                if focused_row_id == entry_row["UID"]:
                    focus = "has_ann_is_focus" if entry_row["HasAnnotation"] else "no_ann_is_focus"
                elif (focused_row_id is None or focused_row_id == '') and i == 0:
                    focus = "has_ann_is_focus" if entry_row["HasAnnotation"] else "no_ann_is_focus"
                else: 
                    focus = "has_ann_not_focus" if entry_row["HasAnnotation"] else "no_ann_not_focus"

                self.entry_tree.insert("",i,i, values=(entry_row["RT"], entry_row["Mass"], entry_row["Intensity"], int(entry_row["Nrpeaks"])), tags=(entry_row["UID"], focus)) 

        #Utils.trace("ref4")

        if reload_entries:
            self.entry_tree.focus(self.entry_tree.get_children()[0])    
            focused_entry = self.entry_tree.item(self.entry_tree.focus())
            focused_id = focused_entry["tags"][0]    
            self.selected_id.set(focused_id)
            self.data.set_selected_peak(focused_id)

        #Utils.trace("ref5")
        self.progress_details_text.set("Loading selected entry details for views...")

        self.data.update_data_frames_for_selected_entry()
        self.data.update_plot_data_frames_for_selected_entry()

        self.refresh_info_view()

        self.refresh_filters_view()
        #Utils.trace("ref6")

        self.refresh_set_view()

        #Utils.trace("ref7")

        self.refresh_annotation_view()

        #Utils.trace("ref8")

        self.refresh_identification_view()

        #Utils.trace("ref9")
        self.progress_details_text.set("Loading selected entry plots...")
        self.refresh_graph_view()

        #Utils.trace("ref10")
        self.progress_details_text.set("Entry loaded.")

    def select_entry(self, event):
        self.refresh_entry_selected_with_progress()

    def refresh_entry_selected(self):
        
        focused_entry = self.entry_tree.item(self.entry_tree.focus())
        focused_id = focused_entry["tags"][0]    
        self.selected_id.set(focused_id)
        self.data.set_selected_peak(focused_id)

        self.refresh_entry_view(False)

    def update_sets_view(self, event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # Save check status of each list
            for item in self.set_tree.get_children():
                for child_item in self.set_tree.get_children(item):
                    uid = self.set_tree.item(child_item)["tags"][0]
                    selected_status = False if self.set_tree.item(child_item)["tags"][2] == "unchecked" else True
                    self.data.update_set_selection(uid, selected_status)
            # Refresh grid
            self.generate_plot_peak()

    def refresh_identification_view(self):
        self.identification_tree.delete(*self.identification_tree.get_children())
        df_identification = self.data.get_identification_view()
        smiles_details = None
        inchi_details = None
        if df_identification is not None:
            for i in range(len(df_identification)):
                identification_row = df_identification.iloc[i]
                self.identification_tree.insert("",i,i, values=(identification_row["ID"],identification_row["Formula"],identification_row["PPM"],identification_row["Adduct"],identification_row["Name"],identification_row["Class"],identification_row["Description"]))
                smiles_details = identification_row["Smiles"]
                inchi_details = identification_row["InChi"]

        self.refresh_molecule_view(inchi_details, smiles_details)

    def refresh_set_view(self):  
        self.set_tree.delete(*self.set_tree.get_children())
        df_sets = self.data.get_set_view()
        if df_sets is not None:
            df_sets_parent = df_sets.loc[df_sets['Parent'].isnull()]

            if df_sets_parent is not None:
                for i in range(len(df_sets_parent)):
                    set_parent_row = df_sets_parent.iloc[i]    
                    name_parent = set_parent_row["Name"]

                    select_parent = "checked" if set_parent_row["Selected"] else "unchecked"

                    colour_tag = "colour_" + name_parent
                    self.set_tree.tag_configure(colour_tag, foreground=set_parent_row["Color"])
                    folder = self.set_tree.insert("", i, name_parent, values=(name_parent), tags=("uid",select_parent, colour_tag))
                    
                    df_sets_child = df_sets.loc[df_sets['Parent'] == name_parent]

                    if df_sets_child is not None:

                        for j in range(len(df_sets_child)):
                            set_child_row = df_sets_child.iloc[j]    
                            select_child = "checked" if set_child_row["Selected"] else "unchecked"

                            self.set_tree.insert(folder, "end", set_child_row["Name"], values=(set_child_row["Name"]), tags=(set_child_row["UID"], select_child, colour_tag))

    def refresh_annotation_view(self):    
        self.annotation_tree.delete(*self.annotation_tree.get_children())
        df_annotation = self.data.get_annotation_view()

        if df_annotation is not None:
            for i in range(len(df_annotation)):
                annotation_row = df_annotation.iloc[i]
                self.annotation_tree.insert("", i, i, values=(annotation_row["Label"], annotation_row["Value"]))

    def refresh_filters_view(self):
        self.filter_tree.delete(*self.filter_tree.get_children())
        df_filters = self.data.get_filters_list()

        if df_filters is not None:
            for i in range(len(df_filters)):
                filter_row = df_filters.iloc[i]
                self.filter_tree.insert("", i, i, values=(filter_row["Type"], filter_row["Settings"]), tags=(filter_row["ID"]))

    def refresh_molecule_view(self, inchi_data, smiles_data):
        self.molecule_canvas.delete("all")

        if inchi_data is not None:
            mol = inchi.MolFromInchi(inchi_data)
            mol_image = Draw.MolToImage(mol, size=(300,200))

        elif smiles_data is not None:
            mol = Chem.MolFromSmiles(smiles_data)
            mol_image = Draw.MolToImage(mol, size=(300,200))       
        else:
            mol_image = Image.new(mode="RGB", size=(300,200), color = (255, 255, 255))

        self.mol_img = ImageTk.PhotoImage(mol_image)
        self.molecule_canvas.create_image(150, 100, image=self.mol_img)

    # Graph View Methods

    def refresh_graph_view(self):
        
        #Utils.trace("plot1")
        self.generate_plot_peak()
        #Utils.trace("plot2")
        self.generate_plot_derivatives()
        #Utils.trace("plot3")
        self.generate_plots_int()
        #Utils.trace("plot4")

    def generate_plot_peak(self):
        df = self.data.get_plot_peak_view()    
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

    def generate_plot_derivatives(self):
        df = self.data.get_plot_derivative_view()
        self.generate_plot_der(df, "All", self.figure_der_all, self.axes_der_all)
        self.generate_plot_der(df, "Log", self.figure_der_log, self.axes_der_log)
        
    def generate_plot_der(self, data, type, figure_der, axes_der):
        axes_der.clear()

        mass_values = data['Mass']
        intensity_values = data['Intensity']
        label_values = data['Description']

        intensity_values_float = []

        for j in range(len(intensity_values)):
            intensity_values_float.append(float(intensity_values[j]))

        axes_der.stem(mass_values, intensity_values, markerfmt=" ")

        for i in range(len(data)):
            axes_der.annotate(label_values[i],(mass_values[i],intensity_values[i]))

        if type == "Log":
            axes_der.set_yscale('log')

        axes_der.set_xlabel("Mass")
        axes_der.set_ylabel("Intensity")
        figure_der.canvas.draw()
        figure_der.tight_layout()

    def generate_plots_int(self):
        df = self.data.get_plot_intensity_view()
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


            if len(Intensities_float):

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
        refresh = False

        option = self.filter_option_selected.get()
        if option == "Filter Mass":
            refresh = self.filter_mass_dialog()
        elif option == "Filter Intensity":
            refresh = self.filter_intensity_dialog()
        elif option == "Filter Retention Time":
            refresh = self.filter_retention_time_dialog()
        elif option == "Filter Number Detections":
            refresh = self.filter_number_detections_dialog()
        elif option == "Filter Annotations":
            refresh = self.filter_annotations_dialog()
        elif option == "Sort":
            refresh = self.filter_sort_dialog()
        elif option == "Sort time-series":
            refresh = self.filter_sort_time_series_dialog()

        if refresh:
            self.refresh_entry_view_with_progress()

    def remove_filter(self):
        if self.filter_tree.isEmpty:
            focused_filter = self.filter_tree.item(self.filter_tree.focus())
            if focused_filter:
                self.data.remove_filter_by_id(focused_filter["tags"][0])
                self.refresh_entry_view_with_progress()

    def filter_mass_dialog(self):
        dlg = FilterMassDialog(self.root,"Filter mass")
        if dlg.submit:
            self.data.add_filter_mass(dlg.mass_min, dlg.mass_max, dlg.formula, dlg.formula_ppm, dlg.mass_charge, dlg.filter_option)
            return True
        else:
            return False

    def filter_intensity_dialog(self):
        dlg = FilterIntensityDialog(self.root,"Filter intensity")
        if dlg.submit:
            self.data.add_filter_intensity(dlg.intensity_min)
            return True
        else:
            return False

    def filter_retention_time_dialog(self):
        rt_min, rt_max = self.get_min_max_retention_time()
        dlg = FilterRetentionTimeDialog(self.root,"Filter retention-time", rt_min, rt_max)
        if dlg.submit:
            self.data.add_filter_retention_time(dlg.retention_time_min_sec, dlg.retention_time_max_sec, dlg.retention_time_min_minu, dlg.retention_time_max_minu)
            return True
        else:
            return False

    def filter_number_detections_dialog(self):
        dlg = FilterNumberDetectionsDialog(self.root,"Filter number of detections")
        if dlg.submit:
            self.data.add_filter_number_detections(dlg.detection_number)
            return True
        else:
            return False

    def filter_annotations_dialog(self):
        dlg = FilterAnnotationsDialog(self.root,"Filter annotations")
        if dlg.submit:
            self.data.add_filter_annotations(dlg.annotation_name, dlg.annotation_relation, dlg.annotation_value)
            return True
        else:
            return False

    def filter_sort_dialog(self):
        dlg = SortDialog(self.root,"Sort")
        if dlg.submit:
            self.data.add_filter_sort()
            return True
        else:
            return False

    def filter_sort_time_series_dialog(self):
        dlg = SortTimeSeriesDialog(self.root,"Sort time series")
        if dlg.submit:
            self.data.add_filter_sort_times_series()
            return True
        else:
            return False

    def preferences_dialog(self):
        dlg = PreferencesDialog(self.root,"Preferences", self.data)
        if dlg.submit:
            self.data.update_settings(dlg.decdp, dlg.databases)
            self.refresh_info_view()
            self.refresh_entry_view_with_progress()

