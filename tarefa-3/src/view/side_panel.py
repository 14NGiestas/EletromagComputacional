try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3


class SidePanel:
    def __init__(self, root):
        self.panel = Tk.Frame(root)
        self.panel.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        # Button to start plotting the animation
        self.plot_button = Tk.Button(self.panel, text="")
        self.plot_button.pack(side="top", fill=Tk.BOTH)
        # Button 
        self.clear_button = Tk.Button(self.frame2, text="Clear")
        self.clear_button.pack(side="top", fill=Tk.BOTH)

