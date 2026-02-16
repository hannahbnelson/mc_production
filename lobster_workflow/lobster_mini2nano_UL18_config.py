#IMPORTANT: The workers that are submitted to this lobster master, MUST come from T3 resources

import datetime
import os
import sys
from os import path
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, Dataset, StorageConfiguration, Workflow

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

RUN_SETUP = 'UL_production'
UL_YEAR = 'UL18'
prod_tag = "central_mini2nano_test"
version = "TTto2L2Nu_1Jets_smeft_MTT_900toInf"

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

sample_list = {
    "TTto2L2Nu_1Jets_smeft_MTT_0to700" : ['hnelson2/mc/RunIISummer20UL18MiniAODv2/TTto2L2Nu-1Jets-smeft_MTT-0to700_TuneCP5_13TeV_madgraphMLM-pythia8',  'ul_cfgs/TOP-RunIISummer20UL18NanoAODv9-cfg.py'],
    "TTto2L2Nu_1Jets_smeft_MTT_700to900" : ['hnelson2/mc/RunIISummer20UL18MiniAODv2/TTto2L2Nu-1Jets-smeft_MTT-700to900_TuneCP5_13TeV_madgraphMLM-pythia8', 'ul_cfgs/TOP-RunIISummer20UL18NanoAODv9-cfg.py'],
    "TTto2L2Nu_1Jets_smeft_MTT_900toInf" : ['hnelson2/mc/RunIISummer20UL18MiniAODv2/TTto2L2Nu-1Jets-smeft_MTT-900toInf_TuneCP5_13TeV_madgraphMLM-pythia8', 'ul_cfgs/TOP-RunIISummer20UL18NanoAODv9-cfg.py'],
}

nano_resources = Category(
            name="naod",
            cores=4,    
            memory=3000,
            disk=3000
        )

wf = []
print("Generating workflows:")
for key, value in sample_list.items():
    print(key)
    #cmsswSource='/afs/crc.nd.edu/user/h/hnelson2/cmssw/noEFT/CMSSW_10_6_26/'
    #cmsswSource='/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_10_6_32_patch1/'
    cmsswSource = '/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_10_6_26/'
    nanoAOD = Workflow(
        label='nanoAOD_{tag}'.format(tag=key),
        command='cmsRun {cfg}'.format(cfg= value[1]),
        sandbox=cmssw.Sandbox(release=cmsswSource),
        merge_size='256M',
        merge_command='python haddnano.py @outputfiles @inputfiles',
        extra_inputs=['/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_10_6_26/src/PhysicsTools/NanoAODTools/scripts/haddnano.py'],
        cleanup_input=False,
        globaltag=False,
        outputs=['NAOD-00000.root'],
        dataset=Dataset(
            files=value[0],
            files_per_task=1,
            patterns=["*.root"],
        ),
        category=nano_resources,
    )
    wf.extend([nanoAOD])

config = Config(
    label=master_label,
    workdir=workdir_path,
    plotdir=plotdir_path,
    storage=storage,
    workflows=wf,
    advanced=AdvancedOptions(
        bad_exit_codes=[127, 160],
        log_level=1,
        payload=10,
        osg_version='3.6',
        #xrootd_servers=['ndcms.crc.nd.edu','cmsxrootd.fnal.gov']
    )
)
