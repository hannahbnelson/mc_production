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
