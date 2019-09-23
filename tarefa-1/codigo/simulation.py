import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import elliptical_conductor as ec

# Counter of Samples
s = 0
# Counter of Interactions
i = 0 
# Maximum Samples
max_s = (1e5)
# Energy Variation
dE = []
# Minimum energies of Samples
dE_min = []
# Semi-Major and Semi-Minor Axes
a, b = 2.0, 1.0
# Number of Charges
N = 50
# Sample Amount
sample = int(0.6 * N)
# Zero
zero = 1e-10
# Charges Dynamics
dynCharges = []
# Control Energy Variation
k_max = 20
k = 0
# Energy Precision
eps = 1e-4
# is Biased?
bias = False
# Assymmetry of bias
assy = 0.1 
# Change problem dimension
dim = 2
w_ass = 0.1 * (1 / N)

## Set Initial Conditions of Conductor ##
cond = ec.EllipticalConductor(a, b)
cond.fill(N)

# Initial condition data
dynCharges.append(cond.charges.copy())
opt = [j for j in range(N)]
w = np.array([1 / N for j in range(N)])

## Run Simulation ##
while s < max_s:
    dE_sample = []

    for j in range(sample):
        # Choose a charge
        idx = np.random.choice(opt, 1, p=w)[0]
        if w[idx] >= w_ass:
            w[idx] -= (w_ass / N)
            w = w + 0.5 * (w_ass / N)
            w = w / sum(w)

        # Choose a charge
        #idx = np.random.randint(0, N-1)
        
        # Move Charge
        dEi = cond.move_charge(idx, dim, bias, assy)
        if dEi < zero:
            dE_sample.append(dEi)
            dE.append(dEi)
        i += 1

    if len(dE_sample) > 0: dE_min.append(min(dE_sample))
    if i % 500 == 0: print(i)
    if s > 2:
        if abs(dE_min[-1] - dE_min[-2]) < eps: k += 1
        if k >= k_max: break

    s += 1

dynCharges.append(cond.charges.copy())
info = 'N: ' + str(N) + '; i: ' + str(i)
code = str(int(datetime.datetime.now().timestamp()))

## Create Root Folder ##
path = 'data/' + code
os.mkdir(path)

## Save Parameters ##
filename = path + '/params.dat' 
fileObj = open(filename, 'w+')
fileObj.write('a: ' + str(a) + '\n') # Semi-Major Axis
fileObj.write('b: ' + str(b) + '\n') # Semi-Minor Axis
fileObj.write('N: ' + str(N) + '\n') # Number of Charges
fileObj.write('bias: ' + str(bias) + '\n') # Biased
fileObj.write('assy: ' + str(assy) + '\n') # Assymmetry of bias
fileObj.write('dim: ' + str(dim) + '\n') # Dimension of Problem
fileObj.write('sample: ' + str(sample) + '\n') # Sample
fileObj.write('k: ' + str(k) + '\n') # Control Energy Variation
fileObj.write('k_max: ' + str(k_max) + '\n')
fileObj.write('eps: ' + str(eps) + '\n')
fileObj.write('i: ' + str(i) + '\n') # Iterations
fileObj.write('s: ' + str(s) + '\n') # Numbers of Samples
fileObj.close() 

## Save Energies ##
filename = path + '/energies.dat' 
fileObj = open(filename, 'w+')
for dEi in dE:
    fileObj.write(str(dEi) + '\n')
fileObj.close() 

## Save Minimum Energies of Samples ##
filename = path + '/min-energies.dat' 
fileObj = open(filename, 'w+')
for dEi in dE_min:
    fileObj.write(str(dEi) + '\n')
fileObj.close() 

## Initial Charges Positions ##
filename = path + '/initial-pos.dat' 
fileObj = open(filename, 'w+')
for pos in dynCharges[0]:
    for ri in pos: fileObj.write(str(ri) + ' ')
    fileObj.write('\n')
fileObj.close() 

## Final Charges Positions ##
filename = path + '/final-pos.dat' 
fileObj = open(filename, 'w+')
for pos in dynCharges[1]:
    for ri in pos: fileObj.write(str(ri) + ' ')
    fileObj.write('\n')
fileObj.close() 

path = 'data/' + code + '/'
if not os.path.isdir(path + 'plots/'): os.mkdir(path + 'plots')

## Plot Energies ##
plt.clf()
plt.hist(dE)
plt.title('Energy Variations ' + info)
plt.xlabel('Energy')
plt.grid(linestyle='--')
plt.savefig(path + 'plots/energies.png')

## Plot Minimuns Energies ##
plt.clf()
plt.scatter([i+1 for i in range(len(dE_min))], dE_min)
plt.title('Samples Minimum Energies ' + info)
plt.xlabel('Sample Iterations')
plt.ylabel('Minimum Energies')
plt.grid(linestyle='--')
plt.savefig(path + 'plots/min-energies.png')

## Plot Initial Pos ##
ini_pos = np.array(dynCharges[0])
t = np.linspace(0, 2 * np.pi, 1000)

plt.clf()
plt.plot(a*np.cos(t), b*np.sin(t), color='black')
plt.scatter(ini_pos[:,0], ini_pos[:,1], color='blue')
plt.title('Initial positions of charges ' + info)
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(-a - 0.2, a + 0.2)
plt.ylim(-a - 0.2, a + 0.2)
plt.grid(linestyle='--')
plt.savefig(path + 'plots/ini-pos.png')

## Plot Final Pos ##
final_pos = np.array(dynCharges[-1])

plt.clf()
plt.plot(a*np.cos(t), b*np.sin(t), color='black')
plt.scatter(final_pos[:,0], final_pos[:,1], color='red')
plt.title('Final positions of charges ' + info)
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(-a - 0.2, a + 0.2)
plt.ylim(-a - 0.2, a + 0.2)
plt.grid(linestyle='--')
plt.savefig(path + 'plots/final-pos.png')


## Code Simulation ##
print()
print(code)
