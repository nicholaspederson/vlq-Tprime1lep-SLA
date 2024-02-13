# singleLepAnalyzer

Analyzer for making stack plots and/or limit-setting templates. This version can read files created by [vlq-BtoTW-RDF](http://github.com/jmhogan/vlq-BtoTW-RDF/)

## Installation

Based on the connection to vlq-BtoTW-RDF, the default assumption is that this repository will be cloned inside a `CMSSW_12_4_8` area. 
If the RDataFrame analyzer is eventally used, releases > `CMSSW_11` will be needed so that the ROOT version is high enough. But
`ROOT` and `python` are all that's used here, `CMSSW` is not explicitly required.

```
cmsrel CMSSW_12_4_8
cd CMSSW_12_4_8/src
git clone https://github.com/jmhogan/vlq-BtoTW-SLA/
cd vlq-BtoTW-SLA
```

*Note:* this CMSSW release is really annoying in that it doesn't support the ROOT package in python2. Either set up an alias 
so that calling `python` gives python3, or explicitly call `python3` for most scripts. 

## Scripts in the top folder:

The scripts in the top-level folder and generically useful and are often imported at the beginning of scripts in the subfolders.

* `weights.py`: this is historical and not currently used. It's a helpful reference for cross sections and should be kept around.
* `utils.py`: a file full of utility functions! File-reading, normalizing things, all that type of stuff lives here. 
* `samples.py`: almost a direct copy of the samples.py found in vlq-BtoTW-RDF, but not quite
   * cross sections and number of events are filled in (via the output of `dumpcounts.py`)
   * samples with "extensions" don't appear separately here -- in RDF we want them to be seem separately because they have separate DAS dataset names. But now for the analyzer we always want original samples + extensions to be accessed together as one dataset.
* `dumpcounts.py`: a script to find the effective number of events in a dataset. To use it:
   * Customize the ROOT file path
   * Customize the sample list to process
   * Customize the year (use search-replace, it appears twice)
   * Run the script with `python3`
   * the output is formatted so that it can be pasted into `samples.py` to set the `nrun` value for the datasets that you queried

The most important script in the top-level folder is `analyze.py`. This is the master script that creates histograms by applying cuts and weights to a branch in the input ROOT file. 
There are currently 2 versions: 

* `analyze.py`: this creates histograms using `TTree->Draw()`. 
   * After building up strings for the cuts and weights needed, histograms (for all uncertainties) are created and then filled. 
   * This script is functional but extremely slow -- many uncertainties are currently (Feb 2024) commented out for speed.
   * TO-DO: the PDF uncertainties are not implemented yet (Feb 2024).
* `analyze_RDF.py`: this creates histograms using `RDataFrame.Histo1D()`.
   * The first half of the script is identical to the other -- building up the cut and weight strings needed
   * The `TTree` is opened as an `RDataFrame` and `.Filter` and `.Define` are used to apply the cut and save the weights
   * The `makeTemplates/doHists.py` needs to be edited to call this method instead of the other
   * earlier tests shows BIG issues here with both speed (slower than TTree) and memory (crashing node), so changes are needed. Comments in the script give some brainstorming ideas.

## Making plots in `makeTemplates`

**Note: files in the repository that were last updated > 1 year ago can be safely ignored for now**

Scripts in this folder are used to **make ROOT files of nice histograms for Combine** and to **make plot images**.

### Common script features:

Most of the scripts include the following definitions. Yes, we could probably try to define these once somewhere else...

* `isEMlist`: string list like ['E','M'] for electron and muon, or 'L' for combined leptons
* `taglist`: string list of categories, like ['tjet','wjet',...]. Default is 'all' if the histograms weren't categorized
  * `isCategorized`: flag for whether or not to expect different tags in the histogram names
* `region`: string describing the cuts in a histogram, like 'all' or 'D' or 'B', etc

### Preparing to make histograms

1. Check samples.py --> if the input RDF files are new, do the sample counts need updating?

2. Check analyze.py (or the RDF version) --> do you want to change any cuts, weights, or uncertainty histograms?

3. Check doHists.py --> is the input file EOS path correct? Do you want to add any new plot definition? Do you need to change the settings for running uncertainties? Do you need to change the sample list to process?

4. Test doHists.py to see that it doesn't crash: `python3 -u doHists.py`   (you can kill this test once it gets through 1 or 2 MC samples)

5. Edit doCondorTemplates.py:
   * Define a "pfix" label for this set of plots
   * Define the region and turn of/off isCategorized
   * Comment/uncomment to get the right list of plots

### Running condor jobs for histograms

On the LPC:

```
voms-proxy-init -voms cms -valid 168:00

cd CMSSW_12_4_8/src/vlq-BtoTW-SLA/makeTemplates/
python -u doCondorTemplates.py
```

Check status with `condor_q` and similar commands. The output files, including condor log/err/out files will go to `makeTemplates/kinematicsREGION_YOURPFIX/LEPTON_all/`. If you chose to make categorized plots, the path will look like `makeTemplates/templatesREGION_YOURPFIX/LEPTON_TAG/`.

### Making ROOT files and tables

1. Edit doTemplates.py to set the region and prefix to match a set of plots. You can also control the samples and uncertainties that are processed (e.g. you can ignore some samples or uncertainties that were created in the condor job). This script converts pickle files to ROOT files and write a latex-formatted yield table.

2. Edit modifyBinning.py (**Note: not updated yet for BtoTW**) to control binning and add certain uncertainties. This script is important for uncertainties that are defined based on looking at the final bin contents of some histogram and doing operations on them -- notably PDF and Scale uncertainties. Edit runRebinning.sh to rebin multiple plots

3. python3 -u doTemplates.py

(4. sh runRebinning.sh) Later, when it's ready. Historically, the output of modifyBinning.py has been the set of ROOT files used for the Higgs Combine limit setting tool.

### Making plot images

1. Edit plotTemplates.py for all plot-level controls, including systematic uncertainties. Edit runPlotting.sh for multiple plots.
	
2. sh runPlotting.sh

## Setting limits in `combineLimits`

Write me!

## Plotting individual uncertainty effects in `plotShapeShifts`

Write me!

