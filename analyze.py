#!/usr/bin/python
from ROOT import TH1D,TTree,TFile
from array import array
from numpy import linspace
from weights import *

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
def analyze(tTree,process,cutList,doAllSys,doJetRwt,iPlot,plotDetails,category,region,isCategorized):
	print "*****"*20
	print "*****"*20
	print "DISTRIBUTION:", iPlot
	print "            -name in ljmet trees:", plotDetails[0]
	print "            -x-axis label is set to:", plotDetails[2]
	print "            -using the binning as:", plotDetails[1]
	plotTreeName=plotDetails[0]
	xbins=array('d', plotDetails[1])
	xAxisLabel=plotDetails[2]
	
	print "/////"*5
	print "PROCESSING: ", process
	print "/////"*5

	# Define categories
	isEM  = category['isEM']
	tag   = category['tag']
	algo  = category['algo']
	catStr = 'is'+isEM+'_'+tag#+'_'+algo
	if algo != '': catStr = catStr+'_'+algo
	if 'ALGO' in plotTreeName: plotTreeName = plotTreeName.replace("ALGO",algo)
	if 'Algo' in plotTreeName: 
		if algo == 'BEST': plotTreeName = plotTreeName.replace('Algo','Best')
		elif algo == 'DeepAK8': plotTreeName = plotTreeName.replace('Algo','DeepAK8')
		elif algo == 'DeepAK8DC':
			plotTreeName = plotTreeName.replace('Algo','DeepAK8')
			plotTreeName = plotTreeName.replace('dnn_','decorr_')

	# Define general cuts (These are the only cuts for 'PS')
	cut  = '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (AK4HT > '+str(cutList['HTCut'])+')'
	cut += ' && (minDR_lepJet > 0.4 || ptRel_lepJet > 40)'
	
	if 'CR' in region: # 'CR' or 'CRinc' ----> bad, need to fix
		cut += ' && (NJetsAK8_JetSubCalc == '+str(cutList['nAK8Cut'])+') && (minDR_leadAK8otherAK8 >= '+str(cutList['drCut'])+')'
	elif 'SR' in region: # 'SR', 'SRalgos'
		cut += ' && (NJetsAK8_JetSubCalc >= '+str(cutList['nAK8Cut'])+') && (minDR_leadAK8otherAK8 < '+str(cutList['drCut'])+')'
	elif 'NoDR' in region: # 'noDR'
		cut += ' && (NJetsAK8_JetSubCalc >= '+str(cutList['nAK8Cut'])+') && (minDR_leadAK8otherAK8 < '+str(cutList['drCut'])+')'
	elif 'PS' in region: # 'PS', 'PSalgos'
		cut += ' && (NJetsAK8_JetSubCalc >= '+str(cutList['nAK8Cut'])+') && (minDR_leadAK8otherAK8 < '+str(cutList['drCut'])+')'
		if '0b' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc == 0)'
		elif '1b' in region: cut += ' && (NJetsCSVwighSF_JetSubCalc == 1)'
		elif '2b' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc >= 2)'

	# Define weights
	TrigEffUp = '1'
	TrigEffDn = '1'
	TrigEff = '1'
	cut += ' && DataPastTrigger == 1 && MCPastTrigger == 1'

	jetSFstr='1'
	jetSFstrUp = '1'
	jetSFstrDn = '1'
	if (process!='WJetsMG' and 'WJetsMG' in process):
		jetSFstr = 'HTSF_Pol'
		jetSFstrUp = 'HTSF_PolUp'
		jetSFstrDn = 'HTSF_PolDn'

	weightStr = '1'
	if 'Data' not in process: 
		# replaced isoSF, MuTrkSF with 1
		weightStr          += ' * '+jetSFstr+' * '+TrigEff+' * pileupWeight * lepIdSF * EGammaGsfSF * (MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc)) * '+str(weight[process])
		if 'TTJets' in process: weightStr = 'topPtWeight13TeV * '+weightStr
		#weightTrigEffUpStr  = weightStr.replace(TrigEff,TrigEffUp)
		#weightTrigEffDownStr= weightStr.replace(TrigEff,TrigEffDn)
		weightPileupUpStr   = weightStr.replace('pileupWeight','pileupWeightUp')
		weightPileupDownStr = weightStr.replace('pileupWeight','pileupWeightDown')
		weightmuRFcorrdUpStr   = 'renormWeights[5] * '+weightStr
		weightmuRFcorrdDownStr = 'renormWeights[3] * '+weightStr
		weightmuRUpStr      = 'renormWeights[4] * '+weightStr
		weightmuRDownStr    = 'renormWeights[2] * '+weightStr
		weightmuFUpStr      = 'renormWeights[1] * '+weightStr
		weightmuFDownStr    = 'renormWeights[0] * '+weightStr
		weighttopptUpStr    = weightStr.replace('topPtWeight13TeV','1')
		weighttopptDownStr  = weightStr.replace('topPtWeight13TeV','topPtWeight13TeV*topPtWeight13TeV')
		weightjsfUpStr      = weightStr.replace(jetSFstr,jetSFstrUp)
		weightjsfDownStr    = weightStr.replace(jetSFstr,jetSFstrDn)

	# For N-1 tagging cuts
	pt_var = 'theJetAK8Pt_JetSubCalc_PtOrdered'
	soft_massvar='theJetAK8SoftDropCorr_JetSubCalc_PtOrdered'
	doubleB_var = 'theJetAK8oubleB_JetSubCalc_PtOrdered'
	tau21var = 'theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered'
	tau32var = 'theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered'
	if 'SoftDropWZNm1' in iPlot: cut+=  ' && ('+tau21var+' < 0.55 && '+pt_var+' > 200)'
	if 'SoftDropHNm1' in iPlot: cut+=  ' && ('+doubleB_var+' > .6 && '+pt_var+' > 300)'
	if 'SoftDropTNm1' in iPlot: cut+=  ' && ('+tau32var+' < 0.65 && '+pt_var+' > 400)'
	if 'Tau21Nm1' in iPlot:  cut += ' && ('+soft_massvar+' > 65 && '+soft_massvar+' < 105 && '+pt_var+' > 200)'
	if 'Tau32Nm1' in iPlot:  cut += ' && ('+soft_massvar+' > 105 && '+soft_massvar+' < 210 && '+pt_var+' > 400)'
	if 'DoubleBNm1' in iPlot: cut += ' && ('+soft_massvar+' > 105 && '+soft_massvar+' < 135 && '+pt_var+' > 300)'

	# Design the EM cuts for categories
	isEMCut=''
	if isEM=='E': isEMCut+=' && isElectron==1'
	elif isEM=='M': isEMCut+=' && isMuon==1'
		
	# Design the tagging cuts for categories
	tagCut = ''
	if isCategorized:
		if tag == 'taggedbWbW': tagCut += ' && taggedBWBW_'+algo+' == 1'
		if tag == 'taggedtHbW': tagCut += ' && taggedTHBW_'+algo+' == 1'
		if tag == 'taggedtZbW': tagCut += ' && taggedTZBW_'+algo+' == 1'
		if tag == 'taggedtHtH': tagCut += ' && taggedTHTH_'+algo+' == 1'
		if tag == 'taggedtZtH': tagCut += ' && taggedTZTH_'+algo+' == 1'
		if tag == 'taggedtZtZ': tagCut += ' && taggedTZTZ_'+algo+' == 1'
		if tag == 'taggedtZHtZH': tagCut += ' && (taggedTZTZ_'+algo+' == 1 || taggedTZTH_'+algo+' == 1 || taggedTHTH_'+algo+' == 1)'
		if tag == 'notV'  : tagCut += ' && isValidVLQDecayMode_'+algo+' == 0'

	fullcut = cut+isEMCut+tagCut

	### Not implemented yet
	# nbtagLJMETname = 'NJetsCSVwithSF_JetSubCalc' #shifts will be: nbtagLJMETname+'_shifts[0/1/2/3]' #####WARNING: THIS STRING DOESN'T EXIST IN STEP1
	# # replace cuts for shifts
        # cut_btagUp = fullcut.replace('btagged','btagged_shifts[0]').replace(nbtagLJMETname,nbtagLJMETname+'_shifts[0]').replace('notH_JetSubCalc','notH_JetSubCalc_shifts[0]')
        # cut_btagDn = fullcut.replace('btagged','btagged_shifts[1]').replace(nbtagLJMETname,nbtagLJMETname+'_shifts[1]').replace('notH_JetSubCalc','notH_JetSubCalc_shifts[1]')
        # cut_mistagUp = fullcut.replace('btagged','btagged_shifts[2]').replace(nbtagLJMETname,nbtagLJMETname+'_shifts[2]').replace('notH_JetSubCalc','notH_JetSubCalc_shifts[2]')
        # cut_mistagDn = fullcut.replace('btagged','btagged_shifts[3]').replace(nbtagLJMETname,nbtagLJMETname+'_shifts[3]').replace('notH_JetSubCalc','notH_JetSubCalc_shifts[3]')	

	print 'plotTreeName: '+plotTreeName
	print 'Flavour: '+isEM+' #tag: '+tag+' #algo: '+algo
	print "Weights:",weightStr
	print 'Cuts: '+fullcut

	# Declare histograms --- COMMENTS FOR UNCERTAINTIES NOT BEING RUN YET
	hists = {}
	hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		#hists[iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#hists[iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		# hists[iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		# hists[iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		# hists[iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		# hists[iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#hists[iPlot+'btagUp_'       +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagUp_'       +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#hists[iPlot+'btagDown_'     +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagDown_'     +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#hists[iPlot+'mistagUp_'     +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'mistagUp_'     +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#hists[iPlot+'mistagDown_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'mistagDown_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			
		#if tTree[process+'jerUp']: 
		#	hists[iPlot+'jerUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#	hists[iPlot+'jerDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#if tTree[process+'jecUp']:
		#	hists[iPlot+'jecUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#	hists[iPlot+'jecDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#for i in range(100): hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[process].Draw(plotTreeName+' >> '+iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
	if doAllSys:
		#tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffUpStr+'*('+fullcut+')', 'GOFF')
		#tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process, weightPileupUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process, weightPileupDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdUpStr  +'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdDownStr+'*('+fullcut+')', 'GOFF')
		# tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuRUpStr+'*('+fullcut+')', 'GOFF')
		# tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuRDownStr+'*('+fullcut+')', 'GOFF')
		# tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuFUpStr+'*('+fullcut+')', 'GOFF')
		# tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuFDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process, weighttopptUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process, weighttopptDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightjsfUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightjsfDownStr+'*('+fullcut+')', 'GOFF')

		# Change the plot name itself for shifts if needed
		# BTAGupName = plotTreeName.replace('_lepBJets','_bSFup_lepBJets')
		# BTAGdnName = plotTreeName.replace('_lepBJets','_bSFdn_lepBJets')
		# MISTAGupName = plotTreeName.replace('_lepBJets','_lSFup_lepBJets')
		# MISTAGdnName = plotTreeName.replace('_lepBJets','_lSFdn_lepBJets')
		# if 'CSVwithSF' in BTAGupName or 'btagged' in BTAGupName or 'MleppB' in BTAGupName or 'BJetLead' in BTAGupName or 'minMlb' in BTAGupName or 'notH' in BTAGupName or 'notPH' in BTAGupName:
		# 	BTAGupName = BTAGupName+'_shifts[0]'
		# 	BTAGdnName = BTAGdnName+'_shifts[1]'
		# 	MISTAGupName = MISTAGupName+'_shifts[2]'
		# 	MISTAGdnName = MISTAGdnName+'_shifts[3]'
		# print 'BTAG SHIFT LJMET NAMES',BTAGupName,BTAGdnName,MISTAGupName,MISTAGdnName
		# tTree[process].Draw(BTAGupName+' >> '+iPlot+'btagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagUp+')', 'GOFF')
		# tTree[process].Draw(BTAGdnName+' >> '+iPlot+'btagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagDn+')', 'GOFF')
		# tTree[process].Draw(MISTAGupName+' >> '+iPlot+'mistagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagUp+')', 'GOFF')
		# tTree[process].Draw(MISTAGdnName+' >> '+iPlot+'mistagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagDn+')', 'GOFF')

		# if tTree[process+'jecUp']:
		# 	tTree[process+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		# 	tTree[process+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		# if tTree[process+'jerUp']:
		# 	tTree[process+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		# 	tTree[process+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		# for i in range(100): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+fullcut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
