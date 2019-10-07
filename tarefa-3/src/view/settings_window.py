try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3
    from tkinter import messagebox
    from tkinter import filedialog

class SettingsWindow(Tk.Toplevel):
    def __init__(self, root, settings):
        super().__init__(root)
        self.resizable(False, False)
        self.title("Settings")
        # Left Size
        self.left_side = Tk.Frame(self)
        self.left_side.grid(row=0, column=0)

        # Right Size
        self.right_side = Tk.Frame(self)
        self.right_side.grid(row=0, column=1)
        # Simulation Time
        self.label_time = Tk.Label(self.right_side, text="Simulation Time")
        self.label_time.grid(row=0)
        self.entry_time = Tk.Entry(self.right_side)
        self.entry_time.grid(row=1)
        # Simulation Step
        self.label_time_step = Tk.Label(self.right_side, text="Simulation Time Step")
        self.label_time_step.grid(row=2)
        self.entry_time_step = Tk.Entry(self.right_side)
        self.entry_time_step.grid(row=3)
        # Mesh Size Section
        self.label_mesh_size = Tk.Label(self.right_side, text="Mesh Size")
        self.label_mesh_size.grid(row=4)
        self.mesh_size_x = Tk.Entry(self.right_side)
        self.mesh_size_x.grid(row=5, column=0)
        self.mesh_size_y = Tk.Entry(self.right_side)
        self.mesh_size_y.grid(row=5, column=1)
        # Mesh Ticks Section
        self.label_mesh_ticks = Tk.Label(self.right_side, text="Mesh Ticks")
        self.label_mesh_ticks.grid(row=6)
        self.mesh_ticks_x = Tk.Entry(self.right_side)
        self.mesh_ticks_x.grid(row=7, column=0)
        self.mesh_ticks_y = Tk.Entry(self.right_side)
        self.mesh_ticks_y.grid(row=7, column=1)
        # Window Buttons
        self.confirm_button = Button(self, command=self.confirm)
        self.cancel_button = Button(self, command=self.cancel)
    
    def confirm(self):
        pass
