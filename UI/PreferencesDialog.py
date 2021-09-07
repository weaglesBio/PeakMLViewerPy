import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import os.path
import Logger as lg
import Enums as e
from UI.ViewerDialog import ViewerDialog
class PreferencesDialog(ViewerDialog):

    @property
    def plot_options(self) -> "dict[e.Filter, str]":
        return self._plot_options

    def __init__(self, parent, title, data):
        self.decdp = data.get_settings_preference_by_name('decdp')
        self.defplot = data.get_settings_preference_by_name('defplot')
        self.databases = data.get_settings_database_paths()
        self.submit = False

        self._plot_options = {}
        self._plot_options[e.Plot.Peak] = "Peak"
        self._plot_options[e.Plot.DerivativesAll] = "Derivatives:All"
        self._plot_options[e.Plot.DerivativesLog] = "Derivatives:Log"
        self._plot_options[e.Plot.IntensityPatternAll] = "Intensity:All"
        self._plot_options[e.Plot.IntensityPatternTrend] = "Intensity:Log"

        super().__init__(parent, title, width=500, height=280, take_focus=True, extendable=False)
    
    def body(self, frame):

        #Set up tabs.

        self.tabs_preferences = ttk.Notebook(frame)
        self.tab_appearance = ttk.Frame(self.tabs_preferences)
        self.tab_databases = ttk.Frame(self.tabs_preferences)
        
        self.tabs_preferences.add(self.tab_appearance, text = "Appearance")
        self.tabs_preferences.add(self.tab_databases, text = "Databases")
        self.tabs_preferences.pack(expand = 1, fill = "both")

        # Appearance section
        self.val_decdp = tk.StringVar(value=self.decdp)

        self.plot_option_selected = tk.StringVar(value=self.defplot)

        self.lbl_decdp = tk.Label(self.tab_appearance, width=15, text="Decimal Points:")
        self.spbx_decdp = tk.Spinbox(self.tab_appearance, width=15, from_=0, to=30, state='readonly', textvariable=self.val_decdp)

        self.lbl_decdp.grid(row=0, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")
        self.spbx_decdp.grid(row=0, column=1, padx=(2,2), pady=(5,5),sticky="NEWS")

        self.lbl_defplot = tk.Label(self.tab_appearance, width=15, text="Default Plot:")
        self.lbl_defplot.grid(row=1, column=0, padx=(2,2), pady=(5,5),sticky="NEWS")

        option_list = [
            self.plot_options[e.Plot.Peak], 
            self.plot_options[e.Plot.DerivativesAll], 
            self.plot_options[e.Plot.DerivativesLog], 
            self.plot_options[e.Plot.IntensityPatternAll],
            self.plot_options[e.Plot.IntensityPatternTrend]
            ]

        self.plot_opm = tk.OptionMenu(self.tab_appearance, self.plot_option_selected, *option_list)
        self.plot_opm.grid(row=1, column=1, padx=(2,2), pady=(2,2), sticky="NEWS")

        

        # Database section
        self.database_grid_frame = tk.Frame(self.tab_databases)

        self.database_tree = ttk.Treeview(self.database_grid_frame, height = 6)
        self.database_tree["columns"]=["Name","Path"]
        self.database_tree.column("#0", width = 10, stretch = tk.YES)
        self.database_tree.column("#1", width = 100, stretch = tk.YES)
        self.database_tree.column("#2", width = 200, stretch = tk.YES)
        self.database_tree.heading("#0", text="",)
        self.database_tree.heading("#1", text="Name")
        self.database_tree.heading("#2", text="Path")
        self.database_tree.grid(row=0, column=0)

        self.database_tree_vsb = ttk.Scrollbar(self.database_grid_frame, orient="vertical", command=self.database_tree.yview)
        self.database_tree_vsb.grid(row=0, column=1, sticky="NEWS")
        self.database_tree_hsb = ttk.Scrollbar(self.database_grid_frame, orient="horizontal", command=self.database_tree.xview)
        self.database_tree_hsb.grid(row=1, column=0, sticky="NEWS")
        self.database_tree.configure(yscrollcommand=self.database_tree_vsb.set, xscrollcommand=self.database_tree_hsb.set)

        self.database_grid_frame.grid(row=0, column=0, padx=(2,2), pady=(2,2), sticky="NEWS")

        self.database_button_frame = tk.Frame(self.tab_databases)
        self.database_button_frame.grid(row=0, column=1, sticky="NEWS")

        self.database_add = tk.Button(self.database_button_frame, text="Add", command=self.add_database)
        self.database_remove = tk.Button(self.database_button_frame, text="Remove", command=self.remove_database)

        self.database_add.grid(row=0, column=0, padx=(5,5), pady=(2,2), sticky="NEWS")
        self.database_remove.grid(row=1, column=0, padx=(5,5), pady=(0,0), sticky="NEWS")

        self.refresh_databases_grid()

    def refresh_databases_grid(self):
        self.database_tree.delete(*self.database_tree.get_children())    
        if self.databases is not None:
            for i in range(len(self.databases)):
                database_row = self.databases.iloc[i]
                self.database_tree.insert("", i, i, values=(database_row["Name"], database_row["Path"]))

    def buttonbox(self):
        self.btn_close = tk.Button(self, text='Close', width=5, command=self.close_btn_clicked)
        self.btn_close.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_save = tk.Button(self, text='Save', width=5, command=self.save_btn_clicked)
        self.btn_save.pack(side="right", padx=(5,5), pady=(5,10))
        self.bind("<Return>", lambda event: self.save_btn_clicked())
        self.bind("<Escape>", lambda event: self.close_btn_clicked())

    def save_btn_clicked(self):
        self.decdp = self.val_decdp.get()
        self.defplot = self.plot_option_selected.get()
        self.submit = True
        self.destroy()

    def close_btn_clicked(self):
        self.destroy()
    
    def add_database(self):
        try:
            filepath = fd.askopenfilename()  
            if filepath:
                filename = os.path.split(filepath)[1]
                self.databases = self.databases.append({"Name": filename, "Path": filepath}, ignore_index=True)
                self.refresh_databases_grid()
        except IOError as ioerr:
            lg.log_error("Error (IO): {ioerr}")
        except Exception as err:
            lg.log_error(f"Error: {err}")

    def remove_database(self):
        focused_entry = self.database_tree.item(self.database_tree.focus())
        self.databases.drop(self.databases[self.databases["Name"] == focused_entry["values"][0]].index, inplace=True)
        self.refresh_databases_grid()