#IMPORTANT: The workers that are submitted to this lobster master, MUST come from T3 resources

import datetime
import os
import sys
from os import path
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, MultiProductionDataset, StorageConfiguration, Workflow

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

prod_tag = "NanoGen"
version="ctj8_v9"

process_whitelist = []
coeff_whitelist   = []
runs_whitelist    = []    # (i.e. MG starting points)

master_label = 'T3_EFT_{tstamp}'.format(tstamp=timestamp_tag)

output_path  = "/store/user/$USER/Run3test/{tag}/{ver}".format(tag=prod_tag, ver=version)
workdir_path = "/tmpscratch/users/$USER/Run3test/{tag}/{ver}".format(tag=prod_tag, ver=version)
plotdir_path = "~/www/lobster/Run3test/{tag}/{ver}".format(tag=prod_tag, ver=version)

storage = StorageConfiguration(
    input = [
        "file:///cms/cephfs/data/store/user/",
        "root://hactar01.crc.nd.edu//store/user/",
    ],
    
    output=[
        "file:///cms/cephfs/data" + output_path,
        "root://hactar01.crc.nd.edu/"+output_path,    
    ],
)

# gridpack list is a dictionary of the form {'process': [gridpack path, config (path from this dir), events per gridpack, events per lumi]}
gridpack_list = {
    #"TT01j2l_Run3": ["hnelson2/gridpack_scans/TT01j2lCARef_el9_amd64_gcc11_CMSSW_13_2_9_tarball.tar.xz", '/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_13_0_14/src/SMP-Run3Summer23NanoAODv12-00489_1_cfg.py', 2000, 1000]
    "TT01j2l_ctj8_Run3": ["hnelson2/gridpack_scans/TT01j2l_ctj8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", '/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_13_0_14/src/SMP-Run3Summer23NanoAODv12-00489_1_cfg.py', 2000, 1000]
    #"TT01j2l_ctj8": ["hnelson2/gridpack_scans/TT01j2l_ctj8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 2000, 1000]
}

nanoGen = Category(
            name="nanoGen",
            cores=2,
            memory=4000,
            disk=6800
        )

wf = []
print("Generating workflows:")
for key, value in gridpack_list.items():
    print(key)
    cmsswSource = '/afs/crc.nd.edu/user/h/hnelson2/CMSSW_13_0_14/'
    #cmsswSource='/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_13_0_14/'
    #cmsswSource = '/afs/crc.nd.edu/user/h/hnelson2/cmssw/test/CMSSW_13_2_9/'
    GN = Workflow(
        label='NanoGen_{tag}'.format(tag=key),
        command='cmsRun {cfg}'.format(cfg= value[1]),
        sandbox=cmssw.Sandbox(release=cmsswSource),
        merge_size='256M',
        merge_command='python haddnano.py @outputfiles @inputfiles',
        extra_inputs=['/afs/crc.nd.edu/user/h/hnelson2/CMSSW_13_0_14/src/PhysicsTools/NanoAODTools/scripts/haddnano.py'],
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
        # dashboard = False,
        bad_exit_codes=[127, 160],
        log_level=1,
        payload=10,
        threshold_for_failure=2,
        #osg_version='3.6',
        # xrootd_servers=['ndcms.crc.nd.edu',
        #                'cmsxrootd.fnal.gov',
        #                'deepthought.crc.nd.edu']
    )
)
