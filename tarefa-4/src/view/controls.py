import tkinter as Tk
from tkinter import Label, Scale
from pubsub import pub

class ControlPanel(Tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        # Simulation Input Sliders
        # * "density" $ n = \frac{h}{L} $
        # * * Density Label
        self.density_label = Label(self, text=u"Density (h/L)")
        self.density_label.pack(fill=Tk.BOTH)
        # * * Density Slider
        self.density_slider = Scale(self, from_=0, to=200, orient=Tk.HORIZONTAL)
        self.density_slider.bind('<ButtonRelease-1>', self.on_input)
        self.density_slider.pack(fill=Tk.BOTH)

        # * "aspect" $ a = \frac{R}{L} $ 
        # * * Aspect Label
        self.aspect_label = Label(self, text=u"Aspect (R/L)")
        self.aspect_label.pack(fill=Tk.BOTH)
        # * * Aspect Slider
        self.aspect_slider = Scale(self, from_=0, to=200, orient=Tk.HORIZONTAL)
        self.aspect_slider.bind('<ButtonRelease-1>', self.on_input)
        self.aspect_slider.pack(fill=Tk.BOTH)

        # Simulation Output Buttons
        # * Save Button
        self.save_button = Tk.Button(self, text=u"Save")
        self.save_button.bind('<Button>', self.on_save)
        self.save_button.pack(fill=Tk.BOTH)
        # * Load Button
        self.load_button = Tk.Button(self, text=u"Load")
        self.load_button.bind('<Button>', self.on_load)
        self.load_button.pack(fill=Tk.BOTH)

    def on_input(self, event):
        ''' Inform that the user changed some input '''
        pub.sendMessage('on_input', params=self.state)

    def on_save(self, event):
        ''' Inform that the user pressed the save button '''
        pub.sendMessage('on_save', params=self.state)

    def on_load(self, event):
        ''' Inform that the user pressed the load button '''
        pub.sendMessage('on_load')

    @property
    def state(self):
        density = self.density_slider.get()
        aspect  = self.aspect_slider.get()
        # ...
        return {
            'density': density,
            'aspect': aspect,
            # ...
        }

