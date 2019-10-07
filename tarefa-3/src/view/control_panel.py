import tkinter as Tk

class ControlPanel(Tk.Frame):
    def __init__(self, root, settings):
        super().__init__(root)
        self.pack(side=Tk.RIGHT, fill=Tk.BOTH)
        time_total = settings.time_total
        time_step  = settings.time_step
        # Save Button
        self.save_button = Tk.Button(self, text=u"Save")
        self.save_button.pack(fill=Tk.BOTH)
        # Calculate Button
        self.calc_button= Tk.Button(self, text=u"Calculate")
        self.calc_button.pack(fill=Tk.BOTH)
        # Play Button
        self.play_button = Tk.Button(self, text="Play")
        self.play_button.pack(fill=Tk.BOTH)
