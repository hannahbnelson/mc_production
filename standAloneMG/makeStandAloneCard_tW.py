import os
import json
import argparse
import random
import datetime

def add_tW_proc(out_name=''):
    txt = ("import model SMEFTsim_top_MwScheme_UFO-massless_tW \n\n"
           "define p = g u c d s u~ c~ d~ s~ b b~ \n"
           "define j = p \n"
           "define l+ = e+ mu+ ta+ \n"
           "define l- = e- mu- ta- \n"
           "define vl = ve vm vt \n"
           "define vl~ = ve~ vm~ vt~ \n\n"
           "generate  p p > t l- vl~, (t > l+ vl b NPprop=0 SMHLOOP=0 NP=0) @0 NPprop=0 SMHLOOP=0 NP=1 \n"
           "add process  p p > t~ l+ vl, (t~ > l- vl~ b~ NPprop=0 SMHLOOP=0 NP=0) @1 NPprop=0 SMHLOOP=0 NP=1 \n\n"
           f"output {out_name} \n\n")

    return txt

def make_card_frozen(wc_names, scan_points, outname, basetxt='', extra=''):

    print("Creating card with WCs frozen to SM.")
    
    rwgtCards = basetxt

    rwgtCards += f"launch -n SM \n"
    rwgtCards += f"{extra}"
    for wc in wc_names: 
        rwgtCards += f"set param_card {wc} 0.0 \n"

    for wc in wc_names:
        for i in scan_points: 
            if wc=='ctGRe' or wc=='ctGIm':
                i = i/10.0
            rwgtCards += f"launch -n {wc}={i}\n"
            rwgtCards += f"{extra}"
            for j in wc_names: 
                if wc == j: 
                    rwgtCards += f"set param_card {j} {i} \n"
                else: 
                    rwgtCards += f"set param_card {j} 0.0 \n"

    fname = f"{outname}_MGstandalone.dat"
    open(fname, 'wt').write(rwgtCards)
    print(f"card saved to: {fname}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Command Line options parser")
    parser.add_argument("jsonFile", help="Json that contains settings")
    parser.add_argument("--outname", '-o', help="output file name")
    args = parser.parse_args()

    jsonFile = args.jsonFile

    if args.outname is not None: 
        outname = args.outname 
    else: 
        outname = datetime.datetime.now().strftime('%Y%m%d_%H%M')

    with open(jsonFile) as jf: 
        options = json.load(jf)

    wc_names = options['wc_names']
    scan_points = options['scan_points']
    process = options['process']
    extra = options['extra']

    if process=='tW':
        temp_txt = add_tW_proc(outname)
    else: temp_txt = ''
    
    make_card_frozen(wc_names, scan_points, outname, temp_txt, extra)
