from numpy import cos, exp

def harmonic_oscilator(t, angular_velocity=1, amplitude=1, phase=0):
    '''
    Simple Harmonic Oscilator
    '''
    return amplitude*cos(angular_velocity*t + phase)

def damped_oscilator(t, damping=1, angular_velocity=1, amplitude=1, phase=0):
    '''
    Damped Oscilator
    '''
    return amplitude*exp(-damping*t)*cos(angular_velocity*t + phase)
