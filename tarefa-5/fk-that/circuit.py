import ahkab
from ahkab.circuit import Circuit
from ahkab.symbolic import symbolic_analysis
import matplotlib.pyplot as plt

R = 1 #0.1e3
L = 1e-2 #0.2e-12
C = 0.5 #0.3e-9
c = Circuit('Sincronização de circuito LC')
# resistors must be placed so all tanks are connected through one
c.add_resistor('R1', 'n1', 'n2', R)
c.add_resistor('R2', 'n2', 'n3', R)
c.add_resistor('R3', 'n3', 'n4', R)
c.add_resistor('R3', 'n4', 'n2', R)
# tank1
c.add_inductor('L1', 'n1', c.gnd, L)
c.add_capacitor('C1', 'n1', c.gnd, C)
# tank2
c.add_inductor('L2', 'n2', c.gnd, L)
c.add_capacitor('C2', 'n2', c.gnd, C)
# tank3
c.add_inductor('L3', 'n3', c.gnd, L)
c.add_capacitor('C3', 'n3', c.gnd, C)
# tank4
c.add_inductor('L4', 'n4', c.gnd, L)
c.add_capacitor('C4', 'n4', c.gnd, C)

# Interferência destrutiva
x0 = ahkab.new_x0(c, {'V(n1)':-0.2/C, 'V(n2)':-0.1/C, 'V(n3)':0.1/C, 'V(n4)':0.2/C})
tran = ahkab.new_tran(tstart=0.0, tstop=(L*C)**0.5*100, tstep=1e-3, x0=x0, outfile='results')
res = ahkab.run(c, tran)['tran']
plt.plot(res.get_x(), res['VN1'])
plt.plot(res.get_x(), res['VN2'])
plt.plot(res.get_x(), res['VN3'])
plt.plot(res.get_x(), res['VN4'])
plt.savefig('interferencia.png')
plt.show()
# Sincronização
x0 = ahkab.new_x0(c, {'V(n1)':0.1/C, 'V(n2)':0.2/C, 'V(n3)':0.3/C, 'V(n4)':0.4/C})
tran = ahkab.new_tran(tstart=0.0, tstop=(L*C)**0.5*100, tstep=1e-3, x0=x0, outfile='results')
res = ahkab.run(c, tran)['tran']
plt.plot(res.get_x(), res['VN1'])
plt.plot(res.get_x(), res['VN2'])
plt.plot(res.get_x(), res['VN3'])
plt.plot(res.get_x(), res['VN4'])
plt.savefig('sincronizacao.png')
plt.show()
