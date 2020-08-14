import sys, subprocess, ROOT


run_name='Toys500Sig1FullMuandCombine'
expectSignal='1'

post_file = ROOT.TFile.Open('fitDiagnostics'+run_name+'.root')
tree_fit_sb = post_file.Get('tree_fit_sb')

# Final plotting
result_can = ROOT.TCanvas('sigpull_can','sigpull_can',800,700)

# fit_status>=0 just ensures you aren't including fits that failed
tree_fit_sb.Draw("(r-"+expectSignal+")/(rHiErr*(r<"+expectSignal+")+rLoErr*(r>"+expectSignal+"))>>sigpull(20,-5,5)","fit_status>=0")
tree_fit_sb.Draw("(r-"+expectSignal+")>>sigstrength(20,-1,1)","fit_status>=0")

hsigpull = ROOT.gDirectory.Get('sigpull')
hsignstrength = ROOT.gDirectory.Get('sigstrength')

hsigpull.Fit("gaus","L")
hsigpull.SetTitle(run_name)
hsigpull.GetXaxis().SetTitle('(r-'+expectSignal+')/rErr')
result_can.cd()
hsigpull.Draw('pe')
result_can.Print(run_name+'_sigpull.png','png')

hsignstrength.Fit("gaus","L")
hsignstrength.SetTitle(run_name)
hsignstrength.GetXaxis().SetTitle('r-'+expectSignal)
result_can.cd()
hsignstrength.Draw('pe')
result_can.Print(run_name+'_sigstrength.png','png')
