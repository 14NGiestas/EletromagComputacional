from moving_charge import MovingCharge
from scipy.misc import derivative
from numpy import linspace, meshgrid

class LienardWiecherModel:
    def __init__(self, movement):
        self.charge = MovingCharge(movement)

    def calculate(self):
        x_axis = linspace(-5, 5, self.x_ticks)
        y_axis = linspace(-5, 5, self.y_ticks)
        (x,y) = meshgrid(x_axis, y_axis)
        z = self.charges.fields(x, y)
        return (x,y,z)

    @property
    def results(self):
        return self._results
