from BetaArrestin import *

ctrl = pd.read_csv('InputVsMAPKpp.csv')
ctrl = ctrl[ctrl['slevel'] == 'StotNative']
ctrl = ctrl[['Input','MI']]
ctrl['name'] = 'ctrl'


rab11dn = dose_response( { 'slevel' : 'StotNative', 'p4a':0 } )

rab11dn = rab11dn.reset_index()
rab11dn.rename(columns={'l':'Input'}, inplace=True)
rab11dn = rab11dn[['Input','MI']]
rab11dn['name'] = 'rab11dn'

csv = pd.DataFrame()
csv = csv.append( ctrl    , ignore_index=True )
csv = csv.append( rab11dn , ignore_index=True )

csv.to_csv('rab11dn.csv', index=False)
