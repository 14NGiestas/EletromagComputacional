import tkinter as Tk
from pubsub import pub
from model import HelicoidalSolenoid 
from view  import SolenoidView

from threading import Thread


class SolenoidApp:
    def __init__(self):
        self.model = HelicoidalSolenoid()
        self.view  = SolenoidView("Tarefa 4 - Campo magnetico em um solenoide")
        #self.view  = SolenoidView("Magnetic Field in Solenoid")
        # App Events 
        pub.subscribe(self.save_simulation, 'on_save')
        pub.subscribe(self.load_simulation, 'on_load')
        pub.subscribe(self.calculate_field, 'on_input')

    def calculate_field(self, params):
        ''' Feed the model with the input parameters and calculate ''' 
        self.model.feed(params)
        task = Thread(target=self.model.calculate)
        task.start()
        self.view.open_running(task)
        pub.sendMessage('update_view', results=self.model.results)

    def save_simulation(self):
        ''' Opens the view save file dialog '''
        self.view.save_dialog(results=self.model.results)

    def load_simulation(self):
        ''' Opens the view load file dialog '''
        self.view.load_dialog()

    def run(self):
        self.view.open()
