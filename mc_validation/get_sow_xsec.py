import awkward as ak
import numpy as np
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
NanoAODSchema.warn_missing_crossrefs = False


files = ["nanoGen_ttbar_LO_SMEFT.root",
         "nanogen_ttbar_ref.root", 
         "nanogen_small.root", 
         "nanogen_ttJets_LO_SMEFT.root", 
         "small_nanoGen_ttbar_LO_SMEFT.root", 
         "nanogen_ttbar_ref.root", 
         "central_ttbar.root"
         ]

for item in files: 
    fname = "/afs/crc.nd.edu/user/h/hnelson2/ttbarEFT_mcgen/mc_validation/input_samples/nanoGen_files/" + item 
    events = NanoEventsFactory.from_root(
        fname,
        schemaclass=NanoAODSchema.v6,
        metadata={"dataset": "ttbar"},
    ).events()

    # Extract the EFT quadratic coefficients and optionally use them to calculate the coefficients on the w**2 quartic function
    # eft_coeffs is never Jagged so convert immediately to numpy for ease of use.
    eft_coeffs = ak.to_numpy(events['EFTfitCoefficients']) if hasattr(events, "EFTfitCoefficients") else None
    
    print("file: ", item)

    if eft_coeffs is None:
        event_weights = events["genWeight"]
        print("Total SM cross section for all files: ", np.sum(event_weights))
        print("SM cross section: ", np.sum(event_weights)/20) 
    else:
        event_weights = np.ones_like(events['event'])
        eft_sum = np.sum(eft_coeffs, axis=0)
        print("Total SM cross section for all files: ", eft_sum[0])
        print("SM cross section: ", eft_sum[0]/20)

    sow = np.sum(event_weights)

    print("sow: ", sow, "\n")
