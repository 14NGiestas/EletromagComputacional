from controller import LienardWiechertApp
from model.movements import harmonic_oscilator

if __name__ == "__main__":
    app = LienardWiechertApp(movement=harmonic_oscilator)
    app.run()
