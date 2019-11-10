import tkinter as Tk
from tkinter import messagebox
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

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
        self.axes = self.figure.add_axes((0.05, .05, .90, .90), projection='3d')
        #self.axes = self.figure.add_axes((0.05, .05, .90, .90))
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
        import numpy as np
        X,  Y,  Z  = results['X'],  results['Y'],  results['Z']
        Bx, By, Bz = results['Bx'], results['By'], results['Bz']
        B = np.sqrt(Bx**2 + By**2 + Bz**2)

        self.axes.clear()
        self.canvas.draw()

        #self.axes.contourf(X[:,:,0], Y[:,:,0], B[:,:,0]) 
        #self.axes.contourf(X[:,:,0], Z[:,:,0], B[:,:,0]) 
        self.axes.quiver(X, Y, Z, Bx, By, Bz, length=1, color='k') 
        #self.axes.streamplot(X[:,:,0], Y[:,:,0], Bx[:,:,0], By[:,:,0])
        #self.axes.streamplot(X[:,:,0], Z[:,:,0], Bx[:,:,0], Bz[:,0,:])

        l = self.control_panel.state['turns']
        s = self.control_panel.state['stretch']
        t = np.linspace(0, l, 1000)
        x = s*np.cos(t)
        y = s*np.sin(t)
        z = t
        self.axes.plot(x,y,z, 'r', lw=2)

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
    
    def open(self):
        self.mainloop()
