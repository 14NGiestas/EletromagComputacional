from numpy import sin, cos, exp

class SimpleHarmonicOscilator:
    def __init__(self, **kwargs):
        self.frequency = kwargs.get('frequency', 1)
        self.amplitude = kwargs.get('amplitude', 1)
        self.phase     = kwargs.get('phase',     0)

    def position(self, t):
        omega, A, phi = self.frequency, self.amplitude, self.phase
        return A*cos(omega*t + phi)

    def velocity(self, t):
        omega, A, phi = self.frequency, self.amplitude, self.phase
        return -A*omega*sin(omega*t + phi)

    def aceleration(self, t): 
        omega, A, phi = self.frequency, self.amplitude, self.phase
        return -A*omega**2*cos(omega*t + phi)
    
    @property
    def parameters(self):
        return {'frequency': self.frequency,
                'amplitude': self.amplitude,
                'phase': self.phase}
        
