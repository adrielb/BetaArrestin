from BetaArrestin import *
from FigDisplay import *

sim = pd.read_csv('InputVsMAPKpp.csv')
sim = sim.set_index( ['Input'] )
sim = sim.pivot( sim.index, 'slevel' )

#displayfig()

colorN = 'blue'
colorO = 'red'

# MAPKpp {{{
fig, ax = genfig()
ax.set_title("MAPKpp input response")
ax.set_xlabel("Input")
ax.set_ylabel("MAPKpp")
ax.set_xlim(0.5, 1)
ax.set_ylim(0.5, 0.85)
ax.plot( sim.index , sim['MAPKpp']['StotNative'] , label='Native'        , color=colorN )
ax.plot( sim.index , sim['MAPKpp']['StotOE']     , label='Overexpressed' , color=colorO )
ax.legend()
fig.savefig( "InputVsMAPKpp.pdf", transparent=True )
showfig()
#}}}

# MI {{{
fig, ax = genfig(2)
ax.set_title("MI input response")
ax.set_xlabel("Input")
ax.set_ylabel("MI")
ax.set_xlim(auto=True)
ax.set_ylim(-2, 6)
ax.set_xlim(0.5, 1)
ax.axhline( 0, color='black', lw=1 )
ax.plot( sim.index , sim['MI']['StotNative'] , label='Native'        , color=colorN )
ax.plot( sim.index , sim['MI']['StotOE']     , label='Overexpressed' , color=colorO )
ax.legend()
fig.savefig( "InputVsMI.pdf", transparent=True )
showfig(2)
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
fig.savefig( "InputVsSmem.pdf", transparent=True )
showfig()
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
showfig(-1)
#}}}
