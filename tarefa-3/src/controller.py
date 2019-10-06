try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3

from model import LienardWiechertModel
from view  import LienardWiechertView


class LienardWiechertApp:
    def __init__(self):
        self.root  = Tk.Tk() 
        self.model = LienardWiechertModel()
        self.view  = LienardWiechertView(self.root, self.model)
    
    def run(self):
        self.root.title("Tarefa 3 - Cargas em movimento")
        self.root.deiconify()
        self.root.mainloop()

