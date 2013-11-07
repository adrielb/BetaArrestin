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

sim = dose_response({'slevel' : 'StotNative' }).append(
      dose_response({'slevel' : 'StotOE' }) )
sim = sim.pivot( sim.index, 'slevel' )
sim.MAPKpp

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
ax.set_ylim(-5, 10)
ax.set_title("MI input response")
ax.plot( sim.index, sim['MI']['StotNative'], label='Native' )
ax.plot( sim.index, sim['MI']['StotOE'], label='Overexpressed' )
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
ax.plot( simStot.index, simStot['MAPKpp_Norm'], color='red', label='MAPKpp' )
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


fig = plt.gcf()
fig = plt.figure(3)
fig.canvas.set_window_title('tp = 1e-2')

# time constant tp
sim =             dose_response( { 'slevel' : 'StotOE', 'p4a':0, 'tp':1e0 } )
sim = sim.append( dose_response( { 'slevel' : 'StotOE', 'p4a':0, 'tp':1e-1} ))
sim = sim.append( dose_response( { 'slevel' : 'StotOE', 'p4a':0, 'tp':1e-2} ))
sim = sim.pivot( sim.index, 'tp' )

fig, ax = genfig(1)
ax = sim['MI'].plot()
ax.set_ylim(-2,2)
ax.get_figure().show()
showfig(1)


# no p4a, amp but no transition
sim = dose_response({'lbl' : 'N', 'slevel' : 'StotNative' }).append(
      dose_response({'lbl' : 'OE', 'slevel' : 'StotOE' })).append(
      dose_response({'lbl' : 'Na', 'p4a':0, 'slevel' : 'StotNative' })).append(
      dose_response({'lbl' : 'OEa', 'p4a':0, 'slevel' : 'StotOE' }))
sim = sim.pivot( sim.index, 'lbl' )

fig, ax = genfig()
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(-5, 10)
ax.set_title("MI input response")
ax.plot( sim.index, sim['MI']['N'],  label='Amp Native', color='red' )
ax.plot( sim.index, sim['MI']['Na'], label='No Amp Native', color='pink' )
ax.plot( sim.index, sim['MI']['OE'], label='Amp Overexpressed', color='blue' )
ax.plot( sim.index, sim['MI']['OEa'],label='No Amp Overexpressed', color='cyan' )
ax.legend()
fig.canvas.draw()
fig.show()
fig.savefig( "MI_Amp_comparison.pdf", transparent=True )

sim = dose_response({'lbl' : 'N', 'slevel' : 'StotNative' }).append(
      dose_response({'lbl' : 'OE', 'slevel' : 'StotOE' })).append(
      dose_response({'lbl' : 'Na', 'p4a':-DEFAULT_PARAMS['p4a'], 'slevel' : 'StotNative' })).append(
      dose_response({'lbl' : 'OEa', 'p4a':-DEFAULT_PARAMS['p4a'], 'slevel' : 'StotOE' }))
sim = sim.pivot( sim.index, 'lbl' )

# p4a sign flip, amp and transition, messed up native
fig, ax = genfig()
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(-5, 10)
ax.set_title("MI input response")
ax.plot( sim.index, sim['MI']['N'],  label='Pos Amp Native', color='red' )
ax.plot( sim.index, sim['MI']['Na'], label='Neg Amp Native', color='pink' )
ax.plot( sim.index, sim['MI']['OE'], label='Pos Amp Overexpressed', color='blue' )
ax.plot( sim.index, sim['MI']['OEa'],label='Neg Amp Overexpressed', color='cyan' )
ax.legend()
fig.canvas.draw()
fig.show()
fig.savefig( "p4a_sign_change.pdf", transparent=True )


# single sigmoid
sim = dose_response( { 'slevel' : 'StotOE'             , 'tp':1e-2} ).append(
      dose_response( { 'slevel' : 'StotOE', 'p4a': 4e-3, 'tp':1e-2} )).append(
      dose_response( { 'slevel' : 'StotOE', 'p4a': 2e-3, 'tp':1e-2} )).append(
      dose_response( { 'slevel' : 'StotOE', 'p4a': 1e-3, 'tp':1e-2} ))
sim = sim.pivot( sim.index, 'p4a' )

ax = sim['MI'].plot()
ax.set_title('sigmoid polarity indicator')
ax.set_ylim(-5,5)
ax.get_figure().canvas.draw()
ax.get_figure().show()
ax.get_figure().savefig( "sig_pol_ind_2.pdf", transparent=True )


sim = dose_response( { 'slevel' : 'StotOE', 'p4a':10e-3, 'tp':1e-2 } ).append(
      dose_response( { 'slevel' : 'StotOE', 'p4a': 7e-3, 'tp':1e-2 } )).append(
      dose_response( { 'slevel' : 'StotOE', 'p4a': 4e-3, 'tp':1e-2 } ))
sim = sim.pivot( sim.index, 'p4a' )
ax = sim['MI'].plot()
ax.set_title('sigmoid MI')
ax.set_ylim(-5,5)
ax.set_ylim(auto=True)
ax.get_figure().canvas.draw()
ax.get_figure().show()

dM = pd.DataFrame(index = df1.index)
dM['MAPKpp+1'] = df1['MAPKpp']
dM['MAPKpp.0'] = df0['MAPKpp']
dM['MAPKpp-1'] = df2['MAPKpp']
dM.plot()

dfNa = dose_response( { 'slevel' : 'StotNative' } )
dfOE = dose_response( { 'slevel' : 'StotOE' } )
df = pd.DataFrame(index = df1.index)


