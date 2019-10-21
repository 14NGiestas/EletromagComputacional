import tkinter as Tk
from tkinter import Scale

class ParamsPanel(Tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        # Simulation Input Sliders
        # * "density"  $ n = \frac{h}{L} $
        self.density_slider = scale(root, from_=0, to=200, orient=Tk.HORIZONTAL)
        self.density_slider.bind('<buttonrelease-1>', self.on_input)
        self.density_slider.pack(fill=Tk.BOTH)
        # * "geometry" $   = \frac{R}{L} $ 
        # ..

    @property
    def state(self):
        density = self.density_slider.get()
        # ...
        return {
            'density': density,
            # ...

        }

    def on_input(self, event):
        # Gather user interface state 
        pub.sendMessage('on_input', data=self.state)


class ExportPanel(Tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        # Simulation Output Buttons
        # * Save Button
        self.save_button = Tk.Button(self, text=u"Save")
        self.load_button.bind('<Button>', self.on_save)
        self.save_button.pack(fill=Tk.BOTH)
        # * Load Button
        self.load_button = Tk.Button(self, text=u"Load")
        self.load_button.bind('<Button>', self.on_load)
        self.load_button.pack(fill=Tk.BOTH)

    def on_save(self, event):
        ''' Inform that the user pressed the save button '''
        pub.sendMessage('on_save')

    def on_load(self, event):
        ''' Inform that the user pressed the load button '''
        pub.sendMessage('on_load')
