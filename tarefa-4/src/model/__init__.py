import numba as nb
import numpy as np
from numpy import cos, sin, pi

class HelicoidalSolenoid:
    def __init__(self):
        self.turns = 0
        self.stretch = 0
        self.results = {}

    '''
    def calculate(self):

        h = self.stretch
        l = self.turns

        @nb.njit
        def dBx(x,y,z,t):
          return 2*pi*cos(2*pi*t)*(z - h*t) - h*(y - sin(2*pi*t)) \
                 / ((x - cos(2*pi*t))**2 + (y - sin(2*pi*t))**2 + (z - h*t)**2)**(3/2)

        @nb.njit
        def dBy(x,y,z,t):
            return (2*pi*cos(2*pi*t)*(z-h*t) + h*(x - sin(2*pi*t))) \
                   / ((x - cos(2*pi*t))**2 + (y - sin(2*pi*t))**2 + (z - h*t)**2)**(3/2)

        @nb.njit
        def dBz(x,y,z,t):
            return - 2*pi*sin(2*pi*t)*(y - sin(2*pi*t)) - 2*pi*cos(2*pi*t)*(x - cos(2*pi*t)) \
                   / ((x - cos(2*pi*t))**2 + (y - sin(2*pi*t))**2 + (z - h*t)**2)**(3/2)

        def integrate(f, x, y, z, b):
            @nb.vectorize
            def simpson(x, y, z, b):
                n = 1000
                h = b / n
                k = 0.0
                t = h

                for i in range(1, n//2 + 1):
                    k += 4*f(x,y,z,i)
                    t += 2*h

                t = 2*h
                for i in range(1, n//2):
                    k += 2*f(x,y,z,t)
                    t += 2*h

                return (h/3)*(f(x,y,z,0)+f(x,y,z,b)+k) 
            return simpson(x,y,z,b)

        h_axis = np.linspace(-2, 2, 100)
        v_axis = np.linspace(-h*(l-1), -h, 100)

        H, V = np.meshgrid(h_axis, v_axis)

        Bz = integrate(dBz, H, 0, V, l)
        Bx = integrate(dBx, H, 0, V, l)

        self.results = {
            'hv': (H, V),
            'xz': (Bx, Bz),
        }
    '''
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
        self.turns = params['turns'];
        self.stretch = params['stretch'];

