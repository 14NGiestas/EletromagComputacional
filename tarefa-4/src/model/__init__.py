import numpy as np
import numba as nb

class HelicoidalSolenoid:
    def __init__(self):
        self._results = None
        self._turns = 0
        self._stretch = 0

    @property
    def results(self):
        return self._results
    
    def calculate(self):

        s = self._stretch
        l = self._turns

        def dBx(x, y, z, t):
            n = np.cos(t)*(z*self._stretch - t) + (y - np.sin(t))
            d = ((x - np.cos(t))**2 + (y - np.sin(t))**2 + (z - t/s)**2)**(3/2)
            return n / d

        def dBy(x, y, z, t):
            n = (x - np.cos(t)) + np.sin(t) * (z *  - t)
            d = ((x - np.cos(t))**2 + (y - np.sin(t))**2 + (z - t/s)**2)**(3/2)
            return n / d

        def dBz(x, y, z, t):
            n = - np.cos(t) * (x - np.cos(t)) - np.sin(t)*(y - np.sin(t))
            d = ((x - np.cos(t))**2 + (y - np.sin(t))**2 + (z - t/s)**2)**(3/2)
            return n / d

        @np.vectorize
        def simpson(f, x, y, z, b):
            n = 1000
            h = b / n
            k = 0.0
            t = h

            for i in range(1, n//2 + 1):
                k += 4*f(x, y, z, t)
                t += 2*h

            t = 2*h
            for i in range(1, n//2):
                k += 2*f(x, y, z, t)
                t += 2*h

            return (h/3)*(f(x, y, z, 0)+f(x, y, z, b)+k)    

        x_axis = np.linspace(-10, 10, 10)
        y_axis = np.linspace(-10, 10, 10)
        z_axis = np.linspace(-10, 10, 1)

        X, Y, Z = np.meshgrid(x_axis, y_axis, z_axis, indexing='xy')

        Bx = simpson(dBx, X, Y, Z, l)
        By = simpson(dBx, X, Y, Z, l)
        Bz = simpson(dBx, X, Y, Z, l)

        self._results = {
            'X': X,
            'Y': Y,
            'Z': Z,
            'Bx': Bx,
            'By': By, 
            'Bz': Bz 
        }

    
    def feed(self, params):
        self._turns = params['turns'];
        self._stretch = params['stretch'];

