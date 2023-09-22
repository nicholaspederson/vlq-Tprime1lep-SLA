#!/usr/bin/python
from ROOT import TH1D,TTree,TFile
from array import array
from numpy import linspace
from samples import *
import math

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
def analyze(tTree,sample,doAllSys,iPlot,plotDetails,category,region,isCategorized):
        plotTreeName=plotDetails[0]
	xbins=array('d', plotDetails[1])
	xAxisLabel=plotDetails[2]
        
	# Define categories
	isEM  = category['isEM']
	tag   = category['tag']
	catStr = 'is'+isEM+'_'+tag

	# Define general cuts (These are the only cuts for 'PS')
	cut  = ''

        if region == 'BAX': cut += ' && NJets_forward == 0'                
	elif region == 'DCY': cut += ' && NJets_forward > 0'
        elif region == 'B': cut += ' && NJets_forward == 0 && NJets_central_DeepFlavL < 3'
        elif region == 'A': cut += ' && NJets_forward == 0 && NJets_central_DeepFlavL == 3'
        elif region == 'X': cut += ' && NJets_forward == 0 && NJets_central_DeepFlavL > 3'
        elif region == 'D': cut += ' && NJets_forward > 0 && NJets_central_DeepFlavL < 3'
        elif region == 'C': cut += ' && NJets_forward > 0 && NJets_central_DeepFlavL == 3'
        elif region == 'Y': cut += ' && NJets_forward > 0 && NJets_central_DeepFlavL > 3'

	# Define weights
        topCorr      = '1'
        jetSFstr     = '1'
	if ('WJetsHT' in sample.prefix):
		jetSFstr = 'gcHTCorr_WjetLHE[0]'
		jetSFstrUp = 'gcHTCorr_WjetLHE[1]'
		jetSFstrDn = 'gcHTCorr_WjetLHE[2]'
        if 'TTTo' in sample.prefix or 'TTMT' in sample.prefix:
                topCorr = 'gcHTCorr_top[0]'
                topCorrUp = 'gcHTCorr_top[1]'
                topCorrDn = 'gcHTCorr_top[2]'

	weightStr = '1'
	if 'Single' not in sample.prefix: 
                weightStr += ' * '+jetSFstr+' * '+topCorr+' * PileupWeights[0] * leptonHLTSF[0] * leptonIDSF[0] * leptonIsoSF[0] * leptonRecoSF[0] * btagWeights[0] * '+str(targetlumi[sample.year]*sample.xsec/sample.nrun)+' * (genWeight/abs(genWeight))'

		weightelRecoSFUpStr  = weightStr.replace('leptonRecoSF[0]','(isMu*leptonRecoSF[0]+isEl*leptonRecoSF[1])')
                weightelRecoSFDnStr= weightStr.replace('leptonRecoSF[0]','(isMu*leptonRecoSF[0]+isEl*leptonRecoSF[2])')
		weightmuRecoSFUpStr  = weightStr.replace('leptonRecoSF[0]','(isMu*leptonRecoSF[1]+isEl*leptonRecoSF[0])')
                weightmuRecoSFDnStr= weightStr.replace('leptonRecoSF[0]','(isMu*leptonRecoSF[2]+isEl*leptonRecoSF[0])')
		weightelIdSFUpStr  = weightStr.replace('leptonIDSF[0]','(leptonHLTSF[0]+isEl*leptonHLFSF[1])')
                weightelIdSFDnStr= weightStr.replace('leptonIDSF[0]','(leptonHLTSF[0]-isEl*leptonHLFSF[1])')
		weightmuIdSFUpStr  = weightStr.replace('leptonIDSF[0]','(isEl*leptonHLTSF[0]+isMu*leptonHLFSF[1])')
                weightmuIdSFDnStr= weightStr.replace('leptonIDSF[0]','(isEl*leptonHLTSF[0]+isMu*leptonHLFSF[2])')
		weightelIsoSFUpStr  = weightStr.replace('leptonIsoSF[0]','(leptonIsoSF[0]+isEl*leptonIsoSF[1])')
                weightelIsoSFDnStr= weightStr.replace('leptonIsoSF[0]','(leptonIsoSF[0]-isEl*leptonIsoSF[1])')
		weightmuIsoSFUpStr  = weightStr.replace('leptonIsoSF[0]','(leptonIsoSF[0]+isMu*leptonIsoSF[1])')
                weightmuIsoSFDnStr= weightStr.replace('leptonIsoSF[0]','(leptonIsoSF[0]-isMu*leptonIsoSF[1])')
		weightTrigEffElUpStr  = weightStr.replace('leptonHLTSF[0]','(leptonIDSF[0]+isEl*leptonIDSF[1])')
                weightTrigEffElDnStr= weightStr.replace('leptonHLTSF[0]','(leptonIDSF[0]-isEl*leptonIDSF[1])')
		weightTrigEffMuUpStr  = weightStr.replace('leptonHLTSF[0]','(leptonIDSF[0]+isMu*leptonIDSF[1])')
		weightTrigEffMuDnStr= weightStr.replace('leptonHLTSF[0]','(leptonIDSF[0]-isMu*leptonIDSF[1])')
		weightPileupUpStr   = weightStr.replace('PileupWeights[0]','PileupWeights[1]')
		weightPileupDnStr   = weightStr.replace('PileupWeights[0]','PileupWeights[2]')
		weightBtagHFUpStr   = weightStr.replace('btagWeights[0]','btagWeights[1]')
		weightBtagHFDnStr   = weightStr.replace('btagWeights[0]','btagWeights[2]')
		weightBtagLFUpStr   = weightStr.replace('btagWeights[0]','btagWeights[3]')
		weightBtagLFDnStr   = weightStr.replace('btagWeights[0]','btagWeights[4]')
		weightBtagHFS1UpStr   = weightStr.replace('btagWeights[0]','btagWeights[5]')
		weightBtagHFS1DnStr   = weightStr.replace('btagWeights[0]','btagWeights[6]')
		weightBtagHFS2UpStr   = weightStr.replace('btagWeights[0]','btagWeights[7]')
		weightBtagHFS2DnStr   = weightStr.replace('btagWeights[0]','btagWeights[8]')
		weightBtagLFS1UpStr   = weightStr.replace('btagWeights[0]','btagWeights[9]')
		weightBtagLFS1DnStr   = weightStr.replace('btagWeights[0]','btagWeights[10]')
		weightBtagLFS2UpStr   = weightStr.replace('btagWeights[0]','btagWeights[11]')
		weightBtagLFS2DnStr   = weightStr.replace('btagWeights[0]','btagWeights[12]')
		weightBtagCFE1UpStr   = weightStr.replace('btagWeights[0]','btagWeights[13]')
		weightBtagCFE1DnStr   = weightStr.replace('btagWeights[0]','btagWeights[14]')
		weightBtagCFE2UpStr   = weightStr.replace('btagWeights[0]','btagWeights[15]')
		weightBtagCFE2DnStr   = weightStr.replace('btagWeights[0]','btagWeights[16]')
		weightmuRFcorrdUpStr   = 'LHEScaleWeight[8] * '+weightStr
		weightmuRFcorrdDnStr = 'LHEScaleWeight[0] * '+weightStr
		weightmuRUpStr      = 'LHEScaleWeight[7] * '+weightStr
		weightmuRDnStr    = 'LHEScaleWeight[1] * '+weightStr
		weightmuFUpStr      = 'LHEScaleWeight[5] * '+weightStr
		weightmuFDnStr    = 'LHEScaleWeight[3] * '+weightStr
		weighttopptUpStr    = weightStr.replace(topCorr,topCorrUp)
		weighttopptDnStr  = weightStr.replace(topCorr,topCorrDn)
		weightjsfUpStr      = weightStr.replace(jetSFstr,jetSFstrUp)
		weightjsfDnStr    = weightStr.replace(jetSFstr,jetSFstrDn)


        print "*****"*20
	print "*****"*20
	print "DISTRIBUTION:", iPlot
	print "            -name in ljmet trees:", plotTreeName
	print "            -x-axis label is set to:", xAxisLabel
	print "            -using the binning as:", xbins
       	print "/////"*5
	print "PROCESSING: ", sample.prefix
	print "/////"*5

	# Design the EM cuts for categories
        ## FIXME add "isHole" to RDF
	isEMCut=''
	if isEM=='E': isEMCut+=' && isEl==1'
	elif isEM=='M': isEMCut+=' && isMu==1'
	elif isEM=='L': isEMCut+=' && (isMu==1 || isEl==1)'
		
	# Design the tagging cuts for categories
	tagCut = ''
	if isCategorized:
		if tag == 'tagTjet': tagCut += ' && Bdecay_obs == 1'
		elif tag == 'tagWjet': tagCut += ' && Bdecay_obs == 2'
		elif tag == 'untagTlep': tagCut += ' && Bdecay_obs == 3'
		elif tag == 'untagWlep': tagCut += ' && Bdecay_obs == 4'
		elif tag == 'allWlep': tagCut += ' && (Bdecay_obs == 4 || Bdecay_obs == 1)'
		elif tag == 'allTlep': tagCut += ' && (Bdecay_obs == 2 || Bdecay_obs == 3)'

		# signal categories for basic tag counts

                if '2pW' in tag: tagCut += ' && gcFatJet_nW >= 2'
		elif '2W' in tag: tagCut += ' && gcFatJet_nW == 2'
		elif '1pW' in tag: tagCut += ' && gcFatJet_nW >= 1'
		elif '1W' in tag: tagCut += ' && gcFatJet_nW == 1'
		elif '01W' in tag: tagCut += ' && gcFatJet_nW <= 1'
		elif '0W' in tag: tagCut += ' && gcFatJet_nW == 0'
		
		if '0T' in tag: tagCut += ' && gcFatJet_nT == 0'
		elif '01T' in tag: tagCut += ' && gcFatJet_nT <= 1'
		elif '1T' in tag: tagCut += ' && gcFatJet_nT == 1'
		elif '1pT' in tag: tagCut += ' && gcFatJet_nT >= 1'
		elif '2T' in tag: tagCut += ' && gcFatJet_nT == 2'
                elif '2pT' in tag: tagCut += ' && gcFatJet_nT >= 2'
	       	

	fullcut = cut+isEMCut+tagCut

	print 'plotTreeName: '+plotTreeName
	print 'Flavour: '+isEM+' #tag: '+tag+' #algo: '+algo
	print "Weights:",weightStr
	print 'Cuts: '+fullcut

	# Declare histograms --- COMMENTS FOR UNCERTAINTIES NOT BEING RUN YET
	hists = {}
        process = sample.prefix
	hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		hists[iPlot+'elIdSFUp_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'elIdSFUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'elIdSFDn_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'elIdSFDn_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muIdSFUp_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muIdSFUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muIdSFDn_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muIdSFDn_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'elIsoSFUp_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'elIsoSFUp_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'elIsoSFDn_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'elIsoSFDn_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muIsoSFUp_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muIsoSFUp_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muIsoSFDn_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muIsoSFDn_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'elRecoSFUp_' +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'elRecoSFUp_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'elRecoSFDn_' +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'elRecoSFDn_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRecoSFUp_' +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRecoSFUp_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRecoSFDn_' +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRecoSFDn_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'trigeffElUp_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffElUp_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'trigeffElDn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffElDn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[iPlot+'trigeffMuUp_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffMuUp_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[iPlot+'trigeffMuDn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffMuDn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'pileupUp_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'pileupDn_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupDn_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdUp_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdUp_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdDn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdDn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topptUp_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptUp_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topptDn_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptDn_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfUp_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfUp_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfDn_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfDn_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'btagHFUp_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagHFUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'btagHFDn_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagHFDn_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'btagLFUp_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagLFUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'btagLFDn_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagLFDn_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			
		if process+'jerUp' in tTree: 
			hists[iPlot+'jerUp_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerUp_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'jerDn_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerDn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if process+'jecUp' in tTree:
			hists[iPlot+'jecUp_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecUp_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'jecDn_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecDn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)

		if isCategorized:
                        hists[iPlot+'btagHFS1Up_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagHFS1Up_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagHFS1Dn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagHFS1Dn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagHFS2Up_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagHFS2Up_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagHFS2Dn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagHFS2Dn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagLFS1Up_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagLFS1Up_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagLFS1Dn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagLFS1Dn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagLFS2Up_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagLFS2Up_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagLFS2Dn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagLFS2Dn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagCFE1Up_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagCFE1Up_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagCFE1Dn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagCFE1Dn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagCFE2Up_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagCFE2Up_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        hists[iPlot+'btagCFE2Dn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagCFE2Dn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muRUp_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRUp_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muRDn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRDn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muFUp_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFUp_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muFDn_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFDn_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                        for i in range(1,100): hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[process].Draw(plotTreeName+' >> '+iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
	print 'Nominal hist integral: ',hists[iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process].Integral()
	if doAllSys:
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'elIdSFUp_'   +lumiStr+'fb_'+catStr+'_'+process, weightelIdSFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'elIdSFDn_'   +lumiStr+'fb_'+catStr+'_'+process, weightelIdSFDnStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'elIsoSFUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightelIsoSFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'elIsoSFDn_'  +lumiStr+'fb_'+catStr+'_'+process, weightelIsoSFDnStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'elRecoSFUp_' +lumiStr+'fb_'+catStr+'_'+process, weightelRecoSFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'elRecoSFDn_' +lumiStr+'fb_'+catStr+'_'+process, weightelRecoSFDnStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffElUp_'+lumiStr+'fb_'+catStr+'_'+process, weightTrigEffElUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffElDn_'+lumiStr+'fb_'+catStr+'_'+process, weightTrigEffElDnStr+'*('+fullcut+')', 'GOFF')
                tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffMuUp_'+lumiStr+'fb_'+catStr+'_'+process, weightTrigEffMuUpStr+'*('+fullcut+')', 'GOFF')
                tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffMuDn_'+lumiStr+'fb_'+catStr+'_'+process, weightTrigEffMuDnStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupUp_'   +lumiStr+'fb_'+catStr+'_'+process, weightPileupUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupDn_'   +lumiStr+'fb_'+catStr+'_'+process, weightPileupDnStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdUp_'+lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdUpStr  +'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdDn_'+lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdDnStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptUp_'    +lumiStr+'fb_'+catStr+'_'+process, weighttopptUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptDn_'    +lumiStr+'fb_'+catStr+'_'+process, weighttopptDnStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfUp_'      +lumiStr+'fb_'+catStr+'_'+process, weightjsfUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfDn_'      +lumiStr+'fb_'+catStr+'_'+process, weightjsfDnStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagHFUp_'   +lumiStr+'fb_'+catStr+'_'+process, weightBtagHFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagHFDn_'   +lumiStr+'fb_'+catStr+'_'+process, weightBtagHFDnStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagLFUp_'   +lumiStr+'fb_'+catStr+'_'+process, weightBtagLFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagLFDn_'   +lumiStr+'fb_'+catStr+'_'+process, weightBtagLFDnStr+'*('+fullcut+')', 'GOFF')
		if process+'jecUp' in tTree:
			tTree[process+'jecUp'].Draw(plotTreeName+' >> '+iPlot+'jecUp_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jecDn'].Draw(plotTreeName+' >> '+iPlot+'jecDn_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if process+'jerUp' in tTree:
			tTree[process+'jerUp'].Draw(plotTreeName+' >> '+iPlot+'jerUp_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jerDn'].Draw(plotTreeName+' >> '+iPlot+'jerDn_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')

		if isCategorized:
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagHFS1Up_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagHFS1UpStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagHFS1Dn_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagHFS1DnStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagHFS2Up_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagHFS2UpStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagHFS2Dn_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagHFS2DnStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagLFS1Up_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagLFS1UpStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagLFS1Dn_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagLFS1DnStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagLFS2Up_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagLFS2UpStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagLFS2Dn_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagLFS2DnStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagCFE1Up_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagCFE1UpStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagCFE1Dn_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagCFE1DnStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagCFE2Up_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagCFE2UpStr+'*('+fullcut+')', 'GOFF')
                        tTree[process].Draw(plotTreeName+' >> '+iPlot+'btagCFE2Dn_'+lumiStr+'fb_'+catStr+'_'+process, weightBtagCFE2DnStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRUp_'     +lumiStr+'fb_'+catStr+'_'+process, weightmuRUpStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRDn_'     +lumiStr+'fb_'+catStr+'_'+process, weightmuRDnStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFUp_'     +lumiStr+'fb_'+catStr+'_'+process, weightmuFUpStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFDn_'     +lumiStr+'fb_'+catStr+'_'+process, weightmuFDnStr+'*('+fullcut+')', 'GOFF')
                        for i in range(1,100): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, '(LHEPdfWeight['+str(i)+']) * '+weightStr+'*('+fullcut+')', 'GOFF')	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
