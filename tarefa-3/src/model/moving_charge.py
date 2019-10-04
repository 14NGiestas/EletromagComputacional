from model.constants import light_speed
from scipy import optimize

class MovingCharge:
    def __init__(self, movement, dt=1e-7):
        self.time = 0
        self.step = dt
        self.movement = movement

    def step(self):
        self.time += self.step

    def reset(self):
        self.time = 0

    def electrical_field(self, R):
        q = self.value
        t_ret = self.retarded_time(R)

    def retarded_time(self, R):
        t = self.time
        c = light_speed

        def time_equation(t_ret):
            # Relative distance between the particle and the measurement point
            dx,dy,dz = tuple(ei-ej for ei,ej in zip(R,self.movement(t_ret))) 
            return t - t_ret - 1/c*sqrt(dx**2 + dy**2 + dz**2)
        
        # By default use 
        t_ret = optimize.newton(time_equation, 1.5)
        return t_ret

    @property
    def position(self):
        t = self.time
        return self.movement(t)

    @property
    def velocity(self):
        t, dt = self.time, self.step
        return derivative(self.movement, x0=t, n=1, dx=dt)

    @property
    def aceleration(self):
        t, dt = self.time, self.step
        return derivative(self.movement, xo=t, n=2, dx=dt)
