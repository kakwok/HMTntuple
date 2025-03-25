import FWCore.ParameterSet.Config as cms

def update_thresholds(process):
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
    return 
