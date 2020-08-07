	First off, all of these scripts are important but more than this will be needed to run combine successfully. Follow this documentation to import all the combine tools: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/ . Combine must be ran in sl7 in order to function.

MAKING DATA CARDS
	
	This must be the first step done in Combine. Any of the tests described below can be done in any order but all of them rely on the existence of data cards. The main script we use to make data cards is dataCards.py. Essentially, what this script will do is grab input root files, analyze the channels for that region, and make data cards from them for each mass point. In dataCards.py, you will need to specify which signal to analyze over, which uncertainties should be added to the data cards, a specification of what the output directory should be called, and point the script to the correct root file you wish it to run over. The output directory will look something like /limits_*specified directory name*/*Branching ratio*/*channel names and cmb*/*mass points and common*/*.txt . All of the txt files are data cards. Within cmb/*mass points*/, you should notice a file called workspace.root . This file was made by grabbing each of the datacards in that area then merging them into one file. This file will be very important for running the various tests described below. 

	When it comes to actually running dataCards.py, I made a shell script called runDataCards.sh that will run dataCards.py for each branching ratio specifiec in the .sh file. Looping over the branching ratios in dataCards.py will result in  a crash. Once all the data cards have been made you will be ready then to run the various things described below.

SIGNAL INJECTION TEST

	The first step is to run a fit diagnostics test. To run this, simply use the following command in your terminal: combine -M FitDiagnostics -d workspace.root --saveWorkspace <maybe other commands>. Other commands I have used that prove to be useful is -n (allowing you to have some customization of the name of the output files) and --plots (Will make .png image files. All of these are also in the output fitDiagnostics.root). The output of this test will produce two root files: fitDiagnostics.root and higgsCombineTest.FitDiagnostics.mH120.root. If you want a correlation plot, you will be able to get them from adding --plots to the command. If you display the correlation.png or try to draw it from fitDiagnostics.root, you will notice that the plot is unreadable. Enter in the following commands after opening the root file to fix that problem.

TCanvas *c1 = new TCanvas("c1","c1",1200, 600)
gStyle->SetOptStat(0)
gPad->SetLeftMargin(0.25)
gPad->SetBottomMargin(0.15)
TH2D *second = (TH2D*)_file0->Get("covariance_fit_b")
second->GetYaxis()->SetRange(1,26)
second->GetXaxis()->SetRange(1,26)
second->GetYaxis()->SetRange(second->GetNbinsY()-26,second->GetNbinsY())
gStyle->SetPaintTextFormat("1.2f")
second->SetMarkerSize(1.0)
second->Draw("colz text")

	The next step is to run fitResults.py. The input of this file is the output from the first fitDiagnostics test described above. Place the correct root file there and simply python -u fitResults.py to run it. No need for a log file since as of right now there is no text output. Once this script has finished running, it will create the file initialFitWorkspace.root. 

	After this, you will want to use initial FitWorkspace.root to generate MC toys. This can be done with combine -M GenerateOnly -d initialFitWorkspace.root --snapshotName initialFit --toysFrequentist --bypassFrequentistFit -t <# of toys> --saveToys --expectSignal <r> -n <specified name>. This will create a root file like higgsCombine<name>.GenerateOnly.mH120.123456.root.

	Now it is time for to run fit diagnostics over each of the generated toys made previously. The command to do this is quite similar to before:  combine -M FitDiagnostics -d initialFitWorkspace.root --snapshotName initialFit --robustFit=1 --rMin -5 --rMax 5 --skipBOnlyFit -t <# of toys> -n <name> --toysFile higgsCombine<name>.GenerateOnly.mH120.123456.root

	Once this is finished, you are ready to make the signal injection plot. Copy over signalInjectionPlotter into whichever area you wish to make these plots. Specify which input root file to use (should be the output of this last fit diagnostics test), and run the plotting script. You will get two .png files from this. One of them will be for sigstrength and the other sigpull.



MAKING IMPACT PLOTS

	Navigate to the cmb area you wish to make an impact plot. The first step is to run the initial fit command: combineTool.py -M Impacts -d workspace.root -m <mass value> --doInitialFit --robustFit 1 

	After this, you will want to run a similar command. However, this one will run over each nuisance parameter and make a root file for each parameter. Run combineTool.py -M Impacts -d workspace.root -m <mass> --robustFit 1 --doFits 

	Put that output into a .json file: combineTool.py -M Impacts -d workspace.root -m <mass> -o impacts.json
	
	Making impact plot. Output will be a .pdf file. plotImpacts.py -i impacts.json -o impacts

	

GOODNESS OF FIT TEST

	Begin by running goodness of fit off of the data generating no toys: combine -M GoodnessOfFit workspace.root --algo=saturated
	
	Next, run goodness of fit and generate X number or toys: combine -M GoodnessOfFit workspace.root --algo=saturated -t <# of toys> --toysFrequentist --fixedSignalStrength=0 -s 123456. This will create an output root file.

	For the plotting, run GoFPlotter.py. The input file should be the output from the GoodnessOfFit command you ran that generated X number of toys. For the value of the hline, look at the output of the first command ran for running over data. The value given there is the value you should set the hline to. Run this script and it will create a GoF.png file. The name of the file can be specified in the script itself.


MAKING LIMIT PLOTS

	To get expected asymptotic limit values for individual masses, run combine -M AsymptoticLimits workspace.root --run=blind --cminDefaultMinimizerStrategy 0 within each mass directory you wish to get expected limits. If you want to make limit plots, you will not be able to use the results from this. Also note that removing --run=blind will unblind your analysis and give you observed results in addition to the expected.

	If you want to make limit plots, then you will need to go into your BR string directory. From there, run this command: combineTool.py -M Asymptotic -d cmb/*/workspace.root --there -n .limit --run=blind --parallel 4. This command will create root files in the mass directories that have .limit in the name. 

	Next you will want to take the output from the previous command and toss it into a .json file. combineTool.py -M CollectLimits cmb/*/*.limit.* --use-dirs -o limits.json

	The final step is to plot the limit. All you need to do is point the plotter to the json file that was just created, and run the plotter. 


HELPFUL DOCUMENTATION FOR REFERENCE

limits help: http://cms-analysis.github.io/CombineHarvester/limits.html

Fit diagnostics, impact plots, and channel masking: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#nuisance-parameter-impacts

Goodness of Fit: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#Goodness_of_fit_tests

