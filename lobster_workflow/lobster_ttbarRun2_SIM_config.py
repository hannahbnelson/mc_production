import datetime
import os
import sys
from os import path
from lobster import cmssw
from lobster.core import AdvancedOptions, Category, Config, Dataset, ParentDataset, StorageConfiguration, Workflow

timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')


# UL_YEAR = 'UL16APV'
# UL_YEAR = 'UL16'
# UL_YEAR = 'UL17'
UL_YEAR = 'UL18'

# prod_tag = 'postLHE'
prod_tag = 'SIM'
version = 'v1'

master_label = 'SIM_{tstamp}'.format(tstamp=timestamp_tag)

output_path  = "/store/user/$USER/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)
workdir_path = "/tmpscratch/users/$USER/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)
plotdir_path = "~/www/lobster/mc/ttbarEFT_Run2/{year}/{tag}/{ver}".format(year=UL_YEAR, tag=prod_tag, ver=version)

print(f"\n\n using timestamp: {timestamp_tag} \n\n")

# input_dir_path = "/cms/cephfs/data/store/user/"
input_dir_path = ""

LHEGEN_dirs_all = {
    # "UL16": {
      # "TTto2L2Nu_1Jets_smeft_MTT_0to700":     [
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0000/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0001/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0002/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0003/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0004/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0005/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0006/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0007/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0008/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v1/260223_174050/0009/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0000/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0001/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0002/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0003/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0004/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0005/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0006/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0007/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0008/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0009/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v2/260223_190604/0010/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v3/260224_150150/0000/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v3/260224_150150/0001/"),
      #       os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_0to700/crab_UL16_mtt0to700_v3/260224_150150/0002/"),
      #   ],
    #   "TTto2L2Nu_1Jets_smeft_MTT_700to900":   [
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0003/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0004/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0005/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0006/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0007/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0008/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0009/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v1/260223_201609/0010/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0003/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0004/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0005/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0006/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0007/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0008/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0009/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v2/260223_211405/0010/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0003/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0004/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0005/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0006/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0007/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0008/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0009/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v3/260223_211523/0010/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0003/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0004/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0005/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0006/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0007/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0008/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0009/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v4/260223_211620/0010/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v5/260224_150629/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v5/260224_150629/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v5/260224_150629/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v5/260224_150629/0003/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v5/260224_150629/0004/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v5/260224_150629/0005/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v5/260224_150629/0006/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v5/260224_150629/0007/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_700to900/crab_UL16_mtt700to900_v5/260224_150629/0008/"),
    #       ],
    #   "TTto2L2Nu_1Jets_smeft_MTT_900toInf": [
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0003/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0004/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0005/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0006/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0007/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0008/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0009/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v1/260224_211241/0010/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0003/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0004/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0005/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0006/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0007/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0008/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0009/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v2/260224_211339/0010/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0003/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0004/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0005/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0006/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0007/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0008/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0009/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v3/260224_211746/0010/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0003/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0004/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0005/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0006/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0007/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0008/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0009/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v4/260224_211759/0010/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v5/260227_015432/0000/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v5/260227_015432/0001/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v5/260227_015432/0002/"),
    #         os.path.join(input_dir_path, "hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/TT01j2l_SMEFTsim_LHEGEN_UL16_900toInf/crab_UL16_mtt900toInf_v5/260227_015432/0003/"),
    #     ],  
    # },
    # "UL17": { # UL17/postLHE/v1/
    #     "TTto2L2Nu_1Jets_smeft_MTT_0to700_v1":     os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL17/LHEGEN/v1/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_0to700/"),
    #     "TTto2L2Nu_1Jets_smeft_MTT_700to900_v1":   os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL17/LHEGEN/v1/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_700to900/"),
    #     "TTto2L2Nu_1Jets_smeft_MTT_900toInf_v1":   os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL17/LHEGEN/v1/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_900toInf/"),
    #     "TTto2L2Nu_1Jets_smeft_MTT_0to700_v2":     os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL17/LHEGEN/v2/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_0to700/"),
    #     "TTto2L2Nu_1Jets_smeft_MTT_700to900_v2":   os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL17/LHEGEN/v2/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_700to900/"),
    #     "TTto2L2Nu_1Jets_smeft_MTT_900toInf_v2":   os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL17/LHEGEN/v2/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_900toInf/"),
    # },
    "UL18": {
      "TTto2L2Nu_1Jets_smeft_MTT_0to700":     [
            os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL18/LHEGEN/v1/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_0to700/"), 
            os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL18/LHEGEN/v2/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_0to700"), 
                  ],
      "TTto2L2Nu_1Jets_smeft_MTT_700to900":   [
            os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL18/LHEGEN/v1/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_700to900"), 
            os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL18/LHEGEN/v2/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_700to900"), 
                  ],
      "TTto2L2Nu_1Jets_smeft_MTT_900toInf":   [
            os.path.join(input_dir_path, "hnelson2/mc/ttbarEFT_Run2/UL18/LHEGEN/v1/LHEGEN_TTto2L2Nu_1Jets_smeft_MTT_900toInf"),  
                  ],
    },
}

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

### Resources for Each WF Step ### 
sim_resources = Category(
    name='sim',
    cores=6,
    memory=4000,
    disk=4000,
    mode='fixed',
)
digi_resources = Category(
    name='digi',
    cores=6,
    memory=7800,
    disk=6000,
)
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

lhe_dirs = LHEGEN_dirs_all[UL_YEAR]
for name, lhe_path in lhe_dirs.items():
    print(f"LHE input dir: {lhe_path}")

    print(f"{release_map[UL_YEAR]['sim']}")
    print(f"{UL_configs[UL_YEAR]['sim']}")
    print(f"{lhe_path}")

    sim = Workflow(
        label=f"SIM_{name}",
        command=f"cmsRun {UL_configs[UL_YEAR]['sim']}",
        sandbox=cmssw.Sandbox(release=release_map[UL_YEAR]['sim']),
        merge_size=-1,  # Don't merge files we don't plan to keep
        cleanup_input=False, #Don't clean up LHEGEN files!!!
        globaltag=False,
        outputs=['SIM-00000.root'],
        dataset=Dataset(
            files=lhe_path,
            files_per_task=1,
            patterns=["*.root"]
        ),
        category=sim_resources
    )

    wfs.extend([sim])

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
