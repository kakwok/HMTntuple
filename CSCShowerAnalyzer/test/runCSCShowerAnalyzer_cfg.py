import sys
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from Configuration.Eras.Era_Run3_cff import Run3

isCondor = False 
outname = "HMTnTuple.root"

process = cms.Process("ANALYSIS", Run3)
process.load("FWCore.MessageService.MessageLogger_cfi")


## input to be set by driver script
process.source = cms.Source(
      "PoolSource",
      #fileNames = cms.untracked.vstring(""),
      fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2024I/ZeroBias/RAW/v1/000/386/417/00000/58319fe0-3d8a-4070-9b83-37fbcf7c070d.root'),
      inputCommands = cms.untracked.vstring( 'keep *')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)



process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string(outname)
                                   )


process.load("Configuration/StandardSequences/FrontierConditions_GlobalTag_cff")
process.load("Configuration/StandardSequences/GeometryRecoDB_cff")
process.load("Configuration/StandardSequences/MagneticField_cff")
#process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
#process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')

process.load("CalibMuon.CSCCalibration.CSCL1TPLookupTableEP_cff")

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_data', '')

process.load("EventFilter.DTRawToDigi.dtunpacker_cfi")
process.load("EventFilter.CSCRawToDigi.cscUnpacker_cfi")
process.unpacksequence = cms.Sequence(process.muonCSCDigis*process.muonDTDigis)


process.load("L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi")
process.cscTriggerPrimitiveDigis.CSCComparatorDigiProducer = "muonCSCDigis:MuonCSCComparatorDigi"
process.cscTriggerPrimitiveDigis.CSCWireDigiProducer = "muonCSCDigis:MuonCSCWireDigi"
process.cscTriggerPrimitiveDigis.commonParam.runME11ILT = False 
process.cscTriggerPrimitiveDigis.commonParam.runME21ILT = False

## update emulator loose thresholds
from custom_thresholds import update_thresholds
update_thresholds(process) 

#from L1Trigger.CSCTriggerPrimitives.CSCShowerAnalyzer_cfi import cscTriggerPrimitivesAnalyzer
from HMTntuple.CSCShowerAnalyzer.CSCShowerAnalyzer_cfi import cscTriggerPrimitivesAnalyzer


process.cscTriggerPrimitivesAnalyzer = cscTriggerPrimitivesAnalyzer
process.cscTriggerPrimitivesAnalyzer.debug=cms.bool(False)

process.simpleCSCshowerTreeMaker = cms.EDFilter("SimpleCSCshowerTreeMaker",
    muons = cms.InputTag("muons"),
    dataLCTShower = cms.InputTag("muonCSCDigis","MuonCSCShowerDigi"),
    emulLCTShower = cms.InputTag("cscTriggerPrimitiveDigis"),
    ca4CSCrechitClusters = cms.InputTag("ca4CSCrechitClusters"),
    recHitLabel = cms.InputTag("csc2DRecHits"),
    AsL1filter = cms.bool(True),
    AsRecofilter = cms.bool(False),
    debug = cms.bool(True)
)
process.l1filter_step = cms.Path(process.simpleCSCshowerTreeMaker)
process.l1sequence = cms.Sequence(process.cscTriggerPrimitiveDigis)
#process.l1sequence += process.cscTriggerPrimitivesAnalyzer
#process.cscShowerAnalyzer = cms.Path(cscTriggerPrimitivesAnalyzer)


#import EventFilter.DTRawToDigi.dtunpacker_cfi
#from RecoLocalMuon.DTRecHit.dt1DRecHits_LinearDriftFromDB_cfi import *
#from RecoLocalMuon.CSCRecHitD.cscRecHitD_cfi import *

process.dummy1 = cms.ESSource("EmptyESSource",
                                  recordName = cms.string("CSCIndexerRecord"),
                                  firstValid = cms.vuint32(1),
                                  iovIsRunNotTime = cms.bool(True)
                              )

process.dummy2 = cms.ESSource("EmptyESSource",
                                  recordName = cms.string("CSCChannelMapperRecord"),
                                  firstValid = cms.vuint32(1),
                                  iovIsRunNotTime = cms.bool(True)
                              )

process.CSCIndexerESProducer = cms.ESProducer("CSCIndexerESProducer", AlgoName = cms.string("CSCIndexerStartup") )
process.CSCChannelMapperESProducer = cms.ESProducer("CSCChannelMapperESProducer", AlgoName = cms.string("CSCChannelMapperStartup") )
process.load('RecoLocalMuon.CSCRecHitD.cscRecHitD_cfi')
#process.load('RecoLocalMuon.DTRecHit.dt1DRecHits_LinearDriftFromDB_cfi')
#process.load('RecoLocalMuon.Configuration.RecoLocalMuon_cff')
#process.load('RecoMuon.Configuration.RecoMuonPPonly_cff')
process.reco = cms.Path(process.csc2DRecHits )
#process.reco = cms.Path(process.muonlocalreco * process.standalonemuontracking)
process.recoSeq = cms.Sequence(
                process.csc2DRecHits,
                process.globalreco_trackingTask,
                process.muonGlobalRecoTask)


#process.raw2digi_step = cms.Path(process.RawToDigi)
#process.L1Reco_step = cms.Path(process.L1Reco)
#process.reconstruction_step = cms.Path(process.reconstruction)
#process.reconstruction_step = cms.Path(process.recoSeq)


import RecoMuon.MuonRechitClusterProducer.cscRechitClusterProducer_cfi as CSCcluster 

process.ca4CSCrechitClusters= CSCcluster.cscRechitClusterProducer.clone(
    recHitLabel = "csc2DRecHits",
    nRechitMin  = 50,
    rParam      = 0.4,
    nStationThres = 10, 
) 

process.producer = cms.Path(process.ca4CSCrechitClusters)


outf = "output_reco.root"

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string(outf), # choose your output file
    outputCommands = cms.untracked.vstring(
              'drop *',
              #'keep *',
              #'keep *_gen*_*_*',
              'keep *ShowerDigi*_*cscTriggerPrimitive*_*_*',
              'keep *_csc2DRecHits_*_*',
              #'keep *_muons*_*_*',
              'keep *_ca4*_*_*',
    ),
    #SelectEvents = cms.untracked.PSet(
    #  SelectEvents = cms.vstring("l1filter_step")
    #),

)


#process.end = cms.EndPath(process.out) 
process.end = cms.EndPath() 

process.p = cms.Path(process.unpacksequence * process.l1sequence )

process.schedule = cms.Schedule(process.p, 
                                process.reco,
                                #process.reconstruction_step, 
                                process.producer,
                                process.l1filter_step,
                                process.end)
