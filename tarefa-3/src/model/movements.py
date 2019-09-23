def harmonic(t, angular_velocity=1, amplitude=1, phase=0):
    # Z = Z_0*cos(omega*t + phy)
    return (0, 0, amplitude*cos(angular_velocity*t + phase))

