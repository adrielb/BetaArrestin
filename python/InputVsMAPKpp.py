from BetaArrestin import *


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
