import commands
from CRABClient.UserUtilities import config

config = config()

config.General.requestName          = 'UL16_mtt0to700_v1'
config.General.transferOutputs      = True
config.General.transferLogs         = True
config.General.workArea             = 'crabLHEGEN'

config.JobType.pluginName           = 'PrivateMC'
config.JobType.psetName             = 'TOP-RunIISummer20UL16wmLHEGEN-mtt0to700_cfg.py'
config.JobType.numCores             = 2
config.JobType.maxMemoryMB          = 5000

config.Data.splitting     	        = 'EventBased'
config.Data.unitsPerJob             = 1000
config.Data.totalUnits              = 9739130
config.Data.outputPrimaryDataset    = 'TT01j2l_SMEFTsim_LHEGEN_UL16_0to700'
config.Data.outLFNDirBase           = '/store/user/hnelson/mc/ttbarEFT_Run2/UL16/LHEGEN/'

config.Site.storageSite = 'T3_US_NotreDame'
