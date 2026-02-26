# This needs to be run inside a cc7 container 
# /cvmfs/cms.cern.ch/common/cmssw-cc7 --cleanenv -B /scratch365/ -B /opt/

#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh

CFG_DIR=/users/hnelson2/mc_production/lobster_workflow/ttbar_ulcfgs/
DIGI_PREMIX_DIR=/users/hnelson2/mc_production/lobster_workflow/make_cfgs/
CMSSW_DIR=/users/hnelson2/mc_production/cmssw/

FGEN=GEN-00000.root
FSIM=SIM-00000.root
FDIGI=DIGI-00000.root
FHLT=HLT-00000.root
FRECO=RECO-00000.root
FMINI=MAOD-00000.root
FNANO=NAOD-00000.root

setup_rel(){

    echo $CMSSW_DIR

    cd $CMSSW_DIR
    printf "\nSet up CMSSW release for $1...\n"
    if [ -r $1/src ] ; then
        echo release $1 already exists
    else
        scram p CMSSW $1
    fi
    cd $1/src
    eval `scram runtime -sh`

    scram b

    cd $CFG_DIR
    printf "CMSSW base: $CMSSW_BASE\n"
}

### setup CMSSW_10_6_17_patch1
(
    export SCRAM_ARCH=slc7_amd64_gcc700
    REL=CMSSW_10_6_17_patch1
    setup_rel $REL

    echo $CFG_DIR
    cd $CFG_DIR
    echo "$PWD"

    # 2016 APV #
    # cmsDriver.py  --era Run2_2016_HIPM --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot Realistic25ns13TeV2016Collision --step SIM --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_preVFP_v8 --datatier GEN-SIM --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL16SIMAPV_cfg.py --fileout file:$FSIM --filein file:$FGEN --runUnscheduled --no_exec --mc
    ## with dbs command # cmsDriver.py  --era Run2_2016_HIPM --customise Configuration/DataProcessing/Utils.addMonitoring --pileup 2016_25ns_UltraLegacy_PoissonOOTPU   --step DIGI,L1,DIGI2RAW --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_preVFP_v8 --datatier GEN-SIM-DIGI --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL16DIGIAPV_cfg.py --fileout file:$FDIGI --filein file:$FSIM --pileup_input "dbs:/MinBias_TuneCP5_13TeV-pythia8/RunIISummer20UL16SIM-106X_mcRun2_asymptotic_v13-v2/GEN-SIM" --runUnscheduled --no_exec --mc 
    cmsDriver.py  --era Run2_2016_HIPM --customise Configuration/DataProcessing/Utils.addMonitoring --pileup 2016_25ns_UltraLegacy_PoissonOOTPU   --step DIGI,L1,DIGI2RAW --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_preVFP_v8 --datatier GEN-SIM-DIGI --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL16DIGIAPV_cfg.py --fileout file:$FDIGI --filein file:$FSIM --pileup_input "filelist:$DIGI_PREMIX_DIR/2016APV_DIGIPremix.txt" --runUnscheduled --no_exec --mc 
    # cmsDriver.py  --era Run2_2016_HIPM --customise Configuration/DataProcessing/Utils.addMonitoring --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_preVFP_v8 --datatier AODSIM --eventcontent AODSIM --python_filename TOP-RunIISummer20UL16RECOAPV_cfg.py --fileout file:$FRECO --filein file:$FHLT --runUnscheduled --no_exec --mc 

    # 2016 #
    # cmsDriver.py  --era Run2_2016 --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot Realistic25ns13TeV2016Collision --step SIM --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_v13 --datatier GEN-SIM --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL16SIM_cfg.py --fileout file:$FSIM --filein file:$FGEN --runUnscheduled --no_exec --mc
    ## with dbs command # cmsDriver.py  --era Run2_2016 --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers premix_stage2 --datamix PreMix --step DIGI,DATAMIX,L1,DIGI2RAW --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_v13 --datatier GEN-SIM-DIGI --eventcontent PREMIXRAW --python_filename TOP-RunIISummer20UL16DIGIPremix_cfg.py --fileout file:$FDIGI --filein file:$FSIM  --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX" --runUnscheduled --no_exec --mc
    cmsDriver.py  --era Run2_2016 --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers premix_stage2 --datamix PreMix --step DIGI,DATAMIX,L1,DIGI2RAW --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_v13 --datatier GEN-SIM-DIGI --eventcontent PREMIXRAW --python_filename TOP-RunIISummer20UL16DIGIPremix_cfg.py --fileout file:$FDIGI --filein file:$FSIM  --pileup_input "filelist:$DIGI_PREMIX_DIR/2016_DIGIPremix.txt" --runUnscheduled --no_exec --mc
    # cmsDriver.py  --era Run2_2016 --customise Configuration/DataProcessing/Utils.addMonitoring --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_v13 --datatier AODSIM --eventcontent AODSIM --python_filename TOP-RunIISummer20UL16RECO_cfg.py --fileout file:$FRECO --filein file:$FHLT --runUnscheduled --no_exec --mc

    # 2017 #
    # cmsDriver.py  --era Run2_2017 --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot Realistic25ns13TeVEarly2017Collision --step SIM --geometry DB:Extended --conditions 106X_mc2017_realistic_v6 --datatier GEN-SIM --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL17SIM_cfg.py --fileout file:$FSIM --filein file:$FGEN --runUnscheduled --no_exec --mc
    ## with dbs command # cmsDriver.py  --era Run2_2017 --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers premix_stage2 --datamix PreMix --step DIGI,DATAMIX,L1,DIGI2RAW --geometry DB:Extended --conditions 106X_mc2017_realistic_v6 --datatier GEN-SIM-DIGI --eventcontent PREMIXRAW --python_filename TOP-RunIISummer20UL17DIGIPremix_cfg.py --fileout file:$FDIGI --filein file:$FSIM --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX" --runUnscheduled --no_exec --mc
    cmsDriver.py  --era Run2_2017 --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers premix_stage2 --datamix PreMix --step DIGI,DATAMIX,L1,DIGI2RAW --geometry DB:Extended --conditions 106X_mc2017_realistic_v6 --datatier GEN-SIM-DIGI --eventcontent PREMIXRAW --python_filename TOP-RunIISummer20UL17DIGIPremix_cfg.py --fileout file:$FDIGI --filein file:$FSIM --pileup_input "filelist:$DIGI_PREMIX_DIR/2017_DIGIPremix.txt" --runUnscheduled --no_exec --mc
    # cmsDriver.py  --era Run2_2017 --customise Configuration/DataProcessing/Utils.addMonitoring --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --conditions 106X_mc2017_realistic_v6 --datatier AODSIM --eventcontent AODSIM --python_filename TOP-RunIISummer20UL17RECO_cfg.py --fileout file:$FRECO --filein file:$FHLT --runUnscheduled --no_exec --mc

    # 2018 #
    # cmsDriver.py  --era Run2_2018 --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --geometry DB:Extended --conditions 106X_upgrade2018_realistic_v11_L1v1 --datatier GEN-SIM --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL18SIM_cfg.py --fileout file:$FSIM --filein file:$FGEN --runUnscheduled --no_exec --mc
    ## with dbs command # cmsDriver.py  --era Run2_2018 --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers premix_stage2 --datamix PreMix --step DIGI,DATAMIX,L1,DIGI2RAW --geometry DB:Extended --conditions 106X_upgrade2018_realistic_v11_L1v1 --datatier GEN-SIM-DIGI --eventcontent PREMIXRAW --python_filename TOP-RunIISummer20UL18DIGIPremix_cfg.py --fileout file:$FDIGI --filein file:$FSIM --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" --runUnscheduled --no_exec --mc
    cmsDriver.py  --era Run2_2018 --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers premix_stage2 --datamix PreMix --step DIGI,DATAMIX,L1,DIGI2RAW --geometry DB:Extended --conditions 106X_upgrade2018_realistic_v11_L1v1 --datatier GEN-SIM-DIGI --eventcontent PREMIXRAW --python_filename TOP-RunIISummer20UL18DIGIPremix_cfg.py --fileout file:$FDIGI --filein file:$FSIM --pileup_input "filelist:$DIGI_PREMIX_DIR/2018_DIGIPremix.txt" --runUnscheduled --no_exec --mc
    # cmsDriver.py  --era Run2_2018 --customise Configuration/DataProcessing/Utils.addMonitoring --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --conditions 106X_upgrade2018_realistic_v11_L1v1 --datatier AODSIM --eventcontent AODSIM --python_filename TOP-RunIISummer20UL18RECO_cfg.py --fileout file:$FRECO --filein file:$FHLT --runUnscheduled --no_exec --mc
)

# ### setup CMSSW_8_0_36_UL_patch2
# (
#     export SCRAM_ARCH=slc7_amd64_gcc530
#     REL=CMSSW_8_0_36_UL_patch2
#     setup_rel $REL

#     echo "$PWD"

#     # 2016 APV #
#     cmsDriver.py  --era Run2_2016 --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" --customise Configuration/DataProcessing/Utils.addMonitoring --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*" --step HLT:25ns15e33_v4 --geometry DB:Extended --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --datatier GEN-SIM-RAW --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL16HLTAPV_cfg.py --fileout file:$FHLT --filein file:$FDIGI --no_exec --mc

#     # 2016 #
#     cmsDriver.py  --era Run2_2016 --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" --customise Configuration/DataProcessing/Utils.addMonitoring --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*" --step HLT:25ns15e33_v4 --geometry DB:Extended --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --datatier GEN-SIM-RAW --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL16HLT_cfg.py --fileout file:$FHLT --filein file:$FDIGI --no_exec --mc   
# )


# ### setup CMSSW_10_6_25
# (
#     export SCRAM_ARCH=slc7_amd64_gcc700
#     REL=CMSSW_10_6_25
#     setup_rel $REL

#     echo "$PWD"

#     # 2016 APV #
#     cmsDriver.py  --era Run2_2016_HIPM --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers run2_miniAOD_UL --step PAT --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_preVFP_v11 --datatier MINIAODSIM --eventcontent MINIAODSIM --python_filename TOP-RunIISummer20UL16MiniAODAPVv2_cfg.py --fileout file:$FMINI --filein file:$FRECO --runUnscheduled --no_exec --mc

# )

# ### setup CMSSW_10_6_35_patch1
# (
#     export SCRAM_ARCH=slc7_amd64_gcc700
#     REL=CMSSW_10_6_35_patch1
#     setup_rel $REL

#     echo "$PWD"

#     # 2016 #
#     cmsDriver.py  --era Run2_2016,bParking --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers run2_miniAOD_UL --step PAT --geometry DB:Extended --conditions 106X_mcRun2_asymptotic_v17 --datatier MINIAODSIM --eventcontent MINIAODSIM --python_filename TOP-RunIISummer20UL16MiniAODv2_cfg.py --fileout file:$FMINI --filein file:$FRECO --runUnscheduled --no_exec --mc
# )

# ### setup CMSSW_9_4_14_UL_patch1
# (
#     export SCRAM_ARCH=slc7_amd64_gcc630
#     REL=CMSSW_9_4_14_UL_patch1
#     setup_rel $REL

#     echo "$PWD"

#     # 2017 #
#     cmsDriver.py  --era Run2_2017 --customise Configuration/DataProcessing/Utils.addMonitoring --step HLT:2e34v40 --geometry DB:Extended --conditions 94X_mc2017_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --datatier GEN-SIM-RAW --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL17HLT_cfg.py --fileout file:$FHLT --filein file:$FDIGI --no_exec --mc

# )


# ### setup CMSSW_10_6_20
# (
#     export SCRAM_ARCH=slc7_amd64_gcc700
#     REL=CMSSW_10_6_20
#     setup_rel $REL

#     echo "$PWD"

#     # 2017 #
#     cmsDriver.py  --era Run2_2017 --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers run2_miniAOD_UL --step PAT --geometry DB:Extended --conditions 106X_mc2017_realistic_v9 --datatier MINIAODSIM --eventcontent MINIAODSIM --python_filename TOP-RunIISummer20UL17MiniAODv2_cfg.py --fileout file:$FMINI --filein file:$FRECO --runUnscheduled --no_exec --mc

#     # 2018 #
#     cmsDriver.py  --era Run2_2018 --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers run2_miniAOD_UL --step PAT --geometry DB:Extended --conditions 106X_upgrade2018_realistic_v16_L1v1 --datatier MINIAODSIM --eventcontent MINIAODSIM --python_filename TOP-RunIISummer20UL18MiniAODv2_cfg.py --fileout file:$FMINI --runUnscheduled --no_exec --mc
# )

# ### setup CMSSW_10_2_16_UL
# (
#     export SCRAM_ARCH=slc7_amd64_gcc700
#     REL=CMSSW_10_2_16_UL
#     setup_rel $REL

#     echo "$PWD"

#     # 2018 #
#     cmsDriver.py  --era Run2_2018 --customise Configuration/DataProcessing/Utils.addMonitoring --step HLT:2018v32 --geometry DB:Extended --conditions 102X_upgrade2018_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --datatier GEN-SIM-RAW --eventcontent RAWSIM --python_filename TOP-RunIISummer20UL18HLT_cfg.py --fileout file:$FHLT --filein file:$FDIGI --no_exec --mc
# )

### go to special Nano CMSSW version
# This cmssw release is previously setup for EFT following instructions
# https://github.com/hannahbnelson/mc_production/blob/main/README.md
# (
#     export SCRAM_ARCH=slc7_amd64_gcc700
#     REL=CMSSW_10_6_26

#     cd $CMSSW_DIR/$REL/src
#     scram b
#     cd $CFG_DIR

#     cmsDriver.py  --era Run2_2016_HIPM,run2_nanoAOD_106Xv2 --customise Configuration/DataProcessing/Utils.addMonitoring --step NANO --conditions 106X_mcRun2_asymptotic_preVFP_v11 --datatier NANOAODSIM --eventcontent NANOAODSIM --python_filename TOP-RunIISummer20UL16NanoAODAPVv9_cfg.py --fileout file:NAOD-00000.root --filein file:MAOD-00000.root --no_exec --mc
#     cmsDriver.py  --era Run2_2016,run2_nanoAOD_106Xv2 --customise Configuration/DataProcessing/Utils.addMonitoring --step NANO --conditions 106X_mcRun2_asymptotic_v17 --datatier NANOAODSIM --eventcontent NANOAODSIM --python_filename TOP-RunIISummer20UL16NanoAODv9_cfg.py --fileout file:NAOD-00000.root --filein file:MAOD-00000.root --no_exec --mc
#     cmsDriver.py  --era Run2_2017,run2_nanoAOD_106Xv2 --customise Configuration/DataProcessing/Utils.addMonitoring --step NANO --conditions 106X_mc2017_realistic_v9 --datatier NANOAODSIM --eventcontent NANOAODSIM --python_filename TOP-RunIISummer20UL17NanoAODv9_cfg.py --fileout file:NAOD-00000.root --filein file:MAOD-00000.root --no_exec --mc
#     cmsDriver.py  --era Run2_2018,run2_nanoAOD_106Xv2 --customise Configuration/DataProcessing/Utils.addMonitoring --step NANO --conditions 106X_upgrade2018_realistic_v16_L1v1 --datatier NANOAODSIM --eventcontent NANOAODSIM --python_filename TOP-RunIISummer20UL18NanoAODv9_cfg.py --fileout file:NAOD-00000.root --filein file:MAOD-00000.root  --no_exec --mc
# )