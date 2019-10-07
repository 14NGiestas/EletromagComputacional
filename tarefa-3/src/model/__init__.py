from scipy import optimize
from numpy.linalg import norm
from numpy import linspace, meshgrid, arctan2
from numpy import array, vectorize, dot, cross

from model.constants import light_speed as c
from model.moving_particle import MovingParticle

class LienardWiechertModel:
    def __init__(self, settings):
        size_x = settings.mesh_size_x
        size_y = settings.mesh_size_y
        ticks_x = settings.mesh_ticks_x
        ticks_y = settings.mesh_ticks_y
        self.translation_x = settings.translation_x
        self.translation_y = settings.translation_y
        self.translation_z = settings.translation_z

        self.frames = [] 
        self.time = 0
        self.time_step = settings.time_step
        self.x_axis = linspace(-size_x, size_x, ticks_x)
        self.y_axis = linspace(-size_y, size_y, ticks_y)
        self.charge = MovingParticle(settings)

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

    def electric_field(self, x, y):
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
