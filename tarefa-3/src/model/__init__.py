from scipy import optimize
from numpy.linalg import norm
from numpy import linspace, meshgrid
from numpy import array, vectorize, dot, cross

from model.constants import light_speed as c
from model.moving_particle import MovingParticle

class LienardWiechertModel:
    def __init__(self, dt=1e-4, size=(1.0,1.0), ticks=(100,100)):
        x_axis = linspace(-size[0], size[0], ticks[0])
        y_axis = linspace(-size[1], size[1], ticks[1])
        self.mesh = meshgrid(x_axis, y_axis)
        self.charge = MovingParticle()
        self.time = 0
        self.step = dt

    def calculate(self):
        X, Y = self.mesh
        E = vectorize(self.electrical_field, excluded=['self'])
        return E(X,Y)

    def retarded_time(self, R, r):
        t = self.time

        def time_equation(t_ret):
            return t - t_ret - norm(R - r(t_ret))/c 

        t_ret = optimize.newton(time_equation, t)
        return t_ret

    def electrical_field(self, x, y):
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

