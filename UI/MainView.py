import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import ttkwidgets as ttkw
#If package only available as pip, install with anaconda prompt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.dates import DateFormatter
import statistics as stats
from PIL import ImageTk, Image
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import inchi
import time
import threading
import os
import base64

from UI.ProgressDialog import ProgressDialog
from UI.LogDialog import LogDialog
from UI.EditIdentityDialog import EditIdentityDialog
from UI.FilterMassDialog import FilterMassDialog
from UI.FilterIntensityDialog import FilterIntensityDialog
from UI.FilterRetentionTimeDialog import FilterRetentionTimeDialog
from UI.FilterNumberDetectionsDialog import FilterNumberDetectionsDialog
from UI.FilterAnnotationsDialog import FilterAnnotationsDialog
from UI.SortDialog import SortDialog
from UI.SortTimeSeriesDialog import SortTimeSeriesDialog
from UI.PreferencesDialog import PreferencesDialog
import Icon as i
import Enums as e
import Utilities as u
import Logger as lg
import Progress as p

# Globals
configure_timer = None
class MainView():

# Need to look at more intelligent resizing
# Define starting layout
# Having it grow and shrink with resizing OF MAIN WINDOW
# individual parts can be manually adjusted.
# when resizing
# Each widget resizes to max first, then summary plot expands to fill rest.
# VF0 does not change.
# Can resizing below a certain size be prevented, does it need to be?
# Need to define natural max layout for all other widgets
# Target for the day: 9 hours

    @property
    def filter_options(self) -> dict[e.Filter, str]:
        return self._filter_options

    @property
    def set_width(self) -> int:
        return self._set_width

    @set_width.setter
    def set_width(self, width: int):
        self._set_width = width

    @property
    def set_height(self) -> int:
        return self._set_height

    @set_height.setter
    def set_height(self, height: int):
        self._set_height = height

    @property
    def set_vf0(self) -> int:
        return self._set_vf0

    @set_vf0.setter
    def set_vf0(self, vf0: int):
        self._set_vf0 = vf0

    @property
    def set_vf1(self) -> int:
        return self._set_vf1

    @set_vf1.setter
    def set_vf1(self, vf1: int):
        self._set_vf1 = vf1

    @property
    def set_mf0(self) -> int:
        return self._set_mf0

    @set_mf0.setter
    def set_mf0(self, mf0: int):
        self._set_mf0 = mf0

    @property
    def set_mf1(self) -> int:
        return self._set_mf1

    @set_mf1.setter
    def set_mf1(self, mf1: int):
        self._set_mf1 = mf1

    @property
    def set_mlf0(self) -> int:
        return self._set_mlf0

    @set_mlf0.setter
    def set_mlf0(self, mlf0: int):
        self._set_mlf0 = mlf0

    @property
    def set_mrf0(self) -> int:
        return self._set_mrf0

    @set_mrf0.setter
    def set_mrf0(self, mrf0: int):
        self._set_mrf0 = mrf0

    @property
    def set_mrf1(self) -> int:
        return self._set_mrf1

    @set_mrf1.setter
    def set_mrf1(self, mrf1: int):
        self._set_mrf1 = mrf1

    def __init__(self, data):

        self.root = tk.Tk()

        self.root.title('PeakMLViewerPy')

        #Read icon details and set
        icon_data = base64.b64decode(i.img)
        temp_file = "temp.ico"
        icon_file = open(temp_file, "wb")
        icon_file.write(icon_data)
        icon_file.close()
        self.root.wm_iconbitmap(True, temp_file)
        os.remove(temp_file)

        self.root.resizable(None, None)

        self.set_height = 720
        self.set_width = 1280
        self.first_resize_occurred = False

        self.root.geometry(f"{self.set_width}x{self.set_height}")

        self.style = ttk.Style()
        self.style.map('Treeview', foreground = self.fixed_map('foreground'), background = self.fixed_map('background'))
        self.style.map('Treeview', background=[('selected', 'blue')])

        self.data = data
        self.menubar = tk.Menu(self.root)

        self.filename_text = tk.StringVar()
        self.peak_number_text = tk.StringVar()
        self.warning_text = tk.StringVar()
        self.filter_option_selected = tk.StringVar(self.root)
        self.filter_option_selected.set("Filter mass range")

        self.progress_text = tk.StringVar()
        self.progress_text.set("No file imported.")

        self.progress_val = tk.DoubleVar()
        self.progress_val.set(0)

        self.current_layout = ""
        self.last_resize_initiated = time.time()

        self._filter_options = {}
        self._filter_options[e.Filter.Mass] = "Filter mass range"
        self._filter_options[e.Filter.Intensity] = "Filter minimum intensity"
        self._filter_options[e.Filter.RetentionTime] = "Filter retention time range"
        self._filter_options[e.Filter.NumberDetections] = "Filter to sample count"
        self._filter_options[e.Filter.Annotations] = "Filter to annotation"
        self._filter_options[e.Filter.Sort] = "Sort"
        self._filter_options[e.Filter.SortTimeSeries] = "Sort time-series"

        #Add 'File' category
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.file_open)
        self.filemenu.add_command(label="Save", command=self.file_save)
        self.filemenu.add_command(label="Save as...", command=self.file_save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Preferences", command=self.open_preferences_dialog)
        self.editmenu.add_command(label="Import IPA RData", command=self.import_ipa_file)

        #TODO: Remove from deployment version
        #self.editmenu.add_command(label="Get Layout", command=self.print_layout)

        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="View Log", command=self.open_log_dialog)
        self.menubar.add_cascade(label="Log", menu=self.editmenu)

        self.root_frame = tk.Frame(self.root, padx=0, pady=0)
        self.root_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self.root_frame.bind("<Configure>", self.reset_configure_timer)

        self.viewer_frame = tk.PanedWindow(self.root_frame, orient=tk.VERTICAL)
        self.viewer_frame.pack(fill=tk.BOTH, expand = tk.TRUE, padx=(5,5), pady=(5,5))

        # Top - Info View
        self.top_frame = tk.Frame(self.viewer_frame, padx=0, pady=0)
        self.viewer_frame.add(self.top_frame)

        # Middle - Paned (3x1)
        self.mid_frame = tk.PanedWindow(self.viewer_frame, orient=tk.HORIZONTAL)
        self.viewer_frame.add(self.mid_frame)

        # Bottom - Identification Viewce
        self.bot_frame = tk.LabelFrame(self.viewer_frame, padx=10, pady=10, text="Identities")
        self.viewer_frame.add(self.bot_frame)

        # Middle Left - Paned (1x2)
        self.mid_left_frame = tk.PanedWindow(self.mid_frame, orient=tk.VERTICAL)
        self.mid_frame.add(self.mid_left_frame)

        # Middle Centre - Plots View
        self.mid_cen_frame = tk.LabelFrame(self.mid_frame, text="Summary Plots")
        self.mid_frame.add(self.mid_cen_frame)

        # Middle Right - Paned (1x3)
        self.mid_right_frame = tk.PanedWindow(self.mid_frame, orient=tk.VERTICAL)
        self.mid_frame.add(self.mid_right_frame)

        # Middle Left Top - Entries View
        self.mid_left_top_frame = tk.LabelFrame(self.mid_left_frame, padx=10, pady=10, text="Entries")
        self.mid_left_frame.add(self.mid_left_top_frame)

        # Middle Left Bottom - Filters View
        self.mid_left_bot_frame = tk.LabelFrame(self.mid_left_frame, padx=10, pady=10, text="Filters")  
        self.mid_left_frame.add(self.mid_left_bot_frame)
  
        # Middle Right Top - Sets View
        self.mid_right_top_frame = tk.LabelFrame(self.mid_right_frame, padx=10, pady=10, text="Sets") 
        self.mid_right_frame.add(self.mid_right_top_frame)

        # Middle Right Mid - Details View
        self.mid_right_mid_frame = tk.LabelFrame(self.mid_right_frame, padx=10, pady=10, text="Details") 
        self.mid_right_frame.add(self.mid_right_mid_frame)
 
        # Middle Right Bottom - Molecule Viewer
        self.mid_right_bot_frame = tk.LabelFrame(self.mid_right_frame, padx=10, pady=10, text="Molecule View")      
        self.mid_right_frame.add(self.mid_right_bot_frame)

        # Info View
        filename_lbl = tk.Label(self.top_frame, text = "Filename:")
        filename_lbl.grid(row=0, column=0)
        peak_nr_lbl = tk.Label(self.top_frame, text = "Nr peaks:")
        peak_nr_lbl.grid(row=1, column=0)
        filename_val = tk.Label(self.top_frame, textvariable = self.filename_text)
        filename_val.grid(row=0, column=1)
        peak_nr_val = tk.Label(self.top_frame, textvariable = self.peak_number_text)
        peak_nr_val.grid(row=1, column=1)
        warning_val = tk.Label(self.top_frame, fg= "#ff0000", textvariable = self.warning_text)
        warning_val.grid(row=0, column=2)

        # Entry View
        entry_control_frame = tk.Frame(self.mid_left_top_frame)
        entry_control_frame.pack(side=tk.BOTTOM)
        self.entry_delete_checked_btn = tk.Button(entry_control_frame, text="Delete Checked", command=self.delete_checked_entries)
        self.entry_delete_checked_btn["state"] = "disabled"
        self.entry_delete_checked_btn.grid(row=0, column=0, padx=(2,2), pady=(2,2), sticky="NEWS")

        self.entry_tree = self.initialize_grid(self.mid_left_top_frame, True, [("Selected", 40), ("Retention time", 100), ("Mass", 80), ("Intensity", 80), ("Samples", 50)])

        self.entry_tree.bind('<ButtonRelease-1>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Up>', self.select_entry)
        self.entry_tree.bind('<KeyRelease-Down>', self.select_entry)
        self.entry_tree.tag_configure("has_ann_not_focus", foreground="black")
        self.entry_tree.tag_configure("no_ann_not_focus", foreground="grey")
        self.entry_tree.tag_configure("has_ann_is_focus", foreground="white", background="blue")
        self.entry_tree.tag_configure("no_ann_is_focus", foreground="white", background="blue")
   
        # Filter View
        option_list = [
            self.filter_options[e.Filter.Mass], 
            self.filter_options[e.Filter.Intensity], 
            self.filter_options[e.Filter.RetentionTime], 
            self.filter_options[e.Filter.NumberDetections]
            ]
        filter_control_frame = tk.Frame(self.mid_left_bot_frame)
        filter_control_frame.pack(side=tk.BOTTOM)
        self.filter_opm = tk.OptionMenu(filter_control_frame, self.filter_option_selected, *option_list)
        self.filter_opm.grid(row=0, column=0, padx=(2,2), pady=(2,2), sticky="NEWS")
        self.filter_add_btn = tk.Button(filter_control_frame, text="Add", command=self.add_filter)
        self.filter_add_btn["state"] = "disabled"
        self.filter_add_btn.grid(row=0, column=1, padx=(2,2), pady=(2,2), sticky="NEWS")
        self.filter_remove_btn = tk.Button(filter_control_frame, text="Remove", command=self.remove_filter)
        self.filter_remove_btn["state"] = "disabled"
        self.filter_remove_btn.grid(row=0, column=2, padx=(2,2), pady=(2,2), sticky="NEWS")
        self.filter_tree = self.initialize_grid(self.mid_left_bot_frame, False, [("Selected", 10), ("Type", 100), ("Settings", 100)])

        self.filter_tree.bind('<ButtonRelease-1>', self.select_filter)
        self.filter_tree.tag_configure("not_focus", foreground="black")
        self.filter_tree.tag_configure("is_focus", foreground="white", background="blue")

        # Plot View
        self.tabs_plot = ttk.Notebook(self.mid_cen_frame)
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

        self.figure_peak, self.axes_peak = self.initialize_plot(self.tab_peak)
        self.figure_der_all, self.axes_der_all = self.initialize_plot(self.tab_der_all)
        self.figure_der_log, self.axes_der_log = self.initialize_plot(self.tab_der_log)
        self.figure_int_all, self.axes_int_all = self.initialize_plot(self.tab_int_all)
        self.figure_int_log, self.axes_int_log = self.initialize_plot(self.tab_int_log)

        # Set View
        self.set_tree = self.initialize_grid(self.mid_right_top_frame, True, [("Selected", 60), ("Name", 150)])
        self.set_tree.bind('<ButtonRelease-1>', self.update_sets_view)

        # Annotation View
        self.ann_tree = self.initialize_grid(self.mid_right_mid_frame, False, [("Selected", 10), ("Label", 80), ("Value", 120)])

        # Molecule View
        self.molecule_canvas = tk.Canvas(self.mid_right_bot_frame, bg="white")

        molecule_canvas_vsb = ttk.Scrollbar(self.mid_right_bot_frame, orient="vertical")
        
        molecule_canvas_vsb.pack(side=tk.RIGHT, fill="y")
        molecule_canvas_hsb = ttk.Scrollbar(self.mid_right_bot_frame, orient="horizontal")
        
        molecule_canvas_hsb.pack(side=tk.BOTTOM, fill="x")
        self.molecule_canvas.configure(yscrollcommand=molecule_canvas_vsb.set, xscrollcommand=molecule_canvas_hsb.set)

        self.molecule_canvas.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.TRUE)
        molecule_canvas_vsb.config(command=self.molecule_canvas.yview)
        molecule_canvas_hsb.config(command=self.molecule_canvas.xview)
        #self.molecule_canvas.grid(row=0, column=0, sticky="")

        # Identification View
        iden_control_frame = tk.Frame(self.bot_frame)
        iden_control_frame.pack(side=tk.RIGHT)
        self.iden_edit_selected_btn = tk.Button(iden_control_frame, text="Edit Selected", command=self.edit_selected_identity)
        self.iden_edit_selected_btn["state"] = "disabled"
        self.iden_edit_selected_btn.grid(row=0, column=0, padx=(2,2), pady=(2,2), sticky="NEW")
        self.iden_delete_checked_btn = tk.Button(iden_control_frame, text="Delete Checked", command=self.delete_checked_identities)
        self.iden_delete_checked_btn["state"] = "disabled"
        self.iden_delete_checked_btn.grid(row=1, column=0, padx=(2,2), pady=(2,2), sticky="NEW")

        self.iden_tree = self.initialize_grid(self.bot_frame, True, [("Selected", 40), ("ID", 100), ("Formula", 150), ("PPM", 100), ("Adduct", 150), ("Name", 150), ("Class", 150), ("Description", 200), ("Prior", 100), ("Post", 100), ("Notes", 200)])

        self.iden_tree.bind('<ButtonRelease-1>', self.select_iden)
        self.iden_tree.bind('<KeyRelease-Up>', self.select_iden)
        self.iden_tree.bind('<KeyRelease-Down>', self.select_iden)
        self.iden_tree.tag_configure("not_focus", foreground="black")
        self.iden_tree.tag_configure("is_focus", foreground="white", background="blue")
        
        # Set initial widget layout vf_0, vf_1, mf_0, mf_1, mlf_0, mrf_0, mrf_1
        self.update_layout(43, 551, 303, 1011, 303, 153, 261)

        self.root.config(menu=self.menubar)

        #Set initial configure timer running.
        self.reset_configure_timer()

        # Run GUI until event occurs.
        self.root.mainloop()

    # Fix to bug with tkinter
    def fixed_map(self, option):
        return [elm for elm in self.style.map("Treeview", query_opt=option) 
                if elm[:2] != ("!disabled","!selected")]

#region Layout methods

#   https://stackoverflow.com/questions/38600625/do-something-after-a-period-of-gui-user-inactivity-tkinter
    def reset_configure_timer(self, event=None):
        global configure_timer

        # cancel previous event
        if configure_timer is not None:
            self.root.after_cancel(configure_timer)

        # create new
        configure_timer = self.root.after(200, self.update_layout_if_resize)


    def update_layout(self, vf_0, vf_1, mf_0, mf_1, mlf_0, mrf_0, mrf_1):

        # VF
        self.viewer_frame.update()
        self.viewer_frame.sash_place(0, 1, vf_0)
        self.viewer_frame.update()
        self.viewer_frame.sash_place(1, 1, vf_1)

        # MF
        self.mid_frame.update()
        self.mid_frame.sash_place(0, mf_0, 1)
        self.mid_frame.update()
        self.mid_frame.sash_place(1, mf_1, 1)
        
        # MLF
        self.mid_left_frame.update()
        self.mid_left_frame.sash_place(0, 1, mlf_0)
        
        # MRF
        self.mid_right_frame.update()
        self.mid_right_frame.sash_place(0, 1, mrf_0)
        self.mid_right_frame.update()
        self.mid_right_frame.sash_place(1, 1, mrf_1)

        self.set_vf0 = vf_0
        self.set_vf1 = vf_1
        self.set_mf0 = mf_0
        self.set_mf1 = mf_1
        self.set_mlf0 = mlf_0
        self.set_mrf0 = mrf_0
        self.set_mrf1 = mrf_1

    def get_current_layout(self, label):

        height = self.root_frame.winfo_height()
        width = self.root_frame.winfo_width()

        vf0 = self.viewer_frame.sash_coord(0)[1]
        vf1 = self.viewer_frame.sash_coord(1)[1]
        mf0 = self.mid_frame.sash_coord(0)[0]
        mf1 = self.mid_frame.sash_coord(1)[0]
        mlf0 = self.mid_left_frame.sash_coord(0)[1]
        mrf0 = self.mid_right_frame.sash_coord(0)[1]
        mrf1 = self.mid_right_frame.sash_coord(1)[1]

        print(f"{label}: height: {height}, width: {width}, VF0: {vf0}, VF1: {vf1}, MF0: {mf0}, MF1: {mf1}, MLF0: {mlf0}, MRF0: {mrf0}, MRF1: {mrf1}")


    def update_layout_if_resize(self):

        #print("Resize check.")

        current_height = self.root_frame.winfo_height()
        current_width = self.root_frame.winfo_width()

        # Update layout, if overall window size has changed.
        if (current_height != self.set_height or current_width != self.set_width):

            #print("Resize occurred.")

            height_change = current_height - self.set_height 
            width_change = current_width - self.set_width

            #print(f"hc {height_change} = {current_height} - {self.set_height}")
            #print(f"wc {width_change} = {current_width} - {self.set_width}")

            self.set_height = current_height
            self.set_width = current_width

            #print(f"luh {self.set_height} = {current_height}")
            #print(f"luw {self.set_width} = {current_width}")

            #print(f"hc {height_change}")
            #print(f"wc {width_change}")

            # info_view_w = width
            # info_view_h = vf0
            # entry_view_w = mf0
            # entry_view_h = mlf0
            # filter_view_w = mf0
            # filter_view_h = vf1 - mlf0
            # plot_view_w = mf1 - mf0
            # plot_view_h = vf1 - vf0
            # set_view_w = width - mf1
            # set_view_h = mrf0
            # ann_view_w = width - mf1
            # ann_view_h = mrf1 - mrf0
            # mol_view_w = width - mf1
            # mol_view_h = vf1 - mrf1
            # iden_view_w = width
            # iden_view_h = height - vf1
            # print(f"hc {height_change}")
            # print(f"wc {width_change}")

            # Fixed height, not modified 
            vf0_u = self.set_vf0
            # Increasing the height should be able to increase this an unlimited amount.
            vf1_u = self.set_vf1 + height_change
            # 
            mf0_u = self.set_mf0
            # Increasing the width should be able to increase this an unlimited amount.
            mf1_u = self.set_mf1 + width_change
            #
        
            #self.adjust_mlf(vf1_u, mf0_u)
            mlf0_u = self.set_mlf0


            # 
            mrf0_u = self.set_mrf0
            # 
            mrf1_u = self.set_mrf1
            #print(f"vf0_u {vf0_u}")
            #print(f"vf1_u {vf1_u} = {self.set_vf1} + {height_change}")
            #print(f"mf0_u {mf0_u}")
            #print(f"mf1_u {mf1_u} = {self.set_mf1} + {width_change}")
            #print(f"mlf0_u {mlf0_u}")
            #print(f"mrf0_u {mrf0_u}")
            #print(f"mrf1_u {mrf1_u}")

            self.update_layout(vf0_u, vf1_u, mf0_u, mf1_u, mlf0_u, mrf0_u, mrf1_u)

            #self.get_current_layout("UPDATED")


            def adjust_mlf(self, vf1, mf0):
                print("not implemented")

                #return mlf0

            def adjust_mrf(self, vf1, mf0):
                print("not implemented")

                #return mrf0, mrf1

            #get_adjusted mlf0 from widget heigh method.

            #get


#endregion

#region Control initialise methods

    def initialize_plot(self, tab):
        figure = plt.Figure(figsize=(10,10))#figsize=(7,7)
        axes = figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(figure, tab)
        toolbar_frame = tk.Frame(tab)
        toolbar_frame.pack(side="top",fill ='x', expand=True)
        NavigationToolbar2Tk(canvas, toolbar_frame)
        canvas.get_tk_widget().pack(side="top", fill ='both', expand=True)
        canvas.draw()

        return figure, axes
        
    def initialize_grid(self, frame, is_checkbox, columns):        
        if is_checkbox:
            tree = ttkw.CheckboxTreeview(frame, selectmode="browse", columns=len(columns))
        else:
            tree = ttk.Treeview(frame, columns=len(columns))
            
        tree["columns"] = [i[0] for i in columns]

        for i in range(len(columns)):
            column_name = columns[i][0] if columns[i][0] != "Selected" else ""
            #col_width = tk.font.Font().measure(column_name)
            tree.heading("#{0}".format(i), text=column_name)
            tree.column("#{0}".format(i), width = columns[i][1], stretch = False, anchor=tk.CENTER)
            #tree.column("#{0}".format(i), width = col_width, stretch = False, anchor=tk.CENTER)

        tree_vsb = ttk.Scrollbar(frame, orient="vertical")
        
        tree_vsb.pack(side=tk.RIGHT, fill="y")
        tree_hsb = ttk.Scrollbar(frame, orient="horizontal")
        
        tree_hsb.pack(side=tk.BOTTOM, fill="x")
        tree.configure(yscrollcommand=tree_vsb.set, xscrollcommand=tree_hsb.set)

        tree.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.TRUE)
        tree_vsb.config(command=tree.yview)
        tree_hsb.config(command=tree.xview)

        tree['show'] = ('headings','tree')

        return tree

#endregion

#region Logging methods

    def handle_error(self, error_message, error_details):
        lg.log_error(f'{error_message}: {error_details}')
        mb.showerror("Error", error_message)

#endregion

#region Progress bar methods

    def check_progress(self):
        if self.thread.is_alive():
            self.update_progress_details()
            self.root.after(100, self.check_progress) # Calls this method after 100 ms.
        else:
            self.show_progressbar(False)

    def show_progressbar(self, start):
        if start:
            self.start_progress_dialog()
        else:
            self.progress_text.set("Completed")

    def start_progress_dialog(self):
        self.progress_dlg = ProgressDialog(self.root, self.progress_text, self.progress_val)
        #self.progress_dlg.progress_start()

    def run_process_with_progress(self, func):
        self.show_progressbar(True)

        self.thread = threading.Thread(target=func, args=())
        self.thread.daemon = True
        self.thread.start()

        self.check_progress()

    def update_progress_details(self):
        self.progress_text.set(p.progress_text_global)
        self.progress_val.set(p.progress_value_global)

#endregion

#region IO Methods

    def import_peakml_file(self):
        p.update_progress("Importing file", 0)

        try:
            # Load data objects
            self.data.import_peakml_data()

            # Update UI widgets
            self.load_data_from_views()

        except Exception as err:
            self.handle_error("Unable to import PeakML file.", err)
            p.update_progress("Completed", 100)

        p.update_progress("File imported.", 100)

    def import_ipa_rdata_file(self):
        p.update_progress("Importing IPA data", 0)

        try:
            # Load data objects
            self.data.import_ipa_data()

            # Update UI widgets
            self.load_data_from_views()

        except Exception as err:
            self.handle_error("Unable to import IPA file.", err)

            p.update_progress("Completed", 100)

        p.update_progress("IPA data imported.", 100)

    def export_peakml_file(self):
        p.update_progress("Exporting file", 0)

        try:
            self.data.export_peakml()

        except Exception as err:
            self.handle_error("Unable to export PeakML file.", err)
        
        p.update_progress("File exported.", 100)

#endregion

#region Menu Methods

    def file_open(self):
        try:
            filepath = fd.askopenfilename()
            if filepath:
                self.data.import_peakml_filepath = filepath
                self.run_process_with_progress(self.import_peakml_file)
        except IOError as ioerr:
            self.handle_error("Unable to open PeakML file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to open PeakML file.", err)

    def file_save(self):     
        try:
            reply = mb.askokcancel(title="Update Imported File", message=f"Are you sure you want to update the imported file '{self.data.import_peakml_filename}'?")
            if reply == True:
                self.data.export_peakml_filepath = self.data.import_peakml_filepath
                self.run_process_with_progress(self.export_peakml_file)
        except IOError as ioerr:
            self.handle_error("Unable to save PeakML file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to save PeakML file.", err)

    def file_save_as(self):
        try:
            filepath = fd.asksaveasfilename(defaultextension=".peakml")
            if filepath:
                self.data.export_peakml_filepath = filepath
                self.run_process_with_progress(self.export_peakml_file)
        except IOError as ioerr:
            self.handle_error("Unable to save PeakML file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to save PeakML file.", err)

    def import_ipa_file(self):
        try:
            ipa_filepath = fd.askopenfilename(defaultextension=".Rdata")
            if ipa_filepath:
                self.data.import_ipa_filepath = ipa_filepath
                self.run_process_with_progress(self.import_ipa_rdata_file)
        except IOError as ioerr:
            self.handle_error("Unable to open IPA file.", ioerr)
        except Exception as err:
            self.handle_error("Unable to open IPA file.", err)

    def open_preferences_dialog(self):
        dlg = PreferencesDialog(self.root,"Preferences", self.data)
        if dlg.submit:
            self.data.update_settings(dlg.decdp, dlg.databases)
            self.run_process_with_progress(self.refresh_entry_selected)

    def open_log_dialog(self):
        LogDialog(self.root)
        
#endregion

#region Info/Entry View Methods

    def load_data_from_views(self):
        p.update_progress("Loading filter grid", 100)
        self.refresh_filters_grid()

        self.load_peak_data_from_views()

    def load_peak_data_from_views(self):
        p.update_progress("Loading entry grid", 50)
        self.refresh_info_values()
        self.refresh_entry_grid()
        lg.log_progress("Entry grid loaded.")

        p.update_progress("Loading sets grid", 60)
        self.refresh_set_grid()
        lg.log_progress("Sets grid loaded.")

        self.refresh_to_selected_entry()

    def refresh_to_selected_entry(self):

        p.update_progress("Loading annotation grid", 65)
        self.refresh_annotation_grid()
        lg.log_progress("Annotation grid loaded.")

        p.update_progress("Loading identification grid", 70)
        self.refresh_identification_grid()
        lg.log_progress("Identification grid loaded.")

        p.update_progress("Loading plots", 75)
        self.refresh_plots()
        lg.log_progress("Plots loaded.")

    def refresh_info_values(self):
        self.filename_text.set(self.data.import_peakml_filename)
        self.peak_number_text.set(self.data.nr_peaks_details) 

        if self.data.prior_probabilities_modified:
            self.warning_text.set("Warning: Prior values have been updated since import, so posterior probabilities will need to be recalculated.")

    def refresh_entry_grid(self):

        # Clear grid
        self.entry_tree.delete(*self.entry_tree.get_children())

        # Get view object dataframe
        self.df_entry = self.data.entry_view_dataframe

        #If values, populate grid
        if self.df_entry is not None:
            for i in range(len(self.df_entry)):
                entry_row = self.df_entry.iloc[i]

                # Set focus string
                if entry_row["HasAnnotation"] == True:
                    focus = "has_ann_is_focus" if entry_row["Selected"] == True else "has_ann_not_focus"
                else:
                    focus = "no_ann_is_focus" if entry_row["Selected"] == True else "no_ann_not_focus"

                # Add entries to tree
                self.entry_tree.insert("",i,i, values=(entry_row["RT"], entry_row["Mass"], entry_row["Intensity"], entry_row["Nrpeaks"]), tags=(entry_row["UID"], focus, "checked" if entry_row["Checked"] == True else "unchecked")) 

        # If any entries, enable button for adding filters.
        if len(self.entry_tree.get_children()) > 0:
            self.filter_add_btn["state"] = "normal"    
        else:
            self.filter_add_btn["state"] = "disabled"

        # If any checked entries, enable button for deleting checked entries.
        if self.data.check_if_any_checked_entries():
            self.entry_delete_checked_btn["state"] = "normal"
        else:
            self.entry_delete_checked_btn["state"] = "disabled"

    def select_entry(self, event):
     
        lg.log_progress("Begin selecting entry.")

        # Use currently focused row to update the tags on that one.
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        checked_item = self.entry_tree.identify("item", x, y)

        if "image" in elem:
            # Save check status of each list
            uid = self.entry_tree.item(checked_item)["tags"][0]
            selected_status = False if self.entry_tree.item(checked_item)["tags"][2] == "unchecked" else True
            self.data.update_entry_checked_status(uid, selected_status)

            if self.data.check_if_any_checked_entries():
                self.entry_delete_checked_btn["state"] = "normal"
            else:
                self.entry_delete_checked_btn["state"] = "disabled"
        else:
            # Get focused entry
            focused_entry = self.entry_tree.item(self.entry_tree.focus())
            selected_item = self.entry_tree.focus()
            #If exists, update selected entry property
            if focused_entry["tags"]:

                # Short circuit if selecting currently selected
                if self.data.selected_entry_uid != focused_entry["tags"][0]:

                    #TODO replace with dictionary storing uid with item id. 

                    # Find row that was previously selected, and update tag to remove focus.
                    for item in self.entry_tree.get_children():
                        uid = self.entry_tree.item(item)["tags"][0]
                        if uid == self.data.selected_entry_uid:
                            prev_item = item

                    # Update tags to remove focus from previously selected row and add to row being selected
                    self.update_selected_entry_grid_row(selected_item, prev_item)

                    self.data.selected_entry_uid = focused_entry["tags"][0]   

                #Attempt to load details of record, if unable revert to previously selected record.
                try:
                    self.run_process_with_progress(self.refresh_entry_selected)

                except Exception as err:
                    #Restore previous selection by updating tags
                    self.update_selected_entry_grid_row(prev_item, selected_item)
                    self.handle_error("Unable to load entry", err)

            lg.log_progress("Entry selected.")

    def update_selected_entry_grid_row(self, new_item, prev_item):

        # Prev row
        if self.entry_tree.item(prev_item)["tags"][1] == "has_ann_is_focus":
            self.entry_tree.item(prev_item, tags=(self.entry_tree.item(prev_item)["tags"][0], "has_ann_not_focus", self.entry_tree.item(prev_item)["tags"][2]))
        elif self.entry_tree.item(prev_item)["tags"][1] == "no_ann_is_focus":
            self.entry_tree.item(prev_item, tags=(self.entry_tree.item(prev_item)["tags"][0], "no_ann_not_focus", self.entry_tree.item(prev_item)["tags"][2]))

        # New row
        if self.entry_tree.item(new_item)["tags"][1] == "has_ann_not_focus":
            self.entry_tree.item(new_item, tags=(self.entry_tree.item(new_item)["tags"][0], "has_ann_is_focus", self.entry_tree.item(new_item)["tags"][2]))
        elif self.entry_tree.item(new_item)["tags"][1] == "no_ann_not_focus":
            self.entry_tree.item(new_item, tags=(self.entry_tree.item(new_item)["tags"][0], "no_ann_is_focus", self.entry_tree.item(new_item)["tags"][2]))

    def refresh_entry_selected(self):

        # Reloads data view objects for new selected entry.
        self.data.update_selected_entry()

        # Refreshes grids and plots from view object data (identification/annotation/plots)
        self.refresh_to_selected_entry()

    def delete_checked_entries(self):
        reply = mb.askokcancel(title="Delete Checked", message="Do you wish to delete all checked entries?")
        if reply == True:
            self.data.remove_checked_entries()
            self.load_data_from_views()

            #TODO: Avoid full reload if deleted row is not selected.

#endregion

#region Sets View Methods

    def update_sets_view(self, event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        if "image" in elem:
            # Save check status of each list
            for item in self.set_tree.get_children():
                for child_item in self.set_tree.get_children(item):
                    uid = self.set_tree.item(child_item)["tags"][0]
                    selected_status = False if self.set_tree.item(child_item)["tags"][2] == "unchecked" else True
                    self.data.update_set_checked_status(uid, selected_status)
            # Refresh grid
            self.generate_plot_peak()

    def refresh_set_grid(self):
        # Clear grid  
        self.set_tree.delete(*self.set_tree.get_children())

        # Load set view data
        df_sets = self.data.set_view_dataframe

        if df_sets is not None:
            # Filter to sets which have no parent value (so are the parents)
            df_sets_parent = df_sets.loc[df_sets['Parent'].isnull()]

            if df_sets_parent is not None:
                for i in range(len(df_sets_parent)):
                    set_parent_row = df_sets_parent.iloc[i]    
                    name_parent = set_parent_row["Name"]

                    select_parent = "checked" if set_parent_row["Checked"] else "unchecked"

                    colour_tag = "colour_" + name_parent
                    self.set_tree.tag_configure(colour_tag, foreground=set_parent_row["Color"])
                    folder = self.set_tree.insert("", i, name_parent, values=(name_parent), tags=("uid",select_parent, colour_tag))
                    
                    df_sets_child = df_sets.loc[df_sets['Parent'] == name_parent]

                    if df_sets_child is not None:

                        for j in range(len(df_sets_child)):
                            set_child_row = df_sets_child.iloc[j]    
                            select_child = "checked" if set_child_row["Checked"] else "unchecked"

                            self.set_tree.insert(folder, "end", set_child_row["Name"], values=(set_child_row["Name"]), tags=(set_child_row["UID"], select_child, colour_tag))

#endregion

#region Annotation Methods

    def refresh_annotation_grid(self):    
        self.ann_tree.delete(*self.ann_tree.get_children())
        df_annotation = self.data.annotation_view_dataframe

        if df_annotation is not None:
            for i in range(len(df_annotation)):
                ann_row = df_annotation.iloc[i]
                self.ann_tree.insert("", i, i, values=(ann_row["Label"], ann_row["Value"]))

#endregion

#region Identification View methods
    def refresh_identification_grid(self):
        self.iden_tree.delete(*self.iden_tree.get_children())
        df_identification = self.data.identification_view_dataframe

        smiles_details = inchi_details = None

        if df_identification is not None:
            for i in range(len(df_identification)):
                iden_row = df_identification.iloc[i]
                focus = "is_focus" if iden_row["Selected"] == True else "not_focus"
                checked = "checked" if iden_row["Checked"] == True else "unchecked"
                self.iden_tree.insert("",i,i, values=(iden_row["ID"],iden_row["Formula"],iden_row["PPM"],iden_row["Adduct"],iden_row["Name"],iden_row["Class"],iden_row["Description"],iden_row["Prior"],iden_row["Post"],iden_row["Notes"]), tags=(iden_row["UID"], focus, checked))
                
                if iden_row["Selected"] == True:
                    smiles_details = iden_row["Smiles"]
                    inchi_details = iden_row["InChi"]

        if len(self.iden_tree.get_children()) > 0:
            self.iden_edit_selected_btn["state"] = "normal"
        else:
            self.iden_edit_selected_btn["state"] = "disabled"

        if self.data.check_if_any_checked_identifications():
            self.iden_delete_checked_btn["state"] = "normal"
        else:
            self.iden_delete_checked_btn["state"] = "disabled"

        self.refresh_molecule_canvas(inchi_details, smiles_details)

    def refresh_molecule_canvas(self, inchi_data, smiles_data):
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

    def select_iden(self, event):
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify("element", x, y)
        checked_item = self.iden_tree.identify("item", x, y)
        if "image" in elem:
            uid = self.iden_tree.item(checked_item)["tags"][0]
            selected_status = False if self.iden_tree.item(checked_item)["tags"][2] == "unchecked" else True
            self.data.update_identification_checked_status(uid, selected_status)

            if self.data.check_if_any_checked_identifications():
                self.iden_delete_checked_btn["state"] = "normal"
            else:
                self.iden_delete_checked_btn["state"] = "disabled"
        else:
            self.refresh_iden_selected()

    def refresh_iden_selected(self):
        focused_iden = self.iden_tree.item(self.iden_tree.focus())

        if focused_iden["tags"]:
            focused_id = focused_iden["tags"][0]
            self.data.selected_identification_uid = focused_id

        self.refresh_identification_grid()

    def delete_checked_identities(self):
        if self.data.ipa_imported:
            warning_message = "Are you sure you wish to remove selected identities? Prior probabilities of remaining identities will be updated."
        else:
            warning_message = "Do you wish to delete all checked identifications?"

        reply = mb.askokcancel(title="Delete Checked", message=warning_message)
        if reply == True:
            self.data.remove_checked_identifications()
            self.refresh_identification_grid()
            self.refresh_info_values()

    def edit_selected_identity(self):
        self.open_edit_identity_dialog()

    def open_edit_identity_dialog(self):
        uid, id, prior, notes = self.data.get_selected_identification_details()

        dlg = EditIdentityDialog(self.root,"Edit Identity", id, prior, notes, self.data.ipa_imported)
        if dlg.submit:
            self.data.update_identification_details(uid, dlg.prior, dlg.notes)
            self.refresh_identification_grid()
            self.refresh_info_values()

#endregion

#region Plots Methods

    def refresh_plots(self):
        lg.log_progress("Begin loading plots.")

        p.update_progress("Loading peak plots", 75)
        self.generate_plot_peak()
        lg.log_progress("Peak plot loaded.")

        p.update_progress("Loading derivative plots", 80)
        self.generate_plot_derivatives()
        lg.log_progress("Derivative plots loaded.")

        p.update_progress("Loading intensity plots", 90)
        self.generate_plots_int()
        lg.log_progress("Intensity plots loaded.")

    def generate_plot_peak(self):
        df = self.data.plot_peak_view_dataframe   
        plot_count = len(df)
        self.axes_peak.clear()
        for i in range(plot_count):
            RT_values_arr = df.iloc[i]['RT_values']
            Intensity_values_arr = df.iloc[i]['Intensity_values']
            plot_label = df.iloc[i]["Label"]
            colour = df.iloc[i]["Colour"]

            visible = self.data.get_set_checked_status(plot_label)

            if visible:
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
        df = self.data.plot_der_view_dataframe

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

        axes_der.set_xscale('linear')

        if type == "Log":
            axes_der.set_yscale('log')
        else:
            axes_der.set_yscale('linear')

        axes_der.set_xlabel("Mass")
        axes_der.set_ylabel("Intensity")
        figure_der.canvas.draw()
        figure_der.tight_layout()

    def generate_plots_int(self):
        df = self.data.plot_int_all_view_dataframe
        self.generate_plot_int_all(df)
        self.generate_plot_int_log(df)

    def generate_plot_int_all(self, data):
        self.axes_int_all.clear()
        set_id_arr = []
        ints_arr = []
        
        for i in range(len(data)):

            set_id = data.iloc[i]['SetID']
            ints = data.iloc[i]['Intensities']
        
            for j in range(len(ints)):

                set_id_val = str(set_id) + "-" + str(j + 1)
                set_id_arr.append(set_id_val)
                ints_arr.append(float(ints[j]))

        self.axes_int_all.plot(set_id_arr, ints_arr, marker='', linewidth=0.5)

        self.axes_int_all.set_xlabel("Set")
        self.axes_int_all.set_ylabel("Intensity")

        self.axes_int_all.set_xticklabels(set_id_arr, rotation = 90)

        self.figure_int_all.canvas.draw()
        self.figure_int_all.tight_layout()

    def generate_plot_int_log(self, data):
        self.axes_int_log.clear()
        ints_float = []
        set_id_arr = []
        ints_mean_arr = []
        ints_neg_arr = []
        ints_pos_arr = []
    
        for i in range(len(data)):

            set_id = data.iloc[i]['SetID']
            ints = data.iloc[i]['Intensities']

            for i in range(len(ints)):
                ints_float.append(float(ints[i]))

            if len(ints_float):
                ints_mean = stats.mean(ints_float)
                ints_max = max(ints_float)
                ints_min = min(ints_float)

                set_id_arr.append(set_id)
                ints_mean_arr.append(ints_mean)
                ints_neg_arr.append(ints_mean - ints_min)
                ints_pos_arr.append(ints_max - ints_mean)

        self.axes_int_log.errorbar(set_id_arr, ints_mean_arr, yerr=[ints_neg_arr, ints_pos_arr])

        self.axes_int_log.set_xlabel("Set")
        self.axes_int_log.set_ylabel("Intensity")

        self.axes_int_log.set_xticklabels(set_id_arr, rotation = 90)

        self.figure_int_log.canvas.draw()
        self.figure_int_log.tight_layout()

#endregion

#region Filter methods

    def refresh_filters_grid(self):
        self.filter_tree.delete(*self.filter_tree.get_children())
        df_filters = self.data.filter_view_dataframe

        if df_filters is not None:
            for i in range(len(df_filters)):
                filter_row = df_filters.iloc[i]

                focus = "is_focus" if filter_row["Selected"] == True else "not_focus"
                self.filter_tree.insert("", i, i, values=(filter_row["Type"], filter_row["Settings"]), tags=(filter_row["UID"], focus))

        # Toggle disability of remove filter button depending on if filter values exist.
        if len(self.filter_tree.get_children()) > 0:
            self.filter_remove_btn["state"] = "normal"
        else:
            self.filter_remove_btn["state"] = "disabled"

    def select_filter(self, event):
        self.refresh_filter_selected()

    def refresh_filter_selected(self):
        focused_filter = self.filter_tree.item(self.filter_tree.focus())

        if focused_filter["tags"]:
            focused_id = focused_filter["tags"][0]
            self.data.selected_filter_uid = focused_id

        self.refresh_filters_grid()

    def add_filter(self):
        refresh = False

        option = self.filter_option_selected.get()
        if option == self.filter_options[e.Filter.Mass]:
            refresh = self.open_filter_mass_dialog()
        elif option == self.filter_options[e.Filter.Intensity]:
            refresh = self.open_filter_intensity_dialog()
        elif option == self.filter_options[e.Filter.RetentionTime]:
            refresh = self.open_filter_retention_time_dialog()
        elif option == self.filter_options[e.Filter.NumberDetections]:
            refresh = self.open_filter_number_detections_dialog()
        elif option == self.filter_options[e.Filter.Annotations]:
            refresh = self.open_filter_annotations_dialog()
        elif option == self.filter_options[e.Filter.Sort]:
            refresh = self.open_filter_sort_dialog()
        elif option == self.filter_options[e.Filter.SortTimeSeries]:
            refresh = self.open_filter_sort_time_series_dialog()

        if refresh:
            self.run_process_with_progress(self.load_data_from_views)

    def remove_filter(self):
        # Need to include progress on this section
        self.data.remove_filter_by_id(self.data.selected_filter_uid)

        self.run_process_with_progress(self.load_data_from_views)

    def open_filter_mass_dialog(self):
        title = self.filter_options[e.Filter.Mass]
        mass_min, mass_max = self.data.get_min_max_mass()
        dlg = FilterMassDialog(self.root, title, mass_min, mass_max)

        # Need to include progress on this section
        if dlg.submit:
            self.data.add_filter_mass(dlg.mass_min, dlg.mass_max) #, dlg.formula, dlg.formula_ppm, dlg.mass_charge, dlg.filter_option
            return True
        else:
            return False

    def open_filter_intensity_dialog(self):
        title = self.filter_options[e.Filter.Intensity]
        intensity_min, intensity_max = self.data.get_min_max_intensity()
        dlg = FilterIntensityDialog(self.root, title, intensity_min)
        if dlg.submit:
            self.data.add_filter_intensity(dlg.intensity_min)
            return True
        else:
            return False

    def open_filter_retention_time_dialog(self):
        title = self.filter_options[e.Filter.RetentionTime]
        rt_min, rt_max = self.data.get_min_max_retention_time()
        dlg = FilterRetentionTimeDialog(self.root, title, rt_min, rt_max)
        if dlg.submit:
            self.data.add_filter_retention_time(dlg.retention_time_min_sec, dlg.retention_time_max_sec, dlg.retention_time_min_minu, dlg.retention_time_max_minu)
            return True
        else:
            return False

    def open_filter_number_detections_dialog(self):
        title = self.filter_options[e.Filter.NumberDetections]
        sample_count_min, sample_count_max = self.data.get_min_max_samples_count()
        dlg = FilterNumberDetectionsDialog(self.root, title, sample_count_min, sample_count_max)
        if dlg.submit:
            self.data.add_filter_number_detections(dlg.sample_count)
            return True
        else:
            return False

    def open_filter_annotations_dialog(self):
        title = self.filter_options[e.Filter.Annotations]
        dlg = FilterAnnotationsDialog(self.root, title)
        if dlg.submit:
            self.data.add_filter_annotations(dlg.annotation_name, dlg.annotation_relation, dlg.annotation_value)
            return True
        else:
            return False

    def open_filter_sort_dialog(self):
        title = self.filter_options[e.Filter.Sort]
        dlg = SortDialog(self.root, title)
        if dlg.submit:
            self.data.add_filter_sort()
            return True
        else:
            return False

    def open_filter_sort_time_series_dialog(self):
        title = self.filter_options[e.Filter.SortTimeSeries]
        dlg = SortTimeSeriesDialog(self.root, title)
        if dlg.submit:
            self.data.add_filter_sort_times_series()
            return True
        else:
            return False

#endregion