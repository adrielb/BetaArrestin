# Single run
p = [{}]
sim = runsim( p )
sim

p = [ {'Stot' : s, 'p1' : 100, 'p2' : 0, 'p4' : 0} for s in np.arange(0, 2, 0.01) ]
sim = runsim( p )
sim['MAPKpp'] = sim['MAPKpp[0]'] / sim['MAPKpp[0]'].max()

fig, ax = genfig()
ax.clear()
ax.set_xlabel("Stot")
ax.set_ylabel("MAPKpp")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.set_title("Scaffold dose response")
ax.plot( sim['Stot'], sim['MAPKpp'] )
fig.canvas.draw()
fig.show()


# Smem vs p3 transport function
fig, ax = genfig()

p3a = DEFAULT_PARAMS['p3a']
p3b = DEFAULT_PARAMS['p3b']
p3c = DEFAULT_PARAMS['p3c']
p3d = DEFAULT_PARAMS['p3d']
p3e = DEFAULT_PARAMS['p3e']
p3f = DEFAULT_PARAMS['p3f']
Smem = np.arange( 0, 3, 0.01)
p3 = p3_func( Smem, p3a, p3b, p3c, p3d, p3e, p3f )
ax.clear()
ax.set_xlabel("Smem")
ax.set_ylabel("p3")
ax.set_xlim(auto=True)
ax.set_ylim(0, 0.4)
ax.set_title("p3: Smem to Sves")
ax.plot( Smem, p3 )
fig.canvas.draw()
fig.show()


# MAPKpp vs dose
fig, ax = genfig()

sim = dose_response({'Stot' : 42.0})
sim.MAPKpp

ax.clear()
ax.set_xlabel("Input")
ax.set_ylabel("MAPKpp")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.set_title("Input dose response")
ax.plot( sim['l'], sim['MAPKpp'] )
fig.canvas.draw()
fig.show()

ax.clear()
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.set_title("Input dose response")
ax.plot( sim['l'], sim['MI'] )
fig.canvas.draw()
fig.show()

