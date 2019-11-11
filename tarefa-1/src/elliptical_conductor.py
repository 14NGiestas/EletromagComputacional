import numpy as np
from random import uniform, choice

zero = 1e-5

class EllipticalConductor:
    def __init__(self, a, b):
        self.axis = (a, b)
        self.charges = []

    def fill(self, N):
        self.charges = []
        n = 0;

        while(n < N):
            pos = [uniform(-r, r) for r in list(self.axis)]
            if self.contains(pos):
                self.charges.append(pos)
                n += 1

    def contains(self, pos):
        (x, y) = pos
        (a, b) = self.axis
        return x**2 / a**2 + y**2 / b**2 <= 1

    def energy_variation(self, i, new_pos, dim=2):
        E_old = 0
        E_new = 0
        (x0, y0) = self.charges[i]
        (xf, yf) = new_pos
        N = len(self.charges)

        if not (abs(xf - x0) < zero and abs(yf - y0) < zero): 
            for j in range(N):
                if j != i:
                    # Distance
                    pos = self.charges[j]
                    d0 = np.sqrt((pos[0] - x0)**2 + (pos[1] - y0)**2)
                    df = np.sqrt((pos[0] - xf)**2 + (pos[1] - yf)**2)

                    # Energy
                    if dim == 2:
                        E_old -= np.log(d0)
                        E_new -= np.log(df)
                    elif dim == 3:

                        E_old += 1 / d0
                        E_new += 1 / df

        return E_new - E_old

    def move_charge(self, i, dim=2, biased=False, assy=0.1):
        old_pos = self.charges[i].copy()
        new_pos = old_pos.copy()
        delta = np.array(self.axis) / 100

        for j in range(2):
            if biased:
                bias = old_pos[j] / self.axis[0]
                w = (1/3) + assy * np.array([bias, 0, -bias]) * (-1)**(j)
                new_pos[j] += delta[j] * int(np.random.choice([1, 0,-1], 1, p=w)[0])
            else:
                new_pos[j] += delta[j] * np.random.choice([1, 0, -1], 1)[0]

        dE = self.energy_variation(i, new_pos, dim)

        if self.contains(new_pos) and dE < zero:
            self.charges[i] = new_pos

        return dE
