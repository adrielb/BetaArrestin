from BetaArrestin import *

sim = scaffold_response( snum=250 )

s = sim[ ['l', 'Stot', 'MAPKpp', 'MI', 'StotNative'] ]

s.to_csv( 'ScaffoldInputVsMAPKppMI.csv', index=False )

simStot = s.groupby( 'Stot' ).mean()
simStot['MAPKpp_Norm'] = simStot['MAPKpp'] / simStot['MAPKpp'].max()
simStot['MI_Norm']     = simStot['MI']     / simStot['MI'].max()
simStot.index = simStot.index / simStot['StotNative']
simStot.index.name = 'Relative Scaffold'

simStot.to_csv( 'ScaffoldVsMAPKppMI.csv' )
