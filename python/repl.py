import pandas as pd

import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 4

# Single run
p = [{}]
sim = runsim( p )
sim

#
# Steady state MAPKpp vs free scaffold
#
Stot = np.arange(0, 2, 0.01)
p = [ { 'Stot': s,
        'p2'  : 0,
        'p4a' : 0,
        'p4b' : 0,
        'p3a' : 10,
        'p3b' : 0,
        'p3d' : 1 } for s in Stot ]
sim = runsim( p )
sim

fig, ax = genfig()

ax.clear()
ax.set_xlabel("Stot")
ax.set_ylabel("MAPKpp")
ax.set_xlim(auto=True)
ax.set_ylim(0,1.01)
ax.set_title("Open loop scaffold response")
ax.plot( sim['Stot'], sim['MAPKpp'], linewidth=4)
fig.canvas.draw()
fig.show()
fig.savefig( "StotVsMAPKpp.pdf", transparent=True )

# Smem vs p3 transport function
fig, ax = genfig()

p3a = DEFAULT_PARAMS['p3a']
p3b = DEFAULT_PARAMS['p3b']
p3c = DEFAULT_PARAMS['p3c']
p3d = DEFAULT_PARAMS['p3d']
p3e = DEFAULT_PARAMS['p3e']
Smem = np.arange( 0, 3, 0.01)
p3 = p3_func( Smem, p3a, p3b, p3c, p3d, p3e )
ax.clear()
ax.set_xlabel("Smem")
ax.set_ylabel("p3")
ax.set_xlim(auto=True)
ax.set_ylim(0, 0.4)
ax.set_title("p3: Smem to Sves transport")
ax.plot( Smem, p3, linewidth=4, color='lime' )
fig.canvas.draw()
fig.show()
fig.savefig( "SmemVsp3.pdf", transparent=True )

# MAPKpp vs dose
fig, ax = genfig()

simN = dose_response({'Stot' : DEFAULT_PARAMS['StotNative'] })
simOE = dose_response({'Stot' : DEFAULT_PARAMS['StotOE'] })
simOE.MAPKpp

ax.clear()
ax.set_xlabel("Input")
ax.set_ylabel("MAPKpp")
ax.set_xlim(auto=True)
ax.set_ylim(0, 1.01)
ax.set_title("MAPKpp input response")
ax.plot( simN.index, simN['MAPKpp'], label='Native' )
ax.plot( simOE.index, simOE['MAPKpp'], label='Overexpressed' )
ax.legend()
fig.canvas.draw()
fig.show()
fig.savefig( "InputVsMAPKpp.pdf", transparent=True )

ax.clear()
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.set_title("MI input response")
ax.plot( simN.index, simN['MI'], label='Native' )
ax.plot( simOE.index, simOE['MI'], label='Overexpressed' )
ax.legend()
fig.canvas.draw()
fig.show()
fig.savefig( "InputVsMI.pdf", transparent=True )

# MI vs Scaffold
sim = scaffold_response( )

sim.to_csv( '/tmp/scaffold_response.csv', index=False )

sim = pd.read_csv( '/tmp/scaffold_response.csv' )

simStot = sim.groupby( 'Stot' ).mean()
simStot['MAPKpp_Norm'] = simStot['MAPKpp'] / simStot['MAPKpp'].max()
simStot['MI_Norm']     = simStot['MI']     / simStot['MI'].max()
simStot.index = simStot.index / simStot['StotNative']

fig, ax = genfig()

ax.clear()
ax.set_xlabel("Relative Scaffold")
ax.set_ylabel("AU")
ax.set_xlim(auto=True)
ax.set_ylim(-0.3,1.05)
ax.set_title("Scaffold repsonse, avg across dose")
ax.plot( simStot.index, simStot['MAPKpp_Norm'], linewidth=4, color='blue', label='MAPKpp' )
ax.plot( simStot.index, simStot['MI_Norm'],     linewidth=4, color='black', label='MI' )
ax.legend()
fig.canvas.draw()
fig.show()
fig.savefig( "ScaffoldVsMAPKppMI.pdf", transparent=True )



# MI vs Gradient
sim = gradient_response( )
simGrad = sim.groupby(['slevel', 'grad']).mean()
simGrad.to_csv( 'gradient_response.csv' )

simGrad = pd.read_csv( 'gradient_response.csv', index_col=[0,1] )


fig, ax = genfig()

ax.clear()
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.set_title("Gradient repsonse, avg across dose")
fig.add_axes(
    simGrad['MI']['StotNative'].plot(
        linewidth=4, label='Native' ) )
fig.add_axes(
    simGrad['MI']['StotOpt'].plot(
        linewidth=4, label='Optimal' ) )
ax.set_xlabel("Gradient")
ax.set_ylabel("MI")
ax.legend()
fig.canvas.draw()
fig.show()
fig.savefig( "GradientVsMI.pdf", transparent=True )


