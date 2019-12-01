from scipy.linalg import expm, sinm, cosm, sqrtm
import numpy as np
from numpy import linalg as la
import scipy as sc
import sympy as sp
import networkx as nx
import matplotlib.pyplot as plt

r,l,c = 200,200,1
omega_0 = 1/np.sqrt(l*c) # frequência natural
tau_0 = r/l
tau_1 = 1/(r*c) # tempo de relaxação

# parametros
k_p, k_d, g_d, g_p = (omega_0**2, 0, tau_1, 0)
#k_p, k_d, g_d, g_p = (0, 0, 1, 20)
print(omega_0**2, tau_1)
T = omega_0**(-1) * 100 
Ndt = 1000

edges = [
    # resistors
    (1,2, {'v': r}),
    (2,3, {'v': r}),
    (3,4, {'v': r}),
    (4,2, {'v': r}),
    # tank 1
    (1,0,{'v': l}),
    (1,0,{'v': c}),
    # tank 2
    (2,0,{'v': l}),
    (2,0,{'v': c}),
    # tank 3
    (3,0,{'v': l}),
    (3,0,{'v': c}),
    # tank 4 
    (4,0,{'v': l}),
    (4,0,{'v': c}),
]
G = nx.Graph(edges)

# laplace matrix
#         / -a_ij se i != j
# l_ij = |  
#         \ sum(h=1,n,h!=1) a_ih if i=j 

#         / -1        se {i,j} é um nó
# l_ij = |  degree(i) se i = j
#         \ 0 c.c. 
# laplacian matrix pag. 81 of ref[3]

L = nx.laplacian_matrix(G).toarray()
print('L = ')
print(L)
n = L.shape[0]

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
    U = lambda t: np.dot(expm(Q*t),U0)
    q_i = list(map(lambda x: x[:n], map(U, t)))
    return q_i

def sync_case():
    # charges distributed at will, no currents on circuit
    q0 = np.array([1.,2.,3.,4.,5.])
    i0 = np.array([0.,0.,0.,0.,0.])
    # state-space vector
    U0 = np.hstack([q0,i0]).T
    t = np.linspace(0,T/2,Ndt)
    q = solution(Q,U0,t)
    plt.plot(t,q)
    plt.show()

def consensus_case():
    # simetric distributed charges, no currents on circuit
    q0 = np.array([-2.,-1.,0.0,1.0,2.0])
    i0 = np.array([0.0,0.0,0.0,0.0,0.0])
    # state-space vector
    U0 = np.hstack([q0,i0]).T
    t = np.linspace(0,T,Ndt)
    q = solution(Q,U0,t)
    plt.plot(t,q)
    plt.show()

consensus_case()
sync_case()
