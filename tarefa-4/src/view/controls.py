import tkinter as Tk
from tkinter import Label, Scale, Button, Radiobutton, StringVar
from pubsub import pub

class ControlPanel(Tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH)

        # * $ Turns: l = \frac{L}{p} $
        # * * Label
        self.turns_label = Label(self, text=u"Turns (L)")
        self.turns_label.pack(fill=Tk.BOTH)
        # * * Slider
        self.turns_slider = Scale(self, from_=1, to=10, resolution=1, orient=Tk.HORIZONTAL)
        self.turns_slider.pack(fill=Tk.BOTH)

        # * $ Strech: s  = \frac{R}{p} $ 
        # * * Label
        self.stretch_label = Label(self, text=u"Stretch (h/R)")
        self.stretch_label.pack(fill=Tk.BOTH)
        # * * Slider
        self.stretch_slider = Scale(self, from_=0, to=2, resolution=0.01, orient=Tk.HORIZONTAL)
        self.stretch_slider.pack(fill=Tk.BOTH)

        # Simulation View Mode
        self.view_mode = StringVar()

        view_xy = Radiobutton(self, text="View XY", variable=self.view_mode, value='xy')
        view_xy.pack(fill=Tk.BOTH)
        
        view_yz = Radiobutton(self, text="View YZ", variable=self.view_mode, value='yz')
        view_yz.pack(fill=Tk.BOTH)

        # Simulation Output Buttons
        self.calc_button = Button(self, text=u"Calculate")
        self.calc_button.bind('<Button>', self.on_input)
        self.calc_button.pack(fill=Tk.BOTH)
        # * Save Button
        self.save_button = Button(self, text=u"Save")
        self.save_button.bind('<Button>', self.on_save)
        self.save_button.pack(fill=Tk.BOTH)

        self.turns_slider.set(5)
        self.stretch_slider.set(0.5)
        self.view_mode.set('xy')

    def on_input(self, event):
        ''' Inform that the user changed some input '''
        pub.sendMessage('on_input', params=self.state)

    def on_save(self, event):
        ''' Inform that the user pressed the save button '''
        pub.sendMessage('on_save')

    @property
    def state(self):
        turns    = self.turns_slider.get()
        stretch  = self.stretch_slider.get()
        view_mode = self.view_mode.get()

        return {
            'turns':   turns,
            'stretch': stretch,
            'view_mode': view_mode 
        }
