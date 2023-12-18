import pickle #read pickle file
import coffea
from coffea import hist
import topcoffea.modules.HistEFT as HistEFT
import topcoffea.modules.eft_helper as efth
import gzip #read zipped pickle file
import matplotlib.pyplot as plt #plot histograms
import mplhep as hep
import numpy as np

hep.style.use("CMS")
params = {'axes.labelsize': 20,
          'axes.titlesize': 20,
          'legend.fontsize':20}
plt.rcParams.update(params)

fin = 'TT1j2l_cQj31.pkl.gz'

if fin.endswith('.pkl.gz'):
    label = fin[:-7]
else: 
    label = fin
print(label)

hists = {}

ref_pts = {"ctGIm": 1.0, "ctGRe":0.7, "cQj38": 9.0, "cQj18": 7.0, 
            "cQu8": 9.5, "cQd8": 12.0, "ctj8": 7.0, "ctu8": 9.0,
            "ctd8": 12.4, "cQj31": 3.0, "cQj11": 4.2, "cQu1": 5.5, 
            "cQd1": 7.0, "ctj1": 4.4, "ctu1": 5.4, "ctd1": 7.0}

rwgt5_pts = {"ctGIm": 5.0, "ctGRe":5.0, "cQj38": 5.0, "cQj18": 5.0, 
            "cQu8": 5.0, "cQd8": 5.0, "ctj8": 5.0, "ctu8": 5.0,
            "ctd8": 5.0, "cQj31": 5.0, "cQj11": 5.0, "cQu1": 5.0, 
            "cQd1": 5.0, "ctj1": 5.0, "ctu1": 5.0, "ctd1": 5.0}

with gzip.open(fin) as fin: 
    hin = pickle.load(fin)
    for k in hin.keys():
        if k in hists: 
            hists[k]+=hin[k]
        else: 
            hists[k]=hin[k]

def plot_hist_NOrwgt(hists, name, label):
    h = hists[name]
    fig, ax = plt.subplots(1,1) #create an axis for plotting
    hist.plot1d(h, ax=ax, stack=True)
    ax.legend()
    figname = label + '_NOrwgt_' + name + '.pdf'
    fig.savefig(figname)
    print("Histogram saved to:", figname)
    plt.close(fig)

def plot_hist_sm(hists, name, label):
    h = hists[name]
    h.set_sm()
    fig, ax = plt.subplots(1,1) #create an axis for plotting
    hist.plot1d(h, ax=ax, stack=True)
    ax.legend()     
    figname = label + '_SMrwgt_' + name + '.pdf'
    fig.savefig(figname)
    print("Histogram saved to:", figname)
    plt.close(fig)

def plot_hist_rwgt(hists, name, label, rwgt):
    h = hists[name]
    h.set_wilson_coefficients(rwgt)
    fig, ax = plt.subplots(1,1) #create an axis for plotting
    hist.plot1d(h, ax=ax, stack=True)
    ax.legend()
    figname = label + '_rwgt_' + name + '.pdf'
    fig.savefig(figname)
    print("Histogram saved to:", figname)   
    plt.close(fig)

for name in hists: 
    plot_hist_NOrwgt(hists, name, label)
    plot_hist_sm(hists, name, label)
    plot_hist_rwgt(hists, name, label = label+'_refpoint', rwgt=ref_pts)
    plot_hist_rwgt(hists, name, label = label+'_all5', rwgt = rwgt5_pts)

