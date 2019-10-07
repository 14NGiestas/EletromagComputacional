from scipy import optimize
from numpy.linalg import norm
from numpy import linspace, meshgrid, arctan2
from numpy import array, vectorize, dot, cross

from model.constants import light_speed as c
from model.moving_particle import MovingParticle

class LienardWiechertModel:
    def __init__(self, settings):
        self.settings = settings
        size_x = self.settings['simulation'].getfloat('mesh_size_x')
        size_y = self.settings['simulation'].getfloat('mesh_size_y')
        ticks_x = self.settings['simulation'].getfloat('mesh_ticks_x')
        ticks_y = self.settings['simulation'].getfloat('mesh_ticks_y')
        self.field = self.settings['simulation']['field']

        self.charge = MovingParticle()
        self.time = 0
        self.time_step = self.settings['simulation'].getfloat('time_step')
        self.frames = [] 
        self.x_axis = linspace(-size_x, size_x, ticks_x)
        self.y_axis = linspace(-size_y, size_y, ticks_y)

    def calculate(self):
        X, Y = meshgrid(self.x_axis, self.y_axis, indexing='xy')
        if self.field == 'electric':
            E = vectorize(self.electric_field, excluded=['self'])
            self.frames.append(E(X,Y))
        else:
            B = vectorize(self.magnetic_field, excluded=['self'])
            self.frames.append(B(X,Y))

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
        R = array([x,y,0])

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

    def magnetic_field(self, x, y):
        R = array([x,y,0])

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
        B = cross(r_ret/norm(r_ret), E)
        return norm(B)

