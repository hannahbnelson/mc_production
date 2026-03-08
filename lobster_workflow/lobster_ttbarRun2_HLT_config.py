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

prod_tag = 'HLTtest'
version = timestamp_tag

master_label = 'CFE_postLHE_EFT_{tstamp}'.format(tstamp=timestamp_tag)

output_path  = "/store/user/$USER/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)
workdir_path = "/tmpscratch/users/$USER/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)
plotdir_path = "~/www/lobster/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)

# input_dir_path = "/cms/cephfs/data/store/user/"
input_dir_path = ""

SIM_dir = os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL17/postLHE/test_v4/SIM_TTto2L2Nu_1Jets_smeft_MTT_0to700/")
DIGI_dir = os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL17/DIGItest/20260224_1458/DIGI_TT01j2l_mtt0to700/")

UL_configs = {
    'UL16APV': {
        'sim':  'ttbar_ulcfgs/TOP-RunIISummer20UL16SIMAPV_cfg.py',
        'digi': 'ttbar_ulcfgs/TOP-RunIISummer20UL16DIGIAPV_cfg.py',
        'hlt':  'ttbar_ulcfgs/TOP-RunIISummer20UL16HLTAPV_cfg.py',
        'reco': 'ttbar_ulcfgs/TOP-RunIISummer20UL16RECOAPV_cfg.py',
        'mini': 'ttbar_ulcfgs/TOP-RunIISummer20UL16MiniAODAPVv2_cfg.py',
        'nano': 'ttbar_ulcfgs/TOP-RunIISummer20UL16NanoAODAPVv9_cfg.py',
    },
    'UL16': {
        'sim':  'ttbar_ulcfgs/TOP-RunIISummer20UL16SIM_cfg.py',
        'digi': 'ttbar_ulcfgs/TOP-RunIISummer20UL16DIGIPremix_cfg.py',
        'hlt':  'ttbar_ulcfgs/TOP-RunIISummer20UL16HLT_cfg.py',
        'reco': 'ttbar_ulcfgs/TOP-RunIISummer20UL16RECO_cfg.py',
        'mini': 'ttbar_ulcfgs/TOP-RunIISummer20UL16MiniAODv2_cfg.py',
        'nano': 'ttbar_ulcfgs/TOP-RunIISummer20UL16NanoAODv9_cfg.py',
    },
    'UL17': {
        'sim':  'ttbar_ulcfgs/TOP-RunIISummer20UL17SIM_cfg.py',
        'digi': 'ttbar_ulcfgs/TOP-RunIISummer20UL17DIGIPremix_cfg.py',
        'hlt':  'ttbar_ulcfgs/TOP-RunIISummer20UL17HLT_cfg.py',
        'reco': 'ttbar_ulcfgs/TOP-RunIISummer20UL17RECO_cfg.py',
        'mini': 'ttbar_ulcfgs/TOP-RunIISummer20UL17MiniAODv2_cfg.py',
        'nano': 'ttbar_ulcfgs/TOP-RunIISummer20UL17NanoAODv9_cfg.py',
    },
    'UL18': {
        'sim':  'ttbar_ulcfgs/TOP-RunIISummer20UL18SIM_cfg.py',
        'digi': 'ttbar_ulcfgs/TOP-RunIISummer20UL18DIGIPremix_cfg.py',
        'hlt':  'ttbar_ulcfgs/TOP-RunIISummer20UL18HLT_cfg.py',
        'reco': 'ttbar_ulcfgs/TOP-RunIISummer20UL18RECO_cfg.py',
        'mini': 'ttbar_ulcfgs/TOP-RunIISummer20UL18MiniAODv2_cfg.py',
        'nano': 'ttbar_ulcfgs/TOP-RunIISummer20UL18NanoAODv9_cfg.py',
    },
}

cmssw_base_dir = '/users/hnelson2/mc_production/cmssw/'

release_map = {
    'UL16APV': {
        'sim':  os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'digi': os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'hlt':  os.path.join(cmssw_base_dir, 'CMSSW_8_0_36_UL_patch2/'),
        'reco': os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'mini': os.path.join(cmssw_base_dir, 'CMSSW_10_6_25/'),
        'nano': os.path.join(cmssw_base_dir, 'CMSSW_10_6_26/'),
    },
    'UL16': {
        'sim':  os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'digi': os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'hlt':  os.path.join(cmssw_base_dir, 'CMSSW_8_0_36_UL_patch2/'),
        'reco': os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'mini': os.path.join(cmssw_base_dir, 'CMSSW_10_6_35_patch1/'),
        'nano': os.path.join(cmssw_base_dir, 'CMSSW_10_6_26/'),
    },
    'UL17': {
        'sim':  os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'digi': os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'hlt':  os.path.join(cmssw_base_dir, 'CMSSW_9_4_14_UL_patch1/'),
        'reco': os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'mini': os.path.join(cmssw_base_dir, 'CMSSW_10_6_20/'),
        'nano': os.path.join(cmssw_base_dir, 'CMSSW_10_6_26/'),
    },
    'UL18': {
        'sim':  os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'digi': os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'hlt':  os.path.join(cmssw_base_dir, 'CMSSW_10_2_16_UL/'),
        'reco': os.path.join(cmssw_base_dir, 'CMSSW_10_6_17_patch1/'),
        'mini': os.path.join(cmssw_base_dir, 'CMSSW_10_6_20/'),
        'nano': os.path.join(cmssw_base_dir, 'CMSSW_10_6_26/'),
    },
}

hlt_resources = Category(
    name='hlt',
    cores=3,
    memory=5000,
    disk=3000,
)
reco_resources = Category(
    name='reco',
    cores=3,
    memory=5000,
    disk=3000,
)
maod_resources = Category(
    name='maod',
    cores=2,
    memory=3500,
    disk=2000,
)
naod_resources = Category(
    name='naod',
    cores=2,
    memory=3500,
    disk=2000,
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

name = "T01j2l_mtt0to700"

hlt = Workflow(
    label=f"HLT_{name}",
    command=f"cmsRun {UL_configs[UL_YEAR]['hlt']}",
    sandbox=cmssw.Sandbox(release=release_map[UL_YEAR]['hlt']),
    merge_size=-1,  # Don't merge files we don't plan to keep
    cleanup_input=False,
    globaltag=False,
    outputs=['HLT-00000.root'],
    dataset=Dataset(
        files=DIGI_dir,
        files_per_task=1,
        patterns=["*.root"]
    ),
    category=hlt_resources
) 

reco = Workflow(
    label=f"RECO_{name}",
    command=f"cmsRun {UL_configs[UL_YEAR]['reco']}",
    sandbox=cmssw.Sandbox(release=release_map[UL_YEAR]['reco']),
    merge_size=-1,  # Don't merge files we don't plan to keep
    cleanup_input=True,
    globaltag=False,
    outputs=['RECO-00000.root'],
    dataset=ParentDataset(
        parent=hlt,
        units_per_task=1
    ),
    category=reco_resources
) 

maod = Workflow(
    label=f"mAOD_{name}",
    command=f"cmsRun {UL_configs[UL_YEAR]['mini']}",
    sandbox=cmssw.Sandbox(release=release_map[UL_YEAR]['mini']),
    merge_size=-1,  # Don't merge files we don't plan to keep
    cleanup_input=True,
    globaltag=False,
    outputs=['MAOD-00000.root'],
    dataset=ParentDataset(
        parent=reco,
        units_per_task=1
    ),
    category=maod_resources
) 

naod = Workflow(
    label=f"NAOD_{name}",
    command=f"cmsRun {UL_configs[UL_YEAR]['nano']}",
    sandbox=cmssw.Sandbox(release=release_map[UL_YEAR]['nano']),
    merge_size='256M',
    merge_command='python haddnano.py @outputfiles @inputfiles',
    extra_inputs=['/users/hnelson2/mc_production/cmssw/CMSSW_10_6_26/src/PhysicsTools/NanoAODTools/scripts/haddnano.py'],
    cleanup_input=False,
    globaltag=False,
    outputs=['NAOD-00000.root'],
    dataset=ParentDataset(
        parent=maod,
        units_per_task=1
    ),
    category=naod_resources
) 

wfs.extend([hlt, reco, maod, naod])


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
