
class Inductor:
    def __init__(self, L):
        self.inductance = L

    @property
    def dependency(self):
        L = self.inductance
        return lambda Q: L*derivative(Q,2)


class Resistor:
    def __init__(self, R):
        self.resistance = R

    @property
    def dependency(self):
        R = self.resistance
        return lambda Q: R*derivative(Q,1) 


class Capacitor:
    def __init__(self, C):
        self.capacitance = C

    @property
    def dependency(self):
        C = self.capacitance
        return lambda Q: Q/C
