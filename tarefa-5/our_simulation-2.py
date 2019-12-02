from scipy.linalg import expm, sinm, cosm, sqrtm
import numpy as np
from numpy import linalg as la
import scipy as sc
import sympy as sp
import networkx as nx
import matplotlib.pyplot as plt

r,l,c = 2,2,0.5
omega_0 = 1/np.sqrt(l*c) # frequência natural
tau_0 = r/l
tau_1 = 1/(r*c) # tempo de relaxação

# parametros de sincronia de amplitudes
k_p, k_d, g_p, g_d = (omega_0**2, 0, 0, tau_1)

edges = [
    (1,2),(2,3),(3,4),(4,2)
]

G = nx.Graph(edges)
nx.draw(G, with_labels=True)
plt.show()

# weighted laplace matrix
#         / -a_ij se i != j
# l_ij = |  
#         \ sum(h=1,n,h!=1) a_ih if i=j 
# unweighted
#         / -1        se {i,j} é uma aresta 
# l_ij = |  degree(i) se i = j
#         \ 0 c.c. 
# laplacian matrix pag. 81 of ref[3]

L = nx.laplacian_matrix(G).toarray()
print('L = ')
print(L)
n = L.shape[0]
print(n)

I = np.identity(n)
O = 0*I

# operador
Q = np.block([
    [O,                           I],
    [-k_p*I - g_p*L, -k_d*I - g_d*L]
])
print('Q = ')
print(Q)


def solution(Q,U0,t):
    # https://pt.wikipedia.org/wiki/Sistema_de_equa%C3%A7%C3%B5es_diferenciais#M%C3%A9todo_matricial
    # dU/dt = Q U -> U = U0*expm(Q*t)
    U = lambda t: np.dot(expm(Q*t),U0)
    q_i = list(map(lambda x: x[:n], map(U, t)))
    return q_i

def sync_case(start, end, step):
    # charges distributed at will, no currents on circuit
    q0 = np.array([1.,2.,3.,4.])
    i0 = np.array([0.,0.,0.,0.])
    # state-space vector
    U0 = np.hstack([q0,i0]).T
    t = np.linspace(start,end,step)
    q = solution(Q,U0,t)
    plt.plot(t,q)
    plt.grid(1 == 1)
    plt.show()

def consensus_case(start, end, step):
    # simetric distributed charges, no currents on circuit
    q0 = np.array([2.,1.,0.,0.])
    i0 = np.array([0.,0.,0.,0.])
    # state-space vector
    U0 = np.hstack([q0,i0]).T
    t = np.linspace(start,end,step)
    q = solution(Q,U0,t)
    plt.plot(t,q)
    plt.grid(1 == 1)
    plt.show()

SHIFT = 0
RANGE = 1000
NUM_T = 1e4
#consensus_case(SHIFT, RANGE+SHIFT, NUM_T)
sync_case(SHIFT, RANGE+SHIFT, NUM_T)
