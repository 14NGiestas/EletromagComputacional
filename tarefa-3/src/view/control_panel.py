try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3


class ControlPanel(Tk.Frame):
    def __init__(self, root, settings):
        super().__init__(root)
        self.pack(side=Tk.BOTTOM, fill=Tk.BOTH)
        time_total = settings['simulation'].getfloat('time_total')
        time_step = settings['simulation'].getfloat('time_step')
        # Save Button
        self.save_button = Tk.Button(self, text=u"Save")
        self.save_button.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        # Calculate Button
        self.calc_button= Tk.Button(self, text=u"Calc.")
        self.calc_button.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        # Play Button
        self.play_button = Tk.Button(self, text="Play")
        self.play_button.pack(side=Tk.RIGHT, fill=Tk.BOTH)
