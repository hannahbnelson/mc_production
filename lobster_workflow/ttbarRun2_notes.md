# cmsRun Configs 
- Use `mc_production/lobster_workflow/make_cfgs/make_ttbarEFT_Run2_cfgs.sh` to make the UL Run2 configs. These cmsDriver commands were taken from mcm for the 1st iteration of the Run2 ttbar EFT samples. 
- The NanoAOD MCM command uses `--eventcontent NANOEDMAODSIM` but we need `eventcontent NANOAODSIM`. Not sure why the first is used in central generation, just that we want the second option. 

# DIGI Step 
- If the PU files are just `/store/mc/...`, then the default ND redirector is used. This was never able to find the files offsite - I think it's set to the cmsxroot redirector instead of the cmsxcache one. 
- To fix this, the file paths in the DIGI PU PREMIX list should include the global redirector. 
- Not all premix files are available on disk. Use the script `mc_production/lobster_workflow/make_cfgs/get_PU_files_on_disk.py` to save the current list of PU files on disk PLUS the redirector of your choice to a local file.

# HLT Step 
- For this to work, a lobster file had to be modified: 
The file `lobster/core/wrapper.sh` needs the following lines added: 
```
python -m ensurepip --user
python -m pip install --user future
```

These lines should be added before `$*` in this block: 
```
basedir=$PWD
cd $LOBSTER_CMSSW_VERSION
eval $(scramv1 runtime -sh) || exit_on_error $? 174 "The command 'cmsenv' failed!"
cd "$basedir"

log "top" "machine load" top -Mb\|head -n 50
log "env" "environment before execution" env
log "wrapper ready"
date +%s > t_wrapper_ready

log "dir" "working directory before execution" ls -l

$*
res=$?

log "dir" "working directory after execution" ls -l

log "wrapper done"
log "final return status = $res"

exit $res
```

# NANO Step 
At the very top of the Nano config are these lines: 
```
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.<> import <>
from Configuration.Eras.<> import <>

process = cms.Process('NANO', <>, <>)
``` 

AFTER `from Configuration.Eras` and before `process=cms.Process`, the following lines need to be added: 
```
import os
envOverride = {}
if 'HOME' not in os.environ:
    envOverride['HOME'] = os.environ.get('PWD', "/")
os.environ.update(envOverride)
```
If these are not included, you get the following error in the NanoAOD step: 
```
>> cmd: ----- Begin Fatal Exception 24-Sep-2024 14:02:26 EDT-----------------------
>> cmd: An exception of category 'FatalRootError' occurred while
>> cmd: [0] Constructing the EventProcessor
>> cmd: [1] Constructing module: class=BJetEnergyRegressionMVA label='bjetNN'
>> cmd: Additional Info:
>> cmd: [a] Fatal Root Error: @SUB=TSystem::ExpandFileName
>> cmd: input: $HOME/.root.mimes, output: $HOME/.root.mimes
>> cmd:
>> cmd: ----- End Fatal Exception -------------------------------------------------
```
