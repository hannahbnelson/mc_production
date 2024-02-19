import os
import random

# List of processes to make cards for
process_list = ['orig_st']
#scanValues = 200
scanValues = 185

# Starting Point for dim6top from Reza
#couplings = {'ctG':0.7, 'cQq83':9.0, 'cQq81':7.0, 'cQu8':9.5,
#            'cQd8':12.0, 'ctq8':7.0, 'ctu8':9.0, 'ctd8':12.4,
#            'cQq13':4.1, 'cQq11':4.2, 'cQu1':5.5, 'cQd1':7.0,
#            'ctq1':4.4, 'ctu1':5.4, 'ctd1':7.0}

# Starting Point 1: Reza's initial starting point
couplings = {'ctGIm': 0.7, 'ctGRe':0.7, 'cQj38':9.0, 'cQj18':7.0,
            'cQu8':9.5, 'cQd8':12.0, 'ctj8':7.0, 'ctu8':9.0,
            'ctd8':12.4, 'cQj31':3.0, 'cQj11':4.2, 'cQu1':5.5,
            'cQd1':7.0, 'ctj1':4.4, 'ctu1':5.4, 'ctd1':7.0}

# Starting Point 2: Robert's starting point
#couplings = {'ctGIm': 1.0, 'ctGRe':1.0, 'cQj38':3.0, 'cQj18':3.0,
#            'cQu8':3.0, 'cQd8':3.0, 'ctj8':3.0, 'ctu8':3.0,
#            'ctd8':3.0, 'cQj31':3.0, 'cQj11':3.0, 'cQu1':3.0,
#            'cQd1':3.0, 'ctj1':3.0, 'ctu1':3.0, 'ctd1':3.0}

# Starting Point 3: 1/4 of Reza's initial starting point
#couplings = {'ctGIm': 0.25, 'ctGRe':0.18, 'cQj38':2.25, 'cQj18':1.75,
#            'cQu8':2.4, 'cQd8':3.0, 'ctj8':1.75, 'ctu8':2.25,
#            'ctd8':3.1, 'cQj31':0.75, 'cQj11':1.1, 'cQu1':1.38,
#            'cQd1':1.75, 'ctj1':1.1, 'ctu1':1.35, 'ctd1':1.75}

# Starting Point 4: 1/2 of Robert's starting point, ctG sign flipped 
#couplings = {'ctGIm': -0.5, 'ctGRe':-0.5, 'cQj38':1.5, 'cQj18':1.5,
#            'cQu8':1.5, 'cQd8':1.5, 'ctj8':1.5, 'ctu8':1.5,
#            'ctd8':1.5, 'cQj31':1.5, 'cQj11':1.5, 'cQu1':1.5,
#            'cQd1':1.5, 'ctj1':1.5, 'ctu1':1.5, 'ctd1':1.5}

# Starting Point 5: Values based on limits that we have set already, sign of ctG flipped
#couplings = {'ctGIm': -1.2, 'ctGRe':-1.2, 'cQj38':6.5, 'cQj18':5.0,
#            'cQu8':4.0, 'cQd8':9.4, 'ctj8':3.5, 'ctu8':4.75,
#            'ctd8':9.3, 'cQj31':3.1, 'cQj11':3.1, 'cQu1':3.5,
#            'cQd1':5.0, 'ctj1':2.8, 'ctu1':3.6, 'ctd1':5.0}

# Starting point for only ctj8 sample
#couplings = {'ctj8': 7.0}


for item in process_list:

    ### Create Customizecards Card ###
    customizecards = ''
    customizecards += 'set param_card LambdaSMEFT 1.000000e+03 \n'
    customizecards += 'set param_card mass   6  172.5 \n'
    customizecards += 'set param_card yukawa 6  172.5 \n'
    customizecards += 'set param_card mass   25 125.0 \n'
    customizecards += 'set param_card SMEFTcpv 8 1.0e+00 \n'

    for key in couplings:
        customizecards = customizecards + 'set param_card ' + str(key) + ' ' + str(couplings[key]) + '\n'
    open(item+'_customizecards.dat', 'wt').write(customizecards)


    ### Create Reweight Card ###
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
    open(item+'_reweight_card.dat', 'wt').write(rwgtCards)
