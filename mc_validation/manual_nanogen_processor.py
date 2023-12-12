import awkward as ak
import numpy as np
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
NanoAODSchema.warn_missing_crossrefs = False

from coffea.analysis_tools import PackedSelection
from topcoffea.modules import utils


files = ["nanoGen_TT01j2l_10k.root",
         ]
#files = ["nanoGen_ttbar_LO_SMEFT.root",
#         "nanogen_ttbar_ref.root", 
#         "nanogen_small.root", 
#         "nanogen_ttJets_LO_SMEFT.root", 
#         "small_nanoGen_ttbar_LO_SMEFT.root", 
#         "nanogen_ttbar_ref.root", 
#         "central_ttbar.root"
#         ]

# Clean the objects
def is_clean(obj_A, obj_B, drmin=0.4):
    objB_near, objB_DR = obj_A.nearest(obj_B, return_metric=True)
    mask = ak.fill_none(objB_DR > drmin, True)
    return (mask)

for item in files: 
    fname = "/afs/crc.nd.edu/user/h/hnelson2/ttbarEFT_mcgen/mc_validation/input_samples/nanoGen_files/" + item 
    events = NanoEventsFactory.from_root(
        fname,
        schemaclass=NanoAODSchema.v6,
        metadata={"dataset": "ttJets"},
    ).events()

    print(events.GenPart.fields)

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
    #leps_ptsorted = leps[ak.argsort(leps.pt,axis=-1,ascending=False)]
    #leps_num_mask = ak.num(leps_ptsorted)==2


    ######## Jet selection  ########

    jets = jets[(jets.pt>30) & (abs(jets.eta)<2.5)]
    jets_clean = jets[is_clean(jets, leps, drmin=0.4)]
    ht = ak.sum(jets.pt, axis=-1)

    ######## Top selection ########

    gen_top = ak.pad_none(genpart[is_final_mask & (abs(genpart.pdgId) == 6)],2)

    ######## Event selections ########

    nleps = ak.num(leps)
    njets = ak.num(jets_clean)

    at_least_two_leps = ak.fill_none(nleps>=2,False)
    at_least_one_jets = ak.fill_none(njets>=1, False)
    at_least_two_jets = ak.fill_none(njets>=2, False)

    selections2j = PackedSelection()
    #selections2j.add('2l', at_least_two_leps)
    selections2j.add('2j', at_least_two_jets)

    selections1j = PackedSelection()
    #selections1j.add('2l', at_least_two_leps)
    selections1j.add("1j", at_least_one_jets)

    event_selection_mask = selections2j.all("2j")
    event_selection_mask_1j = selections1j.all("1j")

    #leps_cut = leps[event_selection_mask]
    jets_cut = jets_clean[event_selection_mask]
    #print("nleps before cut: ", nleps)
    #print("nleps after cut: ", ak.num(leps_cut))
    print("jets shape before cut: ", ak.count(jets_clean))
    print("jets shape after cut: ", ak.count(jets_cut))
    print("njets before cut: ", njets) 
    print("njets after cut: ", ak.num(jets_cut))

    print(" ------ \n 1j cut")
    #leps_cut = leps[event_selection_mask_1j]
    jets_cut = jets_clean[event_selection_mask_1j]
    #print("nleps before cut: ", nleps)
    #print("nleps after cut: ", ak.num(leps_cut))
    print("jets shape before cut: ", ak.count(jets_clean))
    print("jets shape after cut: ", ak.count(jets_cut))
    print("njets before cut: ", njets)
    print("njets after cut: ", ak.num(jets_cut))
