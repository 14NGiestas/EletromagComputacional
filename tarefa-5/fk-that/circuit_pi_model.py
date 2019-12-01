import sympy as sp
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from utils import direct_sum
from scipy.sparse import block_diag, vstack, bmat
from numpy import linalg as LA
'''
sp.init_printing(use_unicode=True)

R, L, C = sp.symbols('R L C', real=True, positive=True)
Q = sp.Function('Q')
t = sp.Symbol('t', real=True)

dQdt = sp.diff(Q(t),t)
dQdt2 = sp.diff(dQdt,t)

resistor = R*dQdt.doit()
inductor = L*dQdt2.doit()
capacitor = Q(t)/C

print(resistor)
print(inductor)
print(capacitor)
'''

r = 2 #0.1e3
l = 2 #0.2e-12
c = 0.5 #0.3e-9
edges = [
    # resistors
    ('N1','N2', {'r': r}),
    ('N2','N3', {'r': r}),
    ('N3','N4', {'r': r}),
    ('N4','N2', {'r': r}),
    # tank 1
    ('N1','GND',{'l': l, 'c': c}),
    # tank 2
    ('N2','GND',{'l': l, 'c': c}),
    # tank 3
    ('N3','GND',{'l': l, 'c': c}),
    # tank 4 
    ('N4','GND',{'l': l, 'c': c})
]

G = nx.Graph(edges)
r_ij = nx.get_edge_attributes(G,'r')
l_ij = nx.get_edge_attributes(G,'l')
c_ij = nx.get_edge_attributes(G,'c')

O = np.zeros((3,8))
R = nx.incidence_matrix(G, weight='r')
L = nx.incidence_matrix(G, weight='l')
C = nx.incidence_matrix(G, weight='c')
B = nx.incidence_matrix(G, oriented=True)
G = nx.incidence_matrix(G, weight='r')
G.data = 1/R.data

LC = block_diag((L,C)).toarray()
print(LC)
A = [
    [-G, -B],
    [B.T,-R]
]
print(A)
print(LA.inv(C.toarray()))

exit(0)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edges)

eqs = []
for cycles in nx.cycle_basis(G):
    head = cycles[0]
    stack = cycles[::-1]
    eq = None
    while stack:
        u = stack.pop()
        v = stack.pop() if stack else head 
        eq = G[v][u]['val'] if not eq else eq + G[v][u]['val']
    eqs.append(eq)

print(eqs)
