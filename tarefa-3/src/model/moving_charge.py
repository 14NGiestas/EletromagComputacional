import movements

class MovingCharge:
    def __init__(self, charge, movement):
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

    @property
    def position(self):
        t = self.time
        (x,y,z) = (0, 0, self.movement(t))
        return (x,y,z)
