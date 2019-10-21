
from pathlib import Path as path

import tkinter as Tk
from tkinter import messagebox
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from view.controls import ParamsPanel, ExportPanel

plt.style.use('seaborn')

ALLOWED_FILES = (
    ("Simulation Files", "*.sim"),
    ("All Files", "*.*")
)
USER_HOME = str(path.home())

class HelicoidalSolenoidView:
    def __init__(self, root):
        self.root = root
        self.main_frame = Tk.Frame(self.root)
        # Plot Figure Widget
        self.figure = Figure()
        self.axes = self.figure.add_axes((0.05, .05, .90, .90), frameon=False)
        self.main_frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        # UI Input
        self.params_panel = ParamsPanel(self.root)
        self.export_panel = ExportPanel(self.root)
        # Canvas setup
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas.draw()
    
    def save_dialog(self, results):
        ''' Opens a save dialog and save simulation results '''
        filename = filedialog.asksaveasfilename(initialdir=USER_HOME,
                                                filetypes=ALLOWED_FILES,
                                                title="Save simulation file")
        pass


    def load_dialog(self):
        ''' Opens a load dialog and parses the file, updating the view '''
        filename = filedialog.askopenasfilename(initialdir=USER_HOME,
                                                filetypes=ALLOWED_FILES,
                                                title="Load simulation file")
        pass
