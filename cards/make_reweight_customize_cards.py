import os
import json
import argparse
import random

def make_reweight_card(nrwgt, rwgt_dict, name):
    '''Creates the reweight card to make a gridpack. 
    Parameters
    ----------
    nrwgt: int
        Number of reweight points to calculate (doesn't include starting point or SM)
    rwgt_dict: dictionary
        dictioanry of the WC starting point
        {'wc0': val0, 'wc1': val1, 'wc2': val2, ...}
    name: file name that will be appended with "_reweight_card.dat"
    '''
    
    # Start reweight card text
    rwgtCards = ''
    rwgtCards = '# Reference point: ' + str(rwgt_dict) + '\n\n'
    rwgtCards = rwgtCards + 'change rwgt_dir rwgt'+ '\n'+ '\n'

    # save reference point
    rwgtCards = rwgtCards + 'launch --rwgt_name=reference_point'+ '\n'
    rwgtCards = rwgtCards +'\n'

    # save SM point
    rwgtCards = rwgtCards + 'launch --rwgt_name=sm_point'+ '\n'
    for wc in rwgt_dict.keys():
        rwgtCards = rwgtCards +'    set param_card ' + wc + ' 0.0 ' + '\n'

    n=0
    # create all other reweight points
    for i in range (nrwgt):
        # generate random WC point within +- 2*starting point
        randomWC = {}
        for wc in rwgt_dict.keys(): 
            r = random.uniform(-2*rwgt_dict[wc], 2*rwgt_dict[wc])
            randomWC[wc]=round(r,3)

        rwgtCards = rwgtCards + '\n'
        rwgtCards = rwgtCards + 'launch --rwgt_name=EFTrwgt' + str(n) + '_'

        for wc in rwgt_dict.keys():
            idWgt = str(randomWC[wc])
            idWgt = idWgt.replace(".", "p")
            idWgt = idWgt.replace("-", "m")
            rwgtCards = rwgtCards + wc + '_' + idWgt + '_'
        rwgtCards = rwgtCards[:-1]
        rwgtCards = rwgtCards + '\n'

        for wc in rwgt_dict.keys():
            rwgtCards = rwgtCards +'    set param_card ' + wc + ' ' + str(randomWC[wc])  + '\n'

        rwgtCards = rwgtCards +'\n'

        n += 1 

    fname = name+'_reweight_card.dat'
    open(fname, 'wt').write(rwgtCards)
    print("reweight card saved to ", fname)


def make_customize_card(rwgt_dict, name):

    customizecards = 'set param_card LambdaSMEFT 1.000000e+03 \n'
    customizecards = customizecards + 'set param_card mass   6  172.5\n'
    customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
    customizecards = customizecards + 'set param_card mass   25 125.0\n'

    for wc in rwgt_dict.keys():
        customizecards = customizecards + 'set param_card ' + wc + ' ' + str(rwgt_dict[wc]) + '\n'

    # print("customize cards text = \n", customizecards)
    fname = name+'_customizecards.dat'
    open(fname, 'wt').write(customizecards)
    print("customize card saved to ", fname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line options parser")
    parser.add_argument("jsonFile", help="Json that contains dictionaries of reweight points: {rwgt_pt_name: {dict of WC points}}")
    parser.add_argument("--nrwgt", default=2, help="Number of reweight points")
    args = parser.parse_args()

    jsonFile = args.jsonFile
    nrwgt = args.nrwgt

    with open(jsonFile) as jf: 
        rwgt_dicts = json.load(jf)

    print(rwgt_dicts)

    for item in rwgt_dicts:
        make_reweight_card(nrwgt, rwgt_dicts[item], "tW_"+item)
        make_customize_card(rwgt_dicts[item], "tW_"+item)
