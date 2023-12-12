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

#fin = 'TT01j2l.pkl.gz'
#fin = 'TT01j2l_4jtest.pkl.gz'
#fin = 'TT01j2l_cuts_test.pkl.gz'
fin = 'TT01j2l_cuts.pkl.gz'

if fin.endswith('.pkl.gz'):
    label = fin[:-7]
else: 
    label = fin
print(label)

hists = {}

rwgt_pts = [5, 5, 5, 5, 
            5, 5, 5, 5, 
            5, 5, 5, 5, 
            5, 5, 5, 5]

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

def plot_hist_rwgt(hists, name, label):
    h = hists[name]
    h.set_wilson_coeff_from_array(rwgt_pts)
    fig, ax = plt.subplots(1,1) #create an axis for plotting
    hist.plot1d(h, ax=ax, stack=True)
    ax.legend()
    figname = label + '_rwgt_' + name + '.pdf'
    fig.savefig(figname)
    print("Histogram saved to:", figname)   
    plt.close(fig)

#print(hists)
#plot_hist_NOrwgt(hists, 'njets', label)

for name in hists: 
    plot_hist_sm(hists, name, label)
    plot_hist_rwgt(hists, name, label)
    plot_hist_NOrwgt(hists, name, label)

