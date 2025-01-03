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

def add_mdsTables(process):

    process.ca4CSCrechitClusters = cscRechitClusterProducer    
    process.ca4DTrechitClusters = dtRechitClusterProducer
    process.cscMDSClusterTable = cscMDSClusterTable
    process.dtMDSClusterTable = dtMDSClusterTable 

    process.MDSTask = cms.Task(process.ca4CSCrechitClusters)
    process.MDSTask.add(process.ca4DTrechitClusters)
    process.MDSTask.add(process.cscMDSClusterTable)
    process.MDSTask.add(process.dtMDSClusterTable)

    process.nanoTableTaskCommon.add(process.MDSTask)

    return process
