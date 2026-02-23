# To Submit Jobs to CRAB

To use an older version of CMSSW, everything must be run inside a container. Start a singularity container with this command: 
```
/cvmfs/cms.cern.ch/common/cmssw-cc7 --cleanenv -B /scratch365/ -B /opt/ -B /cvmfs/
```

Next, `cd` to the location of your `CMSSW_10_6_42` installation
Then, 
```
cd src
cmsenv
source /cvmfs/cms.cern.ch/crab3/crab.sh
```

Now, `cd` back to `mc_production/crab` and submit with this command: 
```
crab submit <crab submit script>.py
```

These crab submits assume that the cmsRun config is located in the same directory as the crab submission script itself. If this is not the case, update the crab submission script accordingly. 
