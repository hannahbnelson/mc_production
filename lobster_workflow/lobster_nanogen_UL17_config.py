#IMPORTANT: The workers that are submitted to this lobster master, MUST come from T3 resources

import datetime
import os
import sys
from os import path
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, MultiProductionDataset, StorageConfiguration, Workflow

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

RUN_SETUP = 'UL_production'
UL_YEAR = 'UL17'
prod_tag = "NanoGen"
#prod_tag = "test"
#version = "Run3_ttbar"
version="tW_yukawa_redo"

process_whitelist = []
coeff_whitelist   = []
runs_whitelist    = []    # (i.e. MG starting points)

master_label = 'T3_EFT_{tstamp}'.format(tstamp=timestamp_tag)

output_path  = "/store/user/$USER/mc/{tag}/{ver}".format(tag=prod_tag, ver=version)
workdir_path = "/tmpscratch/users/$USER/mc/{tag}/{ver}".format(tag=prod_tag, ver=version)
plotdir_path = "~/www/lobster/mc/{tag}/{ver}".format(tag=prod_tag, ver=version)

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
    #"tW_test": ["hnelson2/gridpack_scans/tW_test_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", "ul_cfgs/nanoGen2017_LO_cfg.py",2000, 1000],
    #"TT01j2lCARef": ["hnelson2/gridpack_scans/TT01j2lCARef_el9_amd64_gcc11_CMSSW_13_2_9_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 10000, 1000]
    #"TT01j2l_ctj8": ["hnelson2/gridpack_scans/TT01j2l_ctj8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 6000000, 1000]
    # "TT01j2l_ctj8_1p5": ["hnelson2/gridpack_scans/TT01j2l_ctj81p5_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 20000000, 1000]
    #"TT01j2l_alt_stpt":["hnelson2/gridpack_scans/TT01j2l_alt_stpt_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 2000, 1000],
    # "tW_orig": ["hnelson2/gridpack_scans/tW_orig_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", "ul_cfgs/nanoGen2017_LO_cfg.py", 100000, 1000],
    # "tW_small": ["hnelson2/gridpack_scans/tW_small_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", "ul_cfgs/nanoGen2017_LO_cfg.py", 100000, 1000],
    # "tW_medium": ["hnelson2/gridpack_scans/tW_medium_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", "ul_cfgs/nanoGen2017_LO_cfg.py", 100000, 1000],
    # "tW_large": ["hnelson2/gridpack_scans/tW_large_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", "ul_cfgs/nanoGen2017_LO_cfg.py", 100000, 1000],
    # "tW_new1": ["hnelson2/gridpack_scans/tW_new1_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", "ul_cfgs/nanoGen2017_LO_cfg.py", 100000, 1000],
    # "tW_new2": ["hnelson2/gridpack_scans/tW_new2_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", "ul_cfgs/nanoGen2017_LO_cfg.py", 100000, 1000],
    "tW_yukawa" : ["hnelson2/gridpack_scans/tW_yukawa_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", "ul_cfgs/nanoGen2017_LO_cfg.py", 100000, 1000],
    # 'tt_LO_SMEFT': ["hnelson2/gridpack_scans/ttbarEFT/tt_LO_SMEFT_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LO_cfg.py',10000, 500],
    # 'ttJets_LO_SMEFT': ["hnelson2/gridpack_scans/ttbarEFT/ttJets_LO_SMEFT_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 10000, 500],
    #'ttJets_LO_ref': ["hnelson2/gridpack_scans/ttbarEFT/ttJets_LO_ref_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 40000, 500],
    # 'tt_LO_SMEFT': ["rgoldouz/gridpack_scans/SMEFT/tt_LO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz", 10, 10]
}

nanoGen = Category(
            name="nanoGen",
            cores=2,
            memory=12000,
            disk=30000
        )

wf = []
print("Generating workflows:")
for key, value in gridpack_list.items():
    print(key)
    cmsswSSource='/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_10_6_26/'
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
        # dashboard = False,
        bad_exit_codes=[127, 160],
        log_level=1,
        payload=10,
        osg_version='3.6',
        # xrootd_servers=['ndcms.crc.nd.edu',
        #                'cmsxrootd.fnal.gov',
        #                'deepthought.crc.nd.edu']
    )
)
