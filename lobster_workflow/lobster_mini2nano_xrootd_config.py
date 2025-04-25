#IMPORTANT: The workers that are submitted to this lobster master, MUST come from T3 resources

'''
To make this work, the dataset validation has to be manually overridden such that in 
se.py XrootD.isfile is true and XrootD.isdir is false.
'''

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
prod_tag = "central_ttbar_nanoAOD"
# version = "UL18"
version = UL_YEAR

process_whitelist = []
coeff_whitelist   = []
runs_whitelist    = []    # (i.e. MG starting points)

master_label = 'CRC_EFT_{tstamp}'.format(tstamp=timestamp_tag)

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
    "UL16APV":{
        "TTto2L2Nu_1Jets_smeft_MTT_0to700":     ['sample_jsons/UL16APV_0_700_miniAOD_files.json', 'ul_cfgs/UL16APV_NAOD_cfg.py'],
        "TTto2L2Nu_1Jets_smeft_MTT_700to900":   ['sample_jsons/UL16APV_700_900_miniAOD_files.json', 'ul_cfgs/UL16APV_NAOD_cfg.py'],
        "TTto2L2Nu_1Jets_smeft_MTT_900toInf":   ['sample_jsons/UL16APV_900_Inf_miniAOD_files.json', 'ul_cfgs/UL16APV_NAOD_cfg.py'],
    },
    "UL16" : {
        "TTto2L2Nu_1Jets_smeft_MTT_0to700":     ['sample_jsons/UL16_0_700_miniAOD_files.json', 'ul_cfgs/UL16_NAOD_cfg.py'],
        "TTto2L2Nu_1Jets_smeft_MTT_700to900":   ['sample_jsons/UL16_700_900_miniAOD_files.json', 'ul_cfgs/UL16_NAOD_cfg.py'],
        "TTto2L2Nu_1Jets_smeft_MTT_900toInf":   ['sample_jsons/UL16_900_Inf_miniAOD_files.json', 'ul_cfgs/UL16_NAOD_cfg.py'],
    },
    "UL17" : {
        "TTto2L2Nu_1Jets_smeft_MTT_0to700":     ['sample_jsons/UL17_0_700_miniAOD_files.json', 'ul_cfgs/TOP-RunIISummer20UL17NanoAODv9-cfg.py'],
        "TTto2L2Nu_1Jets_smeft_MTT_700to900":   ['sample_jsons/UL17_700_900_miniAOD_files.json', 'ul_cfgs/TOP-RunIISummer20UL17NanoAODv9-cfg.py'],
        "TTto2L2Nu_1Jets_smeft_MTT_900toInf":   ['sample_jsons/UL17_900_Inf_miniAOD_files.json', 'ul_cfgs/TOP-RunIISummer20UL17NanoAODv9-cfg.py'],
    },
    "UL18" : {
        "TTto2L2Nu_1Jets_smeft_MTT_0to700" :    ['sample_jsons/UL18_0_700_miniAOD_files.json',  'ul_cfgs/TOP-RunIISummer20UL18NanoAODv9-cfg.py'],
        "TTto2L2Nu_1Jets_smeft_MTT_700to900" :  ['sample_jsons/UL18_700_900_miniAOD_files.json', 'ul_cfgs/TOP-RunIISummer20UL18NanoAODv9-cfg.py'],
        "TTto2L2Nu_1Jets_smeft_MTT_900toInf" :  ['sample_jsons/UL18_900_Inf_miniAOD_files.json', 'ul_cfgs/TOP-RunIISummer20UL18NanoAODv9-cfg.py'],
    },
}

# sample_list = {
#     "UL18" : {
#         "TTto2L2Nu_1Jets_smeft_MTT_0to700" : ['test_UL18MiniAOD_MTT_0_700.json',  'ul_cfgs/TOP-RunIISummer20UL18NanoAODv9-cfg.py'],
#     }
# }

nano_resources = Category(
            name="naod",
            cores=4,    
            memory=6000,
            disk=6000
        )

def get_file_list_from_json(jsonfile):
    
    with open(jsonfile, mode="r") as jf: 
        jsondata = json.load(jf)
        file_list = jsondata['files']

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
        dataset=Dataset(
            # files=value[0],
            files=get_file_list_from_json(value[0]),
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
        xrootd_servers=['hactar02.crc.nd.edu:1096', 'cmsxrootd.fnal.gov']
    )
)
