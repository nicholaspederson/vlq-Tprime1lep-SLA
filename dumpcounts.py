import os,sys
from ROOT import TFile, TH1
from samples import *

## something about samples goes here

for sample in sampleList2018: ## FIXME, use one of Kalin's lists
    print('-------------------------------------------------------')

    step1dir = '/store/user/kjohnso/FIXME/'
    tree = readTreeNominal(sample,step1Dir,"Runs"):
    # this function still needs fixing to work with our file names

    tree.Draw("genEventCount")
    integral = htemp.GetMean()

    tree.Draw("genEventSumw/sqrt(genEventSumw2/genEventCount)")
    adjusted = htemp.GetMean()

    print(str(adjusted)+'. # from integral '+str(integral)+', file '+filekey)

    if 'Bp' in sample:
        # use the LHEScaleWeight and LHEPDFWeight to extract the SFs

