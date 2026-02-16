#IMPORTANT: The workers that are submitted to this lobster master, MUST come from T3 resources

import datetime
import os
import sys
from os import path
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, MultiProductionDataset, StorageConfiguration, Workflow

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

# RUN_SETUP = 'UL_production'
UL_YEAR = 'UL17'
prod_tag = 'LHEGEN'
version='v1'

process_whitelist = []
coeff_whitelist   = []
runs_whitelist    = []    # (i.e. MG starting points)

master_label = 'T3_EFT_{tstamp}'.format(tstamp=timestamp_tag)

output_path  = "/store/user/$USER/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)
workdir_path = "/tmpscratch/users/$USER/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)
plotdir_path = "~/www/lobster/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)

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

Nevents_goal = {
    'UL16APV': {
        'mtt_0to700': 7169843,
        'mtt_700to900': 1977572,
        'mtt_900toInf': 2956891,
    },
    'UL16': {
        'mtt_0to700': 6956519,
        'mtt_700to900': 1979394,
        'mtt_900toInf': 2944757,
    },
    'UL17': {
        'mtt_0to700': 13823659,
        'mtt_700to900': 3832515,
        'mtt_900toInf': 5953931, 
    },
    'UL18': {
        'mtt_0to700': 21148226,
        'mtt_700to900': 6302785,
        'mtt_900toInf': 9186606,
    },
}

UL_configs = {
    'UL16APV': {
        'mtt_0to700': 'ttbar_ulcfgs/TOP-RunIISummer20UL16wmLHEGENAPV-mtt0to700_cfg.py',
        'mtt_700to900': 'ttbar_ulcfgs/TOP-RunIISummer20UL16wmLHEGENAPV-mtt700to900_cfg.py',
        'mtt_900toInf': 'ttbar_ulcfgs/TOP-RunIISummer20UL16wmLHEGENAPV-mtt900toInf_cfg.py',
    },
    'UL16': {
        'mtt_0to700': 'ttbar_ulcfgs/TOP-RunIISummer20UL16wmLHEGEN-mtt0to700_cfg.py',
        'mtt_700to900': 'ttbar_ulcfgs/TOP-RunIISummer20UL16wmLHEGEN-mtt700to900_cfg.py',
        'mtt_900toInf': 'ttbar_ulcfgs/TOP-RunIISummer20UL16wmLHEGEN-mtt900toInf_cfg.py',
    },
    'UL17': {
        'mtt_0to700': 'ttbar_ulcfgs/TOP-RunIISummer20UL17wmLHEGEN-mtt0to700_cfg.py',
        'mtt_700to900': 'ttbar_ulcfgs/TOP-RunIISummer20UL17wmLHEGEN-mtt700to900_cfg.py',
        'mtt_900toInf': 'ttbar_ulcfgs/TOP-RunIISummer20UL17wmLHEGEN-mtt900toInf_cfg.py',
    },
    'UL18': {
        'mtt_0to700': 'ttbar_ulcfgs/TOP-RunIISummer20UL18wmLHEGEN-mtt0to700_cfg.py',
        'mtt_700to900': 'ttbar_ulcfgs/TOP-RunIISummer20UL18wmLHEGEN-mtt700to900_cfg.py',
        'mtt_900toInf': 'ttbar_ulcfgs/TOP-RunIISummer20UL18wmLHEGEN-mtt900toInf_cfg.py',
    },
}

# in/out
LHEGEN_eff = {
    'mtt_0to700': 280/100,
    'mtt_700to900': 2225/100,
    'mtt_900toInf': 1369/100    
}

def Nevents_requested(year, mtt_range): 

    num = Nevents_goal[year][mtt_range] * LHEGEN_eff[mtt_range]
    return int(round(num))


gridpacks = {
    'TTto2L2Nu_1Jets_smeft_MTT_0to700': {
        'path': "hnelson2/gridpack_scans/TT01j2lBSMRef_slc7_amd64_gcc10_CMSSW_12_4_25_tarball.tar.xz",
        'cfg': UL_configs[UL_YEAR]['mtt_0to700'],
        'Nevents': Nevents_requested(year=UL_YEAR, mtt_range='mtt_0to700'),
        'Nevents_perlumi': 1000,
    },
    'TTto2L2Nu_1Jets_smeft_MTT_700to900': {
        'path': "hnelson2/gridpack_scans/TT01j2lBSMRef_slc7_amd64_gcc10_CMSSW_12_4_25_tarball.tar.xz",
        'cfg': UL_configs[UL_YEAR]['mtt_700to900'],
        'Nevents': Nevents_requested(year=UL_YEAR, mtt_range='mtt_700to900'),
        'Nevents_perlumi':1000,
    },
    'TTto2L2Nu_1Jets_smeft_MTT_900toInf': {
        'path': "hnelson2/gridpack_scans/TT01j2lBSMRef_slc7_amd64_gcc10_CMSSW_12_4_25_tarball.tar.xz",
        'cfg': UL_configs[UL_YEAR]['mtt_900toInf'],
        'Nevents': Nevents_requested(year=UL_YEAR, mtt_range='mtt_900toInf'),
        'Nevents_perlumi': 1000,
    },
}

LHEGEN = Category(
            name="LHEGEN",
            cores=1,
            memory=4000,
            disk=5000
        )

cmssw_LHE = '/users/hnelson2/cmssw/CMSSW_10_6_42/'

wf = []
print("Generating workflows:")
for key, gridpack in gridpacks.items():
    print(key)
    lhe = Workflow(
        label='LHEGEN_{tag}'.format(tag=key),
        command='cmsRun {cfg}'.format(cfg=gridpack['cfg']),
        sandbox=cmssw.Sandbox(release=cmssw_LHE),
        # merge_size='256M',
        # merge_command='python haddnano.py @outputfiles @inputfiles',
        # extra_inputs=['/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_10_6_26/src/PhysicsTools/NanoAODTools/scripts/haddnano.py'],
        cleanup_input=False,
        globaltag=False,
        outputs=["LHE-00000.root"],
        dataset=MultiProductionDataset(
            gridpacks=gridpack['path'],
            events_per_gridpack=gridpack['Nevents'],
            events_per_lumi=gridpack['Nevents_perlumi'],
            lumis_per_task=1,
            randomize_seeds=True
        ),
        category=LHEGEN
    )
    wf.extend([lhe])

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
