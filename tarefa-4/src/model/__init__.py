import numpy as np

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
            n = np.cos(t)*(z*self._stretch - t) - (y - np.sin(t))
            d = ((x - np.cos(t))**2 + (y - np.sin(t))**2 + (z - t / self._stretch)**2)**(3/2)
            return n / d

        def dBy(x, y, z, t):
            n = (x - np.cos(t)) + np.sin(t) * (z * self._stretch - t)
            d = ((x - np.cos(t))**2 + (y - np.sin(t))**2 + (z - t / self._stretch)**2)**(3/2)
            return n / d

        def dBz(x, y, z, t):
            n = -np.cos(t) * (x - np.cos(t)) + np.sin(t)*(y - np.sin(t))
            d = ((x - np.cos(t))**2 + (y - np.sin(t))**2 + (z - t / self._stretch)**2)**(3/2)
            return n / d

        h_axis = np.linspace(-1, 1, 10)

        X, Y = np.meshgrid(h_axis, h_axis, indexing='xy')
        Z, X = np.meshgrid(h_axis, h_axis, indexing='xy')

        B = np.vectorize(self.simpson, excluded=['self'])

        self._results = {
            'xy': (B(dBx, X, Y, 0), B(dBy, X, Y, 0)), 
            'xz': (B(dBz, X, 0, Z), B(dBx, X, 0, Z))
        }
        
    def simpson(self, f, x, y, z, n=1000):
        a = 0
        b = self._turns
        h = (b - a) / n
        k = 0.0
        t = a + h

        for i in range(1,n//2 + 1):
            k += 4*f(x, y, z, t)
            t += 2*h

        t = a + 2*h
        for i in range(1,n//2):
            k += 2*f(x, y, z, t)
            t += 2*h

        return (h/3)*(f(x, y, z, a)+f(x, y, z, b)+k)    
    
    def feed(self, params):
        self._turns = params['turns'];
        self._stretch = params['stretch'];

