import movements

class MovingCharge:
    def __init__(self, movement, dt=1e-7):
        self.time = 0
        self.step = dt
        self.movement = movement
        self.path = []

    def step(self):
        self.time += self.step
        self.path.append(self.position)

    def reset(self):
        self.time = 0
        self.path = []

    def electrical_field(x,y):
        pass

    @property
    def position(self):
        t = self.time
        (x,y,z) = self.movement(t)
        return (x,y,z)

    @property
    def velocity(self):
        t = self.time
        return derivative(self.movement, t, n=1, dx=1e-5)

    @property
    def aceleration(self):
        t = self.time
        return derivative(self.movement, t, n=2, dx=1e-5)
