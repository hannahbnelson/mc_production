import datetime
import os
import sys
from os import path
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, Dataset, ParentDataset, StorageConfiguration, Workflow

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')


# UL_YEAR = 'UL16APV'
# UL_YEAR = 'UL16'
UL_YEAR = 'UL17'
# UL_YEAR = 'UL18'

prod_tag = 'DIGItest'
version = timestamp_tag

master_label = 'CFE_postLHE_EFT_{tstamp}'.format(tstamp=timestamp_tag)

output_path  = "/store/user/$USER/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)
workdir_path = "/tmpscratch/users/$USER/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)
plotdir_path = "~/www/lobster/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)

# input_dir_path = "/cms/cephfs/data/store/user/"
input_dir_path = ""

SIM_dir = os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL17/postLHE/test_v4/SIM_TTto2L2Nu_1Jets_smeft_MTT_0to700/")
UL_cfg = 'ttbar_ulcfgs/TOP-2017DIGIPremix_test.py'

cmssw_base_dir = '/users/hnelson2/mc_production/cmssw/'
DIGI_cmssw = os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/')

digi_resources = Category(
    name='digi',
    cores=6,
    memory=7800,
    disk=6000,
)

### Storage ### 
storage = StorageConfiguration(
    input = [
        "file:///cms/cephfs/data/store/user/",
        "root://cmsxrootd.crc.nd.edu//store/user/",
        # "root://cmsxcache.crc.nd.edu/",
        # "root://cmsxrootd.fnal.gov/",
    ],
    
    output=[
        "file:///cms/cephfs/data" + output_path,
        "root://cmsxrootd.crc.nd.edu/"+output_path,    
    ],
)

### Construct Lobster Workflows ### 
wfs = []

digi = Workflow(
    label=f"DIGI_TT01j2l_mtt0to700",
    command=f"cmsRun {UL_cfg}",
    sandbox=cmssw.Sandbox(release=DIGI_cmssw),
    merge_size=-1,  # Don't merge files we don't plan to keep
    cleanup_input=False,
    globaltag=False,
    outputs=['DIGI-00000.root'],
    dataset=Dataset(
        files=SIM_dir,
        files_per_task=1,
        patterns=["*.root"]
    ),
    category=digi_resources
)

wfs.extend([digi])


### Lobster Config ###
config = Config(
    label=master_label,
    workdir=workdir_path,
    plotdir=plotdir_path,
    storage=storage,
    workflows=wfs,
    advanced=AdvancedOptions(
        bad_exit_codes=[127, 160],
        log_level=1,
        payload=10,
        osg_version='3.6',
        xrootd_servers=["cmsxrootd.fnal.gov", "cms-xrd-global.cern.ch", "cmsxcache.crc.nd.edu"]
    )
)
