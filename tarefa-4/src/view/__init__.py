import tkinter as Tk
from tkinter import messagebox, filedialog, Toplevel, Message

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from numpy import hypot, log, pi, cos, sin, linspace

from pubsub import pub
from pathlib import Path as path

from view.controls import ControlPanel 

ALLOWED_FILES = (
    ("Simulation Files", "*.svg"),
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

    def update_view(self, results):
        H,  V  = results['HV'][0], results['HV'][1]
        Bh, Bv = results["Bhv"]

        self.axes.clear()
        self.canvas.draw()
        
        view_mode = self.control_panel.state['view_mode']

        if view_mode == 'yz':
            self.axes.set_aspect('auto')
            c = 2 * log(hypot(Bh, Bv))
            self.axes.streamplot(H, V, Bh, Bv, color=c, cmap='viridis', density=1.5)
        
            l = self.control_panel.state['turns']
            h = self.control_panel.state['stretch']

            ptsY = [h * (i/2 + 1/4) for i in range(2*l)]
            ptsX = [(-1)**(i) for i in range(2*l)]
            self.axes.plot(ptsX, ptsY, 'o', markersize=7, markerfacecolor='w', markeredgewidth=1.5, markeredgecolor=(0, 0, 0, 1))
        elif view_mode == 'xy':
            self.axes.set_aspect('equal')
            self.axes.streamplot(H, V, Bh, Bv, cmap='viridis', density=1.5)
            t_int = linspace(0, 1, 100)
            self.axes.plot(cos(2*pi*t_int), sin(2*pi*t_int), color='black')
        
        self.canvas.draw()

    def save_dialog(self):
        ''' Opens a save dialog and save simulation results in a file '''
        filename = filedialog.asksaveasfilename(initialdir=USER_HOME,
                                                filetypes=ALLOWED_FILES,
                                                title="Save simulation file")
        self.figure.savefig(filename)

    def open_running(self, task):
        ''' Displays a message while running the simulation '''
        popup = Toplevel(self)
        x = self.winfo_x()
        y = self.winfo_y()
        popup.geometry("+%d+%d" % (x//2, y//2))
        popup.title("Running")
        msg = Message(popup, text="Running simulation. Please Wait.")
        msg.pack()
        while task.is_alive():
            popup.update()
        popup.destroy() # only when thread dies.
    
    def open(self):
        self.mainloop()
