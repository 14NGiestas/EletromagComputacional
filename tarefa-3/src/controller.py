try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3

from model import LienardWiecherModel
from view import LienardWiecherView


class LienardWiecherApp:
    def __init__(self, charge, movement):
        self.root  = Tk.Tk() 
        self.model = LienardWiecherModel(charge, movement)
        self.view  = LienardWiecherView(self.root, self.model)

    def run(self):
        self.root.title("Tarefa 3 - Cargas em movimento")
        self.root.deiconify()
        self.root.mainloop()

