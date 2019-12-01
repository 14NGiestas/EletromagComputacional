import ahkab
from ahkab.circuit import Circuit
from ahkab.symbolic import symbolic_analysis
import matplotlib.pyplot as plt

R = 1 #0.1e3
L = 0.05 #0.2e-12
C = 100 #0.3e-9
c = Circuit('Sincronização de circuito LC')
# resistors must be placed so all tanks are connected through one
c.add_capacitor('C3', 'n1', 'n3', C)
# tank1
c.add_inductor('L1', 'n1', 'n2', L)
c.add_capacitor('C1', 'n2', 'n3', C)
# tank2
c.add_inductor('L2', 'n1', 'n4', L)
c.add_capacitor('C2', 'n4', 'n3', C)

# Interferência destrutiva
x0 = ahkab.new_x0(c, {'V(n4)':-0.2/C, 'V(n2)':0.2/C})
tran = ahkab.new_tran(tstart=0.0, tstop=(L*C)**0.5*10, tstep=1e-3, x0=x0, outfile='results')
res = ahkab.run(c, tran)['tran']
print(res.keys())
plt.plot(res.get_x(), res['VN3'])
plt.plot(res.get_x(), res['VN2'])
plt.savefig('interferencia.png')
plt.show()
