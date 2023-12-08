import pickle #read pickle file
import coffea
from coffea import hist
import topcoffea.modules.HistEFT as HistEFT
import topcoffea.modules.eft_helper as efth
import gzip #read zipped pickle file
import matplotlib.pyplot as plt #plot histograms
import numpy as np

fin = "with_mtt.pkl.gz"
hists = {}

with gzip.open(fin) as fin: 
    hin = pickle.load(fin)
    for k in hin.keys():
        if k in hists:
            hists[k]+=hin[k]
        else: 
            hists[k] = hin[k]
        print(hists[k])
    print(hin.keys())

histo = hists['tops_pt']
h = histo.integrate('tops_pt').values()
fig, ax = plt.subplots(1,1, figsize=(7,7)) #create an axis for plotting
hist.plot1d(h, stack=True)
plt.savefig("tops_pt.pdf")
