#!/usr/bin/env python
import numpy as np
import awkward as ak
np.seterr(divide='ignore', invalid='ignore', over='ignore')
from coffea import hist, processor
from coffea.analysis_tools import PackedSelection

# silence warnings due to using NanoGEN instead of full NanoAOD
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
NanoAODSchema.warn_missing_crossrefs = False

from topcoffea.modules.HistEFT import HistEFT
import topcoffea.modules.eft_helper as efth

'''
# Get the lumi for the given year
def get_lumi(year):
    lumi_dict = {
        "2016APV": 19.52,
        "2016": 16.81,
        "2017": 41.48,
        "2018": 59.83
    }
    if year not in lumi_dict.keys():
        raise Exception(f"(ERROR: Unknown year \"{year}\".")
    else:
        return(lumi_dict[year])
'''

# Clean the objects
def is_clean(obj_A, obj_B, drmin=0.4):
    objB_near, objB_DR = obj_A.nearest(obj_B, return_metric=True)
    mask = ak.fill_none(objB_DR > drmin, True)
    return (mask)

# Main analysis processor
class AnalysisProcessor(processor.ProcessorABC):
    def __init__(self, samples, wc_names_lst=[], dtype=np.float32, do_errors=False):
        self._samples = samples
        self._wc_names_lst = wc_names_lst

        self._dtype = dtype
        self._do_errors = do_errors

        print("self._samples", self._samples)
        print("self._wc_names_lst", self._wc_names_lst)

        # Create the histograms with new scikit hist
        self._histo_dict = {
            "tops_pt"      : HistEFT("Events", wc_names_lst, hist.Cat("sample", "sample"), hist.Bin("tops_pt", "pT of the sum of the tops", 50, 0, 500)),
            "ht"           : HistEFT("Events", wc_names_lst, hist.Cat("sample", "sample"), hist.Bin("ht", "Scalar sum of genjet pt", 100, 0, 1000)),
            "njets"        : HistEFT("Events", wc_names_lst, hist.Cat("sample", "sample"), hist.Bin("njets", "njets", 10, 0, 10)), 
            "mtt"          : HistEFT("Events", wc_names_lst, hist.Cat("sample", "sample"), hist.Bin("mtt", "invariant mass of tops", 100, 0, 1000)), 
        }

    @property
    def columns(self):
        return self._columns

    def process(self, events):

        # Dataset parameters
        dataset = events.metadata['dataset']
        hist_axis_name = self._samples[dataset]["histAxisName"]

        year   = self._samples[dataset]['year']
        xsec   = self._samples[dataset]['xsec']
        sow    = self._samples[dataset]['nSumOfWeights']

        # Extract the EFT quadratic coefficients and optionally use them to calculate the coefficients on the w**2 quartic function
        # eft_coeffs is never Jagged so convert immediately to numpy for ease of use.
        eft_coeffs = ak.to_numpy(events['EFTfitCoefficients']) if hasattr(events, "EFTfitCoefficients") else None
        eft_w2_coeffs = efth.calc_w2_coeffs(eft_coeffs,self._dtype) if (self._do_errors and eft_coeffs is not None) else None


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

        ######## Top selection ########

        gen_top = ak.pad_none(genpart[is_final_mask & (abs(genpart.pdgId) == 6)],2)
        mtt = (gen_top[:,0] + gen_top[:,1]).mass

        ######## Event selections ########

        nleps = ak.num(leps)
        njets = ak.num(jets_clean)

        at_least_two_leps = ak.fill_none(nleps>=2,False)

        selections = PackedSelection()
        selections.add('2l', at_least_two_leps)

        ######## Normalization ########

        # Normalize by (xsec/sow)
        #lumi = 1000.0*get_lumi(year)
        #norm = (xsec/sow)
        norm = 1
        if eft_coeffs is None: 
            event_weights = events["genWeight"]
        else:
            event_weights = norm*np.ones_like(events['event'])


        ######## Fill histos ########

        hout = self._histo_dict

        variables_to_fill = {
            "tops_pt" : gen_top.sum().pt,
            "njets" : ak.num(jets_clean),
            "mtt" : mtt,
            "ht" : ht,
        }

        event_selection_mask = selections.all("2l")

        if eft_coeffs is not None:
            eft_coeffs = eft_coeffs[event_selection_mask]

        for var_name, var_values in variables_to_fill.items():

            fill_info = {
                var_name    : var_values[event_selection_mask],
                "sample"   : hist_axis_name,
                "weight"    : event_weights[event_selection_mask],
                "eft_coeff" : eft_coeffs,
            }

            hout[var_name].fill(**fill_info)

        return hout

    def postprocess(self, accumulator):
        return accumulator

