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
* `dumpMuPDFfactors.py`: a script to analyze signal with NO SELECTION APPLIED in order to find out the "raw" or "original" uncertainty from generator scale and factorization weights.
   * TO-DO: update this for NanoAOD inputs! 

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

The following content is old and in the process of being updated, but the general flow is accurate

-----------------------------------------------------------------------------------------------


makeTemplates: plot kinematic distributions and templates for limits 

	-- Categories: anything you define! see isEMlist, catList, tagList objects. Typically E/M/L for basic kinematics, more specific categories for limit templates.
	
	-- Regions: define "PS", "CR", "SR" cuts, or make new regions. Passed to analyze.py to control cuts

	-- One job per category, giving one distribution
	
	PREP:

	1. Edit weights.py and samples.py to define files/counts/xsecs

	2. Edit analyze.py to control TTree->Draw cuts/weights/hists. Teach it how to interpret your regions and categories.

	3. Edit doHists.py to control histogram names/bins/labels, samples to run, and files to read in

	4. Edit doCondorTemplates.py to control output directory, categories, and cuts. 

	RUN:

	1. python -u doHists.py --> this is a test, does it crash?

	2. python -u doCondorTemplates.py

	PLOT:

	1. Edit doTemplates.py to control samples and uncertainties. This script converts pickle files to ROOT files and write a latex-formatted yield table. You can choose to do a branching ratio scan here.

	2. Edit modifyBinning.py to control binning and add certain uncertainties. Edit runRebinning.sh to rebin multiple plots

	3. python -u doTemplates.py

	4. sh runRebinning.sh

	5. Edit plotTemplates.py for all plot-level controls, including systematic uncertainties. Edit runPlotting.sh for multiple plots.
	
	6. sh runPlotting.sh

-----------------------------------------------------------------------------------------------

Uncertainties: various special scripts to treat them

	-- makeTemplates/getCRUncerts.py: Given 3 yield files (templates, ttbar CR, wjets CR), this script returns flat uncertainties based on control regions corresponding to signal region categories.

	-- plotShapeShifts: creates plots of each individual shape uncertainty for cross checks

-----------------------------------------------------------------------------------------------

makeLimits: set limits

	Prep:

	1. Set up theta_config_template(_*).py of your choice with your uncertainties

	2. Set up doThetaLimits.py with directories and an types of histograms to remove from the file

	RUN:

	1. python -u doThetaLimits.py

	PLOT:

	1. python -u PlotLimits.py
	
