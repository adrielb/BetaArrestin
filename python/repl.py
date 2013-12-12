# logging / matplotlib global options {{{
%logstart -o -t /tmp/log.py
import pandas as pd

import matplotlib as mpl
mpl.rcParams['lines.linewidth'] = 4

color_native='red'
color_oe='blue'
#}}}

# Single run {{{
p = [{}]
sim = runsim( p )
sim
# }}}

# Steady state MAPKpp vs free scaffold {{{
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
ax.set_title("Open loop scaffold response")
ax.set_xlabel("Stot")
ax.set_ylabel("MAPKpp")
ax.set_xlim(auto=True)
ax.set_ylim(0,1.01)
ax.plot( sim['Stot'], sim['MAPKpp'])
showfig()
fig.savefig( "StotVsMAPKpp.pdf", transparent=True )
# }}}

# Smem vs p3 transport function {{{
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
showfig()
fig.savefig( "SmemVsp3.pdf", transparent=True )
# }}}

# MAPKpp, MI, Sves vs dose {{{
sim = dose_response({'slevel' : 'StotNative' }).append(
      dose_response({'slevel' : 'StotOE' }) )
sim = sim.pivot( sim.index, 'slevel' )


# MAPKpp {{{
fig, ax = genfig()
ax.set_title("MAPKpp input response")
ax.set_xlabel("Input")
ax.set_ylabel("MAPKpp")
ax.set_xlim(auto=True)
ax.set_ylim(0, 1.01)
ax.plot( sim.index , sim['MAPKpp']['StotNative'] , label='Native'        , color='red' )
ax.plot( sim.index , sim['MAPKpp']['StotOE']     , label='Overexpressed' , color='blue' )
ax.legend()
showfig()
fig.savefig( "InputVsMAPKpp.pdf", transparent=True )
#}}}

# MI {{{
fig, ax = genfig(2)
ax.set_title("MI input response")
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(-5, 10)
ax.axhline( 0, color='black', lw=1 )
ax.plot( sim.index , sim['MI']['StotNative'] , label='Native'        , color='blue' )
ax.plot( sim.index , sim['MI']['StotOE']     , label='Overexpressed' , color='red' )
ax.legend()
showfig(2)
fig.savefig( "InputVsMI.pdf", transparent=True )
#}}}

# Smem {{{
fig, ax = genfig(3)
ax.set_title("Smem input response")
ax.set_xlabel("Input")
ax.set_ylabel("Smem")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( sim.index , sim['Smem[0]']['StotNative'] , label='Native'        , color='blue' )
ax.plot( sim.index , sim['Smem[0]']['StotOE']     , label='Overexpressed' , color='red' )
ax.legend(loc='center right')
showfig()
fig.savefig( "InputVsSmem.pdf", transparent=True )
#}}}

# Diff Smem {{{
dSmem = (sim['Smem[1]'] - sim['Smem[0]']) / sim['gdm']
fig, ax = genfig(4)
ax.set_title("Diff Smem input response")
ax.set_xlabel("Input")
ax.set_ylabel("Diff")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( sim.index , dSmem['StotNative'] , label='Native'        , color='blue' )
ax.plot( sim.index , dSmem['StotOE']     , label='Overexpressed' , color='red' )
ax.legend(loc='center right')
showfig()
#}}}

# p3 {{{
p3a = sim['p3a']
p3b = sim['p3b']
p3c = sim['p3c']
p3d = sim['p3d']
p3e = sim['p3e']
p3_0 = p3_func( sim['Smem[0]'], p3a, p3b, p3c, p3d, p3e )
p3_1 = p3_func( sim['Smem[1]'], p3a, p3b, p3c, p3d, p3e )
fig, ax = genfig(8)
ax.set_title("p3(Smem)")
ax.set_xlabel("Input")
ax.set_ylabel("p3")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( sim.index , p3_0['StotNative'] , label='Native'        , color='blue' )
ax.plot( sim.index , p3_0['StotOE']     , label='Overexpressed' , color='red' )
ax.legend(loc='center right')
showfig()
fig.savefig( "InputVsp3.pdf", transparent=True )
# }}}

# Diff p3 {{{
p3a = sim['p3a']
p3b = sim['p3b']
p3c = sim['p3c']
p3d = sim['p3d']
p3e = sim['p3e']
p3_0 = p3_func( sim['Smem[0]'], p3a, p3b, p3c, p3d, p3e )
p3_1 = p3_func( sim['Smem[1]'], p3a, p3b, p3c, p3d, p3e )
dp3 = p3_1 - p3_0
fig, ax = genfig(7)
ax.set_title("Diff p3(Smem)")
ax.set_xlabel("Input")
ax.set_ylabel("Diff p3")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( sim.index , dp3['StotNative'] , label='Native'        , color='blue' )
ax.plot( sim.index , dp3['StotOE']     , label='Overexpressed' , color='red' )
ax.legend(loc='upper right')
showfig()
fig.savefig( "InputVsDp3.pdf", transparent=True )
# }}}

# Sves {{{
fig, ax = genfig(5)
ax.set_title("Sves input response")
ax.set_xlabel("Input")
ax.set_ylabel("Sves")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( sim.index , sim['Sves[0]']['StotNative'] , label='Native'        , color='blue' )
ax.plot( sim.index , sim['Sves[0]']['StotOE']     , label='Overexpressed' , color='red' )
ax.legend(loc='center right')
showfig()
fig.savefig( "InputVsSves.pdf", transparent=True )
#}}}

# Diff Sves {{{
dsves = ( sim['Sves[1]'] - sim['Sves[0]'] ) / sim['gdm']
p1 = np.array( sim['p1']['StotNative'].tolist()).transpose()
dp1 =( p1[1] - p1[0]) / sim['gdm']['StotNative']
fig, ax = genfig(6)
ax.set_title("Diff Sves input response")
ax.set_xlabel("Input")
ax.set_ylabel("Diff")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.axhline( 0, color='black', lw=1 )
ax.plot( sim.index , dp1                 , label='Input p1'      , color='green' )
ax.plot( sim.index , dsves['StotNative'] , label='Native'        , color='blue' )
ax.plot( sim.index , dsves['StotOE']     , label='Overexpressed' , color='red' )
ax.legend(loc='center right')
showfig()
fig.savefig( "InputVsSvesDiff.pdf", transparent=True )
#}}}

# Sves vs MAPKpp {{{
fig, ax = genfig()
ax.set_title("Sves input response")
ax.set_xlabel("Sves")
ax.set_ylabel("MAPKpp")
ax.set_xlim(auto=True)
ax.set_ylim(0,1.01)
ax.plot( sim['Sves[0]']['StotOE']     , sim['MAPKpp']['StotOE']     , label='Overexpressed' , color='red' , lw=9)
ax.plot( sim['Sves[0]']['StotNative'] , sim['MAPKpp']['StotNative'] , label='Native'        , color='blue' )
ax.legend(loc='bottom right')
showfig()
#}}}

# }}}

# MI vs Scaffold {{{
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
showfig()
fig.savefig( "ScaffoldVsMAPKppMI.pdf", transparent=True )
# }}}

# MI vs Gradient {{{
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
showfig()
fig.savefig( "GradientVsMI.pdf", transparent=True )
# }}}

# Noco and Rab11DN {{{
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

fig, ax = genfig(2)
fig.delaxes( ax )
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
showfig()
fig.savefig( "rab11dn.pdf", transparent=True )

#}}}

# fig title {{{
fig = plt.gcf()
fig = plt.figure(3)
fig.canvas.set_window_title('tp = 1e-2')
#}}}

# time constant tp {{{
sim =             dose_response( { 'slevel' : 'StotOE', 'p4a':0, 'tp':1e0 } )
sim = sim.append( dose_response( { 'slevel' : 'StotOE', 'p4a':0, 'tp':1e-1} ))
sim = sim.append( dose_response( { 'slevel' : 'StotOE', 'p4a':0, 'tp':1e-2} ))
sim = sim.pivot( sim.index, 'tp' )

fig, ax = genfig(1)
ax = sim['MI'].plot()
ax.set_ylim(-2,2)
ax.get_figure().show()
showfig(1)
#}}}

# p4 sim {{{

# constant p4

# p4 func {{{
x = np.array( [0,1] )
#p4a = DEFAULT_PARAMS['p4a']
p4b = DEFAULT_PARAMS['p4b']
#p4n = DEFAULT_PARAMS['p4n']
w=600
dsves = np.linspace( -w, w, 100 )
p4 = np.array( [ p4_func( x, p4a, p4b, p4n, s ) for s in dsves ] )
p4 = p4.transpose()
fig, ax = genfig(1)
ax.plot( dsves , p4[0] , label='x = Back'  , color='black'  )
ax.plot( dsves , p4[1] , label='x = Front' , color='blue' )
ax.set_title("p4( x, dSves)")
ax.set_xlabel("dSves Level")
ax.set_ylabel("p4")
w=600
#ax.set_xlim(-w, w)
w=0.01
ax.set_ylim(p4b-p4a-w, p4b+p4a+w)
ax.legend(loc='center right')
showfig()
fig.savefig( pre+"constant_p4_func.pdf", transparent=True )
# }}}

# p4a zero / pos / neg {{{
sim = dose_response({'lbl' : 'Nz' , 'slevel' : 'StotNative' , 'p4a' : 0 }).append(
      dose_response({'lbl' : 'Oz' , 'slevel' : 'StotOE'     , 'p4a' : 0 })).append(
      dose_response({'lbl' : 'Np' , 'slevel' : 'StotNative' , 'p4a' : p4a })).append(
      dose_response({'lbl' : 'Op' , 'slevel' : 'StotOE'     , 'p4a' : p4a })).append(
      dose_response({'lbl' : 'Nn' , 'slevel' : 'StotNative' , 'p4a' :-p4a })).append(
      dose_response({'lbl' : 'On' , 'slevel' : 'StotOE'     , 'p4a' :-p4a }))
sim = sim.pivot( sim.index        , 'lbl' )


fig, ax = genfig(3)
ax.set_xlabel("Input")
ax.set_ylabel("Sves")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.set_title("Sves input response")
ax.axhline( 0, color='black', lw=1 )
ax.plot( sim.index , sim['Sves[0]']['Nz'] , label='Zero Amp Native'        , color=color_native , linestyle='solid' )
ax.plot( sim.index , sim['Sves[0]']['Np'] , label='Pos Amp Native'         , color=color_native , linestyle='dashed' )
ax.plot( sim.index , sim['Sves[0]']['Nn'] , label='Neg Amp Native'         , color=color_native , linestyle='dotted' )
ax.plot( sim.index , sim['Sves[0]']['Oz'] , label='Zero Amp Overexpressed' , color=color_oe     , linestyle='solid')
ax.plot( sim.index , sim['Sves[0]']['Op'] , label='Pos Amp Overexpressed'  , color=color_oe     , linestyle='dashed' )
ax.plot( sim.index , sim['Sves[0]']['On'] , label='Neg Amp Overexpressed'  , color=color_oe     , linestyle='dotted' )
ax.legend(loc='center right')
showfig()
fig.savefig( "p4a_sign_change_Sves.pdf", transparent=True )

fig, ax = genfig(4)
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(-5, 10)
ax.set_title("MI input response")
ax.axhline( 0, color='black', lw=1 )
ax.plot( sim.index , sim['MI']['Nz'] , label='Zero Amp Native'        , color=color_native , linestyle='solid' )
ax.plot( sim.index , sim['MI']['Np'] , label='Pos Amp Native'         , color=color_native , linestyle='dashed' )
ax.plot( sim.index , sim['MI']['Nn'] , label='Neg Amp Native'         , color=color_native , linestyle='dotted' )
ax.plot( sim.index , sim['MI']['Oz'] , label='Zero Amp Overexpressed' , color=color_oe     , linestyle='solid')
ax.plot( sim.index , sim['MI']['Op'] , label='Pos Amp Overexpressed'  , color=color_oe     , linestyle='dashed' )
ax.plot( sim.index , sim['MI']['On'] , label='Neg Amp Overexpressed'  , color=color_oe     , linestyle='dotted' )
ax.legend(loc='upper right')
showfig()
fig.savefig( "p4a_sign_change_MI.pdf", transparent=True )

# Diff Sves
dsves = ( sim['Sves[1]'] - sim['Sves[0]'] ) / sim['gdm']
p1 = np.array( sim['p1']['Nz'].tolist()).transpose()
dp1 =( p1[1] - p1[0]) / sim['gdm']['Nz']
fig, ax = genfig(5)
ax.set_title("Diff Sves input response")
ax.set_xlabel("Input")
ax.set_ylabel("Diff (Front - Back)")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.axhline( 0      , None        , None                           , color='black'      , lw=1 )
ax.plot( sim.index , dp1         , label='Input p1'               , color='green'      , lw=5 )
ax.plot( sim.index , dsves['Nz'] , label='Zero Amp Native'        , color=color_native , linestyle='solid' )
ax.plot( sim.index , dsves['Np'] , label='Pos Amp Native'         , color=color_native , linestyle='dashed' )
ax.plot( sim.index , dsves['Nn'] , label='Neg Amp Native'         , color=color_native , linestyle='dotted' )
ax.plot( sim.index , dsves['Oz'] , label='Zero Amp Overexpressed' , color=color_oe     , linestyle='solid')
ax.plot( sim.index , dsves['Op'] , label='Pos Amp Overexpressed'  , color=color_oe     , linestyle='dashed' )
ax.plot( sim.index , dsves['On'] , label='Neg Amp Overexpressed'  , color=color_oe     , linestyle='dotted' )
box = ax.get_position()
ax.set_position( [box.x0, box.y0, box.width*0.6, box.height] )
ax.legend(loc='upper right', bbox_to_anchor=(1.8,1) )
showfig()
fig.savefig( "p4a_InputVsSvesDiff.pdf", transparent=True )


# }}}

# coupled p4


# p4a zero / pos {{{
simz= dose_response({'lbl' : 'Nz' , 'slevel' : 'StotNative' , 'p4a' : 0 }).append(
      dose_response({'lbl' : 'Oz' , 'slevel' : 'StotOE'     , 'p4a' : 0 }))

p4a = 0.003
p4n = 2
pre = 'n_'
# sim and plots #{{{
sim = simz.append(
        dose_response({'lbl' : 'Np' , 'slevel' : 'StotNative' , 'p4a' : p4a , 'p4n' : p4n })).append(
        dose_response({'lbl' : 'Op' , 'slevel' : 'StotOE'     , 'p4a' : p4a , 'p4n' : p4n }))
sim = sim.pivot( sim.index, 'lbl' )

# p4 func {{{
x = np.array( [0,1] )
#p4a = DEFAULT_PARAMS['p4a']
p4b = DEFAULT_PARAMS['p4b']
#p4n = DEFAULT_PARAMS['p4n']
w=600
dsves = np.linspace( -w, w, 100 )
p4 = np.array( [ p4_func( x, p4a, p4b, p4n, s ) for s in dsves ] )
p4 = p4.transpose()
fig, ax = genfig(1)
ax.plot( dsves , p4[0] , label='x = Back'  , color='black'  )
ax.plot( dsves , p4[1] , label='x = Front' , color='blue' )
ax.set_title("p4( x, dSves)")
ax.set_xlabel("dSves Level")
ax.set_ylabel("p4")
w=600
#ax.set_xlim(-w, w)
w=0.01
ax.set_ylim(p4b-p4a-w, p4b+p4a+w)
ax.legend(loc='center right')
showfig()
fig.savefig( pre+"coupled_p4_func.pdf", transparent=True )
# }}}

# Sves#{{{
fig, ax = genfig(6)
ax.set_xlabel("Input")
ax.set_ylabel("Sves")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.set_title("Sves input response")
ax.axhline( 0, color='black', lw=1 )
ax.plot( sim.index , sim['Sves[0]']['Nz'] , label='Zero Amp Native'        , color=color_native , linestyle='solid' )
ax.plot( sim.index , sim['Sves[0]']['Np'] , label='Pos Amp Native'         , color=color_native , linestyle='dashed' )
ax.plot( sim.index , sim['Sves[0]']['Oz'] , label='Zero Amp Overexpressed' , color=color_oe     , linestyle='solid')
ax.plot( sim.index , sim['Sves[0]']['Op'] , label='Pos Amp Overexpressed'  , color=color_oe     , linestyle='dashed' )
ax.legend(loc='center right')
showfig()
fig.savefig( pre+"Sves_coupled_p4.pdf", transparent=True )
#}}}

# Diff Sves {{{
dsves = ( sim['Sves[1]'] - sim['Sves[0]'] ) / sim['gdm']
p1 = np.array( sim['p1']['Nz'].tolist()).transpose()
dp1 =( p1[1] - p1[0]) / sim['gdm']['Nz']
fig, ax = genfig(7)
ax.set_title("Diff Sves input response")
ax.set_xlabel("Input")
ax.set_ylabel("Diff (Front - Back)")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
#ax.set_ylim(0,20)
ax.axhline( 0      , None        , None                           , color='black'      , lw=1 )
ax.plot( sim.index , dp1         , label='Input p1'               , color='green'      , lw=5 )
ax.plot( sim.index , dsves['Nz'] , label='Zero Amp Native'        , color=color_native , linestyle='solid' )
ax.plot( sim.index , dsves['Np'] , label='Pos Amp Native'         , color=color_native , linestyle='dashed' )
ax.plot( sim.index , dsves['Oz'] , label='Zero Amp Overexpressed' , color=color_oe     , linestyle='solid')
ax.plot( sim.index , dsves['Op'] , label='Pos Amp Overexpressed'  , color=color_oe     , linestyle='dashed' )
box = ax.get_position()
ax.set_position( [box.x0, box.y0, box.width*0.6, box.height] )
ax.legend(loc='upper right', bbox_to_anchor=(1.8,1) )
showfig()
fig.savefig( pre+"dSves_coupled_p4.pdf", transparent=True )
#}}}

# MI {{{
fig, ax = genfig(8)
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(-5, 10)
ax.set_title("MI input response")
ax.axhline( 0, color='black', lw=1 )
ax.plot( sim.index , sim['MI']['Nz'] , label='Zero Amp Native'        , color=color_native , linestyle='solid' )
ax.plot( sim.index , sim['MI']['Np'] , label='Pos Amp Native'         , color=color_native , linestyle='dashed' )
ax.plot( sim.index , sim['MI']['Oz'] , label='Zero Amp Overexpressed' , color=color_oe     , linestyle='solid')
ax.plot( sim.index , sim['MI']['Op'] , label='Pos Amp Overexpressed'  , color=color_oe     , linestyle='dashed' )
ax.legend(loc='upper right')
showfig()
fig.savefig( pre+"MI_coupled_p4.pdf", transparent=True )
#}}}

#}}}

# }}}

# old p4 code
# p4a magnitude {{{
sim = dose_response({'lbl' : 'N'   , 'slevel' : 'StotNative' }).append(
      dose_response({'lbl' : 'O0'  , 'slevel' : 'StotOE', 'p4a':-0.010 })).append(
      dose_response({'lbl' : 'O1'  , 'slevel' : 'StotOE', 'p4a':-0.005 })).append(
      dose_response({'lbl' : 'O2'  , 'slevel' : 'StotOE', 'p4a':-0.001 })).append(
      dose_response({'lbl' : 'O3'  , 'slevel' : 'StotOE', 'p4a': 0.000 }))
sim = sim.pivot( sim.index, 'lbl' )

fig, ax = genfig(3)
ax.set_title("MI input response")
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(-5, 10)
ax.axhline( 0, color='black', lw=1 )
ax.plot( sim.index, sim['MI']['N'],  label='Pos Amp Native', color='red' )
ax.plot( sim.index, sim['MI']['O0'],label='Neg Amp Overexpressed', color='blue' )
ax.plot( sim.index, sim['MI']['O1'],label='Neg Amp Overexpressed', color='cyan' )
ax.plot( sim.index, sim['MI']['O2'],label='Neg Amp Overexpressed', color='green' )
ax.plot( sim.index, sim['MI']['O3'],label='Neg Amp Overexpressed', color='grey' )
ax.legend()
showfig()
# }}}

# no p4a, amp but no transition {{{
sim = dose_response({'lbl' : 'N', 'slevel' : 'StotNative' }).append(
      dose_response({'lbl' : 'OE', 'slevel' : 'StotOE' })).append(
      dose_response({'lbl' : 'Na', 'p4a':0, 'slevel' : 'StotNative' })).append(
      dose_response({'lbl' : 'OEa', 'p4a':0, 'slevel' : 'StotOE' }))
sim = sim.pivot( sim.index, 'lbl' )

fig, ax = genfig()
ax.set_title("MI input response")
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(-5, 10)
ax.plot( sim.index, sim['MI']['N'],  label='Amp Native', color='red' )
ax.plot( sim.index, sim['MI']['Na'], label='No Amp Native', color='pink' )
ax.plot( sim.index, sim['MI']['OE'], label='Amp Overexpressed', color='blue' )
ax.plot( sim.index, sim['MI']['OEa'],label='No Amp Overexpressed', color='cyan' )
ax.legend()
fig.canvas.draw()
fig.show()
fig.savefig( "MI_Amp_comparison.pdf", transparent=True )

# Sves
fig, ax = genfig()
ax.set_title("Sves input response")
ax.set_xlabel("Input")
ax.set_ylabel("Sves")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( sves.index, sves['N'],  label='Amp Native', color='red' )
ax.plot( sves.index, sves['Na'], label='No Amp Native', color='pink' )
ax.plot( sves.index, sves['OE'], label='Amp Overexpressed', color='blue' )
ax.plot( sves.index, sves['OEa'],label='No Amp Overexpressed', color='cyan' )
ax.legend(loc='center right')
fig.canvas.draw()
fig.show()

# diff Sves
fig, ax = genfig(2)
ax.set_title("Diff Sves input response")
ax.set_xlabel("Input")
ax.set_ylabel("Sves1 - Sves0")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( sves.index, sves1['N']   - sves0['N'],  label='Amp Native', color='red' )
ax.plot( sves.index, sves1['Na']  - sves0['Na'], label='No Amp Native', color='pink' )
ax.plot( sves.index, sves1['OE']  - sves0['OE'], label='Amp Overexpressed', color='blue' )
ax.plot( sves.index, sves1['OEa'] - sves0['OEa'],label='No Amp Overexpressed', color='cyan' )
ax.legend(loc='bottom left')
fig.canvas.draw()
fig.show(2)

# }}}

# single sigmoid {{{
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
# }}}

# }}}

# sigmoid {{{
dSves = np.linspace( -600, 600, 100)
y = np.tanh( dSves/200. )

fig, ax = genfig(1)
ax.set_title("")
ax.set_xlabel("dSves")
ax.set_ylabel("sig")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( dSves , y , label='' )
ax.legend()
showfig()
#fig.savefig( "temp.pdf", transparent=True )
# }}}

# Plot snippet {{{
fig, ax = genfig()
ax.set_title("")
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_xlim(auto=True)
ax.set_ylim(auto=True)
ax.plot( x , y , label='' )
ax.legend()
showfig()
#fig.savefig( "temp.pdf", transparent=True )
# }}}
