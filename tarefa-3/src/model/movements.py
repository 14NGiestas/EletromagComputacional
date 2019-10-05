from numpy import sin, cos, exp

class SimpleHarmonicOscilator:
    def __init__(self, angular_velocity=1, amplitude=1, phase=0):
        self.parameters = angular_velocity, amplitude, phase

    def position(self, t):
        omega, A, phi = self.parameters
        return A*cos(omega*t + phi)

    def velocity(self, t):
        omega, A, phi = self.parameters
        return -A*omega*sin(omega*t + phi)

    def aceleration(self, t): 
        omega, A, phi = self.parameters
        return -A*omega**2*cos(omega*t + phi)


#class DampedOscilator(SimpleOscilator):
#    def __init__(self, axis='x', omega=1, A=1, phi=0, gamma=0):
#        pass
#
#    def position(self):
#        A, omega, phi = self.amplitude, self.angular_velocity, self.phase
#        gamma = self.damping
#        return A*exp(-gamma*t)*cos(omega*t + phi)
#
#    def velocity(self):
#        A, omega, phi = self.amplitude, self.angular_velocity, self.phase
#        gamma = self.damping
#        return -A*(gamma*exp(-gamma*t)*cos(omega*t + phi)
#                   omega*exp(-gamma*t)*sin(omega*t + phi))
#
#    def aceleration(self):
#        A, omega, phi = self.amplitude, self.angular_velocity, self.phase
#        gamma = self.damping
#        pass
#
#
#
#
