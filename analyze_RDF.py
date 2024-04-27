#!/usr/bin/python
from ROOT import TH1D,TTree,TFile,RDataFrame,TH1,EnableImplicitMT,DisableImplicitMT
from array import array
from numpy import linspace
from samples import targetlumi, lumiStr
import math,time

TH1.SetDefaultSumw2(True)
EnableImplicitMT()

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

def analyze(tTree,sample,doAllSys,iPlot,plotDetails,category,region,isCategorized, outHistFile, doABCDnn):
        start_time = time.time()
        plotTreeName=plotDetails[0]
        xbins=array('d', plotDetails[1])
        xAxisLabel=plotDetails[2]
        
 # Define categories
        isEM  = category['isEM']
        tag   = category['tag']
        catStr = 'is'+isEM+'_'+tag
        if isCategorized: catStr += '_'+region
        
 # Define weights
        topCorr     = '1'
        topCorrUp   = '1'
        topCorrDn   = '1'
        jetSFstr    = '1'
        jetSFstrUp  = '1'
        jetSFstrDn  = '1'
        if ('WJetsHT' in sample.prefix):
                jetSFstr   = 'gcHTCorr_WjetLHE[0]' # 
                jetSFstrUp = 'gcHTCorr_WjetLHE[1]' #
                jetSFstrDn = 'gcHTCorr_WjetLHE[2]' #
        if 'TTTo' in sample.prefix or 'TTMT' in sample.prefix:
                topCorr   = 'gcHTCorr_top[0]'
                topCorrUp = 'gcHTCorr_top[1]'
                topCorrDn = 'gcHTCorr_top[2]'

        weightStr = '1'
        doMuRF = True
        if (sample.prefix).find('WW') == 0 or (sample.prefix).find('WZ') == 0 or (sample.prefix).find('ZZ') == 0:
                doMuRF = False

        if 'ABCDnn' in iPlot and not doABCDnn:
                plotTreeName = plotTreeName.split('_ABCDnn')[0]
        # else:
        #         plotTreeName = plotTreeName.split('_ABCDnn')[0] #TEMP # only when doing extended ABCDnn
        print(sample.prefix, plotTreeName)

        if 'Single' not in sample.prefix: 
                if doABCDnn:
                        weightStr += ' * transfer_ABCDnn'
                else:
                        weightStr += ' * '+jetSFstr+' * '+topCorr+' * PileupWeights[0] * L1PreFiringWeight_Nom * leptonIDSF[0] * leptonRecoSF[0] * leptonIsoSF[0] * leptonHLTSF[0] * btagWeights[17] *'+str(targetlumi[sample.year]*sample.xsec/sample.nrun)+' * (genWeight/abs(genWeight))'

                        weightPrefireUpStr = weightStr.replace('PreFiringWeight_Nom','PreFiringWeight_Up')
                        weightPrefireDnStr = weightStr.replace('PreFiringWeight_Nom','PreFiringWeight_Dn')
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
                                if 'Bprime' in sample.prefix: # signals don't have [4] being the 1,1 shift! [8] undefined
                                        weightmuRFcorrdUpStr = 'LHEScaleWeight[7] * '+weightStr
                                        weightmuRUpStr       = 'LHEScaleWeight[6] * '+weightStr
                                        weightmuFUpStr       = 'LHEScaleWeight[4] * '+weightStr
                                        
                        else:
                                weightmuRFcorrdUpStr = '1.15 * '+weightStr
                                weightmuRFcorrdDnStr = '0.85 * '+weightStr
                                weightmuRUpStr       = weightStr
                                weightmuRDnStr       = weightStr
                                weightmuFUpStr       = weightStr
                                weightmuFDnStr       = weightStr
                        weighttopptUpStr     = weightStr.replace(topCorr,topCorrUp)
                        weighttopptDnStr     = weightStr.replace(topCorr,topCorrDn)
                        weightjsfUpStr       = weightStr.replace(jetSFstr,jetSFstrUp)
                        weightjsfDnStr       = weightStr.replace(jetSFstr,jetSFstrDn)
                                

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
        cut  = ' && W_MT < 200' # TODO: 160 or 200
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
        if not doABCDnn:
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
        process = sample.prefix

        if '[0]' in plotTreeName: # TODO: this needs to be changed if ABCDnn variable contains [0]
                df = RDataFrame(tTree[process]).Filter(fullcut)\
                                               .Define('weight',weightStr)\
                                               .Define(iPlot, plotTreeName)
                plotTreeName = iPlot
        else:
                df = RDataFrame(tTree[process]).Filter(fullcut)\
                                               .Define('weight',weightStr)\

        hist = df.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_{process}',xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')             
        if 'Single' not in process and doAllSys:
                if doABCDnn:
                        hist_PEAKUP    = df.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_peakUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),f'{plotTreeName}_PEAKUP','weight')
                        hist_PEAKDN    = df.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_peakDn_{process}' ,xAxisLabel,len(xbins)-1,xbins),f'{plotTreeName}_PEAKDN','weight')
                        hist_TAILUP    = df.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_tailUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),f'{plotTreeName}_TAILUP','weight')
                        hist_TAILDN    = df.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_tailDn_{process}' ,xAxisLabel,len(xbins)-1,xbins),f'{plotTreeName}_TAILDN','weight')
                        hist_CLOSUREUP = df.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_closureUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),f'{plotTreeName}_CLOSUREUP','weight')
                        hist_CLOSUREDN = df.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_closureDn_{process}' ,xAxisLabel,len(xbins)-1,xbins),f'{plotTreeName}_CLOSUREDN','weight')
                else:
                        sel = df.Define('weightelRecoSFUp' ,weightelRecoSFUpStr)\
                                .Define('weightelRecoSFDn' ,weightelRecoSFDnStr)\
                                .Define('weightelIdSFUp'   ,weightelIdSFUpStr)\
                                .Define('weightelIdSFDn'   ,weightelIdSFDnStr)\
                                .Define('weightelIsoSFUp'  ,weightelIsoSFUpStr)\
                                .Define('weightelIsoSFDn'  ,weightelIsoSFDnStr)\
                                .Define('weightTrigEffElUp',weightTrigEffElUpStr)\
                                .Define('weightTrigEffElDn',weightTrigEffElDnStr)\
                                .Define('weightmuRecoSFUp' ,weightmuRecoSFUpStr)\
                                .Define('weightmuRecoSFDn' ,weightmuRecoSFDnStr)\
                                .Define('weightmuIdSFUp'   ,weightmuIdSFUpStr)\
                                .Define('weightmuIdSFDn'   ,weightmuIdSFDnStr)\
                                .Define('weightmuIsoSFUp'  ,weightmuIsoSFUpStr)\
                                .Define('weightmuIsoSFDn'  ,weightmuIsoSFDnStr)\
                                .Define('weightTrigEffMuUp',weightTrigEffMuUpStr)\
                                .Define('weightTrigEffMuDn',weightTrigEffMuDnStr)\
                                .Define('weightPileupUp'   ,weightPileupUpStr)\
                                .Define('weightPileupDn'   ,weightPileupDnStr)\
                                .Define('weightPrefireUp'  ,weightPrefireUpStr)\
                                .Define('weightPrefireDn'  ,weightPrefireDnStr)\
                                .Define('weightjsfUp'      ,weightjsfUpStr)\
                                .Define('weightjsfDn'      ,weightjsfDnStr)\
                                .Define('weighttopptUp'    ,weighttopptUpStr)\
                                .Define('weighttopptDn'    ,weighttopptDnStr)\
                                .Define('weightmuRFcorrdUp',weightmuRFcorrdUpStr)\
                                .Define('weightmuRFcorrdDn',weightmuRFcorrdDnStr)\
                                .Define('weightmuRUp'      ,weightmuRUpStr)\
                                .Define('weightmuRDn'      ,weightmuRDnStr)\
                                .Define('weightmuFUp'      ,weightmuFUpStr)\
                                .Define('weightmuFDn'      ,weightmuFDnStr)\
                                .Define('weightbtagHFCOUp' ,weightBtagHFCOUpStr)\
                                .Define('weightbtagHFCODn' ,weightBtagHFCODnStr)\
                                .Define('weightbtagHFUCUp' ,weightBtagHFUCUpStr)\
                                .Define('weightbtagHFUCDn' ,weightBtagHFUCDnStr)\
                                .Define('weightbtagLFCOUp' ,weightBtagLFCOUpStr)\
                                .Define('weightbtagLFCODn' ,weightBtagLFCODnStr)\
                                .Define('weightbtagLFUCUp' ,weightBtagLFUCUpStr)\
                                .Define('weightbtagLFUCDn' ,weightBtagLFUCDnStr)
                        
                        hist_elRecoSFUp  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_elRecoSFUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightelRecoSFUp' )
                        hist_elRecoSFDn  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_elRecoSFDn_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightelRecoSFDn' )
                        hist_elIdSFUp    = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_elIdSFUp_{process}'   ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightelIdSFUp'   )
                        hist_elIdSFDn    = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_elIdSFDn_{process}'   ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightelIdSFDn'   )
                        hist_elIsoSFUp   = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_elIsoSFUp_{process}'  ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightelIsoSFUp'  )
                        hist_elIsoSFDn   = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_elIsoSFDn_{process}'  ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightelIsoSFDn'  )
                        hist_TrigEffElUp = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_TrigEffElUp_{process}',xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightTrigEffElUp')
                        hist_TrigEffElDn = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_TrigEffElDn_{process}',xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightTrigEffElDn')
                        hist_muRecoSFUp  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muRecoSFUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRecoSFUp' )
                        hist_muRecoSFDn  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muRecoSFDn_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRecoSFDn' )
                        hist_muIdSFUp    = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muIdSFUp_{process}'   ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuIdSFUp'   )
                        hist_muIdSFDn    = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muIdSFDn_{process}'   ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuIdSFDn'   )
                        hist_muIsoSFUp   = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muIsoSFUp_{process}'  ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuIsoSFUp'  )
                        hist_muIsoSFDn   = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muIsoSFDn_{process}'  ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuIsoSFDn'  )
                        hist_TrigEffMuUp = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_TrigEffMuUp_{process}',xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightTrigEffMuUp')
                        hist_TrigEffMuDn = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_TrigEffMuDn_{process}',xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightTrigEffMuDn')
                        hist_PileupUp    = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_PileupUp_{process}'   ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightPileupUp'   )
                        hist_PileupDn    = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_PileupDn_{process}'   ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightPileupDn'   )
                        hist_PrefireUp   = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_PrefireUp_{process}'  ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightPrefireUp'  )
                        hist_PrefireDn   = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_PrefireDn_{process}'  ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightPrefireDn'  )
                        hist_jsfUp       = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_jsfUp_{process}'      ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightjsfUp'      )
                        hist_jsfDn       = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_jsfDn_{process}'      ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightjsfDn'      )
                        hist_topptUp     = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_topptUp_{process}'    ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weighttopptUp'    )
                        hist_topptDn     = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_topptDn_{process}'    ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weighttopptDn'    )
                        hist_muRFcorrdUp = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muRFcorrdUp_{process}',xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRFcorrdUp')
                        hist_muRFcorrdDn = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muRFcorrdDn_{process}',xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRFcorrdDn')
                        hist_muRUp       = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muRUp_{process}'      ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRUp'      )
                        hist_muRDn       = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muRDn_{process}'      ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuRDn'      )
                        hist_muFUp       = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muFUp_{process}'      ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuFUp'      )
                        hist_muFDn       = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_muFDn_{process}'      ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightmuFDn'      )
                        hist_btagHFCOUp  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_btagHFCOUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightbtagHFCOUp' )
                        hist_btagHFCODn  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_btagHFCODn_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightbtagHFCODn' )
                        hist_btagHFUCUp  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_btagHFUCUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightbtagHFUCUp' )
                        hist_btagHFUCDn  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_btagHFUCDn_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightbtagHFUCDn' )
                        hist_btagLFCOUp  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_btagLFCOUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightbtagLFCOUp' )
                        hist_btagLFCODn  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_btagLFCODn_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightbtagLFCODn' )
                        hist_btagLFUCUp  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_btagLFUCUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightbtagLFUCUp' )
                        hist_btagLFUCDn  = sel.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_btagLFUCDn_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightbtagLFUCDn' )

                        ## TO-DO: check tree names for jer and jec!
                        if process+'JERup' in tTree:
                                dfjerUp    = RDataFrame(tTree[process+'JERup'])
                                dfjerDn    = RDataFrame(tTree[process+'JERdn'])
                                if '[0]' in plotDetails[0]:
                                        seljerUp   = dfjerUp.Filter(fullcut).Define('weight',weightStr).Define(iPlot,plotDetails[0])
                                        seljerDn   = dfjerDn.Filter(fullcut).Define('weight',weightStr).Define(iPlot,plotDetails[0])
                                else:
                                        seljerUp   = dfjerUp.Filter(fullcut).Define('weight',weightStr)
                                        seljerDn   = dfjerDn.Filter(fullcut).Define('weight',weightStr)
                                hist_jerUp = seljerUp.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_jerUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')
                                hist_jerDn = seljerDn.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_jerDn_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')

                        if process+'JECup' in tTree:
                                dfjecUp    = RDataFrame(tTree[process+'JECup'])
                                dfjecDn    = RDataFrame(tTree[process+'JECdn'])
                                if '[0]' in plotDetails[0]:
                                        seljecUp   = dfjecUp.Filter(fullcut).Define('weight',weightStr).Define(iPlot,plotDetails[0])
                                        seljecDn   = dfjecDn.Filter(fullcut).Define('weight',weightStr).Define(iPlot,plotDetails[0])
                                else:
                                        seljecUp   = dfjecUp.Filter(fullcut).Define('weight',weightStr)
                                        seljecDn   = dfjecDn.Filter(fullcut).Define('weight',weightStr)
                                hist_jecUp = seljecUp.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_jecUp_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')
                                hist_jecDn = seljecDn.Histo1D((f'{iPlot}_{lumiStr}_{catStr}_jecDn_{process}' ,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weight')

                        ### TO-DO: check how many PDF variations live in NanoAOD, find branch names and get this segment set up correctly
                        # for i in range(100): histptrs[iPlot+'pdf'+str(i)+'_'+lumicatproc] = sel.Define('weightpdf'+str(i),weightStr+'*pdfWeights['+str(i)+']').Histo1D((iPlot+'pdf'+str(i)+'_'+lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightpdf'+str(i))

        # WRITE all the histograms (hopefully no event loop gets triggered until here?)
        hist.Write()
        if 'Single' not in process and doAllSys:
                if doABCDnn:
                        hist_PEAKUP.Write()
                        hist_PEAKDN.Write()
                        hist_TAILUP.Write()
                        hist_TAILDN.Write()
                        hist_CLOSUREUP.Write()
                        hist_CLOSUREDN.Write()
                        
                else:
                        hist_elRecoSFUp.Write()
                        hist_elRecoSFDn.Write()
                        hist_elIdSFUp.Write()
                        hist_elIdSFDn.Write()
                        hist_elIsoSFUp.Write()
                        hist_elIsoSFDn.Write()
                        hist_TrigEffElUp.Write()
                        hist_TrigEffElDn.Write()
                        hist_muRecoSFUp.Write()
                        hist_muRecoSFDn.Write()
                        hist_muIdSFUp.Write()
                        hist_muIdSFDn.Write()
                        hist_muIsoSFUp.Write()
                        hist_muIsoSFDn.Write()
                        hist_TrigEffMuUp.Write()
                        hist_TrigEffMuDn.Write()
                        hist_PileupUp.Write()
                        hist_PileupDn.Write()
                        hist_PrefireUp.Write()
                        hist_PrefireDn.Write()
                        hist_jsfUp.Write()
                        hist_jsfDn.Write()
                        hist_topptUp.Write()
                        hist_topptDn.Write()
                        hist_muRFcorrdUp.Write()
                        hist_muRFcorrdDn.Write()
                        hist_muRUp.Write()
                        hist_muRDn.Write()
                        hist_muFUp.Write()
                        hist_muFDn.Write()
                        hist_btagHFCOUp.Write()
                        hist_btagHFCODn.Write()
                        hist_btagHFUCUp.Write()
                        hist_btagHFUCDn.Write()
                        hist_btagLFCOUp.Write()
                        hist_btagLFCODn.Write()
                        hist_btagLFUCUp.Write()
                        hist_btagLFUCDn.Write()

                        ## TO-DO: check tree names for jer and jec!
                        if process+'JERup' in tTree:
                                hist_jerUp.Write()
                                hist_jerDn.Write()

                        if process+'JECup' in tTree:
                                hist_jecUp.Write()
                                hist_jecDn.Write()
                        
                        ### TO-DO: check how many PDF variations live in NanoAOD, find branch names and get this segment set up correctly
                        # for i in range(100): histptrs[iPlot+'pdf'+str(i)+'_'+lumicatproc] = sel.Define('weightpdf'+str(i),weightStr+'*pdfWeights['+str(i)+']').Histo1D((iPlot+'pdf'+str(i)+'_'+lumicatproc,xAxisLabel,len(xbins)-1,xbins),plotTreeName,'weightpdf'+str(i))

        # del df
        # if 'Single' not in process and doAllSys and not doABCDnn:
        #         del sel
        # if process+'JERup' in tTree:
        #         del dfjerUp
        #         del dfjerDn
        #         if '[0]' in plotDetails[0]:
        #                 del seljerUp
        #                 del seljerDn
        # if process+'JECup' in tTree:
        #         del dfjecUp
        #         del dfjecDn
        #         if '[0]' in plotDetails[0]:
        #                 del seljecUp
        #                 del seljecDn
                
                
        print("--- Analyze: %s minutes ---" % (round((time.time() - start_time)/60,2)))
        #DisableImplicitMT()
