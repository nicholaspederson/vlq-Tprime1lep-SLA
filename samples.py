#!/usr/bin/python

samples = {
'DataERRBCDEF':'SingleElectron_Mar2018',
'DataMRRBCDEF':'SingleMuon_Mar2018',

'TTM700BWBW':'TprimeTprime_M-700_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM800BWBW':'TprimeTprime_M-800_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM900BWBW':'TprimeTprime_M-900_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM1000BWBW':'TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM1100BWBW':'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM1200BWBW':'TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM1300BWBW':'TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM1400BWBW':'TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM1500BWBW':'TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM1600BWBW':'TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM1700BWBW':'TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_BWBW',
'TTM1800BWBW':'TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_BWBW',

'TTM700THBW':'TprimeTprime_M-700_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM800THBW':'TprimeTprime_M-800_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM900THBW':'TprimeTprime_M-900_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM1000THBW':'TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM1100THBW':'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM1200THBW':'TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM1300THBW':'TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM1400THBW':'TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM1500THBW':'TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM1600THBW':'TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM1700THBW':'TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_THBW',
'TTM1800THBW':'TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_THBW',

'TTM700TZBW':'TprimeTprime_M-700_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM800TZBW':'TprimeTprime_M-800_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM900TZBW':'TprimeTprime_M-900_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM1000TZBW':'TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM1100TZBW':'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM1200TZBW':'TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM1300TZBW':'TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM1400TZBW':'TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM1500TZBW':'TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM1600TZBW':'TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM1700TZBW':'TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_TZBW',
'TTM1800TZBW':'TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_TZBW',

'TTM700TZTZ':'TprimeTprime_M-700_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM800TZTZ':'TprimeTprime_M-800_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM900TZTZ':'TprimeTprime_M-900_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM1000TZTZ':'TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM1100TZTZ':'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM1200TZTZ':'TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM1300TZTZ':'TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM1400TZTZ':'TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM1500TZTZ':'TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM1600TZTZ':'TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM1700TZTZ':'TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_TZTZ',
'TTM1800TZTZ':'TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_TZTZ',

'TTM700TZTH':'TprimeTprime_M-700_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM800TZTH':'TprimeTprime_M-800_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM900TZTH':'TprimeTprime_M-900_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM1000TZTH':'TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM1100TZTH':'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM1200TZTH':'TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM1300TZTH':'TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM1400TZTH':'TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM1500TZTH':'TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM1600TZTH':'TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM1700TZTH':'TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_TZTH',
'TTM1800TZTH':'TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_TZTH',

'TTM700THTH':'TprimeTprime_M-700_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM800THTH':'TprimeTprime_M-800_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM900THTH':'TprimeTprime_M-900_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM1000THTH':'TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM1100THTH':'TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM1200THTH':'TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM1300THTH':'TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM1400THTH':'TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM1500THTH':'TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM1600THTH':'TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM1700THTH':'TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_THTH',
'TTM1800THTH':'TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_THTH',

'BBM700TWTW':'BprimeBprime_M-700_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM800TWTW':'BprimeBprime_M-800_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM900TWTW':'BprimeBprime_M-900_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM1000TWTW':'BprimeBprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM1100TWTW':'BprimeBprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM1200TWTW':'BprimeBprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM1300TWTW':'BprimeBprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM1400TWTW':'BprimeBprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM1500TWTW':'BprimeBprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM1600TWTW':'BprimeBprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM1700TWTW':'BprimeBprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_TWTW',
'BBM1800TWTW':'BprimeBprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_TWTW',

'BBM700BHTW':'BprimeBprime_M-700_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM800BHTW':'BprimeBprime_M-800_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM900BHTW':'BprimeBprime_M-900_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM1000BHTW':'BprimeBprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM1100BHTW':'BprimeBprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM1200BHTW':'BprimeBprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM1300BHTW':'BprimeBprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM1400BHTW':'BprimeBprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM1500BHTW':'BprimeBprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM1600BHTW':'BprimeBprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM1700BHTW':'BprimeBprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_BHTW',
'BBM1800BHTW':'BprimeBprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_BHTW',

'BBM700BZTW':'BprimeBprime_M-700_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM800BZTW':'BprimeBprime_M-800_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM900BZTW':'BprimeBprime_M-900_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM1000BZTW':'BprimeBprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM1100BZTW':'BprimeBprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM1200BZTW':'BprimeBprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM1300BZTW':'BprimeBprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM1400BZTW':'BprimeBprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM1500BZTW':'BprimeBprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM1600BZTW':'BprimeBprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM1700BZTW':'BprimeBprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_BZTW',
'BBM1800BZTW':'BprimeBprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_BZTW',

'BBM700BZBZ':'BprimeBprime_M-700_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM800BZBZ':'BprimeBprime_M-800_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM900BZBZ':'BprimeBprime_M-900_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM1000BZBZ':'BprimeBprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM1100BZBZ':'BprimeBprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM1200BZBZ':'BprimeBprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM1300BZBZ':'BprimeBprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM1400BZBZ':'BprimeBprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM1500BZBZ':'BprimeBprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM1600BZBZ':'BprimeBprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM1700BZBZ':'BprimeBprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_BZBZ',
'BBM1800BZBZ':'BprimeBprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_BZBZ',

'BBM700BZBH':'BprimeBprime_M-700_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM800BZBH':'BprimeBprime_M-800_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM900BZBH':'BprimeBprime_M-900_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM1000BZBH':'BprimeBprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM1100BZBH':'BprimeBprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM1200BZBH':'BprimeBprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM1300BZBH':'BprimeBprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM1400BZBH':'BprimeBprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM1500BZBH':'BprimeBprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM1600BZBH':'BprimeBprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM1700BZBH':'BprimeBprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_BZBH',
'BBM1800BZBH':'BprimeBprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_BZBH',

'BBM700BHBH':'BprimeBprime_M-700_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM800BHBH':'BprimeBprime_M-800_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM900BHBH':'BprimeBprime_M-900_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM1000BHBH':'BprimeBprime_M-1000_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM1100BHBH':'BprimeBprime_M-1100_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM1200BHBH':'BprimeBprime_M-1200_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM1300BHBH':'BprimeBprime_M-1300_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM1400BHBH':'BprimeBprime_M-1400_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM1500BHBH':'BprimeBprime_M-1500_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM1600BHBH':'BprimeBprime_M-1600_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM1700BHBH':'BprimeBprime_M-1700_TuneCP5_13TeV-madgraph-pythia8_BHBH',
'BBM1800BHBH':'BprimeBprime_M-1800_TuneCP5_13TeV-madgraph-pythia8_BHBH',

'X53X53M700left':'X53X53_M-700_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M800left':'X53X53_M-800_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M900left':'X53X53_M-900_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1000left':'X53X53_M-1000_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1100left':'X53X53_M-1100_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1200left':'X53X53_M-1200_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1300left':'X53X53_M-1300_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1400left':'X53X53_M-1400_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1500left':'X53X53_M-1500_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1600left':'X53X53_M-1600_LH_TuneCP5_13TeV-madgraph-pythia8',

'X53X53M700right':'X53X53_M-700_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M800right':'X53X53_M-800_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M900right':'X53X53_M-900_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1000right':'X53X53_M-1000_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1100right':'X53X53_M-1100_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1200right':'X53X53_M-1200_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1300right':'X53X53_M-1300_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1400right':'X53X53_M-1400_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1500right':'X53X53_M-1500_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53X53M1600right':'X53X53_M-1600_RH_TuneCP5_13TeV-madgraph-pythia8',

'DY':'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',
'DYMG':'DYJetsToLL_M-50_TuneCP5_13TeV-madgraph-pythia8',
'DYMG100':'DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraph-pythia8',
'DYMG200':'DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraph-pythia8',
'DYMG400':'DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraph-pythia8',
'DYMG600':'DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraph-pythia8',
'DYMG800':'DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraph-pythia8',
'DYMG1200':'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraph-pythia8',
'DYMG2500':'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraph-pythia8',

'WJetsMG':'WJetsToLNu_TuneCP5_13TeV-madgraph-pythia8',
'WJetsMG100':'WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG200':'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG400':'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG600':'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG800':'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG1200':'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG2500':'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsPt100':'WJetsToLNu_Pt-100To250_TuneCP5_13TeV-amcatnloFXFX-pythia8',
'WJetsPt250':'WJetsToLNu_Pt-250To400_TuneCP5_13TeV-amcatnloFXFX-pythia8',
'WJetsPt400':'WJetsToLNu_Pt-400To600_TuneCP5_13TeV-amcatnloFXFX-pythia8',
'WJetsPt600':'WJetsToLNu_Pt-600ToInf_TuneCP5_13TeV-amcatnloFXFX-pythia8',

'WW':'WW_TuneCP5_13TeV-pythia8',
'WZ':'WZ_TuneCP5_13TeV-pythia8',
'ZZ':'ZZ_TuneCP5_13TeV-pythia8',

'TTJets':'TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8',
'WJets':'WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8',

'TTJetsMG':'TTJets_TuneCP5_13TeV-madgraphMLM-pythia8',
## new ttbar for 2017
'TTJetsHad0':'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700',
'TTJetsHad700':'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000',
'TTJetsHad1000':'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf',
'TTJetsSemiLep0':'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700',
'TTJetsSemiLep700':'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000',
'TTJetsSemiLep1000':'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf',
'TTJets2L2nu0':'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700',
'TTJets2L2nu700':'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000',
'TTJets2L2nu1000':'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf',
'TTJetsPH700mtt':'TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8',
'TTJetsPH1000mtt':'TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8',

'Ts':'ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',
'Tbt':'ST_t-channel_antitop_5f_TuneCP5_PSweights_13TeV-powheg-madspin-pythia8_vtd_vts_prod',
'Tt':'ST_t-channel_top_5f_TuneCP5_PSweights_13TeV-powheg-madspin-pythia8_vtd_vts_prod',
'TbtW':'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
'TtW':'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',

'TTWl':'TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8',
'TTWq':'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
'TTZl':'TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8', ## need to fix this, wanted M 10-inf like below
#'TTZl':'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',
'TTZq':'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8',

'QCDht100':'QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8',
'QCDht200':'QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8',
'QCDht300':'QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8',
'QCDht500':'QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8',
'QCDht700':'QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8',
'QCDht1000':'QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8',
'QCDht1500':'QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8',
'QCDht2000':'QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8',
}



