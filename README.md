#Instructions

- If the model has more than one dataset, you need to merge the outputs of susyParameterScanAnalyzer (see below), 
otherwise you can skip this step and just take the genEvts.root file in the output directory of susyParameterScanAnalyzer (from Heppy).

Get the merged ROOT input file:

```bash
./hadd.sh <input_dir> <model>
```

This will create a file in the current directory with the info on the generated events stored as histogram
Model: "T1tttt", "T2bb", etc.


- Fill the dictionary with the information of the masses generated per each dataset

```bash
./submitMassInfo.sh <input_dir> <out_dir_mass_info> <model> <sparticle>

<sparticle> = "Gluino", "Stop", etc. (first letter uppercase)
```


- Compile the ROOT macro:

```bash
gmake
```


- Change the configurables in the config_2016.py file (follow examples there).

sparticle: "Gluino", "Sbottom", etc.

baseInDir: input directory (output of CMGTools)

baseOutDir: output directory (output is large, store somewhere on /vols)

genEvtsFile: ROOT file generated in the first step (see above)

massInfoDir: the one generated in the step before

- In splitTrees.py modify the modelsDict to decide which model to run on.


- Run the splitting on the batch:

```bash
python splitTrees.py
```

You should see jobs running and, at the end, the trees and the skim report in the output directory (specified in splitTrees.py)



- Check the output

```bash
python checkOutputFiles.py -d <output_dir> --resubmit

<output_dir> is the directory where the split trees have been stored in the previous step
```
