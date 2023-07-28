#!/usr/bin/python
from ROOT import TH1D,TTree,TFile
from array import array
from numpy import linspace
from weights import *
import math

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
def analyze(tTree,process,doAllSys,iPlot,plotDetails,category,region,isCategorized):
        plotTreeName=plotDetails[0]
	xbins=array('d', plotDetails[1])
	xAxisLabel=plotDetails[2]
        
	# Define categories
	isEM  = category['isEM']
	tag   = category['tag']
	catStr = 'is'+isEM+'_'+tag

	# Define general cuts (These are the only cuts for 'PS')
	cut  = ''

        if 'CR' in region: # 'CR' or 'CRinc'  certain AK8 jets and low signal node
		cut += ' && (NJetsAK8 >= '+str(cutList['nAK8Cut'])+') && (dnnAll_Tprime < dnnAll_WJets'+BBstr+' || dnnAll_Tprime < dnnAll_ttbar'+BBstr+')'
		if 'TT' in region: cut += ' && (dnnAll_ttbar'+BBstr+' > dnnAll_WJets'+BBstr+')'
		if 'WJ' in region: cut += ' && (dnnAll_ttbar'+BBstr+' <= dnnAll_WJets'+BBstr+')'                
	elif 'SR' in region: # 'SR'  certain AK8 jets, mass reco, high signal node
		#cut += ' && (NJetsAK8 >= '+str(cutList['nAK8Cut'])+') && (Tprime2_'+algo+'_Mass > -1) && (dnnAll_Tprime >= '+str(cutList['dnnCut'])+')'
                cut += ' && (NJetsAK8 >= '+str(cutList['nAK8Cut'])+') && (Tprime2_'+algo+'_Mass > -1) && (dnnAll_Tprime >= dnnAll_WJets'+BBstr+' && dnnAll_Tprime >= dnnAll_ttbar'+BBstr+')'
	elif 'PS' in region: # 'PS'  
		cut += ' && (NJetsAK8 >= '+str(cutList['nAK8Cut'])+')'
		if '0b' in region: cut += ' && (NJetsDeepFlavwithSF == 0)'
		elif '1b' in region: cut += ' && (NJetsDeepFlavwithSF == 1)'
		elif '2b' in region: cut += ' && (NJetsDeepFlavwithSF >= 2)'

	# Define weights
	TrigEffElUp = '(triggSF+isElectron*triggSFUncert)'
	TrigEffElDn = '(triggSF-isElectron*triggSFUncert)'
        TrigEffMuUp='(triggSF+isMuon*triggSFUncert)'
        TrigEffMuDn='(triggSF-isMuon*triggSFUncert)'
	TrigEff = 'triggSF'
        lepIdSF = 'lepIdSF'
        lepIdSFUp = '(lepIdSF + elIdSFUnc)' # add-on is 0 for muons
        lepIdSFDn = '(lepIdSF - elIdSFUnc)'

        
        ## FIXME add these two calcs to the analyzer
        topCorr = '1'
        topCorrUp = '1'
        topCorrDn = '1'
        jetSFstr = '1'
        jetSFstrUp = '1'
        jetSFstrDn = '1'
	if (process!='WJetsMG' and 'WJetsMG' in process):
		jetSFstr = 'HTSF_Pol'
		jetSFstrUp = 'HTSF_PolUp'
		jetSFstrDn = 'HTSF_PolDn'
        if 'TTJets' in process:
                topCorr = 'HT_Corr'#'min(1.0,tpt_Corr)'#'topPtWeight13TeV'#
                topCorrUp = 'HT_CorrUp'#'min(1.0,tpt_CorrUp)'#'1'#
                topCorrDn = 'HT_CorrDn'#'min(1.0,tpt_CorrDn)'#'topPtWeight13TeV'#

	weightStr = '1'
	if 'Data' not in process: 
		if 'TTM' in process or 'BBM' in process:
			weightStr          += ' * '+jetSFstr+' * '+TrigEff+' * pileupWeight * '+lepIdSF+' * EGammaGsfSF * isoSF * '+str(weight[process])+' * pdfWeights4LHC[0] * MCWeight'
		else:
			weightStr          += ' * '+jetSFstr+' * '+topCorr+' * '+TrigEff+' * pileupWeight * '+lepIdSF+' * EGammaGsfSF * isoSF * '+str(weight[process])+' * (MCWeight/abs(MCWeight))'

		weightelIdSFUpStr  = weightStr.replace(lepIdSF,lepIdSFUp)
                weightelIdSFDownStr= weightStr.replace(lepIdSF,lepIdSFDn)
		weightTrigEffElUpStr  = weightStr.replace(TrigEff,TrigEffElUp)
                weightTrigEffElDownStr= weightStr.replace(TrigEff,TrigEffElDn)
		weightTrigEffMuUpStr  = weightStr.replace(TrigEff,TrigEffMuUp)
		weightTrigEffMuDownStr= weightStr.replace(TrigEff,TrigEffMuDn)
		weightPileupUpStr   = weightStr.replace('pileupWeight','pileupWeightUp')
		weightPileupDownStr = weightStr.replace('pileupWeight','pileupWeightDown')
		weightmuRFcorrdUpStr   = 'renormWeights[5] * '+weightStr
		weightmuRFcorrdDownStr = 'renormWeights[3] * '+weightStr
		weightmuRUpStr      = 'renormWeights[4] * '+weightStr
		weightmuRDownStr    = 'renormWeights[2] * '+weightStr
		weightmuFUpStr      = 'renormWeights[1] * '+weightStr
		weightmuFDownStr    = 'renormWeights[0] * '+weightStr
		weighttopptUpStr    = weightStr.replace(topCorr,topCorrUp)
		weighttopptDownStr  = weightStr.replace(topCorr,topCorrDn)
		weightjsfUpStr      = weightStr.replace(jetSFstr,jetSFstrUp)
		weightjsfDownStr    = weightStr.replace(jetSFstr,jetSFstrDn)


        print "*****"*20
	print "*****"*20
	print "DISTRIBUTION:", iPlot
	print "            -name in ljmet trees:", plotTreeName
	print "            -x-axis label is set to:", xAxisLabel
	print "            -using the binning as:", xbins
       	print "/////"*5
	print "PROCESSING: ", process
	print "/////"*5

	# Design the EM cuts for categories
        ## FIXME add "isHole" to RDF
	isEMCut=''
	if isEM=='E': isEMCut+=' && isEl==1 && ((lepton_eta<-2.5 || lepton_eta>-1.479) || (lepton_phi<-1.55 || lepton_phi>-0.9)) ' 
	elif isEM=='M': isEMCut+=' && isMu==1'
	elif isEM=='L': isEMCut+=' && (isMu==1 || (isEl==1 && ((lepton_eta<-2.5 || lepton_eta>-1.479) || (lepton_phi<-1.55 || lepton_phi>-0.9))))'
		
	# Design the tagging cuts for categories
	tagCut = ''
	if isCategorized:
		if tag == 'taggedbWbW': tagCut += ' && taggedBWBW_'+algo+' == 1'
		elif tag == 'taggedtHbW': tagCut += ' && taggedTHBW_'+algo+' == 1'
		elif tag == 'taggedtZbW': tagCut += ' && taggedTZBW_'+algo+' == 1'
		elif tag == 'taggedtHtH': tagCut += ' && taggedTHTH_'+algo+' == 1'
		elif tag == 'taggedtZtH': tagCut += ' && taggedTZTH_'+algo+' == 1'
		elif tag == 'taggedtZtZ': tagCut += ' && taggedTZTZ_'+algo+' == 1'

		# signal categories for basic tag counts
		if 'ttbar' in tag: cut += ' && (dnnAll_ttbar'+BBstr+' > dnnAll_WJets'+BBstr+')'
		if 'wjet' in tag: cut += ' && (dnnAll_ttbar'+BBstr+' <= dnnAll_WJets'+BBstr+')'

		if '3W' in tag: tagCut += ' && nW_'+algo+' == 3'
		elif '3pW' in tag: tagCut += ' && nW_'+algo+' >= 3'
		elif '2pW' in tag: tagCut += ' && nW_'+algo+' >= 2'
		elif '2W' in tag: tagCut += ' && nW_'+algo+' == 2'
		elif '1pW' in tag: tagCut += ' && nW_'+algo+' >= 1'
		elif '1W' in tag: tagCut += ' && nW_'+algo+' == 1'
		elif '01W' in tag: tagCut += ' && nW_'+algo+' <= 1'
		elif '0W' in tag: tagCut += ' && nW_'+algo+' == 0'
		
		if '0T' in tag: tagCut += ' && nT_'+algo+' == 0'
		elif '01T' in tag: tagCut += ' && nT_'+algo+' <= 1'
		elif '1T' in tag: tagCut += ' && nT_'+algo+' == 1'
		elif '1pT' in tag: tagCut += ' && nT_'+algo+' >= 1'
		elif '2pT' in tag: tagCut += ' && nT_'+algo+' >= 2'
		
		if '1pJ' in tag: tagCut += ' && nJ_'+algo+' >= 1'
	       	

	fullcut = cut+isEMCut+tagCut

	print 'plotTreeName: '+plotTreeName
	print 'Flavour: '+isEM+' #tag: '+tag+' #algo: '+algo
	print "Weights:",weightStr
	print 'Cuts: '+fullcut

	# Declare histograms --- COMMENTS FOR UNCERTAINTIES NOT BEING RUN YET
	hists = {}
	hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		hists[iPlot+'elIdSFUp_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'elIdSFUp_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'elIdSFDown_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'elIdSFDown_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'trigeffElUp_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffElUp_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'trigeffElDown_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffElDown_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[iPlot+'trigeffMuUp_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffMuUp_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[iPlot+'trigeffMuDown_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffMuDown_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			
		if process+'jerUp' in tTree: 
			hists[iPlot+'jerUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'jerDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if process+'jecUp' in tTree:
			hists[iPlot+'jecUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'jecDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if process+'btagUp' in tTree: 
			hists[iPlot+'btagUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'btagUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'btagDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'btagDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if process+'ltagUp' in tTree:
			hists[iPlot+'ltagUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'ltagUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'ltagDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'ltagDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)

		if isCategorized:
			hists[iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        if 'Bp' in process:
                                for i in range(30): hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        else:
                                for i in range(100): hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[process].Draw(plotTreeName+' >> '+iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
	print 'Nominal hist integral: ',hists[iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process].Integral()
	if doAllSys:
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'elIdSFUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightelIdSFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'elIdSFDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightelIdSFDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffElUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffElUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffElDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffElDownStr+'*('+fullcut+')', 'GOFF')
                tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffMuUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffMuUpStr+'*('+fullcut+')', 'GOFF')
                tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffMuDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffMuDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process, weightPileupUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process, weightPileupDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdUpStr  +'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process, weighttopptUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process, weighttopptDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightjsfUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightjsfDownStr+'*('+fullcut+')', 'GOFF')

		if process+'jecUp' in tTree:
			tTree[process+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if process+'jerUp' in tTree:
			tTree[process+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if process+'btagUp' in tTree:
			tTree[process+'btagUp'].Draw(plotTreeName   +' >> '+iPlot+'btagUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'btagDown'].Draw(plotTreeName +' >> '+iPlot+'btagDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if process+'ltagUp' in tTree:
			tTree[process+'ltagUp'].Draw(plotTreeName   +' >> '+iPlot+'ltagUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'ltagDown'].Draw(plotTreeName +' >> '+iPlot+'ltagDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')

		if isCategorized:
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuRUpStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuRDownStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuFUpStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuFDownStr+'*('+fullcut+')', 'GOFF')
                        if 'Bp' in process:
                                for i in range(30): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, '(pdfWeights4LHC['+str(i+1)+']/pdfWeights4LHC[0]) * '+weightStr+'*('+fullcut+')', 'GOFF')
                        else:
                                for i in range(100): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, '(pdfWeights['+str(i)+']) * '+weightStr+'*('+fullcut+')', 'GOFF')	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
