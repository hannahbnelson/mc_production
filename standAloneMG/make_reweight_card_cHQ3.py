import os
import json
import argparse

def make_reweight_card(wc_names, scan_points, profiled_dict, outname):

    # Start reweight card text
    rwgtCards = ''
    rwgtCards = rwgtCards + 'change rwgt_dir rwgt'+ '\n'+ '\n'

    # save SM point
    rwgtCards = rwgtCards + 'launch --rwgt_name=sm_point'+ '\n'
    rwgtCards += f"    set param_card cHQ3 0.0 \n"
    for wc in wc_names:
        rwgtCards = rwgtCards +'    set param_card ' + wc + ' 0.0 ' + '\n'
    rwgtCards = rwgtCards +'\n'

    n=0 
    for i in scan_points:
        for wc in wc_names:
            temp1 = str(i)
            temp1 = temp1.replace(".", "p")
            temp1 = temp1.replace("-", "m")

            temp2 = str(profiled_dict[wc])
            temp2 = temp2.replace(".", "p")
            temp2 = temp2.replace("-", "m")

            rwgtCards += f"launch --rwgt_name=EFTrwgt{n}_cHQ3_{temp1}_{wc}_{temp2}\n"

            rwgtCards += f"    set param_card cHQ3 {i} \n"

            for j in wc_names:
                if wc==j:
                    rwgtCards += f"    set param_card {j} {profiled_dict[wc]} \n"
                else:rwgtCards += f"    set param_card {j} 0.0 \n"

            rwgtCards = rwgtCards +'\n'
            n += 1

    fname = f"{outname}_reweight_card.dat"
    open(fname, 'wt').write(rwgtCards)
    print(f"card saved to: {fname}")

if __name__ == "__main__":

    wc_names = ["ctGIm", "ctGRe", "ctWRe", "cleQt3Re", "cleQt1Re", "cQl3", "cbWRe", "cHtbRe"]
    # wc_names = ["ctGIm", "ctGRe", "cHQ3", "ctWRe", "cleQt3Re", "cleQt1Re", "cQl3", "cbWRe", "cHtbRe"]
    scan_points = [-10.0, -7.0, -4.0, -2.0, 2.0, 4.0, 7.0, 10.0]
    profiled_points = {"ctGIm":-1.0, "ctGRe": -1.0, "cHQ3": 2.0, "ctWRe":-2.0, "cleQt3Re":5.0, "cleQt1Re":10.0, "cQl3":5.0, "cbWRe":-3.0, "cHtbRe":3.0}

    make_reweight_card(wc_names, scan_points, profiled_points, "tW_cHQ3")