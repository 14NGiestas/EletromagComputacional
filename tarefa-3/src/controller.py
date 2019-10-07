import tkinter as Tk

from model import LienardWiechertModel
from view  import LienardWiechertView
import settings


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
