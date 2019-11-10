import numba as nb
import numpy as np
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
        n = 1000 # Precision Simpson

        @np.vectorize
        def simpson(f, axis, x, y, z):
            a = 0
            b = l
            h = (a-b) / n
            k = 0.0
            t = h

            for i in range(1, n//2 + 1):
                k += 4*f(x, y, z, t, axis)
                t += 2*h

            t = 2*h
            for i in range(1, n//2):
                k += 2*f(x, y, z, t, axis)
                t += 2*h

            return (h/3)*(f(x, y, z, a, axis)+f(x, y, z, b, axis)+k)

        def dB(x, y, z, t, axis):
            d = ((x - cos(2*pi*t))**2 + (y - np.sin(2*pi*t))**2 + (z - h*t)**2)**(3/2)

            if axis == 'x':
                n = 2*pi*cos(2*pi*t)*(z - h*t) - h*(y - sin(2*pi*t))
            elif axis == 'y':
                n = h*(x - cos(2*pi*t)) + 2*pi*sin(2*pi*t)*(z - h*t)
                #n = (x - np.cos(t)) + np.sin(t) * (z*k - t)
            elif axis == 'z':
                n = - 2*pi*sin(2*pi*t)*(y - sin(2*pi*t)) - 2*pi*cos(2*pi*t)*(x - cos(2*pi*t))
                #n = - np.cos(t) * (x - np.cos(t)) - np.sin(t) * (y - np.sin(t))

            return n / d

        n_axis = 15

        if self.view_mode == 'xy':
            x = np.linspace(-2, 2, n_axis)
            y = np.linspace(-2, 2, n_axis)

            X, Y = np.meshgrid(x, y, indexing='xy')

            Bx = -simpson(dB, 'x', -X, -Y, 0)
            By = -simpson(dB, 'y', -X, -Y, 0)

            self.results = {
                'HV': (X, Y),
                'Bhv': (Bx, By)
            }
        elif self.view_mode == 'yz':
            y = np.linspace(-2, 2, n_axis)
            z = np.linspace(-1, 1 + h*l, n_axis)

            Y, Z = np.meshgrid(y, z, indexing='xy')

            By = -simpson(dB, 'y', 0, -Y, -Z)
            Bz = -simpson(dB, 'z', 0, -Y, -Z)

            self.results = {
                'HV': (Y, Z),
                'Bhv': (By, Bz)
            }

    def feed(self, params):
        self.turns = params['turns']
        self.stretch = params['stretch']
        self.view_mode = params['view_mode']

