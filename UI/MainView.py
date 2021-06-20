import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import ttkwidgets as ttkw
#If package only available as pip, install with anaconda prompt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.dates import DateFormatter
import statistics as stats
from PIL import ImageTk, Image
from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole, ShowMol
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
        self.entry_tree.column("#2", width=100, stretch = tk.YES)
        self.entry_tree.column("#3", width=100, stretch = tk.YES)
        self.entry_tree.column("#4", width=50, stretch = tk.YES)
        self.entry_tree.heading("#0", text="")
        self.entry_tree.heading("#1", text="Retention time")
        self.entry_tree.heading("#2", text="Mass")
        self.entry_tree.heading("#3", text="Intensity")
        self.entry_tree.heading("#4", text="Samples")
        self.entry_tree.bind('<ButtonRelease-1>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Up>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Down>', self.select_entry)
        self.entry_tree.tag_configure("has_ann", foreground="black")
        self.entry_tree.tag_configure("no_ann", foreground="grey")
        self.entry_tree.tag_configure("is_focus", foreground="white", background="blue")
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

        option_list = ["Filter Mass", "Filter Intensity", "Filter Retention Time", "Filter Number Detections", "Filter Annotations", "Sort", "Sort time-series"]
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
        self.sets_grid_frame = tk.LabelFrame(self.middle_right_frame, padx=10, pady=10, text="Sets")

        self.sets_tree = ttkw.CheckboxTreeview(self.sets_grid_frame, height = 15, show=("headings","tree"), selectmode="browse")
        self.sets_tree["columns"]=["Name"]
        self.sets_tree.column("#0", width = 60, stretch = tk.YES)
        self.sets_tree.column("#1", width = 150, stretch = tk.YES)
        self.sets_tree.heading("#0", text="",)
        self.sets_tree.heading("#1", text="Name")
        self.sets_tree.bind('<ButtonRelease-1>', self.update_sets_view)
        self.sets_tree.grid(row=0, column=0)

        self.sets_tree_vsb = ttk.Scrollbar(self.sets_grid_frame, orient="vertical", command=self.sets_tree.yview)
        self.sets_tree_vsb.grid(row=0, column=1, sticky="NEWS")
        self.sets_tree_hsb = ttk.Scrollbar(self.sets_grid_frame, orient="horizontal", command=self.sets_tree.xview)
        self.sets_tree_hsb.grid(row=1, column=0, sticky="NEWS")
        self.sets_tree.configure(yscrollcommand=self.sets_tree_vsb.set, xscrollcommand=self.sets_tree_hsb.set)

        self.sets_grid_frame.grid(row=0, column=0, sticky="NEWS")

        self.details_grid_frame = tk.LabelFrame(self.middle_right_frame, padx=10, pady=10, text="Details")

        self.details_tree = ttk.Treeview(self.details_grid_frame)
        self.details_tree["columns"]=["Label","Value"]
        self.details_tree.column("#0", width = 10, stretch = tk.YES)
        self.details_tree.column("#1", width = 80, stretch = tk.YES)
        self.details_tree.column("#2", width = 120, stretch = tk.YES)
        self.details_tree.heading("#0", text="",)
        self.details_tree.heading("#1", text="Label")
        self.details_tree.heading("#2", text="Value")
        self.details_tree.grid(row=0, column=0)

        self.details_tree_vsb = ttk.Scrollbar(self.details_grid_frame, orient="vertical", command=self.details_tree.yview)
        self.details_tree_vsb.grid(row=0, column=1, sticky="NEWS")
        self.details_tree_hsb = ttk.Scrollbar(self.details_grid_frame, orient="horizontal", command=self.details_tree.xview)
        self.details_tree_hsb.grid(row=1, column=0, sticky="NEWS")
        self.details_tree.configure(yscrollcommand=self.details_tree_vsb.set, xscrollcommand=self.details_tree_hsb.set)

        self.details_grid_frame.grid(row=1, column=0, sticky="NEWS")

        # Annotation View

        self.annotation_grid_frame = tk.LabelFrame(self.bottom_frame, padx=10, pady=10, text="Annotations")

        self.annotation_tree = ttk.Treeview(self.annotation_grid_frame, height = 8)
        self.annotation_tree["columns"]=["ID", "Formula", "PPM", "Adduct", "Name", "Class", "Description"]
        self.annotation_tree.column("#0", width=10, minwidth=10, stretch = tk.NO)
        self.annotation_tree.column("#1", width = 100, stretch = tk.YES)
        self.annotation_tree.column("#2", width = 200, stretch = tk.YES)
        self.annotation_tree.column("#3", width = 100, stretch = tk.YES)
        self.annotation_tree.column("#4", width = 200, stretch = tk.YES)
        self.annotation_tree.column("#5", width = 200)
        self.annotation_tree.column("#6", width = 200, stretch = tk.YES)
        self.annotation_tree.column("#7", width = 200, stretch = tk.YES)
        self.annotation_tree.heading("#0", text="")
        self.annotation_tree.heading("#1", text="ID")
        self.annotation_tree.heading("#2", text="Formula")
        self.annotation_tree.heading("#3", text="PPM")
        self.annotation_tree.heading("#4", text="Adduct")
        self.annotation_tree.heading("#5", text="Name")
        self.annotation_tree.heading("#6", text="Class")
        self.annotation_tree.heading("#7", text="Description")
        self.annotation_tree.grid(row=0, column=0)

        self.annotation_tree_vsb = ttk.Scrollbar(self.annotation_grid_frame, orient="vertical", command=self.annotation_tree.yview)
        self.annotation_tree_vsb.grid(row=0, column=1, sticky="NEWS")
        self.annotation_tree_hsb = ttk.Scrollbar(self.annotation_grid_frame, orient="horizontal", command=self.annotation_tree.xview)
        self.annotation_tree_hsb.grid(row=1, column=0, sticky="NEWS")
        self.annotation_tree.configure(yscrollcommand=self.annotation_tree_vsb.set, xscrollcommand=self.annotation_tree_hsb.set)

        self.annotation_grid_frame.grid(row=0, column=0)

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
            self.progress_bar.grid(row=0, column=1)
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.destroy()

    def import_file(self):
        self.show_progressbar(True)

        self.thread = threading.Thread(target=self.import_peakml_file, args=())
        self.thread.daemon = True
        self.thread.start()

        self.check_progress()

    def import_peakml_file(self):
        self.progress_details_text.set("Importing file...")

        try:
            filepath = self.get_filepath()

            if filepath:
                self.data.import_from_filepath(filepath)
                self.refresh_views(True)
        except Exception as err:
            print (err)

        self.progress_details_text.set("File imported.")

    def export_file(self):
        self.show_progressbar(True)

        self.thread = threading.Thread(target=self.export_peakml_file, args=())
        self.thread.daemon = True
        self.thread.start()

        self.check_progress()

    def export_peakml_file(self):
        self.progress_details_text.set("Exporting file...")

        try:
            filepath = self.get_filepath()

            if filepath:
                self.data.export_data_object_to_file(filepath)
        except Exception as err:
            print (err)
        
        self.progress_details_text.set("File exported.")

    # Menu Methods

    def file_open(self):
        try:
            filepath = fd.askopenfilename()
            self.set_filepath(filepath)    
            self.import_file()
        except IOError as ioerr:
            print("An error occurred")
            print(ioerr)
        except Exception as err:
            print("An error occurred")
            print(err)

    def file_save(self):
        # Ask 'Are you sure you want to update the imported file '<filename>'?
        try:
            self.export_peakml_file()
        except IOError as ioerr:
            print("An error occurred")
            print(ioerr)
        except Exception as err:
            print("An error occurred")
            print(err)

    def file_save_as(self):
        try:
            filepath = fd.asksaveasfilename(defaultextension=".peakml")
            self.set_filepath(filepath)    
            self.export_peakml_file()
        except IOError as ioerr:
            print("An error occurred")
            print(ioerr)
        except Exception as err:
            print("An error occurred")
            print(err)

    def get_filepath(self):
        return self.filepath

    def set_filepath(self,filepath):
        self.filepath = filepath

    def edit_preferences(self):
        self.preferences_dialog()

    # Info View Methods

    def refresh_info_view(self):
        self.filename_text.set(self.data.get_filename())
        self.peak_number_text.set(self.data.get_nr_peaks() + " (" + str(self.data.get_total_nr_peaks()) + ")") 

    # Entry View Methods

    def refresh_entry_view(self, reload_entries):
        focused_row_id = self.selected_id.get()
        self.entry_tree.delete(*self.entry_tree.get_children())    

        if reload_entries:
            self.df_entry = self.data.get_entry_list()

        for i in range(len(self.df_entry)):
            entry_row = self.df_entry.iloc[i]
            focus = "is_focus" if focused_row_id == entry_row["Sha1sum"] or (focused_row_id is None and i == 0) else "not_focus"
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
        self.refresh_sets_view()
        self.refresh_graph_view()
        self.refresh_identification_view()
        self.refresh_details_view()

    def refresh_views(self, reload_entries):
        self.refresh_info_view()
        Utils.trace("ref1")
        self.refresh_entry_view(reload_entries)
        Utils.trace("ref2")
        self.refresh_entry_selected(reload_entries)
        Utils.trace("ref3")
        self.refresh_graph_view()
        #Utils.trace("ref4")
        #self.refresh_identification_view()
        #self.refresh_sets_view()
        #self.refresh_details_view()
        #self.refresh_filters_view()

    def update_sets_view(self, event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # Save check status of each list
            for item in self.sets_tree.get_children():
                for child_item in self.sets_tree.get_children(item):
                    name = self.sets_tree.item(child_item)["values"][0]
                    selected_status = False if self.sets_tree.item(child_item)["tags"][1] == "unchecked" else True
                    self.data.update_set_selection(name, selected_status)
            # Refresh grid
            self.refresh_graph_view()

    def refresh_identification_view(self):
        self.annotation_tree.delete(*self.annotation_tree.get_children())
        df_identifications = self.data.get_identification()
        smiles_details = None
        inchi_details = None
        if df_identifications is not None:
            for i in range(len(df_identifications)):
                identification_row = df_identifications.iloc[i]
                self.annotation_tree.insert("",i,i, values=(identification_row["ID"],identification_row["Formula"],identification_row["PPM"],identification_row["Adduct"],identification_row["Name"],identification_row["Class"],identification_row["Description"]))
                smiles_details = identification_row["Smiles"]
                inchi_details = identification_row["InChi"]

        self.refresh_molecule_view(inchi_details, smiles_details)

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
        self.generate_plot_der(df, "All")
        self.generate_plot_der(df, "Log")
        
    def generate_plot_der(self, data, type):
        self.axes_der_all.clear()

        mass_values = data['Mass']
        intensity_values = data['Intensity']
        label_values = data['Description']

        intensity_values_float = []

        for j in range(len(intensity_values)):
                intensity_values_float.append(float(intensity_values[j]))

        self.axes_der_all.stem(mass_values, intensity_values, markerfmt=None)

        for i in range(len(data)):
            self.axes_der_all.annotate(label_values[i],(mass_values[i],intensity_values[i]))

        if type == "Log":
            self.axes_der_log.set_yscale('log')

        self.axes_der_all.set_xlabel("Mass")
        self.axes_der_all.set_ylabel("Intensity")
        self.figure_der_all.canvas.draw()
        self.figure_der_all.tight_layout()

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

    def preferences_dialog(self):
        dlg = PreferencesDialog(self.root,"Preferences", self.data)
        #self.data.add_filter_intensity(dlg.intensity_min, dlg.intensity_unit)

        self.data.update_settings()

   # def start_progress(self, name):
   #     self.progress = ProgressBarDialog(self.root, name)
        

    #def end_progress(self):
    #    self.progress.close()
        
    #def start_progress_bar(self):
    #    self.progress_bar.progress_start()

    #def stop_progress_bar(self):
    #    self.progress_bar.progress_stop()