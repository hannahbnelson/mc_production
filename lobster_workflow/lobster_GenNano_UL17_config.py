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
version = "tt_ttJets_LO_SMEFT_20231010"
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
    'tt_LO_SMEFT': ["hnelson2/gridpack_scans/ttbarEFT/tt_LO_SMEFT_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LO_cfg.py',10000, 500],
    'ttJets_LO_SMEFT': ["hnelson2/gridpack_scans/ttbarEFT/ttJets_LO_SMEFT_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 10000, 500],
    #'ttJets_LO_ref': ["hnelson2/gridpack_scans/ttbarEFT/ttJets_LO_ref_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", 'ul_cfgs/nanoGen2017_LOJets_cfg.py', 40000, 500],
    # 'tt_LO_SMEFT': ["rgoldouz/gridpack_scans/SMEFT/tt_LO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz", 10, 10]
}

gridpack_list_old = {
    'tt_LO_SMEFTrwgt':["rgoldouz/gridpack_scans/SMEFT/tt_LO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',200000, 1000],
    'tt_LO_SMEFTrwgt_v2':["rgoldouz/gridpack_scans/SMEFT/tt_LO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',5000000, 10000],
    'tt_LO_SMEFTrwgt_v3':["rgoldouz/gridpack_scans/SMEFT/tt_LO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',5000000, 10000],
    'tt_LO_SMEFTrwgt_topPtG300':["rgoldouz/gridpack_scans/SMEFT/tt_LO_SMEFT_topPtG300_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',2000000, 10000],
    'ttJets_LO_SMEFTrwgt':["rgoldouz/gridpack_scans/SMEFT/ttJets_LO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz",'ul_cfgs/nanoGen2017_LOJets_cfg.py',250000, 1000],
    'tt_NLO_SMEFTrwgt':["rgoldouz/gridpack_scans/SMEFT/tt_NLO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz",'ul_cfgs/nanoGen2017_NLO_cfg.py',300000, 1000],
    'tt_NLO_SMEFTrwgt_20Nov2022':["rgoldouz/gridpack_scans/SMEFT/tt_NLO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball_20Nov2022.tar.xz",'ul_cfgs/nanoGen2017_NLO_cfg.py',300000, 1000],
    'tt_LOforMLctGcQq83_SMEFTrwgt':["rgoldouz/gridpack_scans/SMEFT/tt_LOforMLctGcQq83_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',200000, 1000],
    'tt_NLO_SMEFTrwgt_14Dec2022':["rgoldouz/gridpack_scans/SMEFT/tt_NLO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball_14Dec2022.tar.xz",'ul_cfgs/nanoGen2017_NLO_cfg.py',400000, 1000],
    'tt_NLO_SMEFTrwgt__noTopDecay':["rgoldouz/gridpack_scans/SMEFT/tt_NLO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball_noTopDecay.tar.xz",'ul_cfgs/nanoGen2017_NLO_cfg.py',400000, 1000],
    'tt_NLO_SMEFTrwgt_closeToSM':["rgoldouz/gridpack_scans/SMEFT/tt_NLO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball_closeToSM.tar.xz",'ul_cfgs/nanoGen2017_NLO_cfg.py',400000, 1000],
    'tt_NLO_SMEFTrwgt_AllWCZero':["rgoldouz/gridpack_scans/SMEFT/tt_NLO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball_AllWCZero.tar.xz",'ul_cfgs/nanoGen2017_NLO_cfg.py',400000, 1000],
    'tt_NLO_SMEFTrwgt_20Nov2022NoDecayAllWCzero':["rgoldouz/gridpack_scans/SMEFT/tt_NLO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball_20Nov2022NoDecayAllWCzero.tar.xz",'ul_cfgs/nanoGen2017_NLO_cfg.py',400000, 1000],
    'tt_NLO_SMEFTrwgt_29Jan2023':["rgoldouz/gridpack_scans/SMEFT/tt_NLO_SMEFT_slc7_amd64_gcc900_CMSSW_12_0_2_tarball_29Jan2023.tar.xz",'ul_cfgs/nanoGen2017_NLO_cfg.py',400000, 1000],
    'tW_LO_SMEFTrwgt':["rgoldouz/gridpack_scans/SMEFT/tWLO_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',400000, 1000],
    'tW_LOv2_SMEFTrwgt':["rgoldouz/gridpack_scans/SMEFT/tWLO_v2_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',400000, 1000],
    'llb_LO_SMEFTrwgt':["rgoldouz/gridpack_scans/SMEFT/llb_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',300000, 1000],
    'tt_NLO_SMEFTrwgt_NOMSMG332':["rgoldouz/gridpack_scans/SMEFT/tt_NLO_SMEFTNOMSMG332_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz",'ul_cfgs/nanoGen2017_NLO_cfg.py',400000, 1000],

    'tuFCNCrwgt_tllProduction_noH':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noH_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',400000, 1000],
    'tuFCNCrwgt_ullDecay_noH':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noH_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',300000, 1000],
    'tuFCNCrwgt_tHProduction':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tHProduction_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',200000, 1000],
    'tuFCNCrwgt_uHDecay':["rgoldouz/gridpack_scans/FCNC/tuFCNC_uHDecay_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',200000, 1000],

    'tcFCNCrwgt_tllProduction_noH':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noH_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',400000, 1000],
    'tcFCNCrwgt_cllDecay_noH':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noH_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',300000, 1000],
    'tcFCNCrwgt_tHProduction':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tHProduction_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',200000, 1000],
    'tcFCNCrwgt_cHDecay':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cHDecay_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',200000, 1000],

    'tuFCNC_uuddTOtt_LO_SMEFTrwgt_ctz':["rgoldouz/gridpack_scans/MLEFT/uuddTOtt_LO_SMEFT_ctz_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_uuddTOtt_LO_SMEFTrwgt_ctW':["rgoldouz/gridpack_scans/MLEFT/uuddTOtt_LO_SMEFT_ctW_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],

    'tuFCNC_tllProduction_noHcpQM':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHcpQM_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHcpt':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHcpt_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHcQe':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHcQe_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHcQlM':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHcQlM_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHctA':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHctA_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHcte':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHcte_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHctG':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHctG_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHctl':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHctl_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHctlS':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHctlS_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHctlT':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHctlT_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tllProduction_noHctZ':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tllProduction_noHctZ_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHcpQM':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHcpQM_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHcpt':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHcpt_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHcQe':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHcQe_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHcQlM':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHcQlM_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHctA':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHctA_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHcte':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHcte_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHctl':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHctl_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHctlS':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHctlS_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHctlT':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHctlT_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_ullDecay_noHctZ':["rgoldouz/gridpack_scans/FCNC/tuFCNC_ullDecay_noHctZ_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tHProductionctG':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tHProductionctG_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tuFCNC_tHProductionctp':["rgoldouz/gridpack_scans/FCNC/tuFCNC_tHProductionctp_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],

    'tcFCNC_tllProduction_noHcpQM':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHcpQM_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHcpt':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHcpt_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHcQe':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHcQe_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHcQlM':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHcQlM_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHctA':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHctA_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHcte':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHcte_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHctG':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHctG_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHctl':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHctl_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHctlS':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHctlS_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHctlT':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHctlT_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tllProduction_noHctZ':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tllProduction_noHctZ_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHcpQM':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHcpQM_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHcpt':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHcpt_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHcQe':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHcQe_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHcQlM':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHcQlM_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHctA':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHctA_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHcte':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHcte_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHctl':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHctl_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHctlS':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHctlS_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHctlT':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHctlT_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_cllDecay_noHctZ':["rgoldouz/gridpack_scans/FCNC/tcFCNC_cllDecay_noHctZ_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tHProductionctG':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tHProductionctG_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
    'tcFCNC_tHProductionctp':["rgoldouz/gridpack_scans/FCNC/tcFCNC_tHProductionctp_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",'ul_cfgs/nanoGen2017_LO_cfg.py',150000, 1000],
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
    cmsswSSource='/afs/crc.nd.edu/user/h/hnelson2/cmssw/CMSSW_10_6_26/'
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
