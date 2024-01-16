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

sm_pts = {"ctGIm": 0.0, "ctGRe":0.0, "cQj38": 0.0, "cQj18": 0.0,
          "cQu8": 0.0, "cQd8": 0.0, "ctj8": 0.0, "ctu8": 0.0,
          "ctd8": 0.0, "cQj31": 0.0, "cQj11": 0.0, "cQu1": 0.0,
          "cQd1": 0.0, "ctj1": 0.0, "ctu1": 0.0, "ctd1": 0.0}

starting_pts = {"ctGIm": 1.0, "ctGRe":0.7, "cQj38": 9.0, "cQj18": 7.0,
                "cQu8": 9.5, "cQd8": 12.0, "ctj8": 7.0, "ctu8": 9.0,
                "ctd8": 12.4, "cQj31": 3.0, "cQj11": 4.2, "cQu1": 5.5,
                "cQd1": 7.0, "ctj1": 4.4, "ctu1": 5.4, "ctd1": 7.0}

small_pts = {"ctGIm": 1.0, "ctGRe":1.0, "cQj38": 1.0, "cQj18": 1.0,
             "cQu8": 1.0, "cQd8": 1.0, "ctj8": 1.0, "ctu8": 1.0,
             "ctd8": 1.0, "cQj31": 1.0, "cQj11": 1.0, "cQu1": 1.0,
             "cQd1": 1.0, "ctj1": 1.0, "ctu1": 1.0, "ctd1": 1.0}

large_pts = {"ctGIm": 10, "ctGRe":10, "cQj38": 10, "cQj18": 10,
             "cQu8": 10, "cQd8": 10, "ctj8": 10, "ctu8": 10,
             "ctd8": 10, "cQj31": 10, "cQj11": 10, "cQu1": 10,
             "cQd1": 10, "ctj1": 10, "ctu1": 10, "ctd1": 10}

data_files = ["/afs/crc.nd.edu/user/h/hnelson2/ttbarEFT_mcgen/mc_validation/input_samples/nanoGen_files/TT1j2l_cQj31/nanoGen_101.root", 
              "/afs/crc.nd.edu/user/h/hnelson2/ttbarEFT_mcgen/mc_validation/input_samples/nanoGen_files/TT1j2l_cQj31/nanoGen_102.root"]

##############################

# Clean the objects
def is_clean(obj_A, obj_B, drmin=0.4):
    objB_near, objB_DR = obj_A.nearest(obj_B, return_metric=True)
    mask = ak.fill_none(objB_DR > drmin, True)
    return (mask)

# Create list of wc values in the correct order
def order_wc_values(wcs, ref_pts):
    '''Returns list of wc values in the same order as the list of wc names based on a dictionary
    '''
    wc_names = wcs
    ref_pts = ref_pts

    wc_values = []
    for i in wc_names:
        wc_values.append(ref_pts[i])

    return wc_values

# Calculate event weights from wc values and eft fit coefficients
def calc_event_weights(eft_coeffs, wc_vals):
    '''Returns an array that contains the event weight for each event.
    eft_coeffs: Array of eft fit coefficients for each event
    wc_vals: wilson coefficient values desired for the event weight calculation, listed in the same order as the wc_lst
             such that the multiplication with eft_coeffs is correct
             The correct ordering can be achieved with the order_wc_values function
    '''

    event_weight = np.empty_like(eft_coeffs)

    wcs = np.hstack((np.ones(1),wc_vals))
    wc_cross_terms = []
    index = 0
    for j in range(len(wcs)):
        for k in range (j+1):
            term = wcs[j]*wcs[k]
            wc_cross_terms.append(term)
    event_weight = np.sum(np.multiply(wc_cross_terms, eft_coeffs), axis=1)

    return event_weight


    ##############################
for fname in data_files: 

    # Load in events from root file
    events = NanoEventsFactory.from_root(
        fname,
        schemaclass=NanoAODSchema.v6,
        metadata={"dataset": "TT1j2l"},
    ).events()

    wc_lst = utils.get_list_of_wc_names(fname)
    print("wc list: ", wc_lst)

    dataset = events.metadata['dataset']

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

    '''
    h = Hist(hist.axis.Regular(bins=15, start=0, stop=6, name="deltaR"))
    h.fill(dr)

    fig, ax = plt.subplots(1,1)
    hep.histplot(h, ax=ax, stack=True, histtype="fill", label="TT01j2l")
    ax.legend()
    fig.savefig("TT1j2l_deltaR.pdf")
    plt.close(fig)


    ######## Histograms of event weights ########
    eft_coeffs_cut = eft_coeffs[event_selection_mask]

    wc_lst_ref = order_wc_values(wc_lst, starting_pts)
    wc_lst_sm = order_wc_values(wc_lst, sm_pts)
    wc_lst_small = order_wc_values(wc_lst, small_pts)
    wc_lst_lg = order_wc_values(wc_lst, large_pts)

    event_weights_ref = calc_event_weights(eft_coeffs_cut, wc_lst_ref)
    event_weights_sm = calc_event_weights(eft_coeffs_cut, wc_lst_sm)
    event_weights_small = calc_event_weights(eft_coeffs_cut, wc_lst_small)
    event_weights_lg = calc_event_weights(eft_coeffs_cut, wc_lst_lg)

    print("min weight at ref: ", np.min(event_weights_ref))
    print("max weight at ref: ", np.max(event_weights_ref))

    print("min weight at sm: ", np.min(event_weights_sm))
    print("max weight at sm: ", np.max(event_weights_sm))

    print("min weight at small: ", np.min(event_weights_small))
    print("max weight at small: ", np.max(event_weights_small))

    print("min weight at large: ", np.min(event_weights_lg))
    print("max weight at large: ", np.max(event_weights_lg)) 


    h1 = Hist(hist.axis.Regular(bins = 20, start = 0, stop = 4, name="event weight"))
    h1.fill(event_weights_ref)
    fig, ax = plt.subplots(1,1)
    hep.histplot(h1, ax=ax, stack=True, histtype="fill", label="TT1j2l ref")
    ax.legend
    fig.savefig("test_TT1j2l_weight_refpt.pdf")
    plt.close(fig)

    h2 = Hist(hist.axis.Regular(bins = 20, start = 0, stop = 4, name="event weight"))
    h2.fill(event_weights_sm)
    fig, ax = plt.subplots(1,1)
    hep.histplot(h2, ax=ax, stack=True, histtype="fill", label="TT1j2l sm")
    ax.legend
    fig.savefig("test_TT1j2l_weight_smpt.pdf")
    plt.close(fig)

    h3 = Hist(hist.axis.Regular(bins = 20, start = 0, stop = 4, name="event weight"))
    h3.fill(event_weights_other)
    fig, ax = plt.subplots(1,1)
    hep.histplot(h3, ax=ax, stack=True, histtype="fill", label="TT1j2l all wc=1")
    ax.legend
    fig.savefig("test_TT1j2l_weight_otherpt.pdf")
    plt.close(fig)
    '''



