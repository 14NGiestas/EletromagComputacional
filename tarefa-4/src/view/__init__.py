import tkinter as Tk
from tkinter import messagebox, filedialog, Toplevel, Message

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from numpy import hypot, log

from pubsub import pub
from pathlib import Path as path

from view.controls import ControlPanel 

ALLOWED_FILES = (
    ("Simulation Files", "*.sim"),
    ("All Files", "*.*")
)

USER_HOME = str(path.home())

class SolenoidView(Tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.deiconify()
        self.title(title)
        # UI Control Panel
        self.control_panel = ControlPanel(self)
        # UI Plot Widget
        # * Matplotlib Figure
        self.figure = Figure()
        self.axes = self.figure.add_axes((0.05, .05, .90, .90))
        # * Canvas Widget
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.canvas.draw()
        # UI Events
        pub.subscribe(self.update_view, 'update_view')
        pub.subscribe(self.save_dialog, 'save_dialog')
        pub.subscribe(self.load_dialog, 'load_dialog')

    def update_view(self, results):
        ''' Update the window view using given results and params '''

        self.axes.clear()
        self.canvas.draw()

        H,  V  = results['hv'][0], results['hv'][1]
        Bh, Bv = results["xz"]

        c = 2 * log(hypot(Bh, Bv))
        self.axes.streamplot(-H, V, Bh, Bv, color=c, cmap='inferno', density=1.5)

        self.canvas.draw()

    def save_dialog(self, results):
        ''' Opens a save dialog and save simulation results in a file '''
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

    def open_running(self, task):
        popup = Toplevel(self)
        popup.title("Running")
        msg = Message(popup, text="Running simulation. Please Wait.")
        msg.pack()
        while task.is_alive():
            popup.update()
        popup.destroy() # only when thread dies.
    
    def open(self):
        self.mainloop()
