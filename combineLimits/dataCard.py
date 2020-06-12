#!/usr/bin/env python

import os,sys,time,math,datetime,itertools
from ROOT import gROOT,TFile,TH1F
import CombineHarvester.CombineTools.ch as ch
parent = os.path.dirname(os.getcwd())
thisdir= os.path.dirname(os.getcwd()+'/')
sys.path.append(parent)
from utils import *
gROOT.SetBatch(1)

whichsignal = 'TT'

def add_processes_and_observations(cb, prefix=whichsignal):
	print '>> Creating processes and observations...'
	for chn in chns:
		cats_chn = cats[chn]
		if 'isCR' not in chn:
			cb.AddObservations(  ['*'],  [prefix], [era], [chn],                 cats_chn      )
			cb.AddProcesses(     ['*'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )
			cb.AddProcesses(     masses, [prefix], [era], [chn], sig_procs,      cats_chn, True   )
		else:
			cb.AddObservations(  ['all'],  [prefix], [era], [chn],                 cats_chn      )
			cb.AddProcesses(     ['all'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )


def add_shapes(cb):
	print '>> Extracting histograms from input root files...'
	for chn in chns:
		CRbkg_pattern = 'HTNtag_'+lumiStr+'_%s$BIN__$PROCESS' % chn
		SRbkg_pattern = 'DnnTprime_'+lumiStr+'_%s$BIN__$PROCESS' % chn

		if 'isCR' in chn: 
			cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(
				rfile, CRbkg_pattern, CRbkg_pattern + '__$SYSTEMATIC')
		else:
			cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(
				rfile, SRbkg_pattern, SRbkg_pattern + '__$SYSTEMATIC')
		
		CRsig_pattern = 'HTNtag_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn
		SRsig_pattern = 'DnnTprime_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn

		if 'isCR' in chn:
			cb.cp().channel([chn]).era([era]).signals().ExtractShapes(
				rfile, CRsig_pattern, CRsig_pattern + '__$SYSTEMATIC')
		else:
			cb.cp().channel([chn]).era([era]).signals().ExtractShapes(
				rfile, SRsig_pattern, SRsig_pattern + '__$SYSTEMATIC')


def add_bbb(cb):
	print '>> Merging bin errors and generating bbb uncertainties...'
	bbb = ch.BinByBinFactory()
	bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(False)
	
	for chn in chns:
		cb_chn = cb.cp().channel([chn])
		if 'isCR' in chn:
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(bkg_procs[chn]), cb)
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(sig_procs), cb)
		else:
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(bkg_procs[chn]), cb)
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(sig_procs), cb)


def rename_and_write(cb):
	print '>> Setting standardised bin names...'
	ch.SetStandardBinNames(cb)
	
	writer = ch.CardWriter('limits_'+template+saveKey+'/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
						   'limits_'+template+saveKey+'/$TAG/common/$ANALYSIS_$CHANNEL.input.root')
	writer.SetVerbosity(1)
	writer.WriteCards('cmb', cb)
	for chn in chns:
		print chn
		writer.WriteCards(chn, cb.cp().channel([chn]))
	print '>> Done!'


def print_cb(cb):
	for s in ['Obs', 'Procs', 'Systs', 'Params']:
		print '* %s *' % s
		getattr(cb, 'Print%s' % s)()
		print


def add_systematics(cb):
	print '>> Adding systematic uncertainties...'
	
	signal = cb.cp().signals().process_set()
	
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')(['13TeV_R2016'], 1.025)(['13TeV_R2017'], 1.023)(['13TeV_R2018'], 1.025)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
	cb.cp().process(signal + allbkgs).channel(chnsE).AddSyst(cb, 'leptonSFEl', 'lnN', ch.SystMap('era')(['13TeV_R2016'], 1.03)(['13TeV_R2017'], 1.03)(['13TeV_R2018'], 1.03)) # 1.5% el id/iso + 2.5% trigger ~ 3%
	cb.cp().process(signal + allbkgs).channel(chnsM).AddSyst(cb, 'leptonSFMu', 'lnN', ch.SystMap('era')(['13TeV_R2016'], 1.03)(['13TeV_R2017'], 1.03)(['13TeV_R2018'], 1.03)) # 1% mu id/iso + 2.5% trigger ~ 3%
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jec_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0)) # This one is being studied in B2G-19-001/AN2018_322_v7 (take the uncorrelated one to be conservative!)
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jer_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'btag_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'mistag_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pileup', 'shape', ch.SystMap()(1.0)) # Correlated: https://hypernews.cern.ch/HyperNews/CMS/get/b2g/1381.html
 	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pdfNew', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
	if year=='2017':
		cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'prefire', 'shape', ch.SystMap()(1.0))

	for proc in allbkgs:
		cb.cp().process([proc]).channel(chns).AddSyst(cb, 'muRFcorrdNew'+proc, 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
	cb.cp().process(signal).channel(chns).AddSyst(cb, 'muRFcorrdNewSig', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 


def add_autoMCstat(cb):
	print '>> Adding autoMCstats...'
	
	thisDir = os.getcwd()
	for chn in ['cmb']+chns:
		chnDir = os.getcwd()+'/limits_'+template+saveKey+'/'+chn+'/690/'
		os.chdir(chnDir)
		if chn=='cmb': os.system('combineCards.py TTTT_*.txt > DataCard.txt')
		files = [x for x in os.listdir(chnDir) if '.txt' in x]
		for ifile in files:
			with open(chnDir+ifile, 'a') as chnfile: chnfile.write('* autoMCStats 1.')
			print '*'*20
			print 'Making workspace from', chnDir+ifile
			cmd = 'text2workspace.py '+chnDir+ifile+' -v 1 -m 690 --no-b-only'
			os.system(cmd)
		os.chdir(thisDir)


def go(cb):
	add_processes_and_observations(cb)
	add_systematics(cb)
	add_shapes(cb)
	#add_bbb(cb)
	rename_and_write(cb)
	add_autoMCstat(cb)
	#print_cb(cb)


if __name__ == '__main__':
	cb = ch.CombineHarvester()
	#cb.SetVerbosity(20)
	
	year = '2018'
	era = '13TeV_R'+year
	lumiStr = '41p53fb'
	if year=='2018': lumiStr = '59p97fb'

	tag = '_ttHFupLFdown'
	saveKey = '_ttHF'+tag
	fileDir = '/user_data/ssagir/CMSSW_10_2_10/src/singleLepAnalyzer/fourtops/makeTemplates/'
	template = 'R'+year+'_Xtrig_2020_4_25'
	if not os.path.exists('./limits_'+template+saveKey): os.system('mkdir ./limits_'+template+saveKey)
	os.system('cp '+fileDir+'templates_'+template+'/templates_HT_'+lumiStr+tag+'_rebinned_stat0p3.root ./limits_'+template+saveKey+'/')
	rfile = './limits_'+template+saveKey+'/templates_HT_'+lumiStr+tag+'_rebinned_stat0p3.root'
	
	ttbkgs = ['ttnobb','ttbb'] # ['ttjj','ttcc','ttbb','ttbj']
	allbkgs = ttbkgs + ['top','ewk','qcd']
	dataName = 'data_obs'
	tfile = TFile(rfile)
	allHistNames = [k.GetName() for k in tfile.GetListOfKeys() if not (k.GetName().endswith('Up') or k.GetName().endswith('Down'))]
	tfile.Close()
	chns = [hist[hist.find('fb_')+3:hist.find('__')] for hist in allHistNames if '__'+dataName in hist]
	chnsE = [chn for chn in chns if '_isE_' in chn]
	chnsM = [chn for chn in chns if '_isM_' in chn]
	bkg_procs = {chn:[hist.split('__')[-1] for hist in allHistNames if '_'+chn+'_' in hist and not (hist.endswith('Up') or hist.endswith('Down') or hist.endswith(dataName) or hist.endswith('TTTTM690'))] for chn in chns}
	for cat in sorted(bkg_procs.keys()):
		print cat,bkg_procs[cat]
		if 'qcd' in bkg_procs[cat]:
			print '		Removing qcd ...'
			bkg_procs[cat]=bkg_procs[cat][:-1]
# 	if year=='2018':
# 		bkg_procs['isSR_isE_nHOT1p_nT0p_nW0p_nB4p_nJ9']=['ttbb', 'ttcc', 'ttjj', 'top']
	
	sig_procs = ['TTTTM']
	
	cats = {}
	for chn in chns: cats[chn] = [(0, '')]
	
	masses = ch.ValsFromRange('690')
	go(cb)

