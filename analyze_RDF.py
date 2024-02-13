#!/usr/bin/python
from ROOT import TH1D,TTree,TFile,RDataFrame,TH1,EnableImplicitMT
from array import array
from numpy import linspace
from weights import *
from dnnJcorrSF import *
import math,time

TH1.SetDefaultSumw2(True)
EnableImplicitMT()

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

def analyze(tTree,sample,doAllSys,iPlot,plotDetails,category,region,isCategorized):
        start_time = time.time()
        plotTreeName=plotDetails[0]
        xbins=array('d', plotDetails[1])
        xAxisLabel=plotDetails[2]
        
	# Define categories
        isEM  = category['isEM']
        tag   = category['tag']
        catStr = 'is'+isEM+'_'+tag

	# Define weights
        topCorr      = '1'
        topCorrUp      = '1'
        topCorrDn      = '1'
        jetSFstr     = '1'
        jetSFstrUp     = '1'
        jetSFstrDn     = '1'
        if ('WJetsHT' in sample.prefix):
                jetSFstr = 'gcHTCorr_WjetLHE[0]' # 
                jetSFstrUp = 'gcHTCorr_WjetLHE[1]' #
                jetSFstrDn = 'gcHTCorr_WjetLHE[2]' #
        if 'TTTo' in sample.prefix or 'TTMT' in sample.prefix:
                topCorr = 'gcHTCorr_top[0]'
                topCorrUp = 'gcHTCorr_top[1]'
                topCorrDn = 'gcHTCorr_top[2]'

        weightStr = '1'
        doMuRF = True
        if (sample.prefix).find('WW') == 0 or (sample.prefix).find('WZ') == 0 or (sample.prefix).find('ZZ') == 0:
                doMuRF = False
                
        if 'Single' not in sample.prefix: 
                weightStr += ' * '+jetSFstr+' * '+topCorr+' * PileupWeights[0] * leptonIDSF[0] * leptonRecoSF[0] * leptonIsoSF[0] * leptonHLTSF[0] * btagWeights[17] *'+str(targetlumi[sample.year]*sample.xsec/sample.nrun)+' * (genWeight/abs(genWeight))'

                weightelRecoSFUpStr  = weightStr.replace('leptonRecoSF[0]','(isMu*leptonRecoSF[0]+isEl*leptonRecoSF[1])')
                weightelRecoSFDnStr= weightStr.replace('leptonRecoSF[0]','(isMu*leptonRecoSF[0]+isEl*leptonRecoSF[2])')
                weightmuRecoSFUpStr  = weightStr.replace('leptonRecoSF[0]','(isMu*leptonRecoSF[1]+isEl*leptonRecoSF[0])')
                weightmuRecoSFDnStr= weightStr.replace('leptonRecoSF[0]','(isMu*leptonRecoSF[2]+isEl*leptonRecoSF[0])')
                weightelIdSFUpStr  = weightStr.replace('leptonIDSF[0]','(leptonHLTSF[0]+isEl*leptonHLTSF[1])')
                weightelIdSFDnStr= weightStr.replace('leptonIDSF[0]','(leptonHLTSF[0]-isEl*leptonHLTSF[1])')
                weightmuIdSFUpStr  = weightStr.replace('leptonIDSF[0]','(isEl*leptonHLTSF[0]+isMu*leptonHLTSF[1])')
                weightmuIdSFDnStr= weightStr.replace('leptonIDSF[0]','(isEl*leptonHLTSF[0]+isMu*leptonHLTSF[2])')
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
                weightBtagHFCOUpStr   = weightStr.replace('btagWeights[17]','btagWeights[18]')
                weightBtagHFCODnStr   = weightStr.replace('btagWeights[17]','btagWeights[19]')
                weightBtagHFUCUpStr   = weightStr.replace('btagWeights[17]','btagWeights[20]')
                weightBtagHFUCDnStr   = weightStr.replace('btagWeights[17]','btagWeights[21]')
                weightBtagLFCOUpStr   = weightStr.replace('btagWeights[17]','btagWeights[22]')
                weightBtagLFCODnStr   = weightStr.replace('btagWeights[17]','btagWeights[23]')
                weightBtagLFUCUpStr   = weightStr.replace('btagWeights[17]','btagWeights[24]')
                weightBtagLFUCDnStr   = weightStr.replace('btagWeights[17]','btagWeights[25]')
                ### These weights are here in case we ever switch back to btag shape-reweighting scale factors
                # weightBtagHFUpStr   = weightStr.replace('btagWeights[0]','btagWeights[1]')
                # weightBtagHFDnStr   = weightStr.replace('btagWeights[0]','btagWeights[2]')
                # weightBtagLFUpStr   = weightStr.replace('btagWeights[0]','btagWeights[3]')
                # weightBtagLFDnStr   = weightStr.replace('btagWeights[0]','btagWeights[4]')
                # weightBtagHFS1UpStr   = weightStr.replace('btagWeights[0]','btagWeights[5]')
                # weightBtagHFS1DnStr   = weightStr.replace('btagWeights[0]','btagWeights[6]')
                # weightBtagHFS2UpStr   = weightStr.replace('btagWeights[0]','btagWeights[7]')
                # weightBtagHFS2DnStr   = weightStr.replace('btagWeights[0]','btagWeights[8]')
                # weightBtagLFS1UpStr   = weightStr.replace('btagWeights[0]','btagWeights[9]')
                # weightBtagLFS1DnStr   = weightStr.replace('btagWeights[0]','btagWeights[10]')
                # weightBtagLFS2UpStr   = weightStr.replace('btagWeights[0]','btagWeights[11]')
                # weightBtagLFS2DnStr   = weightStr.replace('btagWeights[0]','btagWeights[12]')
                # weightBtagCFE1UpStr   = weightStr.replace('btagWeights[0]','btagWeights[13]')
                # weightBtagCFE1DnStr   = weightStr.replace('btagWeights[0]','btagWeights[14]')
                # weightBtagCFE2UpStr   = weightStr.replace('btagWeights[0]','btagWeights[15]')
                # weightBtagCFE2DnStr   = weightStr.replace('btagWeights[0]','btagWeights[16]')
                if doMuRF:
                        weightmuRFcorrdUpStr = 'LHEScaleWeight[8] * '+weightStr
                        weightmuRFcorrdDnStr = 'LHEScaleWeight[0] * '+weightStr
                        weightmuRUpStr       = 'LHEScaleWeight[7] * '+weightStr
                        weightmuRDnStr       = 'LHEScaleWeight[1] * '+weightStr
                        weightmuFUpStr       = 'LHEScaleWeight[5] * '+weightStr
                        weightmuFDnStr       = 'LHEScaleWeight[3] * '+weightStr
                else:
                        weightmuRFcorrdUpStr = '1.15 * '+weightStr
                        weightmuRFcorrdDnStr = '0.85 * '+weightStr
                        weightmuRUpStr       = weightStr
                        weightmuRDnStr       = weightStr
                        weightmuFUpStr       = weightStr
                        weightmuFDnStr       = weightStr
                weighttopptUpStr             = weightStr.replace(topCorr,topCorrUp)
                weighttopptDnStr             = weightStr.replace(topCorr,topCorrDn)
                weightjsfUpStr               = weightStr.replace(jetSFstr,jetSFstrUp)
                weightjsfDnStr               = weightStr.replace(jetSFstr,jetSFstrDn)


        print("*****"*20)
        print("PROCESSING:  "+sample.prefix)

	# Design the EM cuts for categories -- THIS WILL BE THE FIRST CUT
        isEMCut=''
        if isEM=='E': 
                isEMCut+='isEl==1'
        elif isEM=='M': 
                isEMCut+='isMu==1'
        elif isEM=='L': 
                isEMCut+='(isMu==1 || isEl==1)'
        if 'SingleMuon' in sample.prefix: # don't let data double count
                isEMCut+=' && isMu==1'
        elif 'SingleElec' in sample.prefix:
                isEMCut+=' && isEl==1'
		
	# Define cuts by region. Use region "all" for all selected events
        cut  = ' && W_MT < 160'
        #if 'lowMT' in region:
        #        cut += ' && W_MT < 160'
        if region == 'isoVT':
                cut += ' && lepton_miniIso < 0.05'
        if '1pb' in region: 
                cut += ' && NJets_DeepFlavL > 0'
        elif '2pb' in region: 
                cut += ' && NJets_DeepFlavL > 1'
        elif '0b' in region: 
                cut += ' && NJets_DeepFlavL == 0'
        if region == 'BAX': 
                cut += ' && NJets_forward == 0'                
        elif region == 'DCY': 
                cut += ' && NJets_forward > 0'
        elif region == 'B': 
                cut += ' && NJets_forward == 0 && NJets_DeepFlavL < 3'
        elif region == 'A': 
                cut += ' && NJets_forward == 0 && NJets_DeepFlavL == 3'
        elif region == 'X': 
                cut += ' && NJets_forward == 0 && NJets_DeepFlavL > 3'
        elif region == 'D': 
                cut += ' && NJets_forward > 0 && NJets_DeepFlavL < 3'
        elif region == 'C': 
                cut += ' && NJets_forward > 0 && NJets_DeepFlavL == 3'
        elif region == 'Y': 
                cut += ' && NJets_forward > 0 && NJets_DeepFlavL > 3'

        # Separate ttbar into mass bins for proper normalization 
        if 'TTTo' in sample.prefix:
                if sample.prefix[-4:] == "1000": 
                        cut += ' && genttbarMass > 1000'
                elif sample.prefix[-3:] == "700": 
                        cut += ' && genttbarMass > 700 && genttbarMass <= 1000'
                elif sample.prefix[-1] == "0": 
                        cut += ' && genttbarMass <= 700'

	# Design the tagging cuts for categories
        tagCut = ''
        if isCategorized:
                if tag == 'tagTjet': 
                        tagCut += ' && Bdecay_obs == 1'
                elif tag == 'tagWjet': 
                        tagCut += ' && Bdecay_obs == 2'
                elif tag == 'untagTlep': 
                        tagCut += ' && Bdecay_obs == 3'
                elif tag == 'untagWlep': 
                        tagCut += ' && Bdecay_obs == 4'
                elif tag == 'allWlep': 
                        tagCut += ' && (Bdecay_obs == 4 || Bdecay_obs == 1)'
                elif tag == 'allTlep': 
                        tagCut += ' && (Bdecay_obs == 2 || Bdecay_obs == 3)'

		# signal categories for basic tag counts

                if '2pW' in tag: 
                        tagCut += ' && gcFatJet_nW >= 2'
                elif '2W' in tag: 
                        tagCut += ' && gcFatJet_nW == 2'
                elif '1pW' in tag: 
                        tagCut += ' && gcFatJet_nW >= 1'
                elif '1W' in tag: 
                        tagCut += ' && gcFatJet_nW == 1'
                elif '01W' in tag: 
                        tagCut += ' && gcFatJet_nW <= 1'
                elif '0W' in tag: 
                        tagCut += ' && gcFatJet_nW == 0'		
                if '0T' in tag: 
                        tagCut += ' && gcFatJet_nT == 0'
                elif '01T' in tag: 
                        tagCut += ' && gcFatJet_nT <= 1'
                elif '1T' in tag: 
                        tagCut += ' && gcFatJet_nT == 1'
                elif '1pT' in tag: 
                        tagCut += ' && gcFatJet_nT >= 1'
                elif '2T' in tag: 
                        tagCut += ' && gcFatJet_nT == 2'
                elif '2pT' in tag: 
                        tagCut += ' && gcFatJet_nT >= 2'
	       	

        fullcut = isEMCut+cut+tagCut

        print('plotTreeName: '+plotTreeName)
        print('Flavour: '+isEM+', tag: '+tag)
        print("Weights: "+weightStr)
        print('Cuts: '+fullcut)

	# Declare histograms --- COMMENTS FOR UNCERTAINTIES NOT BEING RUN YET
	histptrs = {}
        hists = {}
        process = sample.prefix
        df = RDataFrame(tTree[process]) 

        try:
                sel = df.Filter(fullcut).Define('weight',weightStr)
        except:
                print 'No dataframe built!!'
                return hists
        if doAllSys and 'Single' not in process:
                try:
                        selMC = df.Filter(fullcut)\
                                  .Define('weight',weightStr)\
                                  .Define('weightelRecoSFUp' ,weightelRecoSFUpStr)\
                                  .Define('weightelRecoSFDn' ,weightelRecoSFDnStr)\
                                  .Define('weightelIdSFUp'   ,weightelIdSFUpStr)\
                                  .Define('weightelIdSFDn'   ,weightelIdSFDnStr)\
                                  .Define('weightelIsoSFUp'  ,weightelIsoSFUpStr)\
                                  .Define('weightelIsoSFDn'  ,weightelIsoSFDnStr)\
                                  .Define('weighttrigeffElUp',weightTrigEffElUpStr)\
                                  .Define('weighttrigeffElDn',weightTrigEffElDnStr)\
                                  .Define('weightmuRecoSFUp' ,weightmuRecoSFUpStr)\
                                  .Define('weightmuRecoSFDn' ,weightmuRecoSFDnStr)\
                                  .Define('weightmuIdSFUp'   ,weightmuIdSFUpStr)\
                                  .Define('weightmuIdSFDn'   ,weightmuIdSFDnStr)\
                                  .Define('weightmuIsoSFUp'  ,weightmuIsoSFUpStr)\
                                  .Define('weightmuIsoSFDn'  ,weightmuIsoSFDnStr)\
                                  .Define('weighttrigeffMuUp',weightTrigEffMuUpStr)\
                                  .Define('weighttrigeffMuDn',weightTrigEffMuDnStr)\
                                  .Define('weightpileupUp'   ,weightPileupUpStr)\
                                  .Define('weightpileupDn'   ,weightPileupDnStr)\
                                  .Define('weightjsfUp'      ,weightjsfUpStr)\
                                  .Define('weightjsfDn'      ,weightjsfDnStr)\
                                  .Define('weighttopptUp'    ,weighttopptUpStr)\
                                  .Define('weighttopptDn'    ,weighttopptDnStr)\
                                  .Define('weightmuRFcorrdUp',weightmuRFcorrdUpStr)\
                                  .Define('weightmuRFcorrdDn',weightmuRFcorrdDnStr)\
                                  .Define('weightmuRUp'      ,weightmuRUpStr)\
                                  .Define('weightmuRDn'      ,weightmuRDnStr)\
                                  .Define('weightmuFUp'      ,weightmuFUpStr)\
                                  .Define('weightmuFDn'      ,weightmuFDnStr)
                                  .Define('weightbtagHFCOUp' ,weightBtagHFCOUpStr)\
                                  .Define('weightbtagHFCODn' ,weightBtagHFCODnStr)\
                                  .Define('weightbtagHFUCUp' ,weightBtagHFUCUpStr)\
                                  .Define('weightbtagHFUCDn' ,weightBtagHFUCDnStr)\
                                  .Define('weightbtagLFCOUp' ,weightBtagLFCOUpStr)\
                                  .Define('weightbtagLFCODn' ,weightBtagLFCODnStr)\
                                  .Define('weightbtagLFUCUp' ,weightBtagLFUCUpStr)\
                                  .Define('weightbtagLFUCDn' ,weightBtagLFUCDnStr)\
                except:
                        print 'No dataframe built!!'
                        return hists

        histptrs[iPlot+'_'+lumicatproc] = sel.Histo1D((iPlot+'_'+lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')
        if doAllSys and 'Single' not in process:
		histptrs[iPlot+'elIdSFUp_'     +lumicatproc] = selMC.Histo1D((iPlot+'elIdSFUp_'     +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightelIdSFUp'     )
		histptrs[iPlot+'elIdSFDown_'   +lumicatproc] = selMC.Histo1D((iPlot+'elIdSFDown_'   +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightelIdSFDown'   )
		histptrs[iPlot+'trigeffElUp_'  +lumicatproc] = selMC.Histo1D((iPlot+'trigeffElUp_'  +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weighttrigeffElUp'  )
		histptrs[iPlot+'trigeffElDown_'+lumicatproc] = selMC.Histo1D((iPlot+'trigeffElDown_'+lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weighttrigeffElDown')
                histptrs[iPlot+'trigeffMuUp_'  +lumicatproc] = selMC.Histo1D((iPlot+'trigeffMuUp_'  +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weighttrigeffMuUp'  )
                histptrs[iPlot+'trigeffMuDown_'+lumicatproc] = selMC.Histo1D((iPlot+'trigeffMuDown_'+lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weighttrigeffMuDown')
		histptrs[iPlot+'pileupUp_'     +lumicatproc] = selMC.Histo1D((iPlot+'pileupUp_'     +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightpileupUp'     )
		histptrs[iPlot+'pileupDown_'   +lumicatproc] = selMC.Histo1D((iPlot+'pileupDown_'   +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightpileupDown'   )
		histptrs[iPlot+'muRFcorrdUp_'  +lumicatproc] = selMC.Histo1D((iPlot+'muRFcorrdUp_'  +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRFcorrdUp'  )
		histptrs[iPlot+'muRFcorrdDown_'+lumicatproc] = selMC.Histo1D((iPlot+'muRFcorrdDown_'+lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRFcorrdDown')
		histptrs[iPlot+'topptUp_'      +lumicatproc] = selMC.Histo1D((iPlot+'topptUp_'      +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weighttopptUp'      )
		histptrs[iPlot+'topptDown_'    +lumicatproc] = selMC.Histo1D((iPlot+'topptDown_'    +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weighttopptDown'    )
		histptrs[iPlot+'jsfUp_'+lumicatproc]    = selMC.Histo1D((iPlot+'jsfUp_'   +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightjsfUp'   )
		histptrs[iPlot+'jsfDown_'+lumicatproc]  = selMC.Histo1D((iPlot+'jsfDown_' +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightjsfDown' )
                ## TO-DO: expand this to get the other lepton and btagging weights in!
			
		if process+'jerUp' in tTree: 
                        dfjerUp = RDataFrame(tTree[process+'jerUp'])
                        seljerUp = dfjerUp.Filter(fullcut).Define('weight',weightStr)
                        dfjerDown = RDataFrame(tTree[process+'jerDown'])
                        seljerDown = dfjerDown.Filter(fullcut).Define('weight',weightStr)
			histptrs[iPlot+'jerUp_'   +lumicatproc] = seljerUp.Histo1D((iPlot+'jerUp_'    +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')
			histptrs[iPlot+'jerDown_' +lumicatproc] = seljerDown.Histo1D((iPlot+'jerDown_'  +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')
		if process+'jecUp' in tTree:                                                                                                                            
                        dfjecUp = RDataFrame(tTree[process+'jecUp'])
                        seljecUp = dfjecUp.Filter(fullcut).Define('weight',weightStr)
                        dfjecDown = RDataFrame(tTree[process+'jecDown'])
                        seljecDown = dfjecDown.Filter(fullcut).Define('weight',weightStr)
			histptrs[iPlot+'jecUp_'   +lumicatproc] = seljecUp.Histo1D((iPlot+'jecUp_'    +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')
			histptrs[iPlot+'jecDown_' +lumicatproc] = seljecDown.Histo1D((iPlot+'jecDown_'  +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')

		if isCategorized:
			histptrs[iPlot+'muRUp_'   +lumicatproc] = selMC.Histo1D((iPlot+'muRUp_'  +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRUp')
			histptrs[iPlot+'muRDown_' +lumicatproc] = selMC.Histo1D((iPlot+'muRDown_'+lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRDown')
			histptrs[iPlot+'muFUp_'   +lumicatproc] = selMC.Histo1D((iPlot+'muFUp_'  +lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightFUp')
			histptrs[iPlot+'muFDown_' +lumicatproc] = selMC.Histo1D((iPlot+'muFDown_'+lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightFDown')

                        ### TO-DO: check how many PDF variations live in NanoAOD, find branch names and get this segment set up correctly
                        # for i in range(100): histptrs[iPlot+'pdf'+str(i)+'_'+lumicatproc] = selMC.Define('weightpdf'+str(i),weightStr+'*pdfWeights['+str(i)+']').Histo1D((iPlot+'pdf'+str(i)+'_'+lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightpdf'+str(i))
                                

        ### THIS SEEMS TO BE THE SLOW PART. Can we just return the dictionary called "histptrs" to the main script? (doHists.py)
        ### The main function will save the dictionaries to pickle files -- should we rather have it .Write() all the elements of histptrs to a ROOT file? 
        ### Should be straightforward to change the doTemplates.py script to open a ROOT file and .Get histograms rather than pickle.load() a .p file and 
        ### access histograms by name from a list.... Could be 1 ROOT per plot per sample...but ideally 1 ROOT for bkg, for sig, for data as done currently.
        ###
        ### The "Sumw2()" here might not be meaningful with RDataFrame...we usually called it on the empty TH1D before doing TTree->Draw()
        ### The "SetDirectory(0)" was needed so that the file could be closed without losing histogram contents. Can it be called on the histptr? Is it needed? 
        for key in histptrs.keys():
                hists[key] = histptrs[key].GetValue()
                hists[key].SetDirectory(0)

        print("--- Analyze: %s minutes ---" % (round((time.time() - start_time)/60,2)))

	return hists
