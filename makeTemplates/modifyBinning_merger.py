#!/usr/bin/python

import os,sys,time,math,fnmatch
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from array import array
from weights import *
from modSyst import *
from utils import *
from ROOT import *
start_time = time.time()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Run me as:
# > python modifyBinning.py
# 
# Optional arguments:
# -- statistical uncertainty threshold
#
# Notes:
# -- Finds certain root files in a given directory and rebins all histograms in each file
# -- A selection of subset of files in the input directory can be done below under "#Setup the selection ..."
# -- A custom binning choice can also be given by manually filling "xbinsList[chn]" for each channel
#    with the preferred choice of binning
# -- If no rebinning is wanted, but want to add PDF and R/F uncertainties, use a stat unc threshold 
#    that is larger than 100% (i.e, >1.)
# -- If CR and SR templates are in the same file and single bins are required for CR templates,
#    this can be done with "singleBinCR" bool (assumes that the CR templates contain "isCR" tags!).
# -- Use "removalKeys" to remove specific systematics from the output file.
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

iPlot='HTdnnL'
if len(sys.argv)>1: iPlot=str(sys.argv[1])

folder = 'templatesCR_Mar2021_TT'
if len(sys.argv)>2: folder=str(sys.argv[2])
inputfolder16 = '/uscms_data/d3/cholz/CMSSW_10_2_10/src/tptp_2016/makeTemplates/'+folder.replace('Mar2021_TT','Feb2021TT').replace('Mar2021_BB','Feb2021BB')
inputfolder17 = '/uscms_data/d3/escharni/CMSSW_10_2_10/src/singleLepAnalyzer/makeTemplates/'+folder
inputfolder18 = '/uscms_data/d3/escharni/CMSSW_10_2_10/src/tptp_2018/makeTemplates/'+folder

stat_saved = 0.2 #statistical uncertainty requirement (enter >1.0 for no rebinning; i.g., "1.1")
if len(sys.argv)>3: stat_saved=float(sys.argv[3])

FullMu = False
if len(sys.argv)>4: FullMu=bool(eval(sys.argv[4]))
if FullMu: addFlat = False
else: addFlat = True

rebinCombine = True #else rebins theta templates ## COME SET TO TRUE WHEN DOING SR OR CR isCatagorized
#print "rebin combine Before: ", rebinCombine
if len(sys.argv)>5: rebinCombine=bool(eval(sys.argv[5])) 

singletOnly = False
if len(sys.argv)>6: singletOnly = bool(eval(sys.argv[6]))

lumi16 = '35p92'
lumi17 = '41p53'
lumi18 = '59p74'
lumi = '137'

templateDir = os.getcwd()+'/'+folder+'/'
if not os.path.exists(templateDir): os.system('mkdir '+templateDir)
print "templateDir: ",templateDir
combinefile = 'Combine.root'
thetafile = 'templates_'+iPlot+'_137fb.root'

rebin4chi2 = False
if 'templatesCR' in folder: rebin4chi2 = True #include data in requirements

normalizeRENORM = True #only for signals
normalizePDF    = True #only for signals
if 'kinematics' in folder:
	normalizeRENORM = False #only for signals
	normalizePDF    = False #only for signals

sigName = 'TT' 
if 'BB' in folder:
	sigName = 'BB'
massList = range(900,1800+1,100)
if sigName == 'BB': massList.append(900)
sigProcList = [sigName+'M'+str(mass) for mass in massList]

bkgProcList = ['top','ewk','qcd'] #put the most dominant process first
era = "13TeV"

if rebinCombine:
	dataName = 'data_obs'
	upTag = 'Up'
	downTag = 'Down' ####Check this
else: #theta
	dataName = 'DATA'
	upTag = '__plus'
	downTag = '__minus'

print "rebin combine:", rebinCombine
print "FullMu: ", FullMu
addShapes = True
lumiSys = 0.018 #lumi uncertainty
eltrigSys = 0.0 #electron trigger uncertainty
mutrigSys = 0.0 #muon trigger uncertainty
elIdSys = 0.00 #electron id uncertainty
muIdSys = 0.02 #muon id uncertainty
elIsoSys = 0.015 #electron isolation uncertainty
muIsoSys = 0.015 #muon isolation uncertainty
elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

#Setup the selection of the files to be rebinned:          only those that aren't rebinned and are this plot
Wdecay = 'bW'
if sigName == 'BB': Wdecay = 'tW'
if rebinCombine: 
        rfiles = [file for file in findfiles(inputfolder17, '*.root') 
                  if 'rebinned' not in file 
                  and (Wdecay in file or 'kinematics' in folder) #### FIXME TO RUN FOR REAL!
                  and combinefile in file 
                  and '_'+iPlot+'_' in file.split('/')[-1]]
else: 
        rfiles = [file for file in findfiles(inputfolder17, '*.root') 
                  if 'rebinned' not in file 
                  and (Wdecay in file or 'kinematics' in folder) #### FIXME TO RUN FOR REAL!
                  and combinefile not in file 
                  and '_'+iPlot+'_' in file.split('/')[-1]]

# Put the file we want most in front
if rebinCombine and Wdecay+'0p5' not in rfiles[0]:
        index = [idx for idx, name in enumerate(rfiles) if Wdecay+'0p5' in name][0]
        firstfile = rfiles.pop(index)
        rfiles.insert(0,firstfile)

print "inputfolder16: ",inputfolder16
print "inputfolder17: ",inputfolder17
print "inputfolder18: ",inputfolder18
print "iPlot: ",iPlot

#Open the lowest mass signal for consistency
print 'List of ROOT files:',rfiles
for rfile in rfiles:
	if not rebinCombine and ('TTM1100' in rfile or 'BBM1100' in rfile): 
                tfile17 = TFile(rfile)
                tfile16 = TFile(rfile.replace(inputfolder17,inputfolder16).replace(lumi17,lumi16))
                tfile18 = TFile(rfile.replace(inputfolder17,inputfolder18).replace(lumi17,lumi18))
if rebinCombine: 
        tfile17 = TFile(rfiles[0])
        tfile16 = TFile(rfiles[0].replace(inputfolder17,inputfolder16).replace(lumi17,lumi16))
        tfile18 = TFile(rfiles[0].replace(inputfolder17,inputfolder18).replace(lumi17,lumi18))

print 'ROOT file16:',tfile16.GetName()
print 'ROOT file17:',tfile17.GetName()
print 'ROOT file18:',tfile18.GetName()

## Datahists should be safe...there should be one for all channels for all years
datahists = [k.GetName() for k in tfile17.GetListOfKeys() if '__'+dataName in k.GetName()]
channels = [hist[hist.find('fb_')+3:hist.find('__')] for hist in datahists if 'isL_' not in hist and '01W' not in hist and '2pW' not in hist and 'notVbH' not in hist and 'notVbZ' not in hist]

## Allhists is trickier -- some uncertainties are only in some years and some background processes are only in some years
allhists17 = {chn:[hist.GetName() for hist in tfile17.GetListOfKeys() if chn in hist.GetName()] for chn in channels}
allhists16 = {chn:[(hist.GetName()).replace(lumi16,lumi17) for hist in tfile16.GetListOfKeys() if chn in hist.GetName()] for chn in channels}
allhists18 = {chn:[(hist.GetName()).replace(lumi18,lumi17) for hist in tfile18.GetListOfKeys() if chn in hist.GetName()] for chn in channels}
allhists = {}
for channel in allhists17:
        set17 = set(allhists17[channel])
        set16 = set(allhists16[channel])
        set18 = set(allhists18[channel])
        list16not17 = list(set16 - set17)
        set16not17 = set(list16not17)
        list18not1617 = list(set18 - set17 - set16not17)
        list161718 = allhists17[channel] + list16not17 + list18not1617
        allhists[channel] = list161718

DataHists = {}
for hist in datahists:
	channel = hist[hist.find('fb_')+3:hist.find('__')]
	DataHists[channel] = tfile17.Get(hist).Clone()
        DataHists[channel].Add(tfile16.Get(hist.replace(lumi17,lumi16)))
        DataHists[channel].Add(tfile18.Get(hist.replace(lumi17,lumi18)))        
        if 'templatesCR' in folder and 'dnnLargeJ' in channel:
                DataHists[channel].Rebin(5)
        

## Background hists will at least check everything. Then we see if any are missing and flag them
## These missing hists flags would then apply to all the uncerts for that process...
totBkgHists = {}
badhistlist = {}
for hist in datahists:
	channel = hist[hist.find('fb_')+3:hist.find('__')]
	totBkgHists[channel]=tfile17.Get(hist.replace('__'+dataName,'__'+bkgProcList[0])).Clone()
	totBkgHists[channel].Add(tfile16.Get(hist.replace(lumi17,lumi16).replace('__'+dataName,'__'+bkgProcList[0])).Clone())
	totBkgHists[channel].Add(tfile18.Get(hist.replace(lumi17,lumi18).replace('__'+dataName,'__'+bkgProcList[0])).Clone())
	for proc in bkgProcList:
		if proc == bkgProcList[0]: continue
		try: 
                        totBkgHists[channel].Add(tfile17.Get(hist.replace('__'+dataName,'__'+proc)))
                except:
                        badhistlist.setdefault(proc+'17',[]).append(hist.replace('__'+dataName,'__'+proc))
                        pass
                try:
                        totBkgHists[channel].Add(tfile16.Get(hist.replace(lumi17,lumi16).replace('__'+dataName,'__'+proc)))
                except:
                        badhistlist.setdefault(proc+'16',[]).append(hist.replace('__'+dataName,'__'+proc))
                        pass
                try:
                        totBkgHists[channel].Add(tfile18.Get(hist.replace(lumi17,lumi18).replace('__'+dataName,'__'+proc)))
		except: 		
                        badhistlist.setdefault(proc+'18',[]).append(hist.replace('__'+dataName,'__'+proc))
                        pass
        if 'templatesCR' in folder and 'dnnLargeJ' in channel:
                totBkgHists[channel].Rebin(5)
        

print 'Processes with missing histograms:',badhistlist.keys()
#for key in badhistlist.keys():
#        print '\t Bad hists for',key,':',badhistlist[key]

## Not currently using this -- it's for rebinning on signal stats.
##SigHists = {}
# for hist in datahists:
# 	channel = hist[hist.find('fb_')+3:hist.find('__')]
# 	if not rebinCombine: SigHists[channel]=tfile.Get(hist.replace('__'+dataName,'__sig')).Clone()
# 	else: 
# 		for proc in sigProcList:
# 			SigHists[channel+proc]=tfile.Get(hist.replace('__'+dataName,'__'+proc)).Clone()
	#SigHists[channel].Rebin(20)

xbinsListTemp = {}
for chn in totBkgHists.keys():
	#if 'notV' in chn and (iPlot == 'Tp2MDnn' or iPlot == 'DnnTprime'): stat = 1.1
	stat = stat_saved

	#print 'Channel',chn,'integral is',totBkgHists[chn].Integral()
	if 'isE' not in chn: continue
	print 'Processing',chn

        xbinsListTemp[chn] = [DataHists[chn].GetXaxis().GetBinUpEdge(DataHists[chn].GetXaxis().GetNbins())]
        Nbins = DataHists[chn].GetNbinsX()

        ## Why are we doing all this re-getting of histograms? Why not just ask for DataHists[chn]? See above.
        # Nbins = 0
	# if 'templates' in folder:
	# 	if 'notV' in chn: ## will be SR, need to skip past the taggedXXXX in case they differ
	# 		xbinsListTemp[chn]=[tfile17.Get(datahists[4]).GetXaxis().GetBinUpEdge(tfile17.Get(datahists[4]).GetXaxis().GetNbins())]
	# 		Nbins = tfile17.Get(datahists[4]).GetNbinsX()
	# 	elif iPlot == 'HTNtag' and 'LargeJ' in chn: ## will be CR, need to skip first 5 that are jet counts
	# 		xbinsListTemp[chn]=[tfile17.Get(datahists[5]).GetXaxis().GetBinUpEdge(tfile17.Get(datahists[5]).GetXaxis().GetNbins())]
	# 		Nbins = tfile17.Get(datahists[5]).GetNbinsX()
	# 	elif iPlot == 'HTdnnL' and 'LargeJ' in chn: ## will be CR, need to skip first 1 that has jet tag
	# 		xbinsListTemp[chn]=[tfile17.Get(datahists[1]).GetXaxis().GetBinUpEdge(tfile17.Get(datahists[1]).GetXaxis().GetNbins())]
	# 		Nbins = tfile17.Get(datahists[1]).GetNbinsX()
	# 	else: ## use the first datahist
	# 		xbinsListTemp[chn]=[tfile17.Get(datahists[0]).GetXaxis().GetBinUpEdge(tfile17.Get(datahists[0]).GetXaxis().GetNbins())]
	# 		Nbins = tfile17.Get(datahists[0]).GetNbinsX()
	# else:
	# 	xbinsListTemp[chn]=[tfile17.Get(datahists[0]).GetXaxis().GetBinUpEdge(tfile17.Get(datahists[0]).GetXaxis().GetNbins())]
	# 	Nbins = tfile17.Get(datahists[0]).GetNbinsX()

	
	totTempBinContent_E = 0.
	totTempBinContent_M = 0.
	totTempBinErrSquared_E = 0.
	totTempBinErrSquared_M = 0.
	totTempDataContent_E = 0.
	totTempDataContent_M = 0.
	totTempDataErrSquared_E = 0.
	totTempDataErrSquared_M = 0.
	totTempSigContent_E = 0;
	totTempSigContent_M = 0;
	for iBin in range(1,Nbins+1):
		totTempBinContent_E += totBkgHists[chn].GetBinContent(Nbins+1-iBin)
		totTempBinContent_M += totBkgHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
		totTempBinErrSquared_E += totBkgHists[chn].GetBinError(Nbins+1-iBin)**2
		totTempBinErrSquared_M += totBkgHists[chn.replace('isE','isM')].GetBinError(Nbins+1-iBin)**2
		try:
			totTempSigContent_E += SigHists[chn].GetBinContent(Nbins+1-iBin)
			totTempSigContent_M += SigHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
		except: pass
		totTempDataContent_E += DataHists[chn].GetBinContent(Nbins+1-iBin)
		totTempDataContent_M += DataHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
		totTempDataErrSquared_E += totBkgHists[chn].GetBinError(Nbins+1-iBin)**2
		totTempDataErrSquared_M += totBkgHists[chn.replace('isE','isM')].GetBinError(Nbins+1-iBin)**2
		
		#print 'totTempBinContent =',totTempBinContent_E,' ',totTempBinContent_M,', totTempBinErrSquared =',totTempBinErrSquared_E,' ',totTempBinErrSquared_M
		#print 'totTempSigContent =',totTempSigContent_E,' ',totTempSigContent_M

		if totTempBinContent_E>0. and totTempBinContent_M>0.:
			#if 'CR' in templateDir or 'ttbar' in templateDir or 'wjets' in templateDir or 'higgs' in templateDir or (totTempSigContent_E>0. and totTempSigContent_M>0):
			if rebin4chi2 and (totTempDataContent_E == 0 or totTempDataContent_M == 0): continue
			if math.sqrt(totTempBinErrSquared_E)/totTempBinContent_E<=stat and math.sqrt(totTempBinErrSquared_M)/totTempBinContent_M<=stat:
				if not rebin4chi2 or (math.sqrt(totTempDataErrSquared_E)/totTempDataContent_E<=stat and math.sqrt(totTempDataErrSquared_M)/totTempDataContent_M<=stat):
					totTempBinContent_E = 0.
					totTempBinContent_M = 0.
					totTempBinErrSquared_E = 0.
					totTempBinErrSquared_M = 0.
					totTempDataContent_E = 0.
					totTempDataContent_M = 0.
					totTempDataErrSquared_E = 0.
					totTempDataErrSquared_M = 0.
					totTempSigContent_E = 0.
					totTempSigContent_M = 0.
					#print 'Appending bin edge',totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin)
					xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))

	## Going right to left -- if the last entry isn't 0 add it
	if iPlot != 'DnnTprime' and iPlot != 'DnnBprime' and 'SR' in folder and xbinsListTemp[chn][-1]!=0: xbinsListTemp[chn].append(0)
	if 'Large' in chn and 'LargeJ' not in chn and 'templatesCR' in folder and iPlot == 'HTNtag' and xbinsListTemp[chn][-1]!=1: xbinsListTemp[chn].append(1)


	if (iPlot == 'DnnTprime' or iPlot == 'DnnBprime') and 'templatesSR' in folder:
		if xbinsListTemp[chn][-1]>0: xbinsListTemp[chn].append(0)
		elif xbinsListTemp[chn][-1]!=0: xbinsListTemp[chn][-1] = 0
	elif (iPlot == 'DnnTprime' or iPlot == 'DnnBprime') and 'CR' in folder and 'SCR' not in folder and xbinsListTemp[chn][0]!=1: xbinsListTemp[chn][0] = 1 
	
	## If the 1st bin is empty or too small, make the left side wider
	if totBkgHists[chn].GetBinContent(1)==0. or totBkgHists[chn.replace('isE','isM')].GetBinContent(1)==0.: 
		if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
	elif totBkgHists[chn].GetBinError(1)/totBkgHists[chn].GetBinContent(1)>stat or totBkgHists[chn.replace('isE','isM')].GetBinError(1)/totBkgHists[chn.replace('isE','isM')].GetBinContent(1)>stat: 
		if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]

	## Set mu and el bins equal
	xbinsListTemp[chn.replace('isE','isM')]=xbinsListTemp[chn]

	## Ignore all this if stat is > 1
	if stat>1.0:
		if 'notV' in chn or 'kinematics' in folder: xbinsListTemp[chn] = [tfile17.Get(datahists[0]).GetXaxis().GetBinUpEdge(tfile17.Get(datahists[0]).GetXaxis().GetNbins())]
		else: xbinsListTemp[chn] = [tfile17.Get(datahists[4]).GetXaxis().GetBinUpEdge(tfile17.Get(datahists[4]).GetXaxis().GetNbins())]
		for iBin in range(1,Nbins+1): 
			xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
		xbinsListTemp[chn.replace('isE','isM')] = xbinsListTemp[chn]

print "==> Here is the binning I found with",stat_saved*100,"% uncertainty threshold: "
print "//"*40
xbinsList = {}
for chn in xbinsListTemp.keys():
	xbinsList[chn] = []
	for bin in range(len(xbinsListTemp[chn])): xbinsList[chn].append(xbinsListTemp[chn][len(xbinsListTemp[chn])-1-bin])
	print chn,"=",xbinsList[chn]
print "//"*40



xbins = {}
for key in xbinsList.keys(): xbins[key] = array('d', xbinsList[key])

tfile16.Close()
tfile17.Close()
tfile18.Close()

#os._exit(1)

### Updated for 2018, JH August 2019. symmetric Hessian PDF version August 2020
muSFsUp = {'TTM900':[0.750,0.745,0.744],
           'TTM1000':[0.749,0.744,0.743],
           'TTM1100':[0.749,0.747,0.737],
           'TTM1200':[0.748,0.742,0.740],
           'TTM1300':[0.747,0.741,0.741],
           'TTM1400':[0.746,0.738,0.737],
           'TTM1500':[0.745,0.740,0.737],
           'TTM1600':[0.744,0.735,0.734],
           'TTM1700':[0.743,0.721,0.735],
           'TTM1800':[0.741,0.746,0.740],
           'BBM900':[0.750,0.744,0.744],
           'BBM1000':[0.749,0.742,0.742],
           'BBM1100':[0.749,0.743,0.742],
           'BBM1200':[0.748,0.742,0.741],
           'BBM1300':[0.747,0.741,0.741],
           'BBM1400':[0.746,0.739,0.739],
           'BBM1500':[0.745,0.735,0.735],
           'BBM1600':[0.744,0.735,0.735],
           'BBM1700':[0.743,0.733,0.720],
           'BBM1800':[0.741,0.731,0.855]
}
muSFsDn = {'TTM900':[1.303,1.311,1.312],
           'TTM1000':[1.304,1.312,1.314],
           'TTM1100':[1.305,1.306,1.323],
           'TTM1200':[1.307,1.315,1.318],
           'TTM1300':[1.309,1.316,1.318],
           'TTM1400':[1.311,1.322,1.324],
           'TTM1500':[1.313,1.319,1.324],
           'TTM1600':[1.315,1.329,1.328],
           'TTM1700':[1.317,1.354,1.330],
           'TTM1800':[1.319,1.311,1.321],
           'BBM900':[1.303,1.312,1.312],
           'BBM1000':[1.304,1.315,1.315],
           'BBM1100':[1.305,1.314,1.316],
           'BBM1200':[1.307,1.316,1.318],
           'BBM1300':[1.309,1.318,1.317],
           'BBM1400':[1.310,1.321,1.321],
           'BBM1500':[1.313,1.329,1.328],
           'BBM1600':[1.315,1.329,1.329],
           'BBM1700':[1.317,1.331,1.356],
           'BBM1800':[1.319,1.337,1.272]
}
pdfSFsUp = {'TTM900':[0.902,0.957],
            'TTM1000':[0.890,0.954],
            'TTM1100':[0.889,0.951],
            'TTM1200':[0.895,0.947],
            'TTM1300':[0.895,0.942],
            'TTM1400':[0.888,0.936],
            'TTM1500':[0.897,0.929],
            'TTM1600':[0.905,0.921],
            'TTM1700':[0.885,0.911],
            'TTM1800':[0.872,0.898],
            'BBM900':[0.903,0.957],
            'BBM1000':[0.889,0.954],
            'BBM1100':[0.889,0.951],
            'BBM1200':[0.895,0.947],
            'BBM1300':[0.895,0.942],
            'BBM1400':[0.889,0.936],
            'BBM1500':[0.897,0.929],
            'BBM1600':[0.904,0.921],
            'BBM1700':[0.884,0.911],
            'BBM1800':[0.872,0.897]
}
pdfSFsDn = {'TTM900': [1.104,1.047],
            'TTM1000':[1.099,1.050],
            'TTM1100':[1.099,1.054],
            'TTM1200':[1.093,1.060],
            'TTM1300':[1.098,1.066],
            'TTM1400':[1.102,1.073],
            'TTM1500':[1.099,1.082],
            'TTM1600':[1.122,1.094],
            'TTM1700':[1.121,1.109],
            'TTM1800':[1.133,1.128],
            'BBM900':[1.104,1.047],
            'BBM1000':[1.100,1.050],
            'BBM1100':[1.099,1.055],
            'BBM1200':[1.093,1.059],
            'BBM1300':[1.097,1.066],
            'BBM1400':[1.102,1.073],
            'BBM1500':[1.099,1.082],
            'BBM1600':[1.121,1.094],
            'BBM1700':[1.122,1.108],
            'BBM1800':[1.132,1.130]
}
        
iRfile=0
yieldsAll = {}
yieldsErrsAll = {}
yieldsSystErrsAll = {}
stat = stat_saved
binValue=0

correlated = ['__btag','__ltag','__pileup','__prefire','__Teff','__Heff','__Zeff','__Weff','__Beff','__toppt','__jsf','__dnnJ']
if 'kinematics' in folder: correlated.append('__muRFcorrd')
uncorrelated = ['__trigeffEl','__trigeffMu','__elIdSF','__Tmis','__Hmis','__Zmis','__Wmis','__Bmis','__jec','__jer']
special = ['__muR','__muF','__muRFcorrd','__pdf']
drop = ['__Jeff','__Jmis']

shortyears = ['16','17','18']

for rfile in rfiles: 
        if singletOnly and 'W0p5' not in rfile: continue
	print "REBINNING FILES:"
        print '\t',rfile
        print '\t',rfile.replace(lumi17,lumi16).replace(inputfolder17,inputfolder16)
        print '\t',rfile.replace(lumi17,lumi18).replace(inputfolder17,inputfolder18)
	#tfiles16 = {}
	#tfiles17 = {}
	#tfiles18 = {}
	#outputRfiles = {}
	#tfiles17[iRfile] = TFile(rfile)	
	#tfiles16[iRfile] = TFile(rfile.replace(lumi17,lumi16).replace(inputfolder17,inputfolder16))	
	#tfiles18[iRfile] = TFile(rfile.replace(lumi17,lumi18).replace(inputfolder17,inputfolder18))	
	tfiles17iRfile = TFile(rfile)	
	tfiles16iRfile = TFile(rfile.replace(lumi17,lumi16).replace(inputfolder17,inputfolder16))	
	tfiles18iRfile = TFile(rfile.replace(lumi17,lumi18).replace(inputfolder17,inputfolder18))	
	if not rebin4chi2: 
		if not FullMu: outputRfilesiRfile = TFile(rfile.replace(lumi17,lumi).replace(inputfolder17,templateDir).replace('.root','_BKGNORM_rebinned_stat'+str(stat).replace('.','p')+'.root'),'RECREATE')
                else: outputRfilesiRfile = TFile(rfile.replace(lumi17,lumi).replace(inputfolder17,templateDir).replace('.root','_rebinned_stat'+str(stat).replace('.','p')+'.root'),'RECREATE')
        else: 
                if not FullMu: outputRfilesiRfile = TFile(rfile.replace(lumi17,lumi).replace(inputfolder17,templateDir).replace('.root','_chi2rb5_BKGNORM_rebinned_stat'+str(stat).replace('.','p')+'.root'),'RECREATE')
		else: outputRfilesiRfile = TFile(rfile.replace(lumi17,lumi).replace(inputfolder17,templateDir).replace('.root','_chi2rb5_rebinned_stat'+str(stat).replace('.','p')+'.root'),'RECREATE')

        signame = rfile.split('/')[-1].split('_')[2]

	if not rebinCombine:
		print 'FOUND SIGNAME = ',signame
		if 'TTM' not in signame and 'BBM' not in signame: print 'DIDNT STORE SIGNAME: ',signame	
                
        print "PROGRESS:"
	for chn in channels:
		print "         ",chn
		rebinnedHists = {}
		#Rebinning histograms
		for hist in allhists[chn]:
                        
                        if any(item in hist for item in drop): continue
                        
                        # pull out the Discrim_stuff_stuff__proc part of the name
                        proc = hist.split('__')[1]
                        basename = hist.split('__')[0]+'__'+proc
                        do = {}
                        if proc+'16' in badhistlist.keys(): do['16'] = bool(basename not in badhistlist[proc+'16'])
                        else: do['16'] = True
                        if proc+'17' in badhistlist.keys(): do['17'] = bool(basename not in badhistlist[proc+'17'])
                        else: do['17'] = True
                        if proc+'18' in badhistlist.keys(): do['18'] = bool(basename not in badhistlist[proc+'18'])                        
                        else: do['18'] = True
                        
                        if rebinCombine and '__'+sigName in hist: 
                                signame = hist.split('__')[1]
                                if sigName not in signame: print "DIDNT GET SIGNAME",signame
                                
                        if 'W0p5' in rfile or 'kinematics' in folder:
				yieldHistName = hist
				if not rebinCombine: 
                                        yieldHistName = hist.replace('_sig','_'+rfile.split('_')[-5]) ### ASSUMING BR IS IN FILE NAME
					if 'kinematics' in folder: yieldHistName = hist.replace('_sig','_'+rfile.split('_')[-2])
                                        
                        if any(item in hist for item in uncorrelated):
                                ## uncorrelated nuisances: add each year to nominal from other years. Try to RENAME HERE with .Rebin
                                for syst in uncorrelated:
                                        if syst not in hist: continue
                                                
                                        if do['16']:
                                                rebinnedHists[hist+'16'] = tfiles16iRfile.Get(hist.replace(lumi17,lumi16)).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi).replace(syst,syst+'2016').replace('trigeffEl','elTrig').replace('trigeffMu','muTrig'),xbins[chn])
                                                if do['17']: rebinnedHists[hist+'16'].Add(tfiles17iRfile.Get(hist.replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                if do['18']: rebinnedHists[hist+'16'].Add(tfiles18iRfile.Get(hist.replace(lumi17,lumi18).replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))

                                        if do['17']:
                                                rebinnedHists[hist+'17'] = tfiles17iRfile.Get(hist).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi).replace(syst,syst+'2017').replace('trigeffEl','elTrig').replace('trigeffMu','muTrig'),xbins[chn])
                                                if do['16']: rebinnedHists[hist+'17'].Add(tfiles16iRfile.Get(hist.replace(lumi17,lumi16).replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                if do['18']: rebinnedHists[hist+'17'].Add(tfiles18iRfile.Get(hist.replace(lumi17,lumi18).replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                
                                        if do['18']: 
                                                rebinnedHists[hist+'18'] = tfiles18iRfile.Get(hist.replace(lumi17,lumi18)).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi).replace(syst,syst+'2018').replace('trigeffEl','elTrig').replace('trigeffMu','muTrig'),xbins[chn])
                                                if do['16']: rebinnedHists[hist+'18'].Add(tfiles16iRfile.Get(hist.replace(lumi17,lumi16).replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi16).replace(syst+upTag,'').replace(syst+downTag,'')+'dummy',xbins[chn]))
                                                if do['17']: rebinnedHists[hist+'18'].Add(tfiles17iRfile.Get(hist.replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                
                                        for year in shortyears: 
                                                if not do[year]: continue
                                                rebinnedHists[hist+year].SetDirectory(0)

                                                # scale Combine signals down to expected xsec for injection tests
                                                if rebinCombine and '__'+sigName in hist: rebinnedHists[hist+year].Scale(100.0/1000) ## try 100fb instead...

                                                if 'W0p5' in rfile or 'kinematics' in folder:
                                                        yieldsAll[yieldHistName.replace(upTag,year+upTag).replace(downTag,year+downTag)] = rebinnedHists[hist+year].Integral()

                                                if rebinCombine and '__'+sigName in hist:
                                                        for iBin in range(1,rebinnedHists[hist+year].GetNbinsX()+1):   
                                                                if rebinnedHists[hist+year].GetBinContent(iBin) == 0:
                                                                        rebinnedHists[hist+year].SetBinContent(iBin,1e-6)
                                                                        rebinnedHists[hist+year].SetBinError(iBin,math.sqrt(1e-6))

                                                rebinnedHists[hist+year].Write()


                        else:  # NOT an uncorrelated histogram
                                if any(item in hist for item in correlated):
                                        ## correlated nuisances: add each year to the others
                                        for syst in correlated:
                                                if syst not in hist: continue

                                                if do['17']:
                                                        rebinnedHists[hist] = tfiles17iRfile.Get(hist).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi),xbins[chn])
                                                        if do['16']: 
                                                                if 'dnnJ' in hist: rebinnedHists[hist].Add(tfiles16iRfile.Get(hist.replace(lumi17,lumi16).replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                                else: rebinnedHists[hist].Add(tfiles16iRfile.Get(hist.replace(lumi17,lumi16)).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                        if do['18']:
                                                                if 'prefire' in hist: rebinnedHists[hist].Add(tfiles18iRfile.Get(hist.replace(lumi17,lumi18).replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                                else: rebinnedHists[hist].Add(tfiles18iRfile.Get(hist.replace(lumi17,lumi18)).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                elif do['16']:
                                                        if 'dnnJ' in hist: rebinnedHists[hist] = tfiles16iRfile.Get(hist.replace(lumi17,lumi16).replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi),xbins[chn])
                                                        else: rebinnedHists[hist] = tfiles16iRfile.Get(hist.replace(lumi17,lumi16)).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi),xbins[chn])

                                                        if do['18']:
                                                                if 'prefire' in hist: rebinnedHists[hist].Add(tfiles18iRfile.Get(hist.replace(lumi17,lumi18).replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                                else: rebinnedHists[hist].Add(tfiles18iRfile.Get(hist.replace(lumi17,lumi18)).Rebin(len(xbins[chn])-1,'dummy',xbins[chn]))
                                                elif do['18']:
                                                        if 'prefire' in hist: rebinnedHists[hist] = tfiles18iRfile.Get(hist.replace(lumi17,lumi18).replace(syst+upTag,'').replace(syst+downTag,'')).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi),xbins[chn])
                                                        else: rebinnedHists[hist] = tfiles18iRfile.Get(hist.replace(lumi17,lumi18)).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi),xbins[chn])


                                elif any(item in hist for item in special) and 'kinematics' not in folder:
                                        ## special: we will deal with these later, for now just rebin and put into rebinnedHists
                                        try:
                                                if do['16']: rebinnedHists[hist+'16'] = tfiles16iRfile.Get(hist.replace(lumi17,lumi16)).Rebin(len(xbins[chn])-1,hist+'16',xbins[chn])
                                                if do['17']: rebinnedHists[hist+'17'] = tfiles17iRfile.Get(hist).Rebin(len(xbins[chn])-1,hist+'17',xbins[chn])
                                                if do['18']: rebinnedHists[hist+'18'] = tfiles18iRfile.Get(hist.replace(lumi17,lumi18)).Rebin(len(xbins[chn])-1,hist+'18',xbins[chn])
                                        except:
                                                if 'pdf' not in hist: print '\t Specials: unexpected missing 2017 or 2018:',hist
                                                pass
                                        if 'muR'+upTag in hist:
                                                ## for the muRF we need a nominal histogram saved...
                                                if do['17']: rebinnedHists[hist[:hist.find('__mu')]+'N17'] = tfiles17iRfile.Get(hist[:hist.find('__mu')]).Rebin(len(xbins[chn])-1,hist[:hist.find('__mu')]+'N17',xbins[chn])
                                                if do['16']: rebinnedHists[hist[:hist.find('__mu')]+'N16'] = tfiles16iRfile.Get((hist[:hist.find('__mu')]).replace(lumi17,lumi16)).Rebin(len(xbins[chn])-1,hist[:hist.find('__mu')]+'N16',xbins[chn])
                                                if do['18']: rebinnedHists[hist[:hist.find('__mu')]+'N18'] = tfiles18iRfile.Get((hist[:hist.find('__mu')]).replace(lumi17,lumi18)).Rebin(len(xbins[chn])-1,hist[:hist.find('__mu')]+'N18',xbins[chn])

                                        for year in shortyears:                                                 
                                                if not do[year]: continue
                                                try:
                                                        rebinnedHists[hist+year].SetDirectory(0)
                                                        # scale Combine signals down to expected xsec for injection tests
                                                        if rebinCombine and '__'+sigName in hist: rebinnedHists[hist+year].Scale(100.0/1000) ## try 100fb instead...
                                                except:
                                                        if 'pdf' not in hist: print '\t Specials: unexpected missing 2017 or 2018:',hist
                                                        pass
                                                if 'muR'+upTag in hist:
                                                        rebinnedHists[hist[:hist.find('__mu')]+'N'+year].SetDirectory(0)
                                                        if rebinCombine and '__'+sigName in hist: rebinnedHists[hist[:hist.find('__mu')]+'N'+year].Scale(100.0/1000) ## try 100fb instead...
                                else:
                                        ## else: not a nuisance, add each year to the others
                                        if do['17']: 
                                                rebinnedHists[hist] = tfiles17iRfile.Get(hist).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi),xbins[chn])
                                                if do['16']: rebinnedHists[hist].Add(tfiles16iRfile.Get(hist.replace(lumi17,lumi16)).Rebin(len(xbins[chn])-1,"dummy",xbins[chn]))
                                                if do['18']: rebinnedHists[hist].Add(tfiles18iRfile.Get(hist.replace(lumi17,lumi18)).Rebin(len(xbins[chn])-1,"dummy",xbins[chn]))
                                        elif do['16']:
                                                rebinnedHists[hist] = tfiles16iRfile.Get(hist.replace(lumi17,lumi16)).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi),xbins[chn])
                                                if do['18']: rebinnedHists[hist].Add(tfiles18iRfile.Get(hist.replace(lumi17,lumi18)).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi),xbins[chn]))
                                        elif do['18']: rebinnedHists[hist] = tfiles18iRfile.Get(hist.replace(lumi17,lumi18)).Rebin(len(xbins[chn])-1,hist.replace(lumi17,lumi),xbins[chn])
                                                
                                        
                                ## Done with these guys -- they are SD(0) and .Scale'd above
                                if any(item in hist for item in special): continue

                                if hist not in rebinnedHists.keys():
                                        print 'No histogram to write for',hist,'in',chn
                                        continue
                                        
                                rebinnedHists[hist].SetDirectory(0)                                

                                # scale Combine signals down to expected xsec for injection tests
                                if rebinCombine and '__'+sigName in hist: rebinnedHists[hist].Scale(100.0/1000) ## try 100fb instead...
                                
                                if 'W0p5' in rfile or 'kinematics' in folder:
                                        yieldsAll[yieldHistName] = rebinnedHists[hist].Integral()
                                        yieldsErrsAll[yieldHistName] = 0.
                                        for ibin in range(1,rebinnedHists[hist].GetXaxis().GetNbins()+1):
                                                yieldsErrsAll[yieldHistName] += rebinnedHists[hist].GetBinError(ibin)**2
                                        yieldsErrsAll[yieldHistName] = math.sqrt(yieldsErrsAll[yieldHistName])

                                if rebinCombine and '__'+sigName in hist:
                                        for iBin in range(1,rebinnedHists[hist].GetNbinsX()+1):   
                                                if rebinnedHists[hist].GetBinContent(iBin) == 0:
                                                        rebinnedHists[hist].SetBinContent(iBin,1e-6)
                                                        rebinnedHists[hist].SetBinError(iBin,math.sqrt(1e-6))

                                rebinnedHists[hist].Write()
		
                ## DONE looping over all hists here... 
                ## Uncorrelated uncerts have been added/renamed/unzeroed/written
                ## Correlated uncerts have been added/unzeroed/written
                ## Special uncerts had just been propagated to rebinnedHists[]
                ## Non-uncerts have been added/unzeroed/written
	

		#Constructing muRF shapes
                muRUphists17 = [hist.GetName() for hist in tfiles17iRfile.GetListOfKeys() if 'muR'+upTag in hist.GetName() and chn in hist.GetName()]
                muRUphists16 = [(hist.GetName()).replace(lumi16,lumi17) for hist in tfiles16iRfile.GetListOfKeys() if 'muR'+upTag in hist.GetName() and chn in hist.GetName()]
                muRUphists18 = [(hist.GetName()).replace(lumi18,lumi17) for hist in tfiles18iRfile.GetListOfKeys() if 'muR'+upTag in hist.GetName() and chn in hist.GetName()]
                muset17 = set(muRUphists17)
                muset16 = set(muRUphists16)
                muset18 = set(muRUphists18)
                mulist16not17 = list(muset16 - muset17)
                muset16not17 = set(mulist16not17)
                mulist18not1617 = list(muset18 - muset17 - muset16not17)
                muRUphists = muRUphists17 + mulist16not17 + mulist18not1617
                #muRUphists = [k.GetName() for k in tfiles17iRfile.GetListOfKeys() if 'muR'+upTag in k.GetName() and chn in k.GetName()]
		for hist in muRUphists:
                        # pull out the Discrim_stuff_stuff__proc part of the name
                        proc = hist.split('__')[1]
                        basename = hist.split('__')[0]+'__'+proc
                        do = {}
                        if proc+'16' in badhistlist.keys(): do['16'] = bool(basename not in badhistlist[proc+'16'])
                        else: do['16'] = True
                        if proc+'17' in badhistlist.keys(): do['17'] = bool(basename not in badhistlist[proc+'17'])
                        else: do['17'] = True
                        if proc+'18' in badhistlist.keys(): do['18'] = bool(basename not in badhistlist[proc+'18'])                        
                        else: do['18'] = True

			newMuRFNameBase = 'muRFcorrdNew'
			if 'qcd__' in hist: newMuRFName = newMuRFNameBase+'QCD'
			if 'ewk__' in hist: newMuRFName = newMuRFNameBase+'Ewk'
			if 'top__' in hist: newMuRFName = newMuRFNameBase+'Top'
			if 'sig__' in hist or (rebinCombine and '__'+sigName in hist): newMuRFName = newMuRFNameBase+'Sig'

                        muRFcorrdNewUpHists = {}
                        muRFcorrdNewDnHists = {}
                        for year in shortyears:
                                if not do[year]: continue

                                muRFcorrdNewUpHists[year] = rebinnedHists[hist+year].Clone(hist.replace(lumi17,lumi).replace('muR'+upTag,newMuRFName+'20'+year+upTag))
                                muRFcorrdNewDnHists[year] = rebinnedHists[hist+year].Clone(hist.replace(lumi17,lumi).replace('muR'+upTag,newMuRFName+'20'+year+downTag))
                                histList = [
                                        rebinnedHists[hist[:hist.find('__mu')]+'N'+year], #nominal 
                                        rebinnedHists[hist+year], #renormWeights[5]
                                        rebinnedHists[(hist+year).replace('muR'+upTag,'muR'+downTag)], #renormWeights[3]
                                        rebinnedHists[(hist+year).replace('muR'+upTag,'muF'+upTag)], #renormWeights[1]
                                        rebinnedHists[(hist+year).replace('muR'+upTag,'muF'+downTag)], #renormWeights[0]
                                        rebinnedHists[(hist+year).replace('muR'+upTag,'muRFcorrd'+upTag)], #renormWeights[4]
                                        rebinnedHists[(hist+year).replace('muR'+upTag,'muRFcorrd'+downTag)] #renormWeights[2]
                                ]
                                for ibin in range(1,histList[0].GetNbinsX()+1):
                                        weightList = [histList[ind].GetBinContent(ibin) for ind in range(len(histList))]
                                        indCorrdUp = weightList.index(max(weightList))
                                        indCorrdDn = weightList.index(min(weightList))
                                                
                                        muRFcorrdNewUpHists[year].SetBinContent(ibin,histList[indCorrdUp].GetBinContent(ibin))
                                        muRFcorrdNewDnHists[year].SetBinContent(ibin,histList[indCorrdDn].GetBinContent(ibin))
                                                
                                        muRFcorrdNewUpHists[year].SetBinError(ibin,histList[indCorrdUp].GetBinError(ibin))
                                        muRFcorrdNewDnHists[year].SetBinError(ibin,histList[indCorrdDn].GetBinError(ibin))

                                ## Special things for signal
                                if normalizeRENORM and ('sig__mu' in hist or '__'+sigName in hist):

                                        if rebinCombine and '__'+sigName in hist: 
                                                signame = hist.split('__')[1]
                                                if sigName not in signame: print "DIDNT GET SIGNAME",signame

                                        scalefactorUp = muSFsUp[signame][int(year)%16]
                                        scalefactorDn = muSFsDn[signame][int(year)%16]
                                        muRFcorrdNewUpHists[year].Scale(scalefactorUp) #drop down .7
                                        muRFcorrdNewDnHists[year].Scale(scalefactorDn) #raise up 1.3

                                        if rebinCombine:
                                                for iBin in range(1,muRFcorrdNewUpHists[year].GetNbinsX()+1):
                                                        if muRFcorrdNewUpHists[year].GetBinContent(iBin) == 0:            ##Check if bin content is zero
                                                                muRFcorrdNewUpHists[year].SetBinContent(iBin,1e-6) ##Setting bin content to nonzero value
                                                                muRFcorrdNewUpHists[year].SetBinError(iBin,math.sqrt(1e-6))
                                                        if muRFcorrdNewDnHists[year].GetBinContent(iBin) == 0:            ##Check if bin content is zero
                                                                muRFcorrdNewDnHists[year].SetBinContent(iBin,1e-6) ##Setting bin content to nonzero value
                                                                muRFcorrdNewDnHists[year].SetBinError(iBin,math.sqrt(1e-6))

                                ## Special things for background
                                if ('sig__mu' not in hist and '__'+sigName not in hist and normalizeRENORM and not FullMu):
                                        renormNomHist = histList[0]
                                        muRFcorrdNewUpHists[year].Scale(renormNomHist.Integral()/muRFcorrdNewUpHists[year].Integral())
                                        muRFcorrdNewDnHists[year].Scale(renormNomHist.Integral()/muRFcorrdNewDnHists[year].Integral())


                        lowyear = min([item for item in do.keys() if do[item] == True])
                        muRFcorrdNewUpHist = muRFcorrdNewUpHists[lowyear].Clone(hist.replace(lumi17,lumi).replace('muR'+upTag,newMuRFName+upTag))
                        muRFcorrdNewDnHist = muRFcorrdNewDnHists[lowyear].Clone(hist.replace(lumi17,lumi).replace('muR'+upTag,newMuRFName+downTag))
                        if lowyear == '17' and do['18']: 
                                muRFcorrdNewUpHist.Add(muRFcorrdNewUpHists[str(int(lowyear)+1)]) #if 17, add 18
                                muRFcorrdNewDnHist.Add(muRFcorrdNewDnHists[str(int(lowyear)+1)]) #if 17, add 18
                        if lowyear == '16':
                                if do['17']: 
                                        muRFcorrdNewUpHist.Add(muRFcorrdNewUpHists[str(int(lowyear)+1)]) #if 16, add 17
                                        muRFcorrdNewDnHist.Add(muRFcorrdNewDnHists[str(int(lowyear)+1)]) #if 16, add 17
                                if do['18']: 
                                        muRFcorrdNewUpHist.Add(muRFcorrdNewUpHists[str(int(lowyear)+2)]) #if 16, add 18
                                        muRFcorrdNewDnHist.Add(muRFcorrdNewDnHists[str(int(lowyear)+2)]) #if 16, add 18

			muRFcorrdNewUpHist.Write()
			muRFcorrdNewDnHist.Write()

                        if 'W0p5' in rfile or 'kinematics' in folder:
                                yieldsAll[muRFcorrdNewUpHist.GetName().replace(lumi,lumi17).replace('_sig','_'+rfile.split('_')[-2])] = muRFcorrdNewUpHist.Integral()
                                yieldsAll[muRFcorrdNewDnHist.GetName().replace(lumi,lumi17).replace('_sig','_'+rfile.split('_')[-2])] = muRFcorrdNewDnHist.Integral()

		#Constructing PDF shapes
                pdfUphists17 = [hist.GetName() for hist in tfiles17iRfile.GetListOfKeys() if 'pdf0' in hist.GetName() and chn in hist.GetName()]
                pdfUphists16 = [(hist.GetName()).replace(lumi16,lumi17) for hist in tfiles16iRfile.GetListOfKeys() if 'pdf0' in hist.GetName() and chn in hist.GetName()]
                pdfUphists18 = [(hist.GetName()).replace(lumi18,lumi17) for hist in tfiles18iRfile.GetListOfKeys() if 'pdf0' in hist.GetName() and chn in hist.GetName()]
                pdfset17 = set(pdfUphists17)
                pdfset16 = set(pdfUphists16)
                pdfset18 = set(pdfUphists18)
                pdflist16not17 = list(pdfset16 - pdfset17)
                pdfset16not17 = set(pdflist16not17)
                pdflist18not1617 = list(pdfset18 - pdfset17 - pdfset16not17)
                pdfUphists = pdfUphists17 + pdflist16not17 + pdflist18not1617

		#pdfUphists = [k.GetName() for k in tfiles17iRfile.GetListOfKeys() if 'pdf0' in k.GetName() and chn in k.GetName()]

		for hist in pdfUphists:
                        # pull out the Discrim_stuff_stuff__proc part of the name
                        proc = hist.split('__')[1]
                        basename = hist.split('__')[0]+'__'+proc
                        do = {}
                        if proc+'16' in badhistlist.keys(): do['16'] = bool(basename not in badhistlist[proc+'16'])
                        else: do['16'] = True
                        if proc+'17' in badhistlist.keys(): do['17'] = bool(basename not in badhistlist[proc+'17'])
                        else: do['17'] = True
                        if proc+'18' in badhistlist.keys(): do['18'] = bool(basename not in badhistlist[proc+'18'])                        
                        else: do['18'] = True

                        pdfNewUpHists = {}
                        pdfNewDnHists = {}
                        for year in ['16','17']: 
                                
                                if year == '16': 
                                        if not do[year]: continue
                                        newPDFName = 'pdfNew2016'
                                        thisyear = '16'
                                else:
                                        thisyear = '17'
                                        add18 = False
                                        if not do['17'] and not do['18']: continue
                                        elif not do['17']: thisyear = '18'
                                        elif do['18']: add18 = True
                                        #else 17 yes, 18 no = default

                                        newPDFName = 'pdfNew20172018'
                                                        
                                pdfNewUpHists[thisyear] = rebinnedHists[hist+thisyear].Clone(hist.replace(lumi17,lumi).replace('pdf0','pdfNew'+thisyear+upTag))
                                pdfNewDnHists[thisyear] = rebinnedHists[hist+thisyear].Clone(hist.replace(lumi17,lumi).replace('pdf0','pdfNew'+thisyear+downTag))
                                centralHist = rebinnedHists[hist.replace('__pdf0','')+'N'+thisyear]
                                if thisyear == '17' and add18: centralHist.Add(rebinnedHists[hist.replace('__pdf0','')+'N18'])
              
                                for ibin in range(1,pdfNewUpHists[thisyear].GetNbinsX()+1):
                                        if thisyear == '16': # replicas
                                                # list of bin contents
                                                weightList = [rebinnedHists[(hist+thisyear).replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]
                
                                                indPDFUp = sorted(range(len(weightList)), key=lambda k: weightList[k])[83]
                                                indPDFDn = sorted(range(len(weightList)), key=lambda k: weightList[k])[15]
                                                pdfNewUpHists[thisyear].SetBinContent(ibin,rebinnedHists[(hist+thisyear).replace('pdf0','pdf'+str(indPDFUp))].GetBinContent(ibin))
                                                pdfNewDnHists[thisyear].SetBinContent(ibin,rebinnedHists[(hist+thisyear).replace('pdf0','pdf'+str(indPDFDn))].GetBinContent(ibin))
                                                pdfNewUpHists[thisyear].SetBinError(ibin,rebinnedHists[(hist+thisyear).replace('pdf0','pdf'+str(indPDFUp))].GetBinError(ibin))
                                                pdfNewDnHists[thisyear].SetBinError(ibin,rebinnedHists[(hist+thisyear).replace('pdf0','pdf'+str(indPDFDn))].GetBinError(ibin))
                                        else:  # Hessian                                                
                                                # list of bin contents for both years together
                                                if add18: 
                                                        if proc == 'sig' or 'TTM' in proc or 'BBM' in proc:
                                                                weightList = [rebinnedHists[(hist+thisyear).replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin)+rebinnedHists[(hist+'18').replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(30)]
                                                        else:
                                                                weightList = [rebinnedHists[(hist+thisyear).replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin)+rebinnedHists[(hist+'18').replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]

                                                else: 
                                                        if proc == 'sig' or 'TTM' in proc or 'BBM' in proc:
                                                                weightList = [rebinnedHists[(hist+thisyear).replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(30)]
                                                        else:
                                                                weightList = [rebinnedHists[(hist+thisyear).replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]

                                                errsq = 0
                                                for weight in weightList:
                                                        ## sum up squares of differences to the central value
                                                        errsq += (weight - centralHist.GetBinContent(ibin))**2
                                                
                                                ## find the percentage of the shift w.r.t the central value
                                                if centralHist.GetBinContent(ibin) != 0: shiftpct = math.sqrt(errsq)/centralHist.GetBinContent(ibin)
                                                else:
                                                        if errsq > 0.0001: print 'Weird: central is 0 but not PDF unc has errsq',errsq,'in bin',ibin,'of hist',hist
                                                        # after looking, seems like truncation error that central is 0...weight < float tolerance in nominal
                                                        shiftpct = 0
                
                                                if abs(shiftpct) > 1 and centralHist.GetBinContent(ibin) > 0.008: print 'WARNING: pdf shift is',shiftpct,', flooring down at 0 in bin',ibin,'of hist',hist,'in',thisyear,'on bin content of',centralHist.GetBinContent(ibin)
                                                
                                                ## multiply the central value by 1 +/- the shift
                                                pdfNewUpHists[thisyear].SetBinContent(ibin, max(0,centralHist.GetBinContent(ibin)*(1 + shiftpct)))
                                                pdfNewDnHists[thisyear].SetBinContent(ibin, max(0,centralHist.GetBinContent(ibin)*(1 - shiftpct)))                                
                                        
                                ## Special things for signal
                                if normalizePDF and ('sig__pdf' in hist or '__'+sigName in hist):
                                        if rebinCombine: 
                                                signame = hist.split('__')[1]
                                                if sigName not in signame: print "DIDNT GET SIGNAME",signame
                                        
                                        sfyear = thisyear
                                        if thisyear == '18': sfyear = '17'
                                        scalefactorUp = pdfSFsUp[signame][int(sfyear)%16]
                                        scalefactorDn = pdfSFsDn[signame][int(sfyear)%16]
                                        pdfNewUpHists[thisyear].Scale(scalefactorUp)
                                        pdfNewDnHists[thisyear].Scale(scalefactorDn)
                
                                        if rebinCombine:
                                                for iBin in range(1,pdfNewUpHists[thisyear].GetNbinsX()+1):
                                                        if pdfNewUpHists[thisyear].GetBinContent(iBin) == 0:            ##Check if bin content is zero
                                                                pdfNewUpHists[thisyear].SetBinContent(iBin,1e-6) ##Setting bin content to nonzero value
                                                                pdfNewUpHists[thisyear].SetBinError(iBin,math.sqrt(1e-6))
                                                        if pdfNewDnHists[thisyear].GetBinContent(iBin) == 0:            ##Check if bin content is zero
                                                                pdfNewDnHists[thisyear].SetBinContent(iBin,1e-6) ##Setting bin content to nonzero value
                                                                pdfNewDnHists[thisyear].SetBinError(iBin,math.sqrt(1e-6))
                
                                if thisyear == '16':
                                        pdfNewUpHist16 = pdfNewUpHists[thisyear].Clone(hist.replace(lumi17,lumi).replace('pdf0',newPDFName+upTag))
                                        if do['17']: pdfNewUpHist16.Add(rebinnedHists[hist.replace('__pdf0','')+'N17'])
                                        if do['18']: pdfNewUpHist16.Add(rebinnedHists[hist.replace('__pdf0','')+'N18'])
                                        pdfNewUpHist16.Write()
                
                                        pdfNewDnHist16 = pdfNewDnHists[thisyear].Clone(hist.replace(lumi17,lumi).replace('pdf0',newPDFName+downTag))
                                        if do['17']: pdfNewDnHist16.Add(rebinnedHists[hist.replace('__pdf0','')+'N17'])
                                        if do['18']: pdfNewDnHist16.Add(rebinnedHists[hist.replace('__pdf0','')+'N18'])
                                        pdfNewDnHist16.Write()
                
                                        if 'W0p5' in rfile or 'kinematics' in folder:
                                                yieldsAll[pdfNewUpHist16.GetName().replace(lumi,lumi17).replace('_sig','_'+rfile.split('_')[-2])] = pdfNewUpHist16.Integral()
                                                yieldsAll[pdfNewDnHist16.GetName().replace(lumi,lumi17).replace('_sig','_'+rfile.split('_')[-2])] = pdfNewDnHist16.Integral()
                                else:
                                        pdfNewUpHist = pdfNewUpHists[thisyear].Clone(hist.replace(lumi17,lumi).replace('pdf0',newPDFName+upTag))
                                        if do['16']: pdfNewUpHist.Add(rebinnedHists[hist.replace('__pdf0','')+'N16'])
                                        pdfNewUpHist.Write()
                
                                        pdfNewDnHist = pdfNewDnHists[thisyear].Clone(hist.replace(lumi17,lumi).replace('pdf0',newPDFName+downTag))
                                        if do['16']: pdfNewDnHist.Add(rebinnedHists[hist.replace('__pdf0','')+'N16'])
                                        pdfNewDnHist.Write()
                
                                        if 'W0p5' in rfile or 'kinematics' in folder:
                                                yieldsAll[pdfNewUpHist.GetName().replace(lumi,lumi17).replace('_sig','_'+rfile.split('_')[-2])] = pdfNewUpHist.Integral()
                                                yieldsAll[pdfNewDnHist.GetName().replace(lumi,lumi17).replace('_sig','_'+rfile.split('_')[-2])] = pdfNewDnHist.Integral()
        
        print 'Closing input files...'
	tfiles16iRfile.Close()
	tfiles17iRfile.Close()
	tfiles18iRfile.Close()
        print 'Closing output file...'
	outputRfilesiRfile.Close()
	iRfile+=1
#tfile16.Close()
#tfile17.Close()
#tfile18.Close()
print ">> Rebinning Done!"


isEMlist =[]
algolist = []
taglist = []

for chn in channels:
	if chn.split('_')[0+rebinCombine] not in isEMlist: isEMlist.append(chn.split('_')[0+rebinCombine])
	if chn.split('_')[1+rebinCombine] not in taglist: taglist.append(chn.split('_')[1+rebinCombine])
	if chn.split('_')[2+rebinCombine] not in algolist: algolist.append(chn.split('_')[2+rebinCombine])

print "List of systematics for "+bkgProcList[0]+" process and "+channels[0]+" channel:"
print "        ",sorted([hist[hist.find(bkgProcList[0])+len(bkgProcList[0])+2:hist.find(upTag)] for hist in yieldsAll.keys() if channels[0] in hist and '__'+bkgProcList[0]+'__' in hist and upTag in hist])

def getShapeSystUnc(proc,chn):
	if not addShapes: return 0
	systematicList = sorted([hist[hist.find(proc)+len(proc)+2:hist.find(upTag)] for hist in yieldsAll.keys() if chn in hist and '__'+proc+'__' in hist and upTag in hist])
	totUpShiftPrctg=0
	totDnShiftPrctg=0
	histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
	nomHist = histoPrefix+proc
	for syst in systematicList:
		for ud in [upTag,downTag]:
			shpHist = histoPrefix+proc+'__'+syst+ud
			shift = yieldsAll[shpHist]/(yieldsAll[nomHist]+1e-20)-1
			if shift>0.: totUpShiftPrctg+=shift**2
			if shift<0.: totDnShiftPrctg+=shift**2
	shpSystUncPrctg = (math.sqrt(totUpShiftPrctg)+math.sqrt(totDnShiftPrctg))/2 #symmetrize the total shape uncertainty up/down shifts
	return shpSystUncPrctg	

flatuncs = {'qcd':0.25,'ewk':0.25,'top':0.30}
if not addFlat: flatuncs = {'qcd':0.0,'ewk':0.0,'top':0.0}
table = []
taglist = ['tagged','notV']
if 'templatesCR' in folder: taglist = ['dnnLarge']
if 'kinematics' in folder: taglist = ['all']
for isEM in isEMlist:
	if isEM=='isE': corrdSys = elcorrdSys
	if isEM=='isM': corrdSys = mucorrdSys
	for tag in taglist:
		table.append(['break'])
		table.append(['',isEM+'_'+tag+'_yields'])
		table.append(['break'])
		table.append(['YIELDS']+[chn for chn in channels if isEM in chn and tag in chn]+['\\\\'])
		for proc in bkgProcList+['totBkg',dataName,'dataOverBkg']+sigProcList:
			row = [proc]
			for chn in channels:
				if not (isEM in chn and tag in chn): continue
				modTag = chn[chn.find('is'):]
				histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
				yieldtemp = 0.
				yielderrtemp = 0.
				if proc=='totBkg' or proc=='dataOverBkg':
					for bkg in bkgProcList:
						try:
							yieldtemp += yieldsAll[histoPrefix+bkg]
							yielderrtemp += yieldsErrsAll[histoPrefix+bkg]**2
                                                        yielderrtemp += (yieldsAll[histoPrefix+bkg]*flatuncs[bkg])**2
							yielderrtemp += (getShapeSystUnc(bkg,chn)*yieldsAll[histoPrefix+bkg])**2
						except:
							if bkg != 'qcd': print "Missing",bkg,"for channel in totBkg or dataOverBkg:",chn
							pass

					yielderrtemp += (corrdSys*yieldtemp)**2
					if proc=='dataOverBkg':
						dataTemp = yieldsAll[histoPrefix+dataName]+1e-20
						dataTempErr = yieldsErrsAll[histoPrefix+dataName]**2
						yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
						yieldtemp = dataTemp/yieldtemp
				else:
					try:
						yieldtemp += yieldsAll[histoPrefix+proc]
						yielderrtemp += yieldsErrsAll[histoPrefix+proc]**2
                                                if proc in bkgProcList: yielderrtemp += (yieldsAll[histoPrefix+proc]*flatuncs[proc])**2
						yielderrtemp += (getShapeSystUnc(proc,chn)*yieldsAll[histoPrefix+proc])**2
					except:
						if proc != 'qcd': print "Missing",proc,"for channel individual:",chn
						pass
					if proc in sigProcList:
						signal=proc
						if 'left' in signal: signal=proc.replace('left','')+'left'
						if 'right' in signal: signal=proc.replace('right','')+'right'
						yieldtemp*=xsec[signal]
						yielderrtemp*=xsec[signal]**2
                                                if rebinCombine:
                                                        yieldtemp*=10
                                                        yielderrtemp*=10**2                                                        
					yielderrtemp += (corrdSys*yieldtemp)**2
				yielderrtemp = math.sqrt(yielderrtemp)
				#print "yieldsAll: ",yieldsAll
				if proc==dataName: row.append(' & '+str(int(yieldsAll[histoPrefix+proc])))
				else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
			row.append('\\\\')
			table.append(row)
			
for tag in taglist:
	table.append(['break'])
	table.append(['','isL_'+tag+'_yields'])
	table.append(['break'])
	table.append(['YIELDS']+[chn.replace('isE','isL') for chn in channels if 'isE' in chn and tag in chn]+['\\\\'])
	for proc in bkgProcList+['totBkg',dataName,'dataOverBkg']+sigProcList:
		row = [proc]
		for chn in channels:
			if not ('isE' in chn and tag in chn): continue
			modTag = chn[chn.find('is'):]
			histoPrefixE = allhists[chn][0][:allhists[chn][0].find('__')+2]
			histoPrefixM = histoPrefixE.replace('isE','isM')
			yieldtemp = 0.
			yieldtempE = 0.
			yieldtempM = 0.
			yielderrtemp = 0. 
			if proc=='totBkg' or proc=='dataOverBkg':
				for bkg in bkgProcList:
					yieldEplusMtemp = 0
					try:
						yieldtempE += yieldsAll[histoPrefixE+bkg]
						yieldtemp += yieldsAll[histoPrefixE+bkg]
						yieldEplusMtemp += yieldsAll[histoPrefixE+bkg]
                                                yielderrtemp += (yieldsAll[histoPrefixE+bkg]*flatuncs[bkg])**2
						yielderrtemp += yieldsErrsAll[histoPrefixE+bkg]**2
						yielderrtemp += (getShapeSystUnc(bkg,chn)*yieldsAll[histoPrefixE+bkg])**2
					except:
						if bkg != 'qcd': print "Missing",bkg,"for channel in totBkg:",chn
						pass
					try:
						yieldtempM += yieldsAll[histoPrefixM+bkg]
						yieldtemp += yieldsAll[histoPrefixM+bkg]
						yieldEplusMtemp += yieldsAll[histoPrefixM+bkg]
                                                yielderrtemp += (yieldsAll[histoPrefixM+bkg]*flatuncs[bkg])**2
						yielderrtemp += yieldsErrsAll[histoPrefixM+bkg]**2
						yielderrtemp += (getShapeSystUnc(bkg,chn.replace('isE','isM'))*yieldsAll[histoPrefixM+bkg])**2
					except:
						if bkg != 'qcd': print "Missing",bkg,"for channel in totBkg:",chn.replace('isE','isM')
						pass
				yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
				if proc=='dataOverBkg':
					dataTemp = yieldsAll[histoPrefixE+dataName]+yieldsAll[histoPrefixM+dataName]+1e-20
					dataTempErr = yieldsErrsAll[histoPrefixE+dataName]**2+yieldsErrsAll[histoPrefixM+dataName]**2
					yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
					yieldtemp = dataTemp/yieldtemp
			else:
				try:
					yieldtempE += yieldsAll[histoPrefixE+proc]
					yieldtemp  += yieldsAll[histoPrefixE+proc]
                                        if proc in bkgProcList: yielderrtemp += (yieldsAll[histoPrefixE+proc]*flatuncs[proc])**2
					yielderrtemp += yieldsErrsAll[histoPrefixE+proc]**2
					yielderrtemp += (getShapeSystUnc(proc,chn)*yieldsAll[histoPrefixE+proc])**2
				except:
					if proc != 'qcd': print "Missing",proc,"for channel individual:",chn
					pass
				try:
					yieldtempM += yieldsAll[histoPrefixM+proc]
					yieldtemp  += yieldsAll[histoPrefixM+proc]
                                        if proc in bkgProcList: yielderrtemp += (yieldsAll[histoPrefixM+proc]*flatuncs[proc])**2
					yielderrtemp += yieldsErrsAll[histoPrefixM+proc]**2
					yielderrtemp += (getShapeSystUnc(proc,chn.replace('isE','isM'))*yieldsAll[histoPrefixM+proc])**2
				except:
					if proc != 'qcd': print "Missing",proc,"for channel individual:",chn.replace('isE','isM')
					pass
				if proc in sigProcList:
					signal=proc
					if 'left' in signal: signal=proc.replace('left','')+'left'
					if 'right' in signal: signal=proc.replace('right','')+'right'
					yieldtempE*=xsec[signal]
					yieldtempM*=xsec[signal]
					yieldtemp*=xsec[signal]
					yielderrtemp*=xsec[signal]**2
                                        if rebinCombine:
                                                yieldtempE*=10
                                                yieldtempM*=10
                                                yieldtemp*=10
                                                yielderrtemp*=10**2                                                
				yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
			yielderrtemp = math.sqrt(yielderrtemp)
			if proc==dataName: row.append(' & '+str(int(yieldsAll[histoPrefixE+proc]+yieldsAll[histoPrefixM+proc])))
			else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
		row.append('\\\\')
		table.append(row)
	
#systematics
table.append(['break'])
table.append(['','Systematics'])
table.append(['break'])
for proc in bkgProcList+sigProcList:
	table.append([proc]+[chn for chn in channels]+['\\\\'])
	systematicList = sorted([hist[hist.find(proc)+len(proc)+2:hist.find(upTag)] for hist in yieldsAll.keys() if channels[0] in hist and '__'+proc+'__' in hist and upTag in hist])
	for syst in systematicList:
		for ud in [upTag,downTag]:
			row = [syst+ud]
			for chn in channels:
				histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
				nomHist = histoPrefix+proc
				shpHist = histoPrefix+proc+'__'+syst+ud
				try: row.append(' & '+str(round(yieldsAll[shpHist]/(yieldsAll[nomHist]+1e-20),2)))
				except:
					if proc != 'qcd': print "Missing",proc,"for channel:",chn,"and systematic:",syst
					pass
			row.append('\\\\')
			table.append(row)
	table.append(['break'])

postFix = ''
if addShapes: postFix+='_addShps'
if not FullMu: postFix+='_BKGNORM'
if addFlat: postFix+='_RateSys'
if rebinCombine: out=open(templateDir+'/'+combinefile.replace('templates','yields').replace('.root','_rebinned_stat'+str(stat).replace('.','p'))+postFix+'.txt','w')
else: out=open(templateDir+'/'+thetafile.replace('templates','yields').replace('.root','_rebinned_stat'+str(stat).replace('.','p'))+postFix+'.txt','w')

printTable(table,out)

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))



