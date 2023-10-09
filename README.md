# HMTntuple

Analysis nTuple for HMT trigger studies. This repository can do the following:

 - Run HMT emulator
   - `CSCShowerAnalyzer` writes emulator-check histograms
 - Run CA4 clustering on HMT hits
 - Save emulated/L1 LCT hits
 - Run standard muon reco [experimental]
 - `SimpleCSCshowerFilter` builds HMT tree to contain the above 

## Setup

```
cmsrel CMSSW_13_2_5
cd CMSSW_13_2_5/src
git clone git@github.com:kakwok/HMTntuple.git
cd HMTntuple/CSCShowerAnalyzer
scram b -j 8
```

## Running the code

For local testing, do:
```
cmsRun runCSCShowerAnalyzer_cfg.py inputFiles=file:~/eos/HLT/Commissioning2022/877caf18-4328-415e-bb74-b40adf51f9b4.root runNumber=351407 maxEvents=10
```

On lxplus, one can submit condor jobs with:
```
./cmsCondorData.py runCSCShowerAnalyzer_cfg.py $cmssw /eos/cms/store/user/kakwok/HLT/Commissioning2023/run370926  -n 2 -q workday -p /afs/cern.ch/user/k/kakwok/work/private/proxy -i list_370926
./sub_total.jobb
```

More example commands in `./test/run.sh`
