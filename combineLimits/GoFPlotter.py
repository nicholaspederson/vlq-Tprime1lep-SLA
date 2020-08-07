import sys, subprocess, ROOT


RFile1=ROOT.TFile.Open('higgsCombineTest.GoodnessOfFit.mH120.123456.root')
limit1=RFile1.Get('limit')
#RFile2=ROOT.TFile.Open('higgsCombineNoToys.GoodnessOfFit.mH120.root')
#limit2=RFile2.Get('limit')
GoF_can=ROOT.TCanvas('GoodnessOfFit')
#limit1.GetXaxis().
limit1.Draw('limit','','pe')
line=ROOT.TLine(205.8,0,205.8,25)
line.SetLineColor(2)
line.SetLineWidth(1)
GoF_can.Update()
line.Draw('Draw')

#GoF_can.Print('GoodnessOfFitCR.png','png')

