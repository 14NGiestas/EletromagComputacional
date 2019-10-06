try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3

from numpy import hypot
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from view.side_panel import SidePanel
plt.style.use('seaborn')

class LienardWiechertView:
    def __init__(self, root, model, figsize=(7.5, 4), dpi=80):
        self.main_frame = Tk.Frame(root)
        self.model = model
        # Plot Figure Widget
        self.figure = plt.Figure()
        self.axes = self.figure.add_axes((0.05, .05, .90, .90), facecolor=(.75, .75, .75), frameon=False)
        self.main_frame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        # UI Controls
        self.sidepanel = SidePanel(root)
        # UI Callbacks
        self.sidepanel.plot_button.bind("<Button>", self.plot)
        self.sidepanel.clear_button.bind("<Button>", self.clear)
        self.sidepanel.simulate_button.bind("<Button>",self.simulate)
        self.sidepanel.save_button.bind("<Button>",self.save)
        # Canvas setup
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas.draw()

    def clear(self, event):
        self.axes.clear()
        self.figure.clear()
        self.figure.canvas.draw()

    def plot(self, event):
        fig = self.axes.imshow(self.model.frames['electric_field'][0],vmin=0, vmax=0.001,cmap='Blues')
        self.figure.colorbar(fig)
        def animate(i):
            #self.axes.clear()
            #self.figure.clear()
            fig.set_array(self.model.frames['electric_field'][i-1])
        self.animation = FuncAnimation(self.figure,animate,interval=100,frames=len(self.model.frames['electric_field']))
        #self.axes.contourf(x,y,E)
        #self.axes.contourf(x,y,B)
        self.canvas.draw()

    def simulate(self,event):
        # 1 --> self.settings.simulation_time

        T = 1e-8
        while self.model.time <= T:
            self.model.calculate()
            self.model.step()
        messagebox.showinfo("Simulation", "Done!!")

    def save(self,event):
        if not self.animation:
             messagebox.showerror("Erro","Plot Primeiro!")
        self.main_frame.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Save file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.animation.save(self.main_frame.filename, writer='imagemagick')



