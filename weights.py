#!/usr/bin/python

targetlumi = 59740. # https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable r23
targetlumi2017 = 41530. 
targetlumi2017 = 35920. 

genHTweight={}
genHTweight['WJetsMG100'] = 0.998056#https://github.com/jmhogan/GenHTweight/blob/master/WJetsToLNuSFs.txt
genHTweight['WJetsMG200'] = 0.978569
genHTweight['WJetsMG400'] = 0.928054
genHTweight['WJetsMG600'] = 0.856705
genHTweight['WJetsMG800'] = 0.757463
genHTweight['WJetsMG1200']= 0.608292
genHTweight['WJetsMG2500']= 0.454246

genHTweight['DYMG100'] = 1.007516#https://github.com/jmhogan/GenHTweight/blob/master/DYJetsToLLSFs.txt
genHTweight['DYMG200'] = 0.992853
genHTweight['DYMG400'] = 0.974071
genHTweight['DYMG600'] = 0.948367
genHTweight['DYMG800'] = 0.883340
genHTweight['DYMG1200']= 0.749894
genHTweight['DYMG2500']= 0.617254

BR={}
BR['BW'] = 0.5
BR['TZ'] = 0.25
BR['TH'] = 0.25
BR['TTBWBW'] = BR['BW']*BR['BW']
BR['TTTHBW'] = 2*BR['TH']*BR['BW']
BR['TTTZBW'] = 2*BR['TZ']*BR['BW']
BR['TTTZTZ'] = BR['TZ']*BR['TZ']
BR['TTTZTH'] = 2*BR['TZ']*BR['TH']
BR['TTTHTH'] = BR['TH']*BR['TH']

BR['TW'] = 0.5
BR['BZ'] = 0.25
BR['BH'] = 0.25
BR['BBTWTW'] = BR['TW']*BR['TW']
BR['BBBHTW'] = 2*BR['BH']*BR['TW']
BR['BBBZTW'] = 2*BR['BZ']*BR['TW']
BR['BBBZBZ'] = BR['BZ']*BR['BZ']
BR['BBBZBH'] = 2*BR['BZ']*BR['BH']
BR['BBBHBH'] = BR['BH']*BR['BH']

# Number of processed MC events (before selections)
nRun={}

#nRun['DYMG200'] = 11206441.0 # from integral 11225887.0, file DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_1_hadd.root 1-5
nRun['DYMG400'] = 9332233.0 # from integral 9358053.0, file DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_1_hadd.root 1-4
nRun['DYMG600'] = 8828622.0 # from integral 8862104.0, file DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG800'] = 3121975.0 # from integral 3138129.0, file DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_1_hadd.root 1-3
nRun['DYMG1200'] = 531762.0 # from integral 536416.0, file DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG2500'] = 415713.0 #from integral 427051.0, file DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root

nRun['QCDht1000'] = 15407797.0 # from integral 15466225.0, file QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht1500'] = 10887751.0  # from integral 10955087.0, file QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht2000'] = 5414545.0 #from integral 5475677.0, file QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
#nRun['QCDht200'] = 54251666.0 # from integral 54289442.0, file QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht300'] = 54598278.0 # from integral 54659058.0, file QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht500'] = 55056202.0 # from integral 55152960.0, file QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht700'] = 48038740.0 # from integral 48158738.0, file QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root

nrunttJets2L2Nu = 63791484.0 # from integral 64310000.0, file TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root
nruntthad = 132368556.0 # from integral 133448000.0.0, file TTToHadronic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_hadd.root
nrunttJetsSemiLep = 100579948.0 # from integral 101400000.0, file TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root
nruntt1000 = 22618461.0 # from integral 23847283.0, file TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8_1_hadd.root
nruntt700 = 37813675.0 # from integral 38538593.0, file TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8_1_hadd.root

nRun['TTJetsHad0'] = nruntthad*0.8832   # hadronic*BR(0-700)
nRun['TTJetsHad700'] = nruntthad*0.0921 + nruntt700*0.457 #hadronic*BR(700-1000) + mass700*BR(hadronic)
nRun['TTJetsHad1000'] = nruntthad*0.02474 + nruntt1000*0.457 #hadronic*BR(1000+) + mass1000*BR(hadronic
nRun['TTJetsSemiLep0'] = nrunttJetsSemiLep*0.8832  # semilept*BR(0-700)
nRun['TTJetsSemiLep700'] = nrunttJetsSemiLep*0.0921 + nruntt700*0.438 #semilept*BR(700-1000) + mass700*BR(semilept)
nRun['TTJetsSemiLep1000'] = nrunttJetsSemiLep*0.02474 + nruntt1000*0.438 #semilept*BR(1000+) + mass1000*BR(semilept)
nRun['TTJets2L2nu0'] = nrunttJets2L2Nu*0.8832  #dilepton*BR(0-700)
nRun['TTJets2L2nu700'] = nrunttJets2L2Nu*0.0921 + nruntt700*0.105 #dilepton*BR(700-1000) + mass700*BR(dilepton)
nRun['TTJets2L2nu1000'] = nrunttJets2L2Nu*0.02474 + nruntt1000*0.105 #dilepton*BR(1000+) + mass1000*BR(dilepton)
nRun['TTJetsPH700mtt'] = nruntt700 + nruntthad*0.0921 + nrunttJetsSemiLep*0.0921 + nrunttJets2L2Nu*0.0921 #mass700 + inclusive*BR(700)
nRun['TTJetsPH1000mtt'] = nruntt1000 + nruntthad*0.02474 + nrunttJetsSemiLep*0.02474 + nrunttJets2L2Nu*0.02474 #mass1000 + inclusive*BR(1000)


nRun['Ts'] = 12458638.0 # from integral 19965000.0, file ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['Tbt'] = 72687396.0 # from integral 77450800.0, file ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8_1_hadd.root
nRun['Tt']= 144094782.0 # from integral 154307600.0, file ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8_hadd.root
nRun['TtW'] = 9553912.0 # from integral 9598000.0, file ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root
nRun['TbtW'] = 7588180. # from integral 7623000.0, file ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root


#nRun['WJetsMG200'] = 25423155.0 # from integral 25468933.0, file WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root 1-7
nRun['WJetsMG400'] = 5915969. # from integral 5932701.0, file WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG600'] = 19699782. # from integral 19771294.0, file WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG800'] = 8362227. # from integral 8402687.0, file WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG1200']= 7571583. # from integral 7633949.0, file WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG2500']= 3191612. # from integral 327980.0, file WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsPt100'] = 120124110.*(1.-2.*0.32) #Full =120124110, neg frac 0.32
nRun['WJetsPt250'] = 12022587.*(1.-2.*0.31555) #Full = 12022587, neg frac 0.31555 
nRun['WJetsPt400'] = 1939947.*(1.-2.*0.30952) #Full = 1939947, neg frac 0.30952
nRun['WJetsPt600'] = 1974619.*(1.-2.*0.29876) #Full = 1974619, neg frac 0.29876

nRun['WW'] = 7958000. # from integral 7958000.0, file WW_TuneCP5_13TeV-pythia8_hadd.root
nRun['WZ'] = 3893000. # from integral 3893000.0, file WZ_TuneCP5_13TeV-pythia8_hadd.root
nRun['ZZ'] = 1979000. # from integral 1979000.0, file ZZ_TuneCP5_13TeV-pythia8_hadd.root
nRun['TTW'] = 9384328. # from integral 9425384.0, file ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8_hadd.root
nRun['TTZ'] = 8519074. # from integral 8536618.0, file ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8_hadd.root
nRun['TTH'] = 9580578. # from integral 9783674.0, file ttH_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root
nRun['TTWq'] = 430310. #from 833298
nRun['TTZq'] = 351164. #from 749400
nRun['TTWl'] = 2686095.0 # from integral 4911941.0, file TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_1_hadd.root 1-2
nRun['TTZl'] = 6274046. #from integral 13280000.0, file TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root
nRun['ttHToNonbb'] = 7368333.0#from integral 7525991.0, file ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root
nRun['ttHTobb'] = 11580577.0 #from integral 11835999.0, file ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root

nRunTTM1000 = 988591.585 # from integral 832000.0
nRunTTM1100 = 1006338.443*829000./838000. # from integral 838000.0, step1 814285.060093. # from integral 829000.0
nRunTTM1200 = 1015599.881 # from integral 841000.0
nRunTTM1300 = 1027236.813 # from integral 850000.0
nRunTTM1400 = 1003266.43 # from integral 832000.0
nRunTTM1500 = 963700.784 # from integral 810000.0
nRunTTM1600 = 988854.229*835000./850000. # from integral 850000.0, step 1 781203.387708. # from integral 835000.0, 
nRunTTM1700 = 953395.981 # from integral 850000.0
nRunTTM1800 = 907874.112*844000./850000. # from integral 850000.0, step1 759316.728757. # from integral 844000.0,
nRunTTM900 = 983788.102 # from integral 838000.0, 
nRun['TTM900BWBW'] = nRunTTM900/9.0
nRun['TTM1000BWBW'] = nRunTTM1000/9.0
nRun['TTM1100BWBW'] = nRunTTM1100/9.0
nRun['TTM1200BWBW'] = nRunTTM1200/9.0
nRun['TTM1300BWBW'] = nRunTTM1300/9.0
nRun['TTM1400BWBW'] = nRunTTM1400/9.0
nRun['TTM1500BWBW'] = nRunTTM1500/9.0
nRun['TTM1600BWBW'] = nRunTTM1600/9.0
nRun['TTM1700BWBW'] = nRunTTM1700/9.0
nRun['TTM1800BWBW'] = nRunTTM1800/9.0
nRun['TTM900THBW'] = nRunTTM900*2.0/9.0
nRun['TTM1000THBW'] = nRunTTM1000*2.0/9.0
nRun['TTM1100THBW'] = nRunTTM1100*2.0/9.0
nRun['TTM1200THBW'] = nRunTTM1200*2.0/9.0
nRun['TTM1300THBW'] = nRunTTM1300*2.0/9.0
nRun['TTM1400THBW'] = nRunTTM1400*2.0/9.0
nRun['TTM1500THBW'] = nRunTTM1500*2.0/9.0
nRun['TTM1600THBW'] = nRunTTM1600*2.0/9.0
nRun['TTM1700THBW'] = nRunTTM1700*2.0/9.0
nRun['TTM1800THBW'] = nRunTTM1800*2.0/9.0
nRun['TTM900TZBW'] = nRunTTM900*2.0/9.0
nRun['TTM1000TZBW'] = nRunTTM1000*2.0/9.0
nRun['TTM1100TZBW'] = nRunTTM1100*2.0/9.0
nRun['TTM1200TZBW'] = nRunTTM1200*2.0/9.0
nRun['TTM1300TZBW'] = nRunTTM1300*2.0/9.0
nRun['TTM1400TZBW'] = nRunTTM1400*2.0/9.0
nRun['TTM1500TZBW'] = nRunTTM1500*2.0/9.0
nRun['TTM1600TZBW'] = nRunTTM1600*2.0/9.0
nRun['TTM1700TZBW'] = nRunTTM1700*2.0/9.0
nRun['TTM1800TZBW'] = nRunTTM1800*2.0/9.0
nRun['TTM900TZTZ'] = nRunTTM900/9.0
nRun['TTM1000TZTZ'] = nRunTTM1000/9.0
nRun['TTM1100TZTZ'] = nRunTTM1100/9.0
nRun['TTM1200TZTZ'] = nRunTTM1200/9.0
nRun['TTM1300TZTZ'] = nRunTTM1300/9.0
nRun['TTM1400TZTZ'] = nRunTTM1400/9.0
nRun['TTM1500TZTZ'] = nRunTTM1500/9.0
nRun['TTM1600TZTZ'] = nRunTTM1600/9.0
nRun['TTM1700TZTZ'] = nRunTTM1700/9.0
nRun['TTM1800TZTZ'] = nRunTTM1800/9.0
nRun['TTM900TZTH'] = nRunTTM900*2.0/9.0
nRun['TTM1000TZTH'] = nRunTTM1000*2.0/9.0
nRun['TTM1100TZTH'] = nRunTTM1100*2.0/9.0
nRun['TTM1200TZTH'] = nRunTTM1200*2.0/9.0
nRun['TTM1300TZTH'] = nRunTTM1300*2.0/9.0
nRun['TTM1400TZTH'] = nRunTTM1400*2.0/9.0
nRun['TTM1500TZTH'] = nRunTTM1500*2.0/9.0
nRun['TTM1600TZTH'] = nRunTTM1600*2.0/9.0
nRun['TTM1700TZTH'] = nRunTTM1700*2.0/9.0
nRun['TTM1800TZTH'] = nRunTTM1800*2.0/9.0
nRun['TTM900THTH'] = nRunTTM900/9.0
nRun['TTM1000THTH'] = nRunTTM1000/9.0
nRun['TTM1100THTH'] = nRunTTM1100/9.0
nRun['TTM1200THTH'] = nRunTTM1200/9.0
nRun['TTM1300THTH'] = nRunTTM1300/9.0
nRun['TTM1400THTH'] = nRunTTM1400/9.0
nRun['TTM1500THTH'] = nRunTTM1500/9.0
nRun['TTM1600THTH'] = nRunTTM1600/9.0
nRun['TTM1700THTH'] = nRunTTM1700/9.0
nRun['TTM1800THTH'] = nRunTTM1800/9.0

nRunBBM1000 = 1003421.665 # from integral 844000.0
nRunBBM1100 = 1021828.79*835000./850000. # from integral 850000.0, step1 827964.928851. # from integral 835000.0,
nRunBBM1200 = 1020164.846 # from integral 844000.0
nRunBBM1300 = 1027983.479 # from integral 850000.0
nRunBBM1400 = 975159.796 # from integral 810000.0
nRunBBM1500 = 1010764.21 # from integral 850000.0
nRunBBM1600 = 943449.549 # from integral 810000.0
nRunBBM1700 = 932757.943 # from integral 832000.0
nRunBBM1800 = 882458.436 # from integral 826000.0
nRunBBM900 = 951074.915 # from integral 810000.0
nRun['BBM900TWTW'] = nRunBBM900/9.0
nRun['BBM1000TWTW'] = nRunBBM1000/9.0
nRun['BBM1100TWTW'] = nRunBBM1100/9.0
nRun['BBM1200TWTW'] = nRunBBM1200/9.0
nRun['BBM1300TWTW'] = nRunBBM1300/9.0
nRun['BBM1400TWTW'] = nRunBBM1400/9.0
nRun['BBM1500TWTW'] = nRunBBM1500/9.0
nRun['BBM1600TWTW'] = nRunBBM1600/9.0
nRun['BBM1700TWTW'] = nRunBBM1700/9.0
nRun['BBM1800TWTW'] = nRunBBM1800/9.0
nRun['BBM900BHTW'] = nRunBBM900*2.0/9.0
nRun['BBM1000BHTW'] = nRunBBM1000*2.0/9.0
nRun['BBM1100BHTW'] = nRunBBM1100*2.0/9.0
nRun['BBM1200BHTW'] = nRunBBM1200*2.0/9.0
nRun['BBM1300BHTW'] = nRunBBM1300*2.0/9.0
nRun['BBM1400BHTW'] = nRunBBM1400*2.0/9.0
nRun['BBM1500BHTW'] = nRunBBM1500*2.0/9.0
nRun['BBM1600BHTW'] = nRunBBM1600*2.0/9.0
nRun['BBM1700BHTW'] = nRunBBM1700*2.0/9.0
nRun['BBM1800BHTW'] = nRunBBM1800*2.0/9.0
nRun['BBM900BZTW'] = nRunBBM900*2.0/9.0
nRun['BBM1000BZTW'] = nRunBBM1000*2.0/9.0
nRun['BBM1100BZTW'] = nRunBBM1100*2.0/9.0
nRun['BBM1200BZTW'] = nRunBBM1200*2.0/9.0
nRun['BBM1300BZTW'] = nRunBBM1300*2.0/9.0
nRun['BBM1400BZTW'] = nRunBBM1400*2.0/9.0
nRun['BBM1500BZTW'] = nRunBBM1500*2.0/9.0
nRun['BBM1600BZTW'] = nRunBBM1600*2.0/9.0
nRun['BBM1700BZTW'] = nRunBBM1700*2.0/9.0
nRun['BBM1800BZTW'] = nRunBBM1800*2.0/9.0
nRun['BBM900BZBZ'] = nRunBBM900/9.0
nRun['BBM1000BZBZ'] = nRunBBM1000/9.0
nRun['BBM1100BZBZ'] = nRunBBM1100/9.0
nRun['BBM1200BZBZ'] = nRunBBM1200/9.0
nRun['BBM1300BZBZ'] = nRunBBM1300/9.0
nRun['BBM1400BZBZ'] = nRunBBM1400/9.0
nRun['BBM1500BZBZ'] = nRunBBM1500/9.0
nRun['BBM1600BZBZ'] = nRunBBM1600/9.0
nRun['BBM1700BZBZ'] = nRunBBM1700/9.0
nRun['BBM1800BZBZ'] = nRunBBM1800/9.0
nRun['BBM900BZBH'] = nRunBBM900*2.0/9.0
nRun['BBM1000BZBH'] = nRunBBM1000*2.0/9.0
nRun['BBM1100BZBH'] = nRunBBM1100*2.0/9.0
nRun['BBM1200BZBH'] = nRunBBM1200*2.0/9.0
nRun['BBM1300BZBH'] = nRunBBM1300*2.0/9.0
nRun['BBM1400BZBH'] = nRunBBM1400*2.0/9.0
nRun['BBM1500BZBH'] = nRunBBM1500*2.0/9.0
nRun['BBM1600BZBH'] = nRunBBM1600*2.0/9.0
nRun['BBM1700BZBH'] = nRunBBM1700*2.0/9.0
nRun['BBM1800BZBH'] = nRunBBM1800*2.0/9.0
nRun['BBM900BHBH'] = nRunBBM900/9.0
nRun['BBM1000BHBH'] = nRunBBM1000/9.0
nRun['BBM1100BHBH'] = nRunBBM1100/9.0
nRun['BBM1200BHBH'] = nRunBBM1200/9.0
nRun['BBM1300BHBH'] = nRunBBM1300/9.0
nRun['BBM1400BHBH'] = nRunBBM1400/9.0
nRun['BBM1500BHBH'] = nRunBBM1500/9.0
nRun['BBM1600BHBH'] = nRunBBM1600/9.0
nRun['BBM1700BHBH'] = nRunBBM1700/9.0
nRun['BBM1800BHBH'] = nRunBBM1800/9.0


# Cross sections for MC samples (in pb) -- most unchanged for 2017
xsec={}
xsec['DY'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG100'] = 147.4*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG200'] = 40.99*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG400'] = 5.678*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG600'] = 1.367*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG800'] = 0.6304*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG1200'] = 0.1514*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG2500'] = 0.003565*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['TTJets'] = 831.76
xsec['WJets'] = 61526.7
xsec['WJetsMG'] = 61526.7
xsec['TTJetsPH'] = 831.76 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
#xsec['TTJetsPH0to700inc'] = 831.76
#xsec['TTJetsPH700to1000inc'] = 831.76*0.0921 #(xsec*filtering coeff.)
#xsec['TTJetsPH1000toINFinc'] = 831.76*0.02474 #(xsec*filtering coeff.)
xsec['TTJetsHad0'] = 831.76*0.8832*0.457  ## BRs from PDG Top Review 2018: 45.7%/43.8%/10.5% 0/1/2 leptons
xsec['TTJetsHad700'] = 831.76*0.0921*0.457
xsec['TTJetsHad1000'] = 831.76*0.02474*0.457
xsec['TTJetsSemiLep0'] = 831.76*0.8832*0.438
xsec['TTJetsSemiLep700'] = 831.76*0.0921*0.438
xsec['TTJetsSemiLep1000'] = 831.76*0.02474*0.438
xsec['TTJets2L2nu0'] = 831.76*0.8832*0.105
xsec['TTJets2L2nu700'] = 831.76*0.0921*0.105
xsec['TTJets2L2nu1000'] = 831.76*0.02474*0.105
xsec['TTJetsPH700mtt'] = 831.76*0.0921 #(xsec*filtering coeff.)
xsec['TTJetsPH1000mtt'] = 831.76*0.02474 #(xsec*filtering coeff.)

xsec['ttHToNonbb'] = 0.2151
xsec['ttHTobb'] = 0.2934

xsec['WJetsMG100'] = 1345.*1.21 # (1.21 = k-factor )# https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG200'] = 359.7*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG400'] = 48.91*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG600'] = 12.05*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG800'] = 5.501*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG1200'] = 1.329*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG2500'] = 0.03216*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns 
xsec['WJetsPt100'] = 676.3 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt250'] = 23.94 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt400'] = 3.031 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt600'] = 0.4524 #B2G-17-010 / AN2016_480_v5
xsec['WW'] = 118.7 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeVInclusive
xsec['WZ'] = 47.13 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['ZZ'] = 16.523 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['TTH'] = 0.5269 # from XsecDB, NLO
xsec['TTW'] = 0.4611 # from XsecDB, LO
xsec['TTZ'] = 0.5407 # from XsecDB, LO
xsec['TTZl'] = 0.2529 # from McM
xsec['TTZq'] = 0.5297 # from McM
xsec['TTWl'] = 0.2043 # from McM
xsec['TTWq'] = 0.4062 # from McM
xsec['Tt'] = 136.02 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Tbt'] = 80.95 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Ts'] = 10.32*0.333 #(leptonic, t+tbar) https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Tbs'] = 3.97*0.333 #(leptonic)# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['TtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['TbtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec

xsec['TTM700']   = 0.455 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM800']  = 0.196 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM900']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1000']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1100']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1300']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1500']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1700']  = 0.000666 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1800'] = 0.000391 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo

xsec['BBM700']   = 0.455 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM800']  = 0.196 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM900']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1000']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1100']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1300']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1500']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1700']  = 0.000666 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1800'] = 0.000391 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo

xsec['X53X53M700left']   = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M700right']  = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M800left']   = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M800right']  = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M900left']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M900right']  = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1000left']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1000right'] = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1100left']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1100right'] = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1200left']  = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1200right'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1300left']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1300right'] = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1400left']  = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1400right'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1500left']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1500right'] = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1600left']  = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1600right'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top

xsec['QCDht100'] = 27990000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht200'] = 1712000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht300'] = 347700. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht500'] = 32100. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht700'] = 6831. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht1000'] = 1207. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht1500'] = 119.9 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht2000'] = 25.24 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): 
	if 'BBM' not in sample and 'TTM' not in sample: 
		#print sample, (xsec[sample]) , (nRun[sample])
		weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
	else: weight[sample] = (targetlumi*BR[sample[:2]+sample[-4:]]*xsec[sample[:-4]]) / (nRun[sample])
# Samples for Jet reweighting (to be able to run w/ and w/o JSF together!):
for sample in sorted(nRun.keys()):
	if 'QCDht' in sample or 'WJetsMG' in sample: weight[sample+'JSF'] = weight[sample]

#  LocalWords:  nRun
