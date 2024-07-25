#!/usr/bin/python
import os,sys,time,math,datetime,pickle,itertools,getopt
from ROOT import TH1D,gROOT,TFile,TTree
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from numpy import linspace

from analyze import *
from samples import samples_electroweak, samples_wjets, samples_ttbar, samples_singletop, samples_ttbarx, samples_qcd, samples_data, samples_signal
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

# ------------- File location and total lumi ---------------

step1Dir = 'root://cmseos.fnal.gov//store/user/jmanagan/BtoTW_Oct2023_fullRun2/'

# ------------- Arguments and default values ------------
iPlot = 'HT' #choose a discriminant from plotList below!
if len(sys.argv)>2: iPlot=sys.argv[2]
region = 'all'
if len(sys.argv)>3: region=sys.argv[3]
isCategorized = False
if len(sys.argv)>4: isCategorized=int(sys.argv[4])

doJetRwt= 1
doAllSys= False
cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templatesTest'+region
if not isCategorized: pfix='kinematicsTEST'+region
print('Set pfix to '+pfix)

# -------------- Groups of background samples to use --------------

# this is a list of group dictionaries. "wjets" has entries like "WJetsHT2002018":WJetsHT2002018, where the 2nd is the class
bkgList = [samples_electroweak,samples_wjets,samples_ttbar,samples_singletop,samples_ttbarx,samples_qcd]

### TO-DO: in samples.py, make up an entry for each year for ABCDnn with dummy information where needed.
### When iPlot == a transform variable, bkgList = [samples_electroweak,samples_ttbarx,samples_abcdnn] (singletop?)

# use "samples_data" and "samples_signal" below for the dictionaries of data and signals

# ------------- Parameters to divide up the histograms --------------

if len(sys.argv)>5: isEMlist=[str(sys.argv[5])]
else: isEMlist = ['E']
if len(sys.argv)>6: taglist=[str(sys.argv[6])]
else: 
	taglist = ['all']
	if isCategorized: taglist=['tagTjet','tagWjet','untagTlep','untagWlep','allWlep','allTlep']

# ------------- Definition of plots to make ------------------

plotList = {#discriminantName:(discriminantLJMETName, binning, xAxisLabel)
        'lepPt' :('lepton_pt',linspace(0, 1000, 51).tolist(),';lepton p_{T} [GeV]'),
        'lepEta':('lepton_eta',linspace(-2.5, 2.5, 51).tolist(),';lepton #eta'),
        'lepPhi':('lepton_phi',linspace(-3.2,3.2,65).tolist(),';lepton #phi'),
        'lepIso':('lepton_miniIso',linspace(0,0.2,51).tolist(),';lepton mini-isolation'),
        'MET'   :('corrMET_pt',linspace(0, 1000, 51).tolist(),';#slash{E}_{T} [GeV]'),
        'METphi':('corrMET_phi',linspace(-3.2,3.2, 65).tolist(),';#slash{E}_{T} phi'),
        'HT':('gcJet_HT',linspace(0, 5000, 51).tolist(),';H_{T} (GeV)'),
        'JetEta':('gcJet_eta',linspace(-3, 3, 41).tolist(),';central AK4 jet #eta'),
        'JetPt' :('gcJet_pt',linspace(0, 1500, 51).tolist(),';central AK4 jet p_{T} [GeV]'),
        'JetPhi':('gcJet_phi',linspace(-3.2,3.2, 65).tolist(),';central AK4 jet phi'),
        'FatJetEta':('gcFatJet_eta',linspace(-3, 3, 41).tolist(),';AK8 jet #eta'),
        'FatJetPt' :('gcFatJet_pt',linspace(0, 1500, 51).tolist(),';AK8 jet p_{T} [GeV]'),
        'FatJetPhi':('gcFatJet_phi',linspace(-3.2,3.2, 65).tolist(),';AK8 jet phi'),
        'FatJetSD' :('gcFatJet_sdmass',linspace(0, 500, 51).tolist(),';AK8 soft drop mass [GeV]'),
        'NFatJets':('NFatJets',linspace(0, 10, 11).tolist(),';AK8 jet multiplicity'),
        'TTbarMass'	:('R_TTbar_Mass',linspace(100, 1000, 7000).tolist(),';TTbar Mass (GeV);N counts'),
        'TTbarAngleCos'	:('R_TTbar_CosAngle',linspace(25, -1.25, 1.25).tolist(),';TTbar decay angle (Radians);N counts'),
        'TTbarAngleDeltaPhi'	:('R_TTbar_DeltaPhiAngle',linspace(50, 0, 3.14).tolist(),';TTbar delta phi decay angle (Radians);N counts'),
        'TTbarPtLAB'	:('R_TTbar_4VectLAB.Pt()',linspace(100, 0, 2000).tolist(),';TTbar (Lab) P_{t} (GeV/c);N counts'),
        'TTbarEtaLAB'	:('R_TTbar_4VectLAB.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';TTbar (Lab) Eta (Radians);N counts'),

        'TMass'	:('R_T_Mass',linspace(100, 0, 4000).tolist(),';T Mass (GeV);N counts'),
        'TAngleCos'	:('R_T_CosAngle',linspace(25, -1.25, 1.25).tolist(),';T decay angle (Radians);N counts'), 
        'TAngleDeltaPhi'	:('R_T_DeltaPhiAngle',linspace(50, 0, 3.14).tolist(),';T delta phi decay angle (Radians);N counts'),
        'TPtLAB'	:('R_T_4VectLAB.Pt()',linspace(100, 0, 4000).tolist(),';T (Lab) P_{t} (GeV/c);N counts'),
        'TEtaLAB'	:('R_T_4VectLAB.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';T (Lab) Eta (Radians);N counts'),
        'TPtTTbar'	:('R_T_4VectTTbar.Pt()',linspace(100, 0, 4000).tolist(),';T (TTbar) P_{t} (GeV/c);N counts'),
        'TEtaTTbar'	:('R_T_4VectTTbar.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';T (TTbar) Eta (Radians);N counts'),

        'TbarMass'	:('R_Tbar_Mass',linspace(100, 0, 4000).tolist(),';Tbar Mass (GeV);N counts'),
        'TbarAngleCos'	:('R_Tbar_CosAngle',linspace(25, -1.25, 1.25).tolist(),';Tbar decay angle (Radians);N counts'),
        'TbarAngleDeltaPhi'	:('R_Tbar_DeltaPhiAngle',linspace(50, 0, 3.14).tolist(),';Tbar delta phi decay angle (Radians);N counts'),
        'TbarPt'	:('R_Tbar_4VectLAB.Pt()',linspace(100, 0, 4000).tolist(),';Tbar (Lab) P_{t} (GeV/c);N counts'),
        'TbarEta'	:('R_Tbar_4VectLAB.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';Tbar (Lab) Eta (Radians);N counts'),
        'TbarPtTTbar'	:('R_Tbar_4VectTTbar.Pt()',linspace(100, 0, 4000).tolist(),';Tbar (TTbar) P_{t} (GeV/c);N counts'),
        'TbarEtaTTbar'	:('R_Tbar_4VectTTbar.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';Tbar (TTbar) Eta (Radians);N counts'),

        'WMass'	:('R_W_Mass',linspace(100, 0, 2000).tolist(),';W Mass (GeV);N counts'),
        'WAngleCos'	:('R_W_CosAngle',linspace(25, -1.25, 1.25).tolist(),';W decay angle (Radians);N counts'),
        'WAngleDeltaPhi'	:('R_W_DeltaPhiAngle',linspace(50, 0, 3.14).tolist(),';W delta phi decay angle (Radians);N counts'),
        'WPtLAB'	:('R_W_4VectLAB.Pt()',linspace(100, 0, 2000).tolist(),';W (Lab) P_{t} (GeV/c);N counts'),
        'WEtaLAB'	:('R_W_4VectLAB.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';W (Lab) Eta (Radians);N counts'),
        'WPtTTbar'	:('R_W_4VectTTbar.Pt()',linspace(100, 0, 2000).tolist(),';W (TTbar) P_{t} (GeV/c);N counts'),
        'WEtaTTbar'	:('R_W_4VectTTbar.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';W (TTbar) Eta (Radians);N counts'),
        'WPtT'	:('R_W_4VectT.Pt()',linspace(100, 0, 2000).tolist(),';W (T) P_{t} (GeV/c);N counts'),
        'WEtaT'	:('R_W_4VectT.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';W (T) Eta (Radians);N counts'),

        'bMass'	:('R_b_Mass',linspace(100, 0, 1000).tolist(),';b Mass (GeV);N counts'),
        'bAngleCos'	:('R_b_CosAngle',linspace(25, -1.25, 1.25).tolist(),';b decay angle (Radians);N counts'),
        'bPtLAB'	:('R_b_4VectLAB.Pt()',linspace(100, 0, 2000).tolist(),';b (Lab) P_{t} (GeV/c);N counts'),
        'bEtaLAB'	:('R_b_4VectLAB.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';b (Lab) Eta (Radians);N counts'),
        'bPtTTbar'	:('R_b_4VectTTbar.Pt()',linspace(100, 0, 2000).tolist(),';b (TTbar) P_{t} (GeV/c);N counts'),
        'bEtaTTbar'	:('R_b_4VectTTbar.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';b (TTbar) Eta (Radians);N counts'),
        'bPtT'	:('R_b_4VectT.Pt()',linspace(100, 0, 2000).tolist(),';b (T) P_{t} (GeV/c);N counts'),
        'bEtaT'	:('R_b_4VectT.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';b (T) Eta (Radians);N counts'),
'''
        'lMass'	:('R_l_Mass',linspace(50, -0.4, 0.4).tolist(),';#it{l} Mass (GeV);N counts'),
        'lAngleCos'	:('R_l_CosAngle',linspace(25, -1.25, 1.25).tolist(),';#it{l} decay angle (Radians);N counts'),
        'lPtLAB'	:('R_l_4VectLAB.Pt()',linspace(100, 0, 2000).tolist(),';#it{l} (Lab) P_{t} (GeV/c);N counts'),
        'lEtaLAB'	:('R_l_4VectLAB.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';#it{l} (Lab) Eta (Radians);N counts'),
        'lPtTTbar'	:('R_l_4VectTTbar.Pt()',linspace(100, 0, 2000).tolist(),';#it{l} (TTbar) P_{t} (GeV/c);N counts'),
        'lEtaTTbar'	:('R_l_4VectTTbar.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';#it{l} (TTbar) Eta (Radians);N counts'),
        'lPtT'	:('R_l_4VectT.Pt()',linspace(100, 0, 2000).tolist(),';#it{l} (T) P_{t} (GeV/c);N counts'),
        'lEtaT'	:('R_l_4VectT.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';#it{l} (T) Eta (Radians);N counts'),
        'lPtW'	:('R_l_4VectW.Pt()',linspace(100, 0, 2000).tolist(),';#it{l} (W) P_{t} (GeV/c);N counts'),
        'lEtaW'	:('R_l_4VectW.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';#it{l} (W) Eta (Radians);N counts'),

        'nuMass'	:('R_Nu_Mass',linspace(50, 0, 1*10^(-15)).tolist(),';#nu Mass (GeV);N counts'),
        'nuAngleCos'	:('R_Nu_CosAngle',linspace(25, -1.25, 1.25).tolist(),';#nu decay angle (Radians);N counts'),
        'nuPtLAB'	:('R_Nu_4VectLAB.Pt()',linspace(100, 0, 2000).tolist(),';#nu (Lab) P_{t} (GeV/c);N counts'),
        'nuEtaLAB'	:('R_Nu_4VectLAB.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';#nu (Lab) Eta (Radians);N counts'),
        'nuPtTTbar'	:('R_Nu_4VectTTbar.Pt()',linspace(100, 0, 2000).tolist(),';#nu (TTbar) P_{t} (GeV/c);N counts'),
        'nuEtaTTbar'	:('R_Nu_4VectTTbar.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';#nu (TTbar) Eta (Radians);N counts'),
        'nuPtT'	:('R_Nu_4VectT.Pt()',linspace(100, 0, 2000).tolist(),';#nu (T) P_{t} (GeV/c);N counts'),
        'nuEtaT'	:('R_Nu_4VectT.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';#nu (T) Eta (Radians);N counts'),
        'nuPtW'	:('R_Nu_4VectW.Pt()',linspace(100, 0, 2000).tolist(),';#nu (W) P_{t} (GeV/c);N counts'),
        'nuEtaW'	:('R_Nu_4VectW.Eta()',linspace(100, -2*3.14, 2*3.14).tolist(),';#nu (W) Eta (Radians);N counts')
'''
# Dictionary for 2D plots to see if there is any correlations?
'''
        'WCos_DeltaPhi'	:('R_W_DeltaPhiAngle:R_W_CosAngle',linspace(25, -1.25, 1.25, 50, 0, 3.14)';W Cos Decay Angle (Radians);W Delta Phi Decay Angle (Radians).tolist(),'), #in the draw command it is 'y:x'
        'TTbarCos_DeltaPhi'	:('R_TTbar_DeltaPhiAngle:R_TTbar_CosAngle', linspace(25, -1.25, 1.25, 50, 0, 3.14)';TTbar Cos Decay Angle (Radians);TTbar Delta Phi Decay Angle (Radians).tolist(),'), 
        'TbarMass_TMass'	:('R_T_Mass:R_Tbar_Mass',linspace(100, 0, 4000, 100, 0, 4000)';Tbar Mass (GeV);T Mass (GeV).tolist(),'),
        'TbarMass_TTbarAngleCos'	:('R_TTbar_CosAngle:R_Tbar_Mass',linspace(100, 0, 4000,  25, -1.25, 1.25)';Tbar Mass (GeV);TTbar Cos Decay Angle (Radians).tolist(),'),
        'TbarMass_TTbarAngleDeltaPhi'	:('R_TTbar_DeltaPhiAngle:R_Tbar_Mass',linspace(100, 0, 4000, 50, 0, 3.14)';Tbar Mass (GeV);TTbar Delta Phi Decay Angle (Radians).tolist(),'),
        'TMass_WAngleCos'	:('R_W_CosAngle:R_T_Mass',linspace(100, 0, 4000,  25, -1.25, 1.25)';T Mass (GeV);W Cos Decay Angle (Radians).tolist(),'),
'''
}

print( "PLOTTING: "+iPlot)
print( "         LJMET Variable: "+        iPlot][0])
print( "         X-AXIS TITLE  : "+        iPlot][2])
print( "         BINNING USED  : "+str(        iPlot][1]))

shapesFiles = ['jec','jer']
tTreeData = {}
tTreeSig = {}
tTreeBkg = {}

catList = list(itertools.product(isEMlist,taglist))
print('Cat list: '+str(catList))
nCats  = len(catList)
catInd = 1
for cat in catList:
        print('==================== Category: '+str(cat)+' ======================')
        catDir = cat[0]+'_'+cat[1]

        if len(sys.argv)>1:
                outDir=sys.argv[1]
                sys.path.append(outDir)
        else: 
                outDir = os.getcwd()+'/'+pfix+'/'+catDir
                if not os.path.exists(outDir): os.system('mkdir -p '+outDir)                
        category = {'isEM':cat[0],'tag':cat[1]}

        print('Running analyze! Storing in outDir = '+outDir)
        datahists = {}
        for data in samples_data.keys(): # "data" is the class 
                print('------------ '+data+' -------------')
                fileprefix = (samples_data[data].samplename).split('/')[1]+((samples_data[data].samplename).split('/')[2])[7]
                tTreeData[data]=readTreeNominal(fileprefix,samples_data[data].year,step1Dir) ## located in utils.py

                ### For analyze_RDF make the switch here (and similar regions below)
                ### Could "datahists" now be "updated" with more histptrs instead of hists? 
                datahists.update(analyze(tTreeData,samples_data[data],False,iPlot,        iPlot],category,region,isCategorized))
                if catInd==nCats: 
                        print('deleting '+data)
                        del tTreeData[data]  

        ### this function puts overflow into the last column -- in utils? Works on histptrs? If not, do this later?
        for data in datahists.keys(): overflow(datahists[data]) 

        ### store the dictionary of hists in a pickle file. Change this to open output ROOT, loop and .Write histptrs?
        pickle.dump(datahists,open(outDir+'/datahists_'+iPlot+'.p','wb'))
        del datahists

        ### Now we begin the same general process but for simulated backgrounds
        igrp = 0
        for bkgGrp in bkgList: 
                bkghists  = {}
                for bkg in bkgGrp.keys():
                        print('------------ '+bkg+' -------------')
                        fileprefix = (bkgGrp[bkg].samplename).split('/')[1]
                        tTreeBkg[bkg]=readTreeNominal(fileprefix,bkgGrp[bkg].year,step1Dir)
                        if doAllSys:
                                for syst in shapesFiles:
                                        for ud in ['Up','Dn']:
                                                print("        "+syst+ud)
                                                tTreeBkg[bkg+syst+ud]=readTreeShift(fileprefix,bkgGrp[bkg].year,syst.upper()+ud.lower(),step1Dir) ## located in utils.py
                        bkghists.update(analyze(tTreeBkg,bkgGrp[bkg],doAllSys,iPlot,        iPlot],category,region,isCategorized))
                        if catInd==nCats:
                                print('deleting '+bkg)
                                del tTreeBkg[bkg]
                                if doAllSys:
                                        for syst in shapesFiles:
                                                for ud in ['Up','Dn']: del tTreeBkg[bkg+syst+ud]

                for bkg in bkghists.keys(): negBinCorrection(bkghists[bkg])
                for bkg in bkghists.keys():   overflow(bkghists[bkg])
                pickle.dump(bkghists,open(outDir+'/bkghists'+str(igrp)+'_'+iPlot+'.p','wb'))
                igrp += 1
        del bkghists

        sighists  = {}
        for sig in samples_signal.keys(): 
                print('------------- '+sig+' ------------')
                fileprefix = (samples_signal[sig].samplename).split('/')[1]
                tTreeSig[sig]=readTreeNominal(fileprefix,samples_signal[sig].year,step1Dir)
                if doAllSys:
                        for syst in shapesFiles:
                                for ud in ['Up','Dn']:
                                        print("        "+syst+ud)
                                        tTreeSig[sig+syst+ud]=readTreeShift(fileprefix,samples_signal[sig].year,syst.upper()+ud.lower(),step1Dir)
                sighists.update(analyze(tTreeSig,samples_signal[sig],doAllSys,iPlot,        iPlot],category,region,isCategorized))
                if catInd==nCats: 
                        print('deleting '+sig)
                        del tTreeSig[sig]
                        if doAllSys:
                                for syst in shapesFiles:
                                        for ud in ['Up','Dn']: del tTreeSig[sig+syst+ud]

        for sig in sighists.keys(): negBinCorrection(sighists[sig])
        for sig in sighists.keys(): overflow(sighists[sig])	
        pickle.dump(sighists,open(outDir+'/sighists_'+iPlot+'.p','wb'))
        del sighists

        catInd+=1

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))
