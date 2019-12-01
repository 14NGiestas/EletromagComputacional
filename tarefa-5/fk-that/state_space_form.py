from scipy.linalg import expm, sinm, cosm, sqrtm
import numpy as np
from numpy import linalg as la
import scipy as sc
import sympy as sp
import networkx as nx
import matplotlib.pyplot as plt

# parametros
r = 2.
l = 2.
c = 1.
w0 = 1/(l*c)**0.5 # natural frequency
T = 20/w0 

# tranformacao
A = np.array([
    [1.,1.,0.,0.],
    [0.,1.,1.,0.],
    [0.,0.,1.,1.],
    [0.,1.,0.,1.]
])
# trans. inversa
IA = la.inv(A)

I = np.identity(4)
O = 0*I

IA_B = np.block([
    [IA, O],
    [O, IA],
])

# operador
Q = np.block([
    [O,                 I],
    [-w0**2*I, -r*w0**2*IA]
])
print(Q)


#X0 = np.array([-0.1,-0.2,0.2,0.1,0.1,0.1,0.1,0.1]).T
X0 = np.array([0.1,0.2,0.3,0.4,0.1,0.1,0.1,0.1]).T
t = np.linspace(0,T,100)
# https://pt.wikipedia.org/wiki/Sistema_de_equa%C3%A7%C3%B5es_diferenciais#M%C3%A9todo_matricial
X = lambda t: np.dot(IA_B,np.dot(expm(Q*t),X0))
x = list(map(X, t))
plt.plot(t,x)
plt.show()

