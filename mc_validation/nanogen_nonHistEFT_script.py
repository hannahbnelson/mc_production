import awkward as ak
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import hist
from hist import Hist
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
NanoAODSchema.warn_missing_crossrefs = False

from coffea.analysis_tools import PackedSelection
from topcoffea.modules import utils
import topcoffea.modules.eft_helper as efth

# histogram style
hep.style.use("CMS")
params = {'axes.labelsize': 20,
          'axes.titlesize': 20,
          'legend.fontsize':20}
plt.rcParams.update(params)

ref_pts = {"ctGIm": 1.0, "ctGRe":0.7, "cQj38": 9.0, "cQj18": 7.0,
            "cQu8": 9.5, "cQd8": 12.0, "ctj8": 7.0, "ctu8": 9.0,
            "ctd8": 12.4, "cQj31": 3.0, "cQj11": 4.2, "cQu1": 5.5,
            "cQd1": 7.0, "ctj1": 4.4, "ctu1": 5.4, "ctd1": 7.0}

fname = "/afs/crc.nd.edu/user/h/hnelson2/ttbarEFT_mcgen/mc_validation/input_samples/nanoGen_files/TT1j2l_cQj31/nanoGen_101.root"


# Clean the objects
def is_clean(obj_A, obj_B, drmin=0.4):
    objB_near, objB_DR = obj_A.nearest(obj_B, return_metric=True)
    mask = ak.fill_none(objB_DR > drmin, True)
    return (mask)

events = NanoEventsFactory.from_root(
    fname,
    schemaclass=NanoAODSchema.v6,
    metadata={"dataset": "ttJets"},
).events()

wc_lst = utils.get_list_of_wc_names(fname)
print("wc list: ", wc_lst)

dataset = events.metadata['dataset']


def order_wc_values(wcs, ref_pts):
    '''Returns list of wc values in the same order as the list of wc names based on a dictionary 
    '''    
    wc_names = wcs
    ref_pts = ref_pts

    wc_values = []
    for i in wc_names:
        wc_values.append(ref_pts[i])

    return wc_values 
    

# Extract the EFT quadratic coefficients and optionally use them to calculate the coefficients on the w**2 quartic function
# eft_coeffs is never Jagged so convert immediately to numpy for ease of use.
eft_coeffs = ak.to_numpy(events['EFTfitCoefficients']) if hasattr(events, "EFTfitCoefficients") else None

if eft_coeffs is None:
    event_weights = events["genWeight"]
else:
    event_weights = np.ones_like(events['event'])

# Initialize objects
genpart = events.GenPart
is_final_mask = genpart.hasFlags(["fromHardProcess","isLastCopy"])
ele  = genpart[is_final_mask & (abs(genpart.pdgId) == 11)]
mu   = genpart[is_final_mask & (abs(genpart.pdgId) == 13)]
jets = events.GenJet

######## Lep selection  ########

e_selec = ((ele.pt>20) & (abs(ele.eta)<2.5))
m_selec = ((mu.pt>20) & (abs(mu.eta)<2.5))
leps = ak.concatenate([ele[e_selec],mu[m_selec]],axis=1)

######## Jet selection  ########

jets = jets[(jets.pt>30) & (abs(jets.eta)<2.5)]
jets_clean = jets[is_clean(jets, leps, drmin=0.4)]
ht = ak.sum(jets.pt, axis=-1)
j0 = jets_clean[ak.argmax(jets_clean.pt, axis=-1, keepdims=True)]

######## Top selection ########

gen_top = ak.pad_none(genpart[is_final_mask & (abs(genpart.pdgId) == 6)],2)
mtt = (gen_top[:,0] + gen_top[:,1]).mass

######## Event selections ########

nleps = ak.num(leps)
njets = ak.num(jets_clean)
ntops = ak.num(gen_top)

at_least_two_leps = ak.fill_none(nleps>=2,False)
at_least_two_jets = ak.fill_none(njets>=2, False)

selections = PackedSelection()
selections.add('2l', at_least_two_leps)
selections.add('2j', at_least_two_jets)
event_selection_mask = selections.all('2l', '2j')

######## Delta R ########
jets_clean = jets_clean[event_selection_mask]
njets = njets[event_selection_mask]
dr = []
for i in range(ak.max(njets)):
    dr_i = jets_clean[njets>=(i+1)][:,i].delta_r(leps[njets>=(i+1)])
    dr.extend(ak.to_list(ak.flatten(dr_i, axis=None)))

h = Hist(hist.axis.Regular(bins=15, start=0, stop=6, name="deltaR"))
h.fill(dr)

fig, ax = plt.subplots(1,1)
hep.histplot(h, ax=ax, stack=True, histtype="fill", label="TT01j2l")
ax.legend()
fig.savefig("old_TT1j2l_deltaR.pdf")
plt.close(fig)


######## Histogram of event weights ########
eft_coeffs_cut = eft_coeffs[event_selection_mask]
wc_values = list(ref_pts.values())
event_weight_calc = []

print(events.LHEWeight.originalXWGTUP)
#print("LHEWeight_originalXWGTUP: ", events["LHEWeight_originalXWGTUP"])

print("wc_list: ", wc_lst)
print("wc ref points: ", ref_pts) 

ordered_lst = order_wc_values(wc_lst, ref_pts)
print("ordered wc value list: ", ordered_lst)

'''
for i in range(len(eft_coeffs_cut)):
    wcs = np.hstack((np.ones(1),ordered_lst))
    wc_cross_terms = []
    index = 0 
    for j in range(len(wcs)):
        for k in range (j+1):       
            term = wcs[j]*wcs[k]
            wc_cross_terms.append(term)  
    weight_calc = np.sum(np.multiply(wc_cross_terms, eft_coeffs_cut[i]))
    event_weight_calc.append(weight_calc)
    
h2 = Hist(hist.axis.Regular(bins = 20, start = 0, stop = 10, name="event weight"))
h2.fill(event_weight_calc)

fig, ax = plt.subplots(1,1)
hep.histplot(h2, ax=ax, stack=True, histtype="fill", label="TT01j2l")
ax.legend()
fig.savefig("ordered_TT1j2l_weights.pdf")
print(len(event_weight_calc))
plt.close(fig)
'''
