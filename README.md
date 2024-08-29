The general CMS Twiki page for Monte Carlo Production can be found here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO

# How to Generate Gridpacks
## Cards
First, you will need to produce a gridpack. General instructions can be found on the twiki here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO#Quick_tutorial_on_how_to_produce
To make a gridpack you need at minumum the following cards: 
- `_run_card.dat`   : This contains settings for MadGraph parameters. 
- `_proc_card.dat`  : This defines the process for MadGraph. 

For an EFT sample, you will also need the following: 
- `_customizecards.dat` : This is where you set constants (eg. LambdaSMEFT) and the starting point in WC for the coefficients you are using. All WCs not defined here are by defaul set to 0. 
- `_extramodels.dat`    : This contains the name of the tar.gz file for the model being used (eg. SMEFTsim_topU3l_MwScheme_UFO_2t.tar.gz)
- `_reweight_card.dat`  : This contains the reweight points for your WCs.

Examples of cards can be found in this repository in the `cards/` directory. 

**Note**: All of the names of the files the prepend `_<card type>.dat` have to be exactly the same, or they will not be correctly picked up during the gridpack generation. 
The output name in the last line of the `_proc_card.dat` also has to match this name, or the gridpack generation will fail. 

## Making a Gridpack
To produce a gridpack based on your cards, follow the instructions in the [Twiki](https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO#Quick_tutorial_on_how_to_produce). 
For producing RunII UL samples, run `git checkout mg265UL` after cloning the genproduction repo. 
Copy your cards to `genproductions/bin/MadGraph5_aMCatNLO/cards/`.

If you are using a model that is saved locally and not generally accessible, save the model directory inside `genproductions/bin/MadGraph5_aMCatNLO/`. 
Then, edit `gridpack_generation.sh` in the following way. In the script there is the following section: 
```
#############################################
#Copy, Unzip and Delete the MadGraph tarball#
#############################################
wget --no-check-certificate ${MGSOURCE}
tar xzf ${MG}
rm "$MG"
```

At the end of this section, after `rm "$MG"`, add the following line: 
```
cp -r <full path to your model dir> $MGBASEDIRORIG/models
```
For example, the full path to the model dir is probably `/afs/crc.nd.edu/user/U/USER/genproductions/bin/MadGraph5_aMCatNLO/MODEL_DIR`. 
This will allow your added model dir to be found when running `gridpack_productions.sh`. 

From here, follow the instructions in the twiki to make the gridpack. Note that you do NOT start a cmssw environment before running `generate_gridpack.sh`. 

## Checking that your gridpack is valid
It can be useful to quickly check that your gridpack can successfully produce events without having to run over a cmsRun config. 
Instructions on how to make a small number of events from just the gridpack to check it works can be found here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO#Standalone_production_running_th

# Setting up CMSSW environment to produce EFT NAOD samples 
The following steps are for producing NAOD v9 samples (with CMSSW_10_6_26). 
The majority of these steps are identical to the ones described in the TopEFT mgprod README.md as described [here](https://github.com/TopEFT/mgprod/edit/master/README.md).

To generate NAOD files that include the EFT weights, we cannot use a generic CMSSW release. We need to include the code that puts the weight information into the NAOD files, so execute the following commands to set up the appropriate CMSSW release and include the necessary packages.
```
cmsrel CMSSW_10_6_26
cd CMSSW_10_6_26/src/
export SCRAM_ARCH=slc7_amd64_gcc700
cmsenv

git cms-addpkg PhysicsTools/NanoAOD
cd PhysicsTools/NanoAOD/
git remote add eftfit https://github.com/GonzalezFJR/cmssw.git
git fetch eftfit
git cherry-pick c0901cfc459a8d5282ebb1bc74374903d29e3eee
git cherry-pick 4068e48b02b1fcb46949b3ebeac6a7b59062c2e0
git cherry-pick 76d0a24615c2b2b3aa7333c5aed5cc7bb6a7fd1d
```

The `NanoAOD/plugins/GenWeightsTableProducer.cc` script requires `WCFit` and `WCPoint`, so clone the `EFTGenReader` inside of `CMSSW_10_6_26/src/`:
```
cd CMSSW_10_6_26/src/ # Or whatever cd gets you into this directory
git clone https://github.com/TopEFT/EFTGenReader.git
```
Finally, we will also need the `NanoAODTools` (described [here](https://twiki.cern.ch/twiki/bin/viewauth/CMS/NanoAODTools#Quickly_make_plots_with_NanoAODT)) in order to get the script we need to merge non-EDM NAOD root files. Follow these steps to clone the repository inside of `PhysicsTools`:
```
cd CMSSW_10_6_26/src
cmsenv
git cms-init   #not really needed unless you later want to add some other cmssw stuff
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
```
In addition to these changes, a couple of files from NanoAODTools need to be changed. 
In a separate directory, clone the following repository: `git clone git@github.com:hannahbnelson/mc_production.git`. 

Then, replace the following files to your CMSSW_10_6_26 release with the modified files from `mc_production` using the correct path to CMSSW_10_6_26 for your setup. 
```
cp nanogen_setup/GenWeightsTableProducer.cc ~/CMSSW_10_6_26/src/PhysicsTools/NanoAOD/plugins/GenWeightsTableProducer.cc
cp nanogen_setup/nanogen_cff.py ~/CMSSW_10_6_26/src/PhysicsTools/NanoAOD/python/nanogen_cff.py
cp nanogen_setup/globals_cff.py ~/CMSSW_10_6_26/src/PhysicsTools/NanoAOD/python/globals_cff.py
```

- This version of `GenWeightsTableProducer.cc` includes changes needed to be able to read the EFT reweight points correctly, and adds the variables needed to make DJR plots from nanoGen samples. 
- This version of `nanogen_cff.py` fixes a bug in NanoGen where GenJets produced in MiniAOD do not include neutrinos, but GenJets produced in NanoGen include neutrions. This fixes the error and defines GenJets the same as they are defined for GenJets in miniAOD. Speficially now, `process.genJetTable.src = "ak4GenJetsNoNu"` 
- This version of `globals_cff.py`,the branch `mc_nMEPartonsFiltered` is added to NanoGen samples. This is useful for DJR plots.

Finally, run `scram b` in `CMSSW_10_6_26/src` to compile all of the changes.

