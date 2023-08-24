import os,sys
from ROOT import TFile, TH1
from samples import *
from utils import *
from math import sqrt

## something about samples goes here

for sample in samples_2018UL:
    #print('-------------------------------------------------------')
    
    samplename = sample.samplename.split('/')[1]

    step1dir = 'root://cmseos.fnal.gov//store/user/jmanagan/BtoTW_Aug2023_2018/'
    tree = readTreeNominal(samplename,step1dir,"Runs")

    integral = 0
    adjusted = 0
    for irun in range(tree.GetEntries()):
        tree.GetEntry(irun)
        integral += tree.genEventCount
        adjusted += tree.genEventSumw/sqrt(tree.genEventSumw2/tree.genEventCount)

    print(sample.prefix+'.nrun = '+str(adjusted)+' # from integral '+str(integral)+', file '+sample.prefix)

    #if 'Bp' in sample:
        # use the LHEScaleWeight and LHEPDFWeight to extract the SFs

