import ahkab
from ahkab.circuit import Circuit
from ahkab.symbolic import symbolic_analysis
import matplotlib.pyplot as plt

R = 200
L = 200 
C = 1
omega_0 = 1/(L*C)**.5 # frequência natural
T = omega_0**(-1) * 100 
Ndt = 1000

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
x0 = ahkab.new_x0(c, {'V(n1)':-2, 'V(n2)':-1, 'V(n3)':1, 'V(n4)':2})
tran = ahkab.new_tran(tstart=0.0, tstop=T, tstep=T/Ndt, x0=x0, outfile='results')
res = ahkab.run(c, tran)['tran']
plt.plot(res.get_x(), res['VN1'])
plt.plot(res.get_x(), res['VN2'])
plt.plot(res.get_x(), res['VN3'])
plt.plot(res.get_x(), res['VN4'])
plt.savefig('interferencia.png')
plt.show()
# Sincronização
x0 = ahkab.new_x0(c, {'V(n1)':1, 'V(n2)':2, 'V(n3)':3, 'V(n4)':4})
tran = ahkab.new_tran(tstart=0.0, tstop=T, tstep=T/Ndt, x0=x0, outfile='results')
res = ahkab.run(c, tran)['tran']
plt.plot(res.get_x(), res['VN1'])
plt.plot(res.get_x(), res['VN2'])
plt.plot(res.get_x(), res['VN3'])
plt.plot(res.get_x(), res['VN4'])
plt.savefig('sincronizacao.png')
plt.show()
