import os
import pickle
import gzip
import argparse
import matplotlib.pyplot as plt
import topcoffea.modules.utils as utils

from coffea import hist
from topcoffea.modules.HistEFT import HistEFT


WCPT_EXAMPLES = {
    "nonsm": {
        "ctq1": 1.5, 
        "cQd1": 1.5,
        "ctu1": 1.5,
        "cQu1": 1.5,
        "cQq11": 1.5, 
        "cQq13": 1.5,
        "cQq83": 1.5, 
        "ctG": 1.5, 
        "cQu8": 1.5, 
        "ctd1": 1.5, 
        "ctd8": 1.5, 
        "cQq81": 1.5, 
        "ctu8": 1.5, 
        "cQd8": 1.5, 
        "ctq8": 1.5,
    },
    "sm": {
        "ctq1": 0.0,
        "cQd1": 0.0,
        "ctu1": 0.0,
        "cQu1": 0.0,
        "cQq11": 0.0,
        "cQq13": 0.0,
        "cQq83": 0.0,
        "ctG": 0.0,
        "cQu8": 0.0,
        "ctd1": 0.0,
        "ctd8": 0.0,
        "cQq81": 0.0,
        "ctu8": 0.0,
        "cQd8": 0.0,
        "ctq8": 0.0,
    }
}

# Takes a hist with one sparse axis and one dense axis, overlays everything on the sparse axis
def make_single_fig(histo):
    fig, ax = plt.subplots(1, 1, figsize=(7,7))
    histo.plot1d(
        stack=False,
    )
    ax.autoscale(axis='y')
    plt.legend()
    return fig


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_histo_file")
    args = parser.parse_args()

    histo_in = args.input_histo_file

    # Get the histograms
    hin_dict = pickle.load(gzip.open(histo_in))

    # Grab the one we want to plot
    variable = "tops_pt"
    histo = hin_dict[variable]

    h = histo.integrate('tops_pt').values()
    fig, ax = plt.subplots(1,1, figsize=(7,7)) #create an axis for plotting
    hist.plot1d(h, stack=True)
    plt.savefig("test_fig.pdf")


main()

