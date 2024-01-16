import os
import random

# List of processes to make cards for
process_list = ['TT1j2l_ctj8only']


#couplings = {'ctG':0.7, 'cQq83':9.0, 'cQq81':7.0, 'cQu8':9.5,
#            'cQd8':12.0, 'ctq8':7.0, 'ctu8':9.0, 'ctd8':12.4,
#            'cQq13':4.1, 'cQq11':4.2, 'cQu1':5.5, 'cQd1':7.0,
#            'ctq1':4.4, 'ctu1':5.4, 'ctd1':7.0}

#couplings = {'ctGIm': 1, 'ctGRe':0.7, 'cQj38':9.0, 'cQj18':7.0, 
#            'cQu8':9.5, 'cQd8':12.0, 'ctj8':7.0, 'ctu8':9.0, 
#            'ctd8':12.4, 'cQj31':3.0, 'cQj11':4.2, 'cQu1':5.5, 
#            'cQd1':7.0, 'ctj1':4.4, 'ctu1':5.4, 'ctd1':7.0}

couplings = {'ctj8': 7.0}

scanValues = 10
#scanValues = 183

for item in process_list:

    n=-1
    rwgtCards = ''
    rwgtCards = rwgtCards + 'change rwgt_dir rwgt'+ '\n'+ '\n'

    # dummy_point
    rwgtCards = rwgtCards + 'launch --rwgt_name=reference_point'+ '\n'
    rwgtCards = rwgtCards +'\n'

    # other points
    for v in range(scanValues):
        randomWC = {}
        for WC in couplings:
            r = random.uniform(-2*couplings[WC], 2*couplings[WC])
            randomWC[WC]=round(r,3)
        n  = n+1
        rwgtCards = rwgtCards + '\n'
        rwgtCards = rwgtCards + 'launch --rwgt_name=EFTrwgt' + str(n) + '_'
        for WC in couplings:
            idWgt = str(randomWC[WC])
            idWgt = idWgt.replace(".", "p" )
            idWgt = idWgt.replace("-", "m" )
            rwgtCards = rwgtCards + WC + '_' + idWgt + '_'
        rwgtCards = rwgtCards[:-1]
        rwgtCards = rwgtCards + '\n'
        for WC in couplings:
            rwgtCards = rwgtCards +'    set param_card ' + WC + ' ' + str(randomWC[WC])  + '\n'
    rwgtCards = rwgtCards +'\n'

    # SM Point
    rwgtCards = rwgtCards + 'launch --rwgt_name=sm_point'+ '\n'
    for WC in couplings:
        rwgtCards = rwgtCards +'    set param_card ' + WC + ' 0.0 ' + '\n'
    open('new_reweight_card.dat', 'wt').write(rwgtCards)
