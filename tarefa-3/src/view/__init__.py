try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3
    from tkinter import messagebox
    from tkinter import filedialog

from numpy import hypot
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib import pyplot as plt

from view.control_panel import ControlPanel 
from view.settings_window import SettingsWindow

plt.style.use('seaborn')

class LienardWiechertView:
    def __init__(self, root, model, settings):
        self.model = model
        self.settings = settings
        self.root = root
        self.main_frame = Tk.Frame(self.root)
        # Plot Figure Widget
        self.figure = Figure()
        self.axes = self.figure.add_axes((0.05, .05, .90, .90), frameon=False)
        self.main_frame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.animation = None
        # UI Controls
        self.control_panel = ControlPanel(self.root, self.settings)
        # UI Callbacks
        self.control_panel.play_button.bind("<Button>", self.play)
        self.control_panel.calc_button.bind("<Button>", self.calculate)
        self.control_panel.save_button.bind("<Button>", self.save)
        # Canvas setup
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas.draw()

    def play(self, event):
        if not self.animation:
             messagebox.showerror("Error", "Simulation not calculated")
             return

        play_pause = self.control_panel.play_button
        if play_pause['text'] == 'Play':
            play_pause.config(text='Pause')
        else:
            play_pause.config(text='Play')
        self.animation.paused = not self.animation.paused

    def calculate(self, event):
        self.settings.read(self.settings.filename)
        self.model.reset()
        time_total = self.settings['simulation'].getfloat('time_total')
        while self.model.time <= time_total:
            self.model.calculate()
            self.model.step()
        messagebox.showinfo("Success", "Simulation finished!")

        dataset = self.model.frames

        fig = self.axes.imshow(dataset[0], vmin=0, vmax=0.1, cmap='Blues')
        self.figure.colorbar(fig)

        def animation(i):
            if not self.animation.paused:
                fig.set_array(dataset[i-1])

        self.animation = FuncAnimation(self.figure, animation, interval=100, frames=len(dataset))
        self.animation.paused = True 
        self.canvas.draw()

    def save(self, event):
        if not self.animation:
             messagebox.showerror("Error", "Simulation not calculated")
             return

        filename = filedialog.asksaveasfilename(initialdir="/", title="Save file", filetypes=(("Animation Files","*.mp4"),("All files","*.*")))

        self.animation.save(filename, writer=FFMpegWriter(fps=10))
