try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3

import settings
from model import LienardWiechertModel
from view  import LienardWiechertView


class LienardWiechertApp(Tk.Tk):
    def __init__(self, configfile='settings.ini'):
        super().__init__()
        self.settings = settings
        self.model = LienardWiechertModel(self.settings)
        self.view  = LienardWiechertView(self, self.model, self.settings)

    def run(self):
        self.title("Tarefa 3 - Cargas em movimento")
        self.deiconify()
        self.mainloop()
