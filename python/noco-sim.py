from BetaArrestin import *

#ctrl = dose_response( { 'slevel' : 'StotNative'} )

ctrl = pd.read_csv('InputVsMAPKpp.csv')
ctrl = ctrl.set_index( 'slevel' )
#ctrl = ctrl.set_index( ['slevel', 'Input'] )
ctrl = ctrl[['Input','MAPKpp']].loc['StotNative']
ctrl['name'] = 'ctrl'


p4b = DEFAULT_PARAMS['p4b'] * 0.2
noco = dose_response( { 'slevel' : 'StotNative', 'p4b': p4b } )
noco = noco.reset_index()
noco.rename(columns={'l':'Input'}, inplace=True)
noco['name'] = 'noco'


csv = pd.DataFrame()
csv = csv.append( noco[ ['name', 'Input', 'MAPKpp'] ] )
csv = csv.append( ctrl, ignore_index=True )
csv.to_csv('noco.csv',index=False)

