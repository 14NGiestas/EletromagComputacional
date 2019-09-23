try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3

import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from side_panel import SidePanel


class View:
    def __init__(self, root, model, figsize=(7.5, 4), dpi=80):
        self.main_frame = Tk.Frame(root)
        self.model = model
        # Setup of plotting figure
        self.figure = Figure(figsize, dpi)
        self.axes = self.figure.add_axes((0.05, .05, .90, .90), facecolor=(.75, .75, .75), frameon=False)
        self.main_frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        # UI Controls
        self.sidepanel = SidePanel(root)
        # UI Callbacks
        self.sidepanel.plot_button.bind("<Button>", self.plot)
        self.sidepanel.clean_button.bind("<Button>", self.clear)
        # Canvas setup
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas.show()

    def clear(self, event):
        self.axes.clear()
        self.figure.canvas.draw()

    def plot(self, event):
        self.model.calculate()
        results = self.model.results()

        self.axis.clear()
        self.axis.contourf(results["x"], results["y"], results["z"])
        self.figure.canvas.draw()

