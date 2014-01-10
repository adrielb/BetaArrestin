from BetaArrestin import *

Smem = np.arange( 0, 3, 0.01)

def p3_eval( params ):
    p = DEFAULT_PARAMS.copy()
    p.update( params )
    p3a  = p['p3a']
    p3b  = p['p3b']
    p3c  = p['p3c']
    p3d  = p['p3d']
    p3e  = p['p3e']
    p3   = p3_func( Smem, p3a, p3b, p3c, p3d, p3e )
    return p3

p3_const = {'p3a' : 0.3,
            'p3b' : 0,
            'p3d' : 1 }

p3_rise = {'p3d' : 1}

p3_fall = {'p3a' : 1,
           'p3b' : 0}

fig, ax = genfig()
ax.set_xlabel("Smem")
ax.set_ylabel("p3")
ax.set_xlim(auto=True)
ax.set_ylim(0, 0.6)
ax.set_title("p3: Smem to Sves transport")
ax.plot( Smem , p3_eval( DEFAULT_PARAMS ) ,  label="model" )
ax.plot( Smem , p3_eval( p3_const )       ,  label="constant" )
ax.plot( Smem , p3_eval( p3_rise )        ,  label="rise" )
ax.plot( Smem , p3_eval( p3_fall )        ,  label="fall" )
ax.legend()
showfig()

fig.savefig( "p3effects.pdf", transparent=True )

def sim( params ):
    p_native           = params.copy()
    p_oe               = params.copy()
    p_native['slevel'] = 'StotNative'
    p_oe['slevel']     = 'StotOE'

    sim = dose_response(p_native).append(
          dose_response(p_oe) )
    sim = sim.pivot( sim.index, 'slevel' )

    return sim

sims = map( sim, [ {}, p3_const, p3_rise, p3_fall ])
sims[0].name = "Bell"
sims[1].name = "Constant"
sims[2].name = "Rising"
sims[3].name = "Falling"

def plotMAPKpp( idx = 1 ):
    sim = sims[idx]
    fig, ax = genfig(idx+1)
    ax.set_title(sim.name + " p3" )
    ax.set_xlabel("Input")
    ax.set_ylabel("MAPKpp")
    ax.set_xlim(auto=True)
    ax.set_ylim(0      , 1.35)
    ax.plot( sim.index , sim['MAPKpp']['StotNative'] , label='MAPKpp Native'  , color='red' )
    ax.plot( sim.index , sim['MAPKpp']['StotOE']     , label='MAPKpp Overexp' , color='blue' )
    ax.legend()
    # MI twin axes
    ax = ax.twinx()
    ax.set_ylabel("MI")
    ax.axhline( 0      , color='black'           , lw=1 )
    ax.plot( sim.index , sim['MI']['StotNative'] , label='MI Native'  , color='red' , linestyle='dashed'  )
    ax.plot( sim.index , sim['MI']['StotOE']     , label='MI Overexp' , color='blue'  , linestyle='dashed'  )
    ax.set_ylim(-2     , 10)
    ax.grid()
    ax.legend(loc='upper left')
    # p3 inset
    p3 = sim.iloc[0].swaplevel(0,1)['StotNative']
    rect = [0.55, 0.55, 0.3, 0.2]
    ax = fig.add_axes(rect)
    ax.set_xlabel("Smem")
    ax.set_ylabel("p3")
    ax.plot( Smem, p3_eval({}) , color='lightgreen' )
    ax.plot( Smem, p3_eval(p3) , color='green' )
    ax.grid()
    fig.savefig( "p3effects_" + sim.name + ".pdf", transparent=True )
    showfig()

map( plotMAPKpp,  range(4) )

#def plotMI( idx =1 ):
    #sim = sims[idx]
    #fig, ax = genfig(idx+5)
    #ax.set_title("MI " + sim.name )
    #ax.set_xlabel("Input")
    #ax.set_ylabel("MI")
    #ax.set_xlim(auto=True)
    #ax.set_ylim(-5, 10)
    #ax.axhline( 0, color='black', lw=1 )
    #ax.plot( sim.index , sim['MI']['StotNative'] , label='Native'        , color='blue' )
    #ax.plot( sim.index , sim['MI']['StotOE']     , label='Overexpressed' , color='red' )
    #ax.legend()
    ##fig.savefig( "InputVsMI.pdf", transparent=True )
    #showfig()

#map( plotMI, range( 4 ) )
