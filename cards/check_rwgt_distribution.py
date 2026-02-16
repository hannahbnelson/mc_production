import hist
from hist import Hist
import mplhep as hep
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import argparse
import os

def read_reweightcard(fname, outname):
    '''
    Return a dictionary of xsec values at different WC points. 

    Parameters
    ---------- 
    fname : str
        file name (and if not in the same directory, the path) of the reweight card
    outname: str
        output file name
    '''
    
    with open(fname, "r") as f: 
        lines = f.read().splitlines() 
    f.close() 

    rwgt_values = {}

    for line in lines: 
        if "set param_card" in line: 
            line = line[19:]
            tmp = line.split(" ")

            wc_name = tmp[0]
            wc_val = float(tmp[1])

            if wc_name not in rwgt_values.keys():
                rwgt_values[wc_name]=[]
            
            rwgt_values[wc_name].append(wc_val)

    hists = {}
    for wc in rwgt_values.keys():
        hists[wc]=Hist(hist.axis.Regular(bins=50, start=min(rwgt_values[wc]), stop=max(rwgt_values[wc]), name=wc, label=wc))
        hists[wc].fill(rwgt_values[wc])

    with PdfPages(f"{outname}.pdf") as pdf:
        for wc in rwgt_values.keys():
            fig, ax = plt.subplots()
            hep.histplot(hists[wc], ax=ax, stack=False, yerr=False, label=wc)
            ax.set_xlabel("reweight values")
            ax.set_ylabel("counts")
            fig.suptitle(f"{wc}")
            pdf.savefig(fig)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Command Line options parser")
    parser.add_argument("file", help="path to reweight card")
    parser.add_argument("--outname", default="rwgt_hists", help="Output file name")
    args = parser.parse_args()

    filename = args.file
    outname = args.outname 

    read_reweightcard(filename, outname)
    print(f"plots saved to {outname}.pdf")

