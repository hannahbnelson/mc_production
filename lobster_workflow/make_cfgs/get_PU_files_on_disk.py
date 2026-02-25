# based on https://github.com/FNALLPC/lpc-scripts/blob/main/get_files_on_disk.py
import os,sys,getpass,warnings,glob,shlex,subprocess,argparse # pylint: disable=multiple-imports
from collections import defaultdict

def getCache(dataset, verbose=False):
    """Gets cached file lists from cvmfs for pileup samples"""
    filelist = None
    cache_dir = "/cvmfs/cms.cern.ch/offcomp-prod/premixPUlist/"
    cache_map_file = "pileup_mapping.txt"
    cache_map_path = os.path.join(cache_dir, cache_map_file)
    if os.path.isfile(cache_map_path):
        cache_map = {}
        with open(cache_map_path, 'r') as mapfile: # pylint: disable=unspecified-encoding
            for line in mapfile:
                line = line.rstrip()
                linesplit = line.split()
                if len(linesplit)==2:
                    cache_map[linesplit[0]] = linesplit[1]

        if dataset in cache_map:
            cache_file = cache_map[dataset]
            cache_file_path = os.path.join(cache_dir, cache_file)
            if verbose:
                print(f"Loading from cache: {cache_file_path}")
            with open(cache_file_path, 'r') as cfile: # pylint: disable=unspecified-encoding
                filelist = [line.rstrip() for line in cfile]

    return filelist


def saveFilelist(filelist, redirector, outfile):

    with open(f'{outfile}.txt', 'w') as f:
        for file in filelist:
            f.write(f"{redirector}{file}\n")

    print(f"file list saved to {outfile}.txt")


if __name__=="__main__":
    default_user = getpass.getuser()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Find all available files (those hosted on disk) for a given dataset"
    )
    site_args = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument("--dataset", type=str,default='/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX', help="dataset to query")
    parser.add_argument("-o","--outfile",type=str,default="UL17_DIGIPremix", help="write to this file instead of stdout")
    parser.add_argument("--redirector", type=str, default="root://cms-xrd-global.cern.ch//", help="redirector to prepend to file names")
    parser.add_argument("--usedict", action='store_true', help='use dictionary in script instead of command line options')
    args = parser.parse_args()

    dataset = args.dataset
    outfile = args.outfile 
    redirector = args.redirector
    use_dict = args.usedict

    if use_dict:

        PU_dict = {
            '2016APV': '/MinBias_TuneCP5_13TeV-pythia8/RunIISummer20UL16SIM-106X_mcRun2_asymptotic_v13-v2/GEN-SIM', 
            '2016': '/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX', 
            '2017': '/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX',
            '2018': '/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX',
        }

        for year in PU_dict: 
            filelist = getCache(dataset=PU_dict[year], verbose=True)
            saveFilelist(filelist, redirector, outfile=f"{year}_DIGIPremix")

    else:  
        filelist = getCache(dataset=dataset, verbose=True)
        saveFilelist(filelist, redirector, outfile)

    # Example
    # global_redirector = "root://cms-xrd-global.cern.ch//"
    # filelist = getCache(dataset="/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX", verbose=True)
    # saveFilelist(filelist, global_redirector, "2016_PREMIX")

