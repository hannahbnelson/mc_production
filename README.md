# mc\_validation 

How to run the scripts: 

```
unset PYTHONPATH
micromamba activate topEFT-env

python3 run_nanogen_processor.py --outname outputName PathToJsonFile

python3 plotter.py
```

The default `outname` is `histos`, resulting in an output file of `histos.pkl.gz`. 
There is also a json file for the mini test sample called `sample_small_ttbar_LO_SMEFT.json`, which points to the sample of just 50 events. 

Inside `plotter.py`, modify the file path to point towards the correct `.pkl.gz`. 

`run_nanogen_processor.py` runs `nanogen_processor.py`. This produces HistEFT objects. 
`run_nonHistEFTprocessor.py` runs `nanogen_nonHistEFT.py`. This produces regular hist objects (not EFT aware histograms). Currently, this produces the plots of event weights at different EFT points and deltaR plots since these are regular histograms. 
