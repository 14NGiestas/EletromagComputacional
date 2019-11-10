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
        l = 5 # Number of Turns
        h = 0.5 # R / h - Stretch
        n = 1000 # Precision Simpson

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
                n = (2*pi*cos(2*pi*t)*(z-h*t) + h*(x - sin(2*pi*t)))
            elif axis == 'z':
                n = - 2*pi*sin(2*pi*t)*(y - sin(2*pi*t)) - 2*pi*cos(2*pi*t)*(x - cos(2*pi*t))
            return n / d

        n_axis = 10

        V = np.linspace(-2, 2, n_axis)
        H = np.linspace(-h*(l-1), -h, n_axis)

        Bz, Bx = np.meshgrid(H, V)

        for i in range(n_axis):
            for j in range(n_axis):
                Bz[i,j] = simpson(dB, 'z', V[i], 0, H[j])
                Bx[i,j] = simpson(dB, 'x', V[i], 0, H[j])

        self.results = {
            'hv': (H, V),
            'xz': (Bz,Bx),
        }

    def feed(self, params):
        self.turns = params['turns']
        self.stretch = params['stretch']
        self.view_mode = params['view_mode']

