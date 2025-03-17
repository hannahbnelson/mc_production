import os
import json
import argparse

def make_reweight_card(wc_names, scan_points, outname):

    # Start reweight card text
    rwgtCards = ''
    rwgtCards = rwgtCards + 'change rwgt_dir rwgt'+ '\n'+ '\n'

    # save SM point
    rwgtCards = rwgtCards + 'launch --rwgt_name=sm_point'+ '\n'
    for wc in wc_names:
        rwgtCards = rwgtCards +'    set param_card ' + wc + ' 0.0 ' + '\n'

    n = 0
    for wc in wc_names: 
        for i in scan_points:
            if wc=='ctGRe' or wc=='ctGIm':
                i = i/10.0
            # rwgtCards += f"launch -n {wc}={i}\n"
            temp = str(i)
            temp = temp.replace(".", "p")
            temp = temp.replace("-", "m")
            rwgtCards += f"launch --rwgt_name=EFTrwgt{n}_{wc}_{temp} \n"
            # rwgtCards += f
            # rwgt_name = f"{wc.replace(".", "p").replace("-", "m")}_{i.replace(".", "p").replace("-", "m")}"
            # rwgt_name = rwgt_name.replace(".", "p")
            # rwgt_name = rwgt_name.replace("-", "m")

            # rwgtCards += rwgtCards + rwgt_name + '\n'

            for j in wc_names: 
                if wc == j: 
                    rwgtCards += f"    set param_card {j} {i} \n"
                else: 
                    rwgtCards += f"    set param_card {j} 0.0 \n"

    fname = f"{outname}_reweight_card.dat"
    open(fname, 'wt').write(rwgtCards)
    print(f"card saved to: {fname}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line options parser")
    parser.add_argument("jsonFile", help="Json that contains settings")
    parser.add_argument("--outname", '-o', default="new", help="output file name")
    args = parser.parse_args()

    jsonFile = args.jsonFile
    outname = args.outname

    with open(jsonFile) as jf: 
        options = json.load(jf)

    wc_names = options['wc_names']
    scan_points = options['scan_points']

    make_reweight_card(wc_names, scan_points, outname)

    # if 'profiled_points' in options and len(options['profiled_points'])!=0:
    #     profiled_points = options['profiled_points']
    #     make_card_profiled(MG_dir, wc_names, scan_points, outname, profiled_points)
    # make_card_frozen(MG_dir, wc_names, scan_points, outname)