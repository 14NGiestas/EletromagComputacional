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
        def dBx(x, y, z, t):
            n = np.cos(t)*(z*self._stretch - t) + (y - np.sin(t))
            d = ((x - np.cos(t))**2 + (y - np.sin(t))**2 + (z - t / self._stretch)**2)**(3/2)
            return n / d

        def dBy(x, y, z, t):
            n = (x - np.cos(t)) + np.sin(t) * (z * self._stretch - t)
            d = ((x - np.cos(t))**2 + (y - np.sin(t))**2 + (z - t / self._stretch)**2)**(3/2)
            return n / d

        def dBz(x, y, z, t):
            n = - np.cos(t) * (x - np.cos(t)) - np.sin(t)*(y - np.sin(t))
            d = ((x - np.cos(t))**2 + (y - np.sin(t))**2 + (z - t / self._stretch)**2)**(3/2)
            return n / d

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

        h_axis = np.linspace(-1, 1, 20)

        H, V = np.meshgrid(h_axis, h_axis, indexing='xy')

        B = np.vectorize(simpson)

        l = self._turns

        self._results = {
            'H': H, 'V': V,
            'Bxy': (B(dBx, H, V, 0, l), B(dBy, H, V, 0, l)), 
            'Bzx': (B(dBz, V, 0, H, l), B(dBx, V, 0, H, l))
        }

    
    def feed(self, params):
        self._turns = params['turns'];
        self._stretch = params['stretch'];

