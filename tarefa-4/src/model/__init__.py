from model.constants import light_speed as c

class HelicoidalSolenoidModel:
    def __init__(self):
        pass

    def calculate(self):
        X, Y = meshgrid(self.x_axis, self.y_axis, indexing='xy')
        E = vectorize(self.electric_field, excluded=['self'])
        self.frames.append(E(X,Y))

    def step(self):
        self.time += self.time_step

    def reset(self):
        self.time = 0
        self.frames = [] 

    def retarded_time(self, R, r):
        f = lambda t_ret: self.time - t_ret - norm(R - r(t_ret))/c
        t_ret = optimize.newton(f, self.time) 
        return t_ret

    def magnetic_field(self, x, y):
        dx, dy, dz = self.translation_x, self.translation_y, self.translation_z
        R = array([x+dx,y+dy,dz])

        r = self.charge.position
        v = self.charge.velocity
        a = self.charge.aceleration

        t_ret = self.retarded_time(R, r)
        r_ret = R - r(t_ret)
        u_ret = c * r_ret / norm(r_ret) - v(t_ret)
        a_ret = a(t_ret)
        v_ret = v(t_ret)

        E = norm(r_ret)/(dot(r_ret,u_ret))**3*(u_ret*(c**2-norm(v_ret)**2)
                                        + cross(r_ret,cross(u_ret,a_ret)))
        return norm(E)
