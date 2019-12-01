import sympy as sp
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from utils import direct_sum
from scipy.sparse import block_diag, vstack, bmat
from numpy import linalg as LA

R = [sp.Symbol(f'R_{i}', real=True, positive=True) for i in range(4)]
L = [sp.Symbol(f'L_{i}', real=True, positive=True) for i in range(4)]
C = [sp.Symbol(f'C_{i}', real=True, positive=True) for i in range(4)]
Q = [sp.Function(f'Q_{i}') for i in range(4)]
t = sp.Symbol('t', real=True)

d1_Q = [sp.diff(q(t),t) for q in Q]
d2_Q = [sp.diff(d1_q,t) for d1_q in d1_Q]

r = [-R[i]*d1_q.doit() for i,d1_q in enumerate(d1_Q)]
l = [-L[i]*d2_q.doit() for i,d2_q in enumerate(d1_Q)]
c = [q(t)/C[i] for i,q in enumerate(Q)]

edges = [
    # resistors
    ('N1','N2', {'r': r[0]}),
    ('N2','N3', {'r': r[1]}),
    ('N3','N4', {'r': r[2]}),
    ('N4','N2', {'r': r[3]}),
    # tank 1
    ('N1','GND',{'l': l[0], 'c': c[0]}),
    # tank 2
    ('N2','GND',{'l': l[1], 'c': c[1]}),
    # tank 3
    ('N3','GND',{'l': l[2], 'c': c[2]}),
    # tank 4 
    ('N4','GND',{'l': l[3], 'c': c[3]})
]

G = nx.Graph(edges)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

basis = nx.cycle_basis(G)
eqs = []
for cycles in basis:
    edges = [(c,cycles[(i+1) % len(cycles)]) for i,c in enumerate(cycles)]
    lhs = None
    rhs = 0
    for u,v in edges:
        node = G[u][v]
        term = node.get('r',0) + node.get('l',0) + node.get('c',0)
        lhs = lhs + term if lhs else term
    lhs = lhs.subs({
        R[1]:R[0], R[2]:R[0], R[3]:R[0],
        L[1]:L[0], L[2]:L[0], L[3]:L[0],
        C[1]:C[0], C[2]:C[0], C[3]:C[0],
        Q[0](t)+Q[1](t):sp.Function('\eta_1')(t),
        Q[1](t)+Q[2](t):sp.Function('\eta_2')(t),
        Q[2](t)+Q[3](t):sp.Function('\eta_3')(t),
        Q[1](t)+Q[3](t):sp.Function('\eta_4')(t)
    })
    eq = sp.Eq(lhs,rhs)

    print(f'{cycles} {eq}')
    eqs.append(eq)
