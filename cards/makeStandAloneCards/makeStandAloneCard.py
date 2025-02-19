import os
import json
import argparse
import random

def make_card_profiled(MG_dir, wc_names, scan_points, outname, profiled_points):
    print("Creating card with WCs profiled: \n", profiled_points, '\n')

    rwgtCards = ''
    rwgtCards += f"launch {MG_dir} \n"

    rwgtCards += f"launch -n SM \n"
    for wc in wc_names: 
        rwgtCards += f"set param_card {wc} {profiled_points[wc]} \n"

    for wc in wc_names:
        for i in scan_points: 
            if wc=='ctGRe' or wc=='ctGIm':
                i = i/10.0
            rwgtCards += f"launch -n {wc}={i}\n"

            for j in wc_names: 
                if wc == j: 
                    rwgtCards += f"set param_card {j} {i} \n"
                else: 
                    rwgtCards += f"set param_card {j} {profiled_points[wc]} \n"

    fname = f"{outname}_profiled.dat"
    open(fname, 'wt').write(rwgtCards)
    print(f"card saved to: {fname}")


def make_card_frozen(MG_dir, wc_names, scan_points, outname):

    print("Creating card with WCs frozen to SM.")
    
    rwgtCards = ''
    rwgtCards += f"launch {MG_dir} \n"

    rwgtCards += f"launch -n SM \n"
    for wc in wc_names: 
        rwgtCards += f"set param_card {wc} 0.0 \n"

    for wc in wc_names:
        for i in scan_points: 
            if wc=='ctGRe' or wc=='ctGIm':
                i = i/10.0
            rwgtCards += f"launch -n {wc}={i}\n"

            for j in wc_names: 
                if wc == j: 
                    rwgtCards += f"set param_card {j} {i} \n"
                else: 
                    rwgtCards += f"set param_card {j} 0.0 \n"

    fname = f"{outname}_frozen.dat"
    open(fname, 'wt').write(rwgtCards)
    print(f"card saved to: {fname}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line options parser")
    parser.add_argument("jsonFile", help="Json that contains settings")
    parser.add_argument("--outname", '-o', default="standAloneCard", help="output file name")
    args = parser.parse_args()

    jsonFile = args.jsonFile
    outname = args.outname

    with open(jsonFile) as jf: 
        options = json.load(jf)

    MG_dir = options['MG_dir']
    wc_names = options['wc_names']
    scan_points = options['scan_points']
    if 'profiled_points' in options and len(options['profiled_points'])!=0:
        profiled_points = options['profiled_points']
        make_card_profiled(MG_dir, wc_names, scan_points, outname, profiled_points)


    make_card_frozen(MG_dir, wc_names, scan_points, outname)
