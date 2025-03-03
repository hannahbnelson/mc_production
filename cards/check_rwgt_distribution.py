import hist
from hist import Hist
import mplhep as hep
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def read_reweightcard(fname):
    '''
    Return a dictionary of xsec values at different WC points. 

    Parameters
    ---------- 
    fname : str
        file name (and if not in the same directory, the path) of the reweight card
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

    with PdfPages('rwgt_values.pdf') as pdf:
        for wc in rwgt_values.keys():
            fig, ax = plt.subplots()
            hep.histplot(hists[wc], ax=ax, stack=False, yerr=False, label=wc)
            ax.set_xlabel("reweight values")
            ax.set_ylabel("counts")
            fig.suptitle(f"{wc}")
            pdf.savefig(fig)

if __name__ == '__main__':
    read_reweightcard("/afs/crc.nd.edu/user/h/hnelson2/unpack_tWgridpack/InputCards/tW_OGstpt_reweight_card.dat")

