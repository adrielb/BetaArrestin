from BetaArrestin import *
from FigDisplay import *

sims = pd.read_csv('p4effects.csv')
sims = sims.set_index( ['lbl','Input'] )

displayfig()

fig, ax = genfig()

index = sims.loc['Nw'].index
index

ax.plot( index, sims['MAPKpp'].loc['Nw'], label='MAPKpp Native'  , color='red' )

showfig(True)



def plotMAPKpp( idx ):
    name = p[idx]
    sim = sims.loc[ name ]
    index = sim['MAPKpp']['StotNative'].index
    fig, ax = genfig(idx+1)
    ax.set_title( name + " p3" )
    ax.set_xlabel("Input")
    ax.set_ylabel("MAPKpp")
    ax.set_xlim(auto=True)
    ax.set_ylim(0      , 1.35)
    ax.plot( index , sim['MAPKpp']['StotNative'] , label='MAPKpp Native'  , color='red' )
    ax.plot( index , sim['MAPKpp']['StotOE']     , label='MAPKpp Overexp' , color='blue' )
    ax.legend(loc='upper left')
    # MI twin axes
    ax = ax.twinx()
    ax.set_ylabel("MI")
    ax.axhline( 0      , color='black'           , lw=1 )
    ax.axvline( 1   , color='black'           , linewidth=10                )
    ax.axvline( 1   , color='white'           , linewidth=10               , linestyle='dashed' )
    ax.plot( index , sim['MI']['StotNative'] , label='MI Native'  , color='red'          , linestyle='dashed' )
    ax.plot( index , sim['MI']['StotOE']     , label='MI Overexp' , color='blue'         , linestyle='dashed' )
    ax.set_ylim(-2     , 10)
    ax.grid()
    ax.legend(loc='upper right')
    # p3 inset
    rect = [0.61, 0.54, 0.25, 0.2]
    ax = fig.add_axes(rect)
    ax.set_xlabel("Smem")
    ax.set_ylabel("p3")
    ax.plot( Smem, p3funcs['Bell'] , color='lightgreen' )
    ax.plot( Smem, p3funcs[name] , color='green' )
    ax.grid()
    fig.savefig( "p4effects_" + name + ".pdf", transparent=True )
    showfig(True)
