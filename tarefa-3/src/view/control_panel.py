try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3


class ControlPanel(Tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(side=Tk.BOTTOM, fill=Tk.BOTH)
        # Slider
        self.slider = Tk.Scale(self,
                               from_=0, to=100,
                               resolution=0.01, 
                               orient=Tk.HORIZONTAL)
        self.slider.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        # Save Button
        self.save_button = Tk.Button(self, text=u"Save")
        self.save_button.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        # Calculate Button
        self.calc_button= Tk.Button(self, text=u"Calc.")
        self.calc_button.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        # Stop Button
        self.stop_button = Tk.Button(self, text="Stop")
        self.stop_button.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        # Play Button
        self.play_button = Tk.Button(self, text="Play")
        self.play_button.pack(side=Tk.RIGHT, fill=Tk.BOTH)
