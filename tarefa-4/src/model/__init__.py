import numba as nb
import numpy as np
from numba import float64
from numpy import cos, sin, pi

class HelicoidalSolenoid:
    def __init__(self):
        self.turns = 0
        self.stretch = 0
        self.results = {}

    def calculate(self):
        # Parameters
        l = self.turns # Number of Turns
        h = self.stretch # R / h - Stretch
        n = 2000 # Precision Simpson

        def integrate(x, y, z, axis):
            def simpson(f, x, y, z):
                a = 0
                b = l
                h = (a-b) / n
                k = 0.0
                t = h

                for i in range(1, n//2 + 1):
                    k += 4*f(x, y, z, t)
                    t += 2*h

                t = 2*h
                for i in range(1, n//2):
                    k += 2*f(x, y, z, t)
                    t += 2*h

                return (h/3)*(f(x, y, z, a)+f(x, y, z, b)+k)

            if axis == 'x':
                @nb.vectorize
                def dBx(x,y,z,t):
                    d = ((x - cos(2*pi*t))**2 + (y - np.sin(2*pi*t))**2 + (z - h*t)**2)**(3/2)
                    n = 2*pi*cos(2*pi*t)*(z - h*t) - h*(y - sin(2*pi*t))
                    return n / d
                return simpson(dBx, x, y, z)
            elif axis == 'y':
                @nb.vectorize
                def dBy(x,y,z,t):
                    d = ((x - cos(2*pi*t))**2 + (y - np.sin(2*pi*t))**2 + (z - h*t)**2)**(3/2)
                    n = h*(x - cos(2*pi*t)) + 2*pi*sin(2*pi*t)*(z - h*t)
                    return n / d
                return simpson(dBy, x, y, z)
            elif axis == 'z':
                @nb.vectorize
                def dBz(x,y,z,t):
                    d = ((x - cos(2*pi*t))**2 + (y - np.sin(2*pi*t))**2 + (z - h*t)**2)**(3/2)
                    n = - 2*pi*sin(2*pi*t)*(y - sin(2*pi*t)) - 2*pi*cos(2*pi*t)*(x - cos(2*pi*t))
                    return n / d
                return simpson(dBz, x, y, z)

        n_axis = 20

        if self.view_mode == 'xy':
            x = np.linspace(-2, 2, n_axis)
            y = np.linspace(-2, 2, n_axis)

            X, Y = np.meshgrid(x, y, indexing='xy')

            Bx = -integrate(-X, -Y, 0, 'x')
            By = -integrate(-X, -Y, 0, 'y')

            self.results = {
                'HV': (X, Y),
                'Bhv': (Bx, By)
            }
        elif self.view_mode == 'yz' or self.view_mode == 'inf':
            y = np.linspace(-2, 2, n_axis)
            z = np.linspace(-1, 1 + h*l, n_axis)

            Y, Z = np.meshgrid(y, z, indexing='xy')

            By = -integrate(0, -Y, -Z, 'y')
            Bz = -integrate(0, -Y, -Z, 'z')

            self.results = {
                'HV': (Y, Z),
                'Bhv': (By, Bz)
            }

    def feed(self, params):
        self.turns = params['turns']
        self.stretch = params['stretch']
        self.view_mode = params['view_mode']

