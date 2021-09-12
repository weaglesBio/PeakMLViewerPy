import tkinter as tk
from UI.ViewerDialog import ViewerDialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

#https://github.com/yuma-m/matplotlib-draggable-plot/blob/master/draggable_plot.py

class SortTimeSeriesDialog(ViewerDialog):
    def __init__(self, parent, title, sets):
        self.sets = sets
        self.submit = False
        super().__init__(parent, title, width=600, height=720, take_focus=True, extendable=True)

    def body(self, frame):

        self._containing_frame = tk.Frame(frame, padx=5, pady=5)
        self._containing_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        # Option frame

        self._options_frame = tk.LabelFrame(self._containing_frame, padx=0, pady=0, text="Preset")
        self._options_frame.pack(fill=tk.BOTH, expand = tk.FALSE)

        self.option_set_selected = tk.StringVar(self._options_frame)
        self.option_set_selected.set(self.sets[0])

        self.lbl_set_select = tk.Label(self._options_frame, width=10, text = "Set associated:")

        self.option_set_select = tk.OptionMenu(self._options_frame, self.option_set_selected, *self.sets)

        self.btn_apply = tk.Button(self._options_frame, text='Apply', width=5, command=self.apply_layout)

        self.lbl_set_select.grid(row=0, column=0, padx=(5,5), pady=(2,2), sticky="NEWS")
        self.option_set_select.grid(row=0, column=1, padx=(5,5), pady=(2,2), sticky="NEWS")
        self.btn_apply.grid(row=0, column=2, padx=(5,5), pady=(2,2), sticky="NEWS")

        # Figure frame

        self._figure_frame = tk.Frame(self._containing_frame, padx=10, pady=10)
        self._figure_frame.pack(fill=tk.BOTH, expand = tk.TRUE)

        self._figure, self._axes, self._line = None, None, None
        self._dragging_point = None
        self._points = {}

        self._figure = plt.Figure(figsize=(6,5))

        self._figure.canvas.mpl_connect('button_press_event', self._on_click)
        self._figure.canvas.mpl_connect('button_release_event', self._on_release)
        self._figure.canvas.mpl_connect('motion_notify_event', self._on_motion)

        self._axes = self._figure.add_subplot(111)

        self._axes.set_xlabel("Set")
        self._axes.set_ylabel("Intensity")

        # Rotate labels so do overlap
        for tick in self._axes.get_xticklabels():
            tick.set_rotation(305)

        self._axes.set_ylim(0,1)

        for set in self.sets:
            self._add_point(set, 0.5)

        self._update_plot()
        
        canvas = FigureCanvasTkAgg(self._figure, self._figure_frame)
        canvas.get_tk_widget().pack(side="top", fill ='both', expand=True)
        canvas.draw()

        self._figure.tight_layout()

    def buttonbox(self):
        self.btn_cancel = tk.Button(self, text='Cancel', width=5, command=self.cancel_btn_clicked)
        self.btn_cancel.pack(side="right", padx=(5,10), pady=(5,10))
        self.btn_ok = tk.Button(self, text='OK', width=5, command=self.ok_btn_clicked)
        self.btn_ok.pack(side="right", padx=(5,10), pady=(5,10))
        self.bind("<Return>", lambda event: self.ok_btn_clicked())
        self.bind("<Escape>", lambda event: self.cancel_btn_clicked())

    def ok_btn_clicked(self):
        self.set_values = self._read_values_from_points()
        self.submit = True
        self.destroy()

    def cancel_btn_clicked(self):
        self.destroy()

    def _read_values_from_points(self):

        set_values = []
        for set in self.sets:
            set_values.append(self._points[set])

        return set_values

    def _update_plot(self):

        x, y = zip(*sorted(self._points.items()))

        if not self._line:
            self._line, = self._axes.plot(x, y, "b", marker="o", markersize=10)
        else:
            self._line.set_data(x, y)

        self._figure.tight_layout()

        self._figure.canvas.draw()


    def _add_point(self, x, y):

        self._points[x] = y

        return x, y

    def _remove_point(self, x, _):

        if x in self._points:
            self._points.pop(x)

    def _find_nearest_point(self, event):

        # Find nearest point along the x axis
        for x, y in self._points.items():

            if x == self.sets[round(event.xdata)]:
                return (x, y)

        return None

    def _on_click(self, event):

        # On click within range of plot
        if event.button == 1 and event.inaxes in [self._axes]:

            # Get nearest point to coordinates of click
            point = self._find_nearest_point(event)

            # Add this to dragging point.
            if point:
                self._dragging_point = point

    def _on_release(self, event):

        # On click within range of plot and dragging point selected.
        if event.button == 1 and event.inaxes in [self._axes] and self._dragging_point:

            # Prevent movement out the line of the draggable point
            self._add_point(self._dragging_point[0], event.ydata)
            self._dragging_point = None
            self._update_plot()

    def _on_motion(self, event):

        # If dragging point selected.
        if not self._dragging_point:
            return

        if event.ydata:

            self._remove_point(*self._dragging_point)

            if event.ydata > 1:
                y = 1
            elif event.ydata < 0:
                y = 0
            else:
                y = event.ydata

            # Prevent movement out the line of the draggable point
            self._dragging_point = self._add_point(self._dragging_point[0], y)
            self._update_plot()  

    def apply_layout(self):

        # Clear all current points
        self._points = {}

        for set_name in self.sets:
            self._add_point(set_name, 1 if self.option_set_selected.get() == set_name else 0)

        self._update_plot()