#!/usr/bin/python

targetlumi = 59690. # 1/pb

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
# new counts for 2017
nRun['DYMG200'] = 8129885.0 # from integral 8143933.0, file DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG400'] = 7964856.0 #from integral 6556310.0, file DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG600'] = 6531484.0 #from integral 6556310.0, file DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG800'] = 3121975.0 #from integral 3138129.0, file DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG1200'] = 531762.0 # from integral 536416.0, file DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG2500'] = 415713.0 #from integral 427051.0, file DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht1000'] = 15407797.0 # from integral 15466225.0, file QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht1500'] = 10887751.0  # from integral 10955087.0, file QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht2000'] = 5414545.0 #from integral 5475677.0, file QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht200'] = 54251666.0 # from integral 54289442.0, file QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht300'] = 53092715.0 # from integral 53151917.0, file QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht500'] = 55056202.0 # from integral 55152960.0, file QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht700'] = 46433365.0 #from integral 46549317.0, file QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root


nRun['TTWl'] = 22618461. #from integral 4911941.0, file TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root
nRun['TTZl'] = 6274046. #from integral 13280000.0, file TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root

# not updated for 2017
#Do NGen*[1-2X], where X is the neg event fraction calculated from the jobs completed! 
#A = P - N = F - 2*N   A/F = 1 - 2*(N/F)  N/F = (1 - A/F)/2
nRun['TTJets'] = 14188545. #need negative counts
nRun['TTJetsPH'] = 111068128.#
nRun['TTJetsHad0'] = 132725582.0*0.8832 #from integral 133808000.0, file TTToHadronic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_hadd.root
nRun['TTJetsHad700'] = 132725582.0*0.0921 + 38520877*0.457 # from integral 133808000.0, file TTToHadronic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_hadd.root
nRun['TTJetsHad1000'] = 132725582.0*0.02474 + 21302221*0.457 # from integral 133808000.0, file TTToHadronic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_hadd.root
nRun['TTJetsSemiLep0'] = 100728756.0*0.8832 # from integral 101550000.0, file TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_hadd.root
nRun['TTJetsSemiLep700'] = 100728756.0*0.0921 + 38520877*0.438# from integral 101550000.0, file TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_hadd.root
nRun['TTJetsSemiLep1000'] = 100728756.0*0.02474 + 21302221*0.438# from integral 101550000.0, file TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_hadd.root
nRun['TTJets2L2nu0'] = 63791484.0*0.8832 # from integral 64310000.0, file TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_Mtt0to700_hadd.root
nRun['TTJets2L2nu700'] = 63791484.0*0.0921 + 63791484*0.105 #from integral 64310000.0, file TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_Mtt700to1000_hadd.root
nRun['TTJets2L2nu1000'] = 63791484.0*0.02474 + 63791484*0.105# TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_Mtt1000toInf_hadd.root
nRun['TTJetsPH700mtt'] = 37813675.0 + 132725582*0.0921 + 100728756*0.0921 + 68595608*0.0921 #from 39258853, file TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8_hadd.root
nRun['TTJetsPH1000mtt'] = 22618461.0 + 132725582*0.02474 + 100728756*0.02474 + 68595608*0.02474 #from integral 23847283.0, file TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8_hadd.root
nRun['Ts'] = 12458638.0 # from integral 19965000.0, file ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['Tbt'] = 74227130.0 # from integral 79090800.0, file ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8_hadd.root
nRun['Tt']= 144094782.0 # from integral 154307600.0, file ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8_hadd.root
nRun['TtW'] = 9553912. # from integral 9598000.0, file ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root
nRun['TbtW'] = 7588180. # from integral 7623000.0, file ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root
nRun['WJetsMG200'] = 25337564.0 # from integral 25383190.0, file WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
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

nRun['ttHToNonbb'] = 7368333.0#from integral 7525991.0, file ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root
nRun['ttHTobb'] = 11590377.0 #from integral 11835999.0, file ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root

nRun['TTM1000BWBW'] = 610453.332184*0.333*0.333
nRun['TTM1100BWBW'] = 745000.0*0.333*0.333#
nRun['TTM1200BWBW'] = 829000.0*0.333*0.333#
nRun['TTM1300BWBW'] = 847000.0*0.333*0.333#
nRun['TTM1400BWBW'] = 811000.0*0.333*0.333#
nRun['TTM1500BWBW'] = 827000.0*0.333*0.333#
nRun['TTM1600BWBW'] = 565461.196087*0.333*0.333#
nRun['TTM1700BWBW'] = 667958.604161*0.333*0.333#
nRun['TTM1800BWBW'] = 827000.0*0.333*0.333#
nRun['TTM1000THBW'] = 610453.332184*0.333*0.333*2
nRun['TTM1100THBW'] = 745000.0*0.333*0.333*2#
nRun['TTM1200THBW'] = 829000.0*0.333*0.333*2#
nRun['TTM1300THBW'] = 847000.0*0.333*0.333*2#
nRun['TTM1400THBW'] = 811000.0*0.333*0.333*2#
nRun['TTM1500THBW'] = 827000.0*0.333*0.333*2#
nRun['TTM1600THBW'] = 565461.196087*0.333*0.333*2#
nRun['TTM1700THBW'] = 667958.604161*0.333*0.333*2#
nRun['TTM1800THBW'] = 827000.0*0.333*0.333*2#
nRun['TTM1000TZBW'] = 610453.332184*0.333*0.333*2
nRun['TTM1100TZBW'] = 745000.0*0.333*0.333*2#
nRun['TTM1200TZBW'] = 829000.0*0.333*0.333*2#
nRun['TTM1300TZBW'] = 847000.0*0.333*0.333*2#
nRun['TTM1400TZBW'] = 811000.0*0.333*0.333*2#
nRun['TTM1500TZBW'] = 827000.0*0.333*0.333*2#
nRun['TTM1600TZBW'] = 565461.196087*0.333*0.333*2#
nRun['TTM1700TZBW'] = 667958.604161*0.333*0.333*2#
nRun['TTM1800TZBW'] = 827000.0*0.333*0.333*2#
nRun['TTM1000TZTZ'] = 610453.332184*0.333*0.333
nRun['TTM1100TZTZ'] = 745000.0*0.333*0.333#
nRun['TTM1200TZTZ'] = 829000.0*0.333*0.333#
nRun['TTM1300TZTZ'] = 847000.0*0.333*0.333#
nRun['TTM1400TZTZ'] = 811000.0*0.333*0.333#
nRun['TTM1500TZTZ'] = 827000.0*0.333*0.333#
nRun['TTM1600TZTZ'] = 565461.196087*0.333*0.333#
nRun['TTM1700TZTZ'] = 667958.604161*0.333*0.333#
nRun['TTM1800TZTZ'] = 827000.0*0.333*0.333#
nRun['TTM1000TZTH'] = 610453.332184*0.333*0.333*2
nRun['TTM1100TZTH'] = 745000.0*0.333*0.333*2#
nRun['TTM1200TZTH'] = 829000.0*0.333*0.333*2#
nRun['TTM1300TZTH'] = 847000.0*0.333*0.333*2#
nRun['TTM1400TZTH'] = 811000.0*0.333*0.333*2#
nRun['TTM1500TZTH'] = 827000.0*0.333*0.333*2#
nRun['TTM1600TZTH'] = 565461.196087*0.333*0.333*2#
nRun['TTM1700TZTH'] = 667958.604161*0.333*0.333*2#
nRun['TTM1800TZTH'] = 827000.0*0.333*0.333*2#
nRun['TTM1000THTH'] = 610453.332184*0.333*0.333
nRun['TTM1100THTH'] = 745000.0*0.333*0.333#
nRun['TTM1200THTH'] = 829000.0*0.333*0.333#
nRun['TTM1300THTH'] = 847000.0*0.333*0.333#
nRun['TTM1400THTH'] = 811000.0*0.333*0.333#
nRun['TTM1500THTH'] = 827000.0*0.333*0.333#
nRun['TTM1600THTH'] = 565461.196087*0.333*0.333#
nRun['TTM1700THTH'] = 667958.604161*0.333*0.333#
nRun['TTM1800THTH'] = 827000.0*0.333*0.333#

nRun['BBM700TWTW'] = 814800.0*0.333*0.333
nRun['BBM800TWTW'] = 817200.0*0.333*0.333
nRun['BBM900TWTW'] = 799800.0*0.333*0.333
nRun['BBM1000TWTW'] = 850000.0*0.333*0.333
nRun['BBM1100TWTW'] = 759504.3537*0.333*0.333
nRun['BBM1200TWTW'] = 728986.804777*0.333*0.333
nRun['BBM1300TWTW'] = 630262.51989*0.333*0.333
nRun['BBM1400TWTW'] = 787197.450755*0.333*0.333
nRun['BBM1500TWTW'] = 809813.568622*0.333*0.333
nRun['BBM1600TWTW'] = 754591.51902*0.333*0.333
nRun['BBM1700TWTW'] = 736994.112268*0.333*0.333
nRun['BBM1800TWTW'] = 1369996.49937*0.333*0.333
nRun['BBM700BHTW'] = 814800.0*0.333*0.333*2
nRun['BBM800BHTW'] = 817200.0*0.333*0.333*2
nRun['BBM900BHTW'] = 799800.0*0.333*0.333*2
nRun['BBM1000BHTW'] = 850000.0*0.333*0.333*2
nRun['BBM1100BHTW'] = 759504.3537*0.333*0.333*2
nRun['BBM1200BHTW'] = 728986.804777*0.333*0.333*2
nRun['BBM1300BHTW'] = 630262.51989*0.333*0.333*2
nRun['BBM1400BHTW'] = 787197.450755*0.333*0.333*2
nRun['BBM1500BHTW'] = 809813.568622*0.333*0.333*2
nRun['BBM1600BHTW'] = 754591.51902*0.333*0.333*2
nRun['BBM1700BHTW'] = 736994.112268*0.333*0.333*2
nRun['BBM1800BHTW'] = 1369996.49937*0.333*0.333*2
nRun['BBM700BZTW'] = 814800.0*0.333*0.333*2
nRun['BBM800BZTW'] = 817200.0*0.333*0.333*2
nRun['BBM900BZTW'] = 799800.0*0.333*0.333*2
nRun['BBM1000BZTW'] = 850000.0*0.333*0.333*2
nRun['BBM1100BZTW'] = 759504.3537*0.333*0.333*2
nRun['BBM1200BZTW'] = 728986.804777*0.333*0.333*2
nRun['BBM1300BZTW'] = 630262.51989*0.333*0.333*2
nRun['BBM1400BZTW'] = 787197.450755*0.333*0.333*2
nRun['BBM1500BZTW'] = 809813.568622*0.333*0.333*2
nRun['BBM1600BZTW'] = 754591.51902*0.333*0.333*2
nRun['BBM1700BZTW'] = 736994.112268*0.333*0.333*2
nRun['BBM1800BZTW'] = 1369996.49937*0.333*0.333*2
nRun['BBM700BZBZ'] = 814800.0*0.333*0.333
nRun['BBM800BZBZ'] = 817200.0*0.333*0.333
nRun['BBM900BZBZ'] = 799800.0*0.333*0.333
nRun['BBM1000BZBZ'] = 850000.0*0.333*0.333
nRun['BBM1100BZBZ'] = 759504.3537*0.333*0.333
nRun['BBM1200BZBZ'] = 728986.804777*0.333*0.333
nRun['BBM1300BZBZ'] = 630262.51989*0.333*0.333
nRun['BBM1400BZBZ'] = 787197.450755*0.333*0.333
nRun['BBM1500BZBZ'] = 809813.568622*0.333*0.333
nRun['BBM1600BZBZ'] = 754591.51902*0.333*0.333
nRun['BBM1700BZBZ'] = 736994.112268*0.333*0.333
nRun['BBM1800BZBZ'] = 1369996.49937*0.333*0.333
nRun['BBM700BZBH'] = 814800.0*0.333*0.333*2
nRun['BBM800BZBH'] = 817200.0*0.333*0.333*2
nRun['BBM900BZBH'] = 799800.0*0.333*0.333*2
nRun['BBM1000BZBH'] = 850000.0*0.333*0.333*2
nRun['BBM1100BZBH'] = 759504.3537*0.333*0.333*2
nRun['BBM1200BZBH'] = 728986.804777*0.333*0.333*2
nRun['BBM1300BZBH'] = 630262.51989*0.333*0.333*2
nRun['BBM1400BZBH'] = 787197.450755*0.333*0.333*2
nRun['BBM1500BZBH'] = 809813.568622*0.333*0.333*2
nRun['BBM1600BZBH'] = 754591.51902*0.333*0.333*2
nRun['BBM1700BZBH'] = 736994.112268*0.333*0.333*2
nRun['BBM1800BZBH'] = 1369996.49937*0.333*0.333*2
nRun['BBM700BHBH'] = 814800.0*0.333*0.333
nRun['BBM800BHBH'] = 817200.0*0.333*0.333
nRun['BBM900BHBH'] = 799800.0*0.333*0.333
nRun['BBM1000BHBH'] = 850000.0*0.333*0.333
nRun['BBM1100BHBH'] = 759504.3537*0.333*0.333
nRun['BBM1200BHBH'] = 728986.804777*0.333*0.333
nRun['BBM1300BHBH'] = 630262.51989*0.333*0.333
nRun['BBM1400BHBH'] = 787197.450755*0.333*0.333
nRun['BBM1500BHBH'] = 809813.568622*0.333*0.333
nRun['BBM1600BHBH'] = 754591.51902*0.333*0.333
nRun['BBM1700BHBH'] = 736994.112268*0.333*0.333
nRun['BBM1800BHBH'] = 1369996.49937*0.333*0.333


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
xsec['TTZToLLNuNu'] = 0.2529
xsec['TTWJetsToLNu'] = 0.2043

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
xsec['Tt'] = 136.02 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Tbt'] = 80.95 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Ts'] = 7.20/3 #(1/3 was suggested by Thomas Peiffer to account for the leptonic branching ratio)# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Tbs'] = 4.16/3 #(1/3 was suggested by Thomas Peiffer to account for the leptonic branching ratio)# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['TtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['TbtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma

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
