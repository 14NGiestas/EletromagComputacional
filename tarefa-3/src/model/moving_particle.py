from numpy import array 

from model.movements import SimpleHarmonicOscilator


class MovingParticle:
    def __init__(self):
        self.movement_x = SimpleHarmonicOscilator(angular_velocity=1e8)
        self.movement_y = SimpleHarmonicOscilator(angular_velocity=1e8, phase=3.1415/2)
        self.movement_z = None

    def position(self, t):
        ''' Returns the particle position vector at a given time t '''
        sx = self.movement_x.position(t) if self.movement_x else 0
        sy = self.movement_y.position(t) if self.movement_y else 0
        sz = self.movement_z.position(t) if self.movement_z else 0
        return array([sx,sy,sz])

    def velocity(self, t):
        ''' Returns the particle velocity vector at a given time t '''
        vx = self.movement_x.velocity(t) if self.movement_x else 0
        vy = self.movement_y.velocity(t) if self.movement_y else 0
        vz = self.movement_z.velocity(t) if self.movement_z else 0
        return array([vx,vy,vz])

    def aceleration(self, t):
        ''' Returns the particle aceleration vector at a given time t '''
        ax = self.movement_x.aceleration(t) if self.movement_x else 0
        ay = self.movement_y.aceleration(t) if self.movement_y else 0
        az = self.movement_z.aceleration(t) if self.movement_z else 0
        return array([ax,ay,az])

