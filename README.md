# mcvalidation 

How to run the scripts: 

```
unset PYTHONPATH
conda activate cmseft2023

python3 run_nanogen_processor.py --outname outputName sample_ttbar_LO_SMEFT.json

python3 plotter.py histos.pkl.gz
```

The default `outname` is `histos`, resulting in an output file of `histos.pkl.gz`. 
There is also a json file for the mini test sample called `sample_small_ttbar_LO_SMEFT.json`, which points to the sample of just 50 events. 
In this case run the processor with `--outname histos_test`. 

