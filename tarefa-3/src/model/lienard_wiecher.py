from moving_charge import MovingCharge
from numpy import linspace, meshgrid

class LienardWiecherModel(MovingCharge):
    def __init__(self, charge, movement):
        super().__init__(charge, movement)

    def calculate(self):
        x_axis = linspace(-5, 5, self.x_ticks)
        y_axis = linspace(-5, 5, self.y_ticks)
        (x,y) = meshgrid(x_axis, y_axis)
        z = self.retarted_fields(x,y)
        return (x,y,z)

    @property
    def results(self):
        return self._results
