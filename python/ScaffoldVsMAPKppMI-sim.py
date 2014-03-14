from BetaArrestin import *

sim = scaffold_response( start=0.5, snum=50 )

s = sim[ ['l', 'Stot', 'MAPKpp', 'MI', 'StotNative'] ]

s.to_csv( 'ScaffoldInputVsMAPKppMI.csv', index=False )

simStot = s.groupby( 'Stot' ).mean()
simStot['MAPKpp_Norm'] = simStot['MAPKpp'] - simStot['MAPKpp'][0]
simStot['MAPKpp_Norm'] = simStot['MAPKpp_Norm'] / simStot['MAPKpp_Norm'].max()
simStot['MI_Norm'] = simStot['MI'] - simStot['MI'].min()
simStot['MI_Norm'] = simStot['MI_Norm'] / simStot['MI_Norm'].max()

simStot.index = simStot.index / simStot['StotNative']
simStot.index.name = 'Relative Scaffold'
simStot.to_csv( 'ScaffoldVsMAPKppMI.csv' )
