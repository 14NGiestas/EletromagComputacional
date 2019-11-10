import tkinter as Tk
from tkinter import Label, Scale, Button
from pubsub import pub

class ControlPanel(Tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH)

        # * $ Turns: l = \frac{L}{p} $
        # * * Label
        self.turns_label = Label(self, text=u"Turns (l = 2πL/h)")
        self.turns_label.pack(fill=Tk.BOTH)
        # * * Slider
        self.turns_slider = Scale(self, from_=0.01, to=100, resolution=0.01, orient=Tk.HORIZONTAL)
        self.turns_slider.bind('<ButtonRelease-1>', self.on_input)
        self.turns_slider.pack(fill=Tk.BOTH)

        # * $ Strech: s  = \frac{R}{p} $ 
        # * * Label
        self.stretch_label = Label(self, text=u"Stretch (s = 2πR/h)")
        self.stretch_label.pack(fill=Tk.BOTH)
        # * * Slider
        self.stretch_slider = Scale(self, from_=0.01, to=10, resolution=0.01, orient=Tk.HORIZONTAL)
        self.stretch_slider.bind('<ButtonRelease-1>', self.on_input)
        self.stretch_slider.pack(fill=Tk.BOTH)

        # Simulation Output Buttons
        # * Save Button
        self.save_button = Button(self, text=u"Save")
        self.save_button.bind('<Button>', self.on_save)
        self.save_button.pack(fill=Tk.BOTH)
        # * Load Button
        self.load_button = Button(self, text=u"Load")
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
        turns    = self.turns_slider.get()
        stretch  = self.stretch_slider.get()
        return {
            'turns':   turns,
            'stretch': stretch,
        }
