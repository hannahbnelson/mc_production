import os
import random

# List of processes to make cards for
process_list = ['tt_LO_SMEFT', 'ttJets_LO_SMEFT']

for item in process_list:

    ### Create Customizecards Card ###
    couplings =['ctG','cQq83','cQq81','cQu8','cQd8','ctq8','ctu8','ctd8','cQq13','cQq11','cQu1','cQd1','ctq1','ctu1','ctd1']

    Ivalue    = [0.7   ,9.0    ,7.0    ,9.5    ,12.0  ,7.0  ,9.0   ,12.4  ,4.1    ,4.2    ,5.5   ,7.0   ,4.4   ,5.4   ,7.0  ]
    customizecards = ''
    customizecards = customizecards + 'set param_card mass   6  172.5\n'
    customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
    customizecards = customizecards + 'set param_card mass   25 125.0\n'

    for gWC in couplings:
        customizecards = customizecards + 'set param_card '+gWC+ ' ' + str(Ivalue[couplings.index(gWC)]) + '\n'    
    open('customizecards.dat', 'wt').write(customizecards)


    ### Create Reweight Card ###
    scanValues = 144
    n=-1
    rwgtCards = ''
    rwgtCards = rwgtCards + 'change rwgt_dir rwgt'+ '\n'+ '\n'

    # dummy_point
    rwgtCards = rwgtCards + 'launch --rwgt_name=reference_point'+ '\n'
    rwgtCards = rwgtCards +'\n'

    # other points
    for v in range(scanValues):
        randomWC = []
        for WC1 in couplings:
            r = random.uniform(-2*Ivalue[couplings.index(WC1)], 2*Ivalue[couplings.index(WC1)])
            randomWC.append(round(r,3))
        n  = n+1
        rwgtCards = rwgtCards + '\n'
        rwgtCards = rwgtCards + 'launch --rwgt_name=EFTrwgt' + str(n) + '_'
        for WC1 in couplings:
            idWgt = str(randomWC[couplings.index(WC1)])
            idWgt = idWgt.replace(".", "p" )
            idWgt = idWgt.replace("-", "m" )        
            rwgtCards = rwgtCards + WC1 + '_' + idWgt + '_'
        rwgtCards = rwgtCards[:-1]
        rwgtCards = rwgtCards + '\n'
        for WC1 in couplings:
            rwgtCards = rwgtCards +'    set param_card ' + WC1 + ' ' + str(randomWC[couplings.index(WC1)])  + '\n'
    rwgtCards = rwgtCards +'\n'

    # SM Point
    rwgtCards = rwgtCards + 'launch --rwgt_name=sm_point'+ '\n'
    for WC1 in couplings:
        rwgtCards = rwgtCards +'    set param_card ' + WC1 + ' 0.0 ' + '\n'
    open('reweight_card.dat', 'wt').write(rwgtCards)


    ### Create Process Card ###
    proc_card = ''
    dir_name = item
    os.system('mkdir '+dir_name)

    proc_card = '' + '\n'
    proc_card = proc_card + 'import model SMEFTatNLO-LO' + '\n'
    proc_card = proc_card + 'define p = g u c d s u~ c~ d~ s~ b b~' + '\n'
    proc_card = proc_card + 'define j = g u c d s u~ c~ d~ s~ b b~' + '\n'
    proc_card = proc_card + 'define l+ = e+ mu+ ta+' + '\n'
    proc_card = proc_card + 'define l- = e- mu- ta-' + '\n'
    proc_card = proc_card + 'define vl = ve vm vt' + '\n'
    proc_card = proc_card + 'define vl~ = ve~ vm~ vt~' + '\n'
    proc_card = proc_card + 'generate p p > t  t~ NP=2 QCD=2 QED=0 , (t > w+ b NP=0, w+ > l+ vl NP=0), (t~ > w- b~ NP=0, w- > l- vl~ NP=0) @0' + '\n'
    if item == 'ttJets_LO_SMEFT':
        proc_card = proc_card + 'add process p p > t  t~ j NP=2 QCD=3 QED=0 , (t > w+ b NP=0, w+ > l+ vl NP=0), (t~ > w- b~ NP=0, w- > l- vl~ NP=0) @1' + '\n'
    proc_card = proc_card + 'output ' + dir_name + ' -f -nojpeg'
    open('proc_card.dat', 'wt').write(proc_card)


    ### Move Created Cards to New Directory ###
    cards_to_make = ['proc_card.dat', 'reweight_card.dat', 'customizecards.dat', 'run_card.dat', 'extramodels.dat']
    for item in cards_to_make:
        if item == "run_card.dat": 
            os.system('cp ' + dir_name + '_' + item + ' ' + dir_name+'/'+dir_name+'_'+item)
        else: 
            os.system('cp ' + item + ' ' + dir_name+'/'+dir_name+'_'+item)

    # remove cards unique to process from current directory 
    os.system('rm proc_card.dat')
    os.system('rm reweight_card.dat')
    os.system('rm customizecards.dat')
