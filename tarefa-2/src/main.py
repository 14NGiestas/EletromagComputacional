from equipotential.app import PaintBucket

app = PaintBucket(2.0, 2.0, N=100)
'''
Monopole
'''
app.add_charge(+0,+0,+100)
app.show()
app.clear()

'''
Dipole
'''
app.add_charge(-1,+0,+100)
app.add_charge(+0,+1,+100)
app.show()
app.clear()

'''
Quadrupole
'''
app.add_charge(+1,+1,+100)
app.add_charge(+1,-1,-100)
app.add_charge(-1,-1,+100)
app.add_charge(-1,+1,-100)
app.show()
app.clear()


'''
Line of Charges
'''
for dl in np.linspace(-2,2,10):
    app.add_charge(dl,0,+100)
app.show()
app.clear()
