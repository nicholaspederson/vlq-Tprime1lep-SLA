#!/usr/bin/env python

import os,sys,time,math,datetime,itertools
from ROOT import gROOT,TFile,TH1F

parent = os.path.dirname(os.getcwd())
thisdir= os.path.dirname(os.getcwd()+'/')
sys.path.append(parent)
from utils import *
import CombineHarvester.CombineTools.ch as ch

gROOT.SetBatch(1)

whichsignal = 'TT'

def add_processes_and_observations(cb, prefix=whichsignal):
	print '>> Creating processes and observations...'
	for chn in chns:
		cats_chn = cats[chn]
		cb.AddObservations(  ['*'],  [prefix], [era], [chn],                 cats_chn      )
		cb.AddProcesses(     ['*'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )
		cb.AddProcesses(     masses, [prefix], [era], [chn], sig_procs,      cats_chn, True   )


def add_shapes(cb):
	print '>> Extracting histograms from input root files...'
	for chn in chns:
		CRbkg_pattern = 'HTNtag_'+lumiStr+'_%s$BIN__$PROCESS' % chn
		SRbkg_pattern = 'DnnTprime_'+lumiStr+'_%s$BIN__$PROCESS' % chn
    #print'SRbkg_pattern: ',SRbkg_pattern
		if whichsignal=='BB':
			CRbkg_pattern = 'HTNtag_'+lumiStr+'_%s$BIN__$PROCESS' % chn
      SRbkg_pattern = 'DnnBprime_'+lumiStr+'_%s$BIN__$PROCESS' % chn

		if 'isCR' in chn: 
			cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(
				rfile, CRbkg_pattern, CRbkg_pattern + '__$SYSTEMATIC')
		else:
			#print 'I made it into the isSR condition'
			cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(
				rfile, SRbkg_pattern, SRbkg_pattern + '__$SYSTEMATIC')
		        
    CRsig_pattern = 'HTNtag_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn
		SRsig_pattern = 'DnnTprime_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn
		#CRsig_pattern = 'HTNtag_'+lumiStr+'_%s__' % chn +'TTM'+str(mass)+'__'
		#SRsig_pattern = 'DnnTprime_'+lumiStr+'_%s__' % chn +'TTM'+str(mass)+'__'
    if whichsignal=='BB':
 			CRsig_pattern = 'HTNtag_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn
	   	SRsig_pattern = 'DnnBprime_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn

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
		if 'CR' in chn:
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(bkg_procs[chn]), cb)
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(sig_procs), cb)
		else:
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(bkg_procs[chn]), cb)
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(sig_procs), cb)


def rename_and_write(cb):
	print '>> Setting standardised bin names...'
	ch.SetStandardBinNames(cb)
	
	writer = ch.CardWriter('limits_'+template+saveKey+'/'+str(eval(sys.argv[1]))+'/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
						   'limits_'+template+saveKey+'/'+str(eval(sys.argv[1]))+'/$TAG/common/$ANALYSIS_$CHANNEL.input.root')
	writer.SetVerbosity(1)
	writer.WriteCards('cmb', cb)
	for chn in chns:
		#print 'value of chn: ',chn
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
	

        ######Uncertainties from Dr Hogan's theta_config_template.py
	#cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')(['13TeV_R2016'], 1.025)(['13TeV_R2017'], 1.023)(['13TeV_R2018'], 1.025)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumi_$ERA', 'lnN', ch.SystMap('era')(['2016'], 1.025)(['2017'], 1.023)(['2018'], 1.025))
	#cb.cp().process(signal + allbkgs).channel(chnsE).AddSyst(cb, 'elIdSys', 'lnN', ch.SystMap('era')(['13TeV_R2016'], 1.027)(['13TeV_R2017'], 1.027)(['13TeV_R2018'], 1.027))
	cb.cp().process(signal + allbkgs).channel(chnsE).AddSyst(cb, 'elIdSys', 'lnN', ch.SystMap('era')(['2016'], 1.027)(['2017'], 1.027)(['2018'], 1.027)) 
	#cb.cp().process(signal + allbkgs).channel(chnsM).AddSyst(cb, 'muIdSys', 'lnN', ch.SystMap('era')(['13TeV_R2016'], 1.027)(['13TeV_R2017'], 1.027)(['13TeV_R2018'], 1.027))
	cb.cp().process(signal + allbkgs).channel(chnsM).AddSyst(cb, 'muIdSys', 'lnN', ch.SystMap('era')(['2016'], 1.027)(['2017'], 1.027)(['2018'], 1.027))
        #cb.cp().process([allbkgs[2]]).channel(chns).AddSyst(cb, 'QCDscale', 'lnN', ch.SystMap('era')(['13TeV_R2016'], 1.25)(['13TeV_R2017'], 1.25)(['13TeV_R2018'], 1.25))
        #cb.cp().process([allbkgs[0]]).channel(chns).AddSyst(cb, 'TTbarscale', 'lnN', ch.SystMap('era')(['13TeV_R2016'], 1.30)(['13TeV_R2017'], 1.30)(['13TeV_R2018'], 1.30))
        #cb.cp().process([allbkgs[1]]).channel(chns).AddSyst(cb, 'EWKscale', 'lnN', ch.SystMap('era')(['13TeV_R2016'], 1.25)(['13TeV_R2017'], 1.25)(['13TeV_R2018'], 1.25))


        ####Uncertainties from ROOT files########
	cb.cp().process(signal + allbkgs).channel(chnsE).AddSyst(cb, 'trigeffEl$ERA', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
	cb.cp().process(signal + allbkgs).channel(chnsM).AddSyst(cb, 'trigeffMu$ERA', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  ##cb.cp().process(ewk).channel(chns).AddSyst(cb, 'jsf_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))###jsf and pileup change to pdfNew. Check ewk in process
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Teff_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Tmis_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Heff_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Hmis_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Zeff_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Zmis_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Weff_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Wmis_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Beff_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Bmis_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Jeff_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Jmis_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
	#cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jer_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jer_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
	#cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'prefire_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7
  #cb.cp().process(signal + allbkgs).channel(chnsE).AddSyst(cb, 'trigeffEl', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chnsM).AddSyst(cb, 'trigeffMu', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(ewk).channel(chns).AddSyst(cb, 'jsf_$ERA', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))###jsf and pileup change to pdfNew. Check ewk in process
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Teff', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Tmis', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Heff', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Hmis', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Zeff', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Zmis', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Weff', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Wmis', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Beff', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Bmis', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  ##cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Jeff', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  ##cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Jmis', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
  #cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jer', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
	#cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jec', 'shape', ch.SystMap('era')(['13TeV_R2016'], 1.0)(['13TeV_R2017'], 1.0)(['13TeV_R2018'], 1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jer$ERA', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jec$ERA', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'prefire', 'shape', ch.SystMap('era')(['2016'], 1.0)(['2017'], 1.0)(['2018'], 1.0)) # Uncorrelated; Ex: B2G-19-001/AN2018_322_v7

 	#cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pdfNew', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pdfNew$ERA', 'shape', ch.SystMap()(1.0))
  cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pileup', 'shape', ch.SystMap()(1.0)) # Correlated: https://hypernews.cern.ch/HyperNews/CMS/get/b2g/1381.html
  cb.cp().process([allbkgs[1]]).channel(chns).AddSyst(cb, 'jsf', 'shape', ch.SystMap()(1.0))###jsf and pileup change to pdfNew. Check ewk in process, and add it back later!!!!!!!

	#if year=='2017':
	#	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'prefire', 'shape', ch.SystMap()(1.0))
	
	print 'allbkgsTop: ', allbkgs[0]
        print 'allbkgsEwk: ', allbkgs[1]
	print 'allbkgsQCD: ', allbkgs[2]
	#for proc in allbkgs:
#		if allbkgs[0]: cb.cp().process([proc[0]]).channel(chns).AddSyst(cb, 'muRFcorrdNewTop', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7 
#		elif allbkgs[1]: cb.cp().process([proc[1]]).channel(chns).AddSyst(cb, 'muRFcorrdNewEwk', 'shape', ch.SystMap()(1.0))
	cb.cp().process([allbkgs[0]]).channel(chns).AddSyst(cb, 'muRFcorrdNewTop', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7
	cb.cp().process([allbkgs[1]]).channel(chns).AddSyst(cb, 'muRFcorrdNewEwk', 'shape', ch.SystMap()(1.0))
	cb.cp().process([allbkgs[2]]).channel(chns).AddSyst(cb, 'muRFcorrdNewQCD', 'shape', ch.SystMap()(1.0))
	cb.cp().process(signal).channel(chns).AddSyst(cb, 'muRFcorrdNewSig', 'shape', ch.SystMap()(1.0)) # Correlated, PDF and QCD Scale (not recalculated in 2018); Ex: B2G-19-001/AN2018_322_v7



def add_autoMCstat(cb):
	print '>> Adding autoMCstats...'
	
	thisDir = os.getcwd()
	mass=0
	massList = range(900,1800+1,100)

	_bW0p0_tZ0p0_tH1p0='_bW0p0_tZ0p0_tH1p0'
        _bW0p0_tZ0p5_tH0p5='_bW0p0_tZ0p5_tH0p5'
        _bW0p0_tZ1p0_tH0p0='_bW0p0_tZ1p0_tH0p0'
        _bW0p5_tZ0p25_tH0p25='_bW0p5_tZ0p25_tH0p25'
        _bW1p0_tZ0p0_tH0p0='_bW1p0_tZ0p0_tH0p0'

        _tW0p0_bZ0p0_bH1p0='_tW0p0_bZ0p0_bH1p0'
        _tW0p0_bZ0p5_bH0p5='_tW0p0_bZ0p5_bH0p5'
        _tW0p0_bZ1p0_bH0p0='_tW0p0_bZ1p0_bH0p0'
        _tW0p5_bZ0p25_bH0p25='_tW0p5_bZ0p25_bH0p25'
        _tW1p0_bZ0p0_bH0p0='_tW1p0_bZ0p0_bH0p0'
	
	BRconfStr=str(eval(sys.argv[1]))
        print'BR string: ',BRconfStr

	for chn in chns+['cmb']:
        #for chn in chns:
		for mass in massList:
			chnDir = os.getcwd()+'/limits_'+template+saveKey+'/'+BRconfStr+'/'+chn+'/'+str(mass)+'/'
                	#chnDir = os.getcwd()+'/limits_'+template+saveKey+'/'
			print 'chnDir: ',chnDir
			os.chdir(chnDir)
			files = [x for x in os.listdir(chnDir) if '.txt' in x]
			for ifile in files:
				with open(chnDir+ifile, 'a') as chnfile: chnfile.write('* autoMCStats 1.')
			os.chdir(thisDir)

def create_workspace(cb):
	print '>> Creating workspace...'


	_bW0p0_tZ0p0_tH1p0='_bW0p0_tZ0p0_tH1p0'
  _bW0p0_tZ0p5_tH0p5='_bW0p0_tZ0p5_tH0p5'
  _bW0p0_tZ1p0_tH0p0='_bW0p0_tZ1p0_tH0p0'
  _bW0p5_tZ0p25_tH0p25='_bW0p5_tZ0p25_tH0p25'
  _bW1p0_tZ0p0_tH0p0='_bW1p0_tZ0p0_tH0p0'

  _tW0p0_bZ0p0_bH1p0='_tW0p0_bZ0p0_bH1p0'
  _tW0p0_bZ0p5_bH0p5='_tW0p0_bZ0p5_bH0p5'
  _tW0p0_bZ1p0_bH0p0='_tW0p0_bZ1p0_bH0p0'
  _tW0p5_bZ0p25_bH0p25='_tW0p5_bZ0p25_bH0p25'
  _tW1p0_bZ0p0_bH0p0='_tW1p0_bZ0p0_bH0p0'


	BRconfStr=str(eval(sys.argv[1]))
	for chn in ['cmb']+chns:
		chnDir = os.getcwd()+'/limits_'+template+saveKey+'/'+BRconfStr+'/'+chn+'/*'
		cmd = 'combineTool.py -M T2W -i '+chnDir+' -o workspace.root --parallel 4'
		os.system(cmd)


def go(cb):
	add_processes_and_observations(cb)
	add_systematics(cb)
	add_shapes(cb)
	#add_bbb(cb)
	rename_and_write(cb)
	add_autoMCstat(cb)
	create_workspace(cb)
	#print_cb(cb)


if __name__ == '__main__':
	cb = ch.CombineHarvester()
	#cb.SetVerbosity(20)
  _bW0p0_tZ0p0_tH1p0='_bW0p0_tZ0p0_tH1p0'
	_bW0p0_tZ0p5_tH0p5='_bW0p0_tZ0p5_tH0p5'
	_bW0p0_tZ1p0_tH0p0='_bW0p0_tZ1p0_tH0p0'
	_bW0p5_tZ0p25_tH0p25='_bW0p5_tZ0p25_tH0p25'
	_bW1p0_tZ0p0_tH0p0='_bW1p0_tZ0p0_tH0p0'
	
	_tW0p0_bZ0p0_bH1p0='_tW0p0_bZ0p0_bH1p0'
	_tW0p0_bZ0p5_bH0p5='_tW0p0_bZ0p5_bH0p5'
	_tW0p0_bZ1p0_bH0p0='_tW0p0_bZ1p0_bH0p0'
	_tW0p5_bZ0p25_bH0p25='_tW0p5_bZ0p25_bH0p25'
	_tW1p0_bZ0p0_bH0p0='_tW1p0_bZ0p0_bH0p0'
	
	year = '2016'
	#era = '13TeV_R'+year
	era = year
	lumiStr = ''
	lumiStrDir = ''
	if year=='2018': 
		lumiStr = '59p69fb'
		lumiStrDir = '59p69'
	if year=='2017': 
		lumiStr = '41p53fb'
		lumiStrDir = '41p53'
        if year=='2016': 
		lumiStr = '35p867fb'
		lumiStrDir = '35p867'

	tag = 'June2020' ##Tag and saveKey are used for output directory names
	saveKey = tag+'TTChiSquareand0p15Test'
        fileDir = '/uscms_data/d3/cholz/CMSSW_10_2_13/src/makeTemplates/'
        template = 'templatesCR_' ##Change template to template directory. e.g.: templatesSR_......
        if not os.path.exists('./limits_'+template+saveKey): os.system('mkdir ./limits_'+template+saveKey)

        BRconfStr=str(eval(sys.argv[1]))
	print'BR string: ',BRconfStr
        BRs={}
	if not os.path.exists('./limits_'+template+saveKey+str(eval(sys.argv[1]))): os.system('mkdir ./limits_'+template+saveKey+'/')

	if whichsignal=='TT':
        	BRs['BW']=[0.0,0.50,1.0,0.0,0.0]#,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
        	BRs['TH']=[0.5,0.25,0.0,1.0,0.0]#,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
        	BRs['TZ']=[0.5,0.25,0.0,0.0,1.0]#,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
        	nBRconf=len(BRs['BW'])
	elif whichsignal=='BB':
        	BRs['TW']=[0.0,0.50,1.0,0.0,0.0]#,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
        	BRs['BH']=[0.5,0.25,0.0,1.0,0.0]#,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]  # May or may not want to keep these lines, have to ask
        	BRs['BZ']=[0.5,0.25,0.0,0.0,1.0]#,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
        	nBRconf=len(BRs['TW'])

	#for BRind in range(nBRconf):
	#if whichsignal=='TT': BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
        #elif whichsignal=='BB': BRconfStr='_tW'+str(BRs['TW'][BRind]).replace('.','p')+'_bZ'+str(BRs['BZ'][BRind]).replace('.','p')+'_bH'+str(BRs['BH'][BRind]).replace('.','p')
	if whichsignal=='TT' and 'CRSR' in template:
                #os.system('cp '+'CRSR_June2020TT/templates_haddTT'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3.root ./limits_'+template+saveKey+'/')
		os.system('cp '+'CRSR_FullMuandSmoothJec_June2020TT/templates_haddTT'+BRconfStr+'_'+lumiStrDir+'_Combine_rebinned_stat0p3_smoothed.root ./limits_'+template+saveKey+'/')
        elif whichsignal=='TT' and 'CR' in template:
                #os.system('cp '+fileDir+template+'June2020TT/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3.root ./limits_'+template+'/')
		#os.system('cp '+'CR_FullMuAndCombine/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_rebinned_stat0p3.root ./limits_'+template+saveKey+'/')
		#os.system('cp '+'CR_SmoothJecandJerTT/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3_smoothed.root ./limits_'+template+saveKey+'/')
		#os.system('cp '+'CR_FullMuandSmoothJecandJer/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_rebinned_stat0p3_smoothed.root ./limits_'+template+saveKey+'/')
		#os.system('cp '+'CR_ChiSquared/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_chi2_rebinned_stat0p3_smoothed.root ./limits_'+template+saveKey+'/')
		#os.system('cp '+'CR_0p15Test'+BRconfStr+'_'+lumiStrDir+'_Combine_rebinned_stat0p15.root ./limits_'+template+saveKey+'/')
		os.system('cp '+'CR_0p15_ChiSquared'+BRconfStr+'_'+lumiStrDir+'_Combine_chi2_rebinned_stat0p15.root ./limits_'+template+saveKey+'/')
        elif whichsignal=='BB' and 'CRSR' in template:
		os.system('cp '+'CRSR_June2020BB/templates_DnnBprime'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3.root ./limits_'+template+saveKey+'/')
        elif whichsignal=='BB' and 'CR' in template:
                os.system('cp '+fileDir+template+'June2020BB/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3.root ./limits_'+template+saveKey+'/')

	#for BRind in range(nBRconf):
        #if whichsignal=='TT': BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
        #elif whichsignal=='BB': BRconfStr='_tW'+str(BRs['TW'][BRind]).replace('.','p')+'_bZ'+str(BRs['BZ'][BRind]).replace('.','p')+'_bH'+str(BRs['BH'][BRind]).replace('.','p')
	if whichsignal=='TT' and 'CRSR' in template:
		#rfile = 'CRSR_June2020TT/templates_haddTT'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3.root'
		rfile = 'CRSR_FullMuandSmoothJec_June2020TT/templates_haddTT'+BRconfStr+'_'+lumiStrDir+'_Combine_rebinned_stat0p3_smoothed.root'
	elif whichsignal=='TT' and 'CR' in template:
		#rfile = '../makeTemplates/'+template+'June2020TT/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3.root'
		#rfile = 'CR_FullMuAndCombine/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_rebinned_stat0p3.root'
		#rfile = 'CR_SmoothJecandJerTT/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3_smoothed.root'
		#rfile = 'CR_FullMuandSmoothJecandJer/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_rebinned_stat0p3_smoothed.root'
		#rfile = 'CR_ChiSquared/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_chi2_rebinned_stat0p3_smoothed.root'
		#rfile = 'CR_0p15Test/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_rebinned_stat0p15.root'
		rfile = 'CR_0p15_ChiSquared/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_chi2_rebinned_stat0p15.root'
        elif whichsignal=='BB' and 'CRSR' in template:
		rfile = 'CRSR_June2020BB/templates_haddBB'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3.root'
	elif whichsignal=='BB' and 'CR' in template:
		rfile = '../makeTemplates/'+template+'/templates_HTNtag'+BRconfStr+'_'+lumiStrDir+'_Combine_BKGNORM_rebinned_stat0p3.root'
	print'File: ',rfile
	#ttbkgs = ['ttnobb','ttbb'] # ['ttjj','ttcc','ttbb','ttbj']
	allbkgs = ['top','ewk','qcd']

	dataName = 'data_obs'
	tfile = TFile(rfile)
	allHistNames = [k.GetName() for k in tfile.GetListOfKeys() if not (k.GetName().endswith('Up') or k.GetName().endswith('Down'))]
	tfile.Close()
	chns = [hist[hist.find('fb_')+3:hist.find('__')] for hist in allHistNames if '__'+dataName in hist]

	chnsE = [chn for chn in chns if '_isE_' in chn]
	chnsM = [chn for chn in chns if '_isM_' in chn]
	bkg_procs = {chn:[hist.split('__')[-1] for hist in allHistNames if '_'+chn+'_' in hist and not (hist.endswith('Up') or hist.endswith('Down') or hist.endswith(dataName) or 'TTM' in hist or 'BBM' in hist)] for chn in chns}
	for cat in sorted(bkg_procs.keys()):
		print cat,bkg_procs[cat]
	if 'qcd' in bkg_procs[cat]:
		print '		Removing qcd ...'
		bkg_procs[cat]=bkg_procs[cat][:-1]
# 	if year=='2018':
# 		bkg_procs['isSR_isE_nHOT1p_nT0p_nW0p_nB4p_nJ9']=['ttbb', 'ttcc', 'ttjj', 'top']
	
	if whichsignal=='TT': sig_procs = ['TTM']
	elif whichsignal=='BB': sig_procs = ['BBM'] 	

	cats = {}
	for chn in chns: cats[chn] = [(0, '')]
	
	masses = ch.ValsFromRange('900:1800|100')	
	print 'masses: ',masses

	go(cb)

