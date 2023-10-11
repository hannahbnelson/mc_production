#IMPORTANT: The workers that are submitted to this lobster master, MUST come from T3 resources

import datetime
import os
import sys
from os import path
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, MultiProductionDataset, StorageConfiguration, Workflow

#sys.path.append(os.getcwd())
sys.path.append('/afs/crc.nd.edu/user/h/hnelson2/mgprod/ttbarEFT/')
from helpers.utils import regex_match

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

#events_per_gridpack = 5e5
#events_per_gridpack = 100e3
events_per_gridpack = 4000
events_per_lumi = 500

RUN_SETUP = 'UL_production'
UL_YEAR = 'UL17'
version = "tt_ttJets_LO_ref_20231011"
prod_tag = "nanoGen"

process_whitelist = []
coeff_whitelist   = []
runs_whitelist    = []    # (i.e. MG starting points)

master_label = 'T3_EFT_{tstamp}'.format(tstamp=timestamp_tag)


output_path  = "/store/user/$USER/ttbarEFT/{tag}/{ver}".format(tag=prod_tag, ver=version)
workdir_path = "/tmpscratch/users/$USER/ttbarEFT/{tag}/{ver}".format(tag=prod_tag, ver=version)
plotdir_path = "~/www/lobster/ttbarEFT/{tag}/{ver}".format(tag=prod_tag, ver=version)

input_path = "/store/user/"
input_path_full = "/hadoop" + input_path

storage = StorageConfiguration(
    input = [
        "hdfs://eddie.crc.nd.edu:19000"  + input_path,
        "root://deepthought.crc.nd.edu/" + input_path,  # Note the extra slash after the hostname!
        "gsiftp://T3_US_NotreDame"       + input_path,
        "srm://T3_US_NotreDame"          + input_path,
    ],
    output=[
        "hdfs://eddie.crc.nd.edu:19000"  + output_path,
         #ND is not in the XrootD redirector, thus hardcode server.
        "root://deepthought.crc.nd.edu/" + output_path, # Note the extra slash after the hostname!
        "gsiftp://T3_US_NotreDame"       + output_path,
        "srm://T3_US_NotreDame"          + output_path,
        "file:///hadoop"                 + output_path,
    ],
    disable_input_streaming=True,
)

# gridpack list is a dictionary of the form {'process': [gridpack path, config (path from this dir), events per gridpack, events per lumi]}
gridpack_list = {
    'ttJets_LO_ref': ["hnelson2/gridpack_scans/ttbarEFT/ttJets_LO_ref_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 4000, 500],
    'tt_LO_ref': ["hnelson2/gridpack_scans/ttbarEFT/tt_LO_ref_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LO_cfg.py', 4000, 500],
}


nanoGen = Category(
            name="nanoGen",
            cores=2,
            memory=4000,
            disk=6800
        )

wf = []
print "Generating workflows:"
for key, value in gridpack_list.items():
    # if path.exists('/hadoop/store/user/rgoldouz/FullProduction/nanoGen/NanoGen_' + key):
    #     continue
    print key
    cmsswSSource='/afs/crc.nd.edu/user/h/hnelson2/cmssw/noEFT/CMSSW_10_6_26/'
    # cmsswSSource='/afs/crc.nd.edu/user/r/rgoldouz/MakeLobsterJobs/UL/mgprod/lobster_workflow/CMSSW_10_6_26'
    # if 'rwgt' in key:
    #     cmsswSSource='/afs/crc.nd.edu/user/r/rgoldouz/MakeLobsterJobs/UL/mgprod/lobster_workflow/CMSSW_10_6_26'
    # else:
    #     cmsswSSource='/afs/crc.nd.edu/user/r/rgoldouz/MakeLobsterJobs/UL/mgprod/lobster_workflow/noEFTCMSSSWSource/CMSSW_10_6_26'
    GN = Workflow(
        label='NanoGen_{tag}'.format(tag=key),
        command='cmsRun {cfg}'.format(cfg= value[1]),
        sandbox=cmssw.Sandbox(release=cmsswSSource),
        merge_size='256M',
        merge_command='python haddnano.py @outputfiles @inputfiles',
        extra_inputs=['/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_10_6_26/src/PhysicsTools/NanoAODTools/scripts/haddnano.py'],
        cleanup_input=False,
        globaltag=False,
        outputs=['nanoGen.root'],
        dataset=MultiProductionDataset(
            gridpacks=value[0],
            events_per_gridpack=value[2],
            events_per_lumi=value[3],
            lumis_per_task=1,
            randomize_seeds=True
        ),
        category=nanoGen
    )
    wf.extend([GN])

config = Config(
    label=master_label,
    workdir=workdir_path,
    plotdir=plotdir_path,
    storage=storage,
    workflows=wf,
    advanced=AdvancedOptions(
        dashboard = False,
        bad_exit_codes=[127, 160],
        log_level=1,
        payload=10,
        xrootd_servers=['ndcms.crc.nd.edu',
                       'cmsxrootd.fnal.gov',
                       'deepthought.crc.nd.edu']
    )
)
