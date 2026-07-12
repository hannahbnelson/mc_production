import datetime
import os
import sys
from os import path
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, Dataset, ParentDataset, StorageConfiguration, Workflow

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

UL_YEAR = 'UL16APV'

prod_tag = 'UL16APV_DIGI'
version = timestamp_tag

master_label = 'condorfe_test_{tstamp}'.format(tstamp=timestamp_tag)

output_path  = "/store/user/$USER/mc/ttbarEFT_Run2/condorfe_test/{tag}/{ver}".format(tag=prod_tag, ver=version)
workdir_path = "/tmpscratch/users/$USER/mc/ttbarEFT_Run2/condorfe_test/{tag}/{ver}".format(tag=prod_tag, ver=version)
plotdir_path = "~/www/lobster/mc/ttbarEFT_Run2/condorfe_test/{tag}/{ver}".format(tag=prod_tag, ver=version)

# input_dir_path = "/cms/cephfs/data/store/user/"
input_dir_path = ""

DIGI_file = os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL16APV/postLHE/v1/DIGI_TTto2L2Nu_1Jets_smeft_MTT_900toInf/DIGI-00000_58249.root")
UL_config = 'ttbar_ulcfgs/TOP-RunIISummer20UL16HLTAPV_cfg.py'
cmssw_base_dir = '/users/hnelson2/mc_production/cmssw/'
release = os.path.join(cmssw_base_dir, 'CMSSW_8_0_36_UL_patch2/')

hlt_resources = Category(
    name='hlt',
    cores=3,
    memory=5000,
    disk=3000,
)

### Storage ### 
storage = StorageConfiguration(
    input = [
        "file:///cms/cephfs/data/store/user/",
        "root://cmsxrootd.crc.nd.edu//store/user/",
    ],
    
    output=[
        "file:///cms/cephfs/data" + output_path,
        "root://cmsxrootd.crc.nd.edu/"+output_path,    
    ],
)

wfs = []
name = "T01j2l_mtt900toInf"

hlt = Workflow(
    label=f"HLT_{name}",
    command=f"cmsRun {UL_config}",
    sandbox=cmssw.Sandbox(release=release),
    merge_size=-1,  # Don't merge files we don't plan to keep
    cleanup_input=False,
    globaltag=False,
    outputs=['HLT-00000.root'],
    dataset=Dataset(
        files=DIGI_file,
        files_per_task=1,
        patterns=["*.root"]
    ),
    category=hlt_resources
) 

wfs.extend([hlt])

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
        threshold_for_failure=40,
        threshold_for_skipping=40,
        osg_version='3.6',
        # xrootd_servers=["cmsxcache.crc.nd.edu", "cmsxrootd.fnal.gov", "cms-xrd-global.cern.ch"]
    )
)