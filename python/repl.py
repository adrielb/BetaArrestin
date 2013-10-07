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
