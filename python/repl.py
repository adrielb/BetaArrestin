%logstart -o -t /tmp/log.py
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
ax.plot( sim['Stot'], sim['MAPKpp'])
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
ax.plot( Smem, p3, color='lime', label="p3()" )
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
ax.plot( simStot.index, simStot['MAPKpp_Norm'], color='blue', label='MAPKpp' )
ax.plot( simStot.index, simStot['MI_Norm'],     color='black', label='MI' )
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
    simGrad['MI']['StotNative'].plot( label='Native' ) )
fig.add_axes(
    simGrad['MI']['StotOpt'].plot( label='Optimal' ) )
ax.set_xlabel("Gradient")
ax.set_ylabel("MI")
ax.legend()
fig.canvas.draw()
fig.show()
fig.savefig( "GradientVsMI.pdf", transparent=True )

# Noco and Rab11DN
'''
Noco inhibits
Rab11: recycling endosomes
active transport btwn front and back
gradient of ves sharper than gradient of ligand
  due to Rab11 / microtubles
Rab11 enhances ves transport to membrane
Rab11 localized to back
Rab11DN inhibits recycling to mem
E. Noco: Vesicle to mem inhib (p4 50%)
C. Drug: Mem to ves (p3 95%)
more Rab11 in back in WT
Rab11 enables ves transport
p4 sensitive to F/B, proportional to position (or
  1/scaffold)
Rab11 inhibition - makes gradient smaller (scale
  factor)
Noco  -  suppress assym of Rab11
Noco  -  inhibits Arrb2 polarization
         increases ERK-P
Rab11DN eliminates gradient of recycling (p4
  evenly distributed across cell)
'''

ctrl = dose_response( { 'slevel' : 'StotNative'} )

p4b = DEFAULT_PARAMS['p4b'] * 0.2
noco = dose_response( { 'slevel' : 'StotNative', 'p4b': p4b } )

fig = plt.figure(1)
fig.clear()
ctrl['MAPKpp-noco'] = noco['MAPKpp']
ax = ctrl['MAPKpp'].plot(color='blue', label='MAPKpp-ctrl')
ax = ctrl['MAPKpp-noco'].plot(color='red')
ax.set_title('Nocodazole treatment')
ax.set_ylabel('MAPKpp')
ax.set_xlabel('Input')
plt.legend(loc='lower right')
fig.savefig( "noco.pdf", transparent=True )

# Rab11DN
rab11dn = dose_response( { 'slevel' : 'StotNative', 'p4a':0 } )

fig = plt.figure(2)
fig.show()
fig.clear()
ax = fig.add_subplot( 1,2,1 )
ax.plot( ctrl.index, ctrl['MI'] , label='Ctrl', color='blue' )
ax.plot( ctrl.index, rab11dn['MI'] , label='Rab11DN', color='pink' )
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.legend(loc='center right')
ax = fig.add_subplot( 1,2,2 )
ax.set_ylabel("Avg MI")
avgMI = pd.Series(
            [ ctrl['MI'].mean(), rab11dn['MI'].mean() ],
            index = ['Ctrl', 'Rab11DN']
            )
ax = avgMI.plot(kind='bar', color=['blue','pink'])
ax.set_xticklabels(['Ctrl','Rab11DN'],rotation='horizontal')
fig.canvas.draw()
fig.savefig( "rab11dn.pdf", transparent=True )


def popwindow():
    plt.ion()
    plt.get_current_fig_manager().window.activateWindow()
    plt.get_current_fig_manager().window.raise_()


