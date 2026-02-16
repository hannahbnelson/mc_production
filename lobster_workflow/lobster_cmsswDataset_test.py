#IMPORTANT: The workers that are submitted to this lobster master, MUST come from T3 resources

import datetime
import os
import sys
import json
from os import path
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, Dataset, StorageConfiguration, Workflow

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')

RUN_SETUP = 'UL_production'
# UL_YEAR = 'UL16APV'
# UL_YEAR = 'UL16'
# UL_YEAR = 'UL17'
UL_YEAR = 'UL18'
prod_tag = "central_mini2nano_test"
version = "UL18_cmsswtest"

process_whitelist = []
coeff_whitelist   = []
runs_whitelist    = []    # (i.e. MG starting points)

master_label = 'T3_EFT_{tstamp}'.format(tstamp=timestamp_tag)

output_path  = "/store/user/$USER/mc/{tag}/{ver}".format(tag=prod_tag, ver=version)
workdir_path = "/tmpscratch/users/$USER/mc/{tag}/{ver}".format(tag=prod_tag, ver=version)
plotdir_path = "~/www/lobster/mc/{tag}/{ver}".format(tag=prod_tag, ver=version)

storage = StorageConfiguration(
    input = [
        # "file:///cms/cephfs/data/store/user/",
        # "root://hactar01.crc.nd.edu//store/user/",
        "root://hactar02.crc.nd.edu:1096//",
    ],
    
    output=[
        "file:///cms/cephfs/data" + output_path,
        "root://hactar01.crc.nd.edu//"+output_path,    
    ],
)

sample_list = {
    "UL18" : {
        "TTto2L2Nu_1Jets_smeft_MTT_0to700" : ['test_UL18MiniAOD_MTT_0_700.json',  'ul_cfgs/TOP-RunIISummer20UL18NanoAODv9-cfg.py'],
    }
}

nano_resources = Category(
            name="naod",
            cores=4,    
            memory=3000,
            disk=3000
        )

def get_file_list_from_json(jsonfile):
    with open(jsonfile, mode="r") as jf: 
        jsondata = json.load(jf)
        file_list = jsondata['files']

        # print("length of file_list: ", len(file_list))
        # print("type of file_list: ", type(file_list))
        # print("file list: ", file_list)
        return file_list

wf = []
print("Generating workflows:")
# for key, value in sample_list.items():
for key, value in sample_list[UL_YEAR].items():
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
        dataset=cmssw.Dataset(
            dataset="/TTto2L2Nu-1Jets-smeft_MTT-0to700_TuneCP5_13TeV_madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM",
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
