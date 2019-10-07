from numpy import sin, cos, exp, pi

class SimpleHarmonicOscilator:
    def __init__(self, settings):
        self.frequency = settings.frequency
        self.amplitude = settings.amplitude
        self.phase     = settings.phase

    def position(self, t):
        omega, A, phi = self.frequency, self.amplitude, self.phase
        return A*cos(omega*t + phi)

    def velocity(self, t):
        omega, A, phi = self.frequency, self.amplitude, self.phase
        return -A*omega*sin(omega*t + phi)

    def aceleration(self, t): 
        omega, A, phi = self.frequency, self.amplitude, self.phase
        return -A*omega**2*cos(omega*t + phi)

class Pulse:
    def __init__(self, settings):
        self.frequency = settings.frequency
        self.amplitude = settings.amplitude
        self.phase     = settings.phase

    def position(self, t):
        if t > 1e-9:
            return 0
        else: 
            omega, A, phi = self.frequency, self.amplitude, self.phase
            return A*cos(omega*t + phi)

    def velocity(self, t):
        if t > 1e-9:
            return 0
        else:
            omega, A, phi = self.frequency, self.amplitude, self.phase
            return -A*omega*sin(omega*t + phi)

    def aceleration(self, t): 
        if t > 1e-9:
            return 0
        else:
            omega, A, phi = self.frequency, self.amplitude, self.phase
            return -A*omega**2*cos(omega*t + phi)
