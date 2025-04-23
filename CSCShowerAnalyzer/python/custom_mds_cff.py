import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

# CSC clusters
from RecoMuon.MuonRechitClusterProducer.cscRechitClusterProducer_cfi import cscRechitClusterProducer
from RecoMuon.MuonRechitClusterProducer.dtRechitClusterProducer_cfi import dtRechitClusterProducer 

cscMDSClusterTable = cms.EDProducer("SimpleMuonRecHitClusterFlatTableProducer",
    src  = cms.InputTag("ca4CSCrechitClusters"),
    name = cms.string("cscMDSHLTCluster"),
    doc  = cms.string("MDS cluster at HLT"),
    variables = cms.PSet(
        eta = Var("eta", float, doc="cluster eta"),
        phi = Var("phi", float, doc="cluster phi"),
        x   = Var("x"  , float, doc="cluster x"),
        y   = Var("y"  , float, doc="cluster y"),
        z   = Var("z"  , float, doc="cluster z"),
        r   = Var("r"  , float, doc="cluster r"),
        size   = Var("size"  , int, doc="cluster size"),
        nStation   = Var("nStation"  , int, doc="cluster nStation"),
        avgStation   = Var("avgStation"  , float, doc="cluster avgStation"),
        nMB1   = Var("nMB1"  , int, doc="cluster nMB1"),
        nMB2   = Var("nMB2"  , int, doc="cluster nMB2"),
        nME11   = Var("nME11"  , int, doc="cluster nME11"),
        nME12   = Var("nME12"  , int, doc="cluster nME12"),
        nME41   = Var("nME41"  , int, doc="cluster nME41"),
        nME42   = Var("nME42"  , int, doc="cluster nME42"),
        time   = Var("time"  , float, doc="cluster time = avg cathode and anode time"),
        timeSpread   = Var("timeSpread"  , float, doc="cluster timeSpread")
    )
)

dtMDSClusterTable = cscMDSClusterTable.clone(
    src = cms.InputTag("ca4DTrechitClusters"),
    name= cms.string("dtMDSHLTCluster")
)

from HMTntuple.CSCShowerAnalyzer.cscShowerDigiTable_cfi import cscShowerDigiTable
from HMTntuple.CSCShowerAnalyzer.cscMDSshowerTable_cfi import cscMDSshowerTable 
from HMTntuple.CSCShowerAnalyzer.dtMDSshowerTable_cfi import dtMDSshowerTable 

dataCSCdigiTable = cscShowerDigiTable.clone(
    LCTShower = cms.InputTag("muonCSCDigis","MuonCSCShowerDigi"),
    name = cms.string("lct")
)
emulCSCdigiTable = cscShowerDigiTable.clone(
    LCTShower =  cms.InputTag("cscTriggerPrimitiveDigis"),
    name = cms.string("elct")
)

from HMTntuple.CSCShowerAnalyzer.cscRechitsTable_cfi import cscRechitsTable 
from HMTntuple.CSCShowerAnalyzer.dtRechitsTable_cfi import dtRechitsTable 
from HMTntuple.CSCShowerAnalyzer.rpcRechitsTable_cfi import rpcRechitsTable 
from HMTntuple.CSCShowerAnalyzer.cscSegmentsTable_cfi import cscSegmentsTable 
from HMTntuple.CSCShowerAnalyzer.dtSegmentsTable_cfi import dtSegmentsTable 

cscMDSshowerTable = cscMDSshowerTable.clone( 
    name = cms.string("cscMDSCluster"),
    recHitLabel = cms.InputTag("csc2DRecHits"),
    segmentLabel = cms.InputTag("dt4DSegments"),
    rpcLabel = cms.InputTag("rpcRecHits")
)
dtMDSshowerTable = dtMDSshowerTable.clone( 
    name = cms.string("dtMDSCluster"),
    recHitLabel = cms.InputTag("dt1DRecHits"),
    rpcLabel = cms.InputTag("rpcRecHits")
)

cscRechitsTable = cscRechitsTable.clone( 
    recHitLabel = cms.InputTag("csc2DRecHits")
)
dtRechitsTable = dtRechitsTable.clone( 
    recHitLabel = cms.InputTag("dt1DRecHits")
)
rpcRechitsTable = rpcRechitsTable.clone( 
    recHitLabel = cms.InputTag("rpcRecHits")
)
cscSegmentsTable = cscSegmentsTable.clone( 
    segmentLabel = cms.InputTag("cscSegments")
)
dtSegmentsTable = dtSegmentsTable.clone( 
    segmentLabel = cms.InputTag("dt4DSegments")
)


def add_mdsTables(process, MDSshowerDigi=False,saveRechits=False):

    # produce the tables for offline clusters 
    process.cscMDSshowerTable = cscMDSshowerTable    
    process.dtMDSshowerTable = dtMDSshowerTable   
    # produce the HLT clusters 
    process.ca4CSCrechitClusters = cscRechitClusterProducer    
    process.ca4DTrechitClusters = dtRechitClusterProducer
    # produce the tables for HLT clusters 
    process.cscMDSClusterTable = cscMDSClusterTable
    process.dtMDSClusterTable = dtMDSClusterTable 

    process.MDSTask = cms.Task(process.ca4CSCrechitClusters)
    process.MDSTask.add(process.ca4DTrechitClusters)
    process.MDSTask.add(process.cscMDSClusterTable)
    process.MDSTask.add(process.dtMDSClusterTable)
    process.MDSTask.add(process.cscMDSshowerTable)
    process.MDSTask.add(process.dtMDSshowerTable)

    if MDSshowerDigi:
        process.load("CalibMuon.CSCCalibration.CSCL1TPLookupTableEP_cff")
        process.load("L1Trigger.CSCTriggerPrimitives.cscTriggerPrimitiveDigis_cfi")
        process.cscTriggerPrimitiveDigis.CSCComparatorDigiProducer = "muonCSCDigis:MuonCSCComparatorDigi"
        process.cscTriggerPrimitiveDigis.CSCWireDigiProducer = "muonCSCDigis:MuonCSCWireDigi"
        process.cscTriggerPrimitiveDigis.commonParam.runME11ILT = False
        process.cscTriggerPrimitiveDigis.commonParam.runME21ILT = False
        process.cscTriggerPrimitiveDigis.showerParam.cathodeShower.showerThresholds = cms.vuint32(
            # ME1/1
            100, 100, 100,
            # ME1/2
            10000, 10000, 10000,
            # ME1/3
            10000, 10000, 10000,
            # ME2/1
            6, 33, 35,
            # ME2/2
            10000, 10000, 10000,
            # ME3/1
            6, 31, 33,
            # ME3/2
            10000, 10000, 10000,
            # ME4/1
            6, 34, 36,
            # ME4/2
            10000, 10000, 10000
        ) 
        process.cscTriggerPrimitiveDigis.showerParam.anodeShower.showerThresholds = cms.vuint32(
            # ME1/1
            140, 140, 140,
            # ME1/2
            140, 140, 140,
            # ME1/3
            7, 14, 18,
            # ME2/1
            12, 56, 58,
            # ME2/2
            12, 28, 32,
            # ME3/1
            12, 55, 57,
            # ME3/2
            12, 26, 34,
            # ME4/1
            12, 62, 64,
            # ME4/2
            12, 27, 31
        ) 
        process.dataCSCdigiTable = dataCSCdigiTable 
        process.emulCSCdigiTable = emulCSCdigiTable 

        process.MDSTask.add(process.cscTriggerPrimitiveDigis)
        process.MDSTask.add(process.dataCSCdigiTable)
        process.MDSTask.add(process.emulCSCdigiTable)

    if saveRechits:
        process.cscRechitsTable = cscRechitsTable
        process.dtRechitsTable = dtRechitsTable
        process.rpcRechitsTable = rpcRechitsTable
        process.cscSegmentsTable = cscSegmentsTable 
        process.dtSegmentsTable = dtSegmentsTable 
        process.MDSTask.add(process.cscRechitsTable)
        process.MDSTask.add(process.dtRechitsTable)
        process.MDSTask.add(process.rpcRechitsTable)
        process.MDSTask.add(process.cscSegmentsTable)
        process.MDSTask.add(process.dtSegmentsTable)


    process.nanoTableTaskCommon.add(process.MDSTask)

    return process
