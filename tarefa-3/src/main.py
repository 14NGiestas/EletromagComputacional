from controller import LienardWiecherApp
from model.movements import harmonic_oscilator

if __name__ == "__main__":
    app = LienardWiecherApp(charge=1e-5, movement=harmonic_oscilator)
    app.run()
