// -*- C++ -*-
//
// Package:    L1Trigger/CSCTriggerPrimitives
// Class:      SimpleCSCshowerFilter
//
/**\class SimpleCSCshowerFilter SimpleCSCshowerFilter.cc L1Trigger/CSCTriggerPrimitives/plugins/SimpleCSCshowerFilter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Ka Hei Martin Kwok
//         Created:  Thu, 07 Jul 2022 16:53:22 GMT
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/MuonReco/interface/MuonRecHitCluster.h"
#include "DataFormats/CSCDigi/interface/CSCShowerDigiCollection.h"
#include "DataFormats/CSCRecHit/interface/CSCRecHit2DCollection.h"

#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
//
// class declaration
//

class SimpleCSCshowerFilter : public edm::stream::EDFilter<> {
public:
  explicit SimpleCSCshowerFilter(const edm::ParameterSet&);
  ~SimpleCSCshowerFilter();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;
  //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  
  //void reset();
  //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

  // ----------member data ---------------------------
  //
  const edm::EDGetTokenT<reco::MuonRecHitClusterCollection> ca4CSCrechitClusters_token_;
  const edm::EDGetTokenT<edm::TriggerResults> triggerBitsToken_; 
  bool debug_;
  bool isHLT_PPZeroBias;
 
};

SimpleCSCshowerFilter::SimpleCSCshowerFilter(const edm::ParameterSet& iConfig) :
  ca4CSCrechitClusters_token_(consumes(iConfig.getParameter<edm::InputTag>("ca4CSCrechitClusters"))),
  triggerBitsToken_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("hltresults"))) 
{
  debug_ = iConfig.getParameter<bool>("debug");
}

SimpleCSCshowerFilter::~SimpleCSCshowerFilter() {
}

//
// member functions
//

// ------------ method called on each new Event  ------------
bool SimpleCSCshowerFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;

  edm::Handle<reco::MuonRecHitClusterCollection> ca4CSCrechitClusters;
  edm::Handle<edm::TriggerResults> triggerBits;

  auto const& clusters = iEvent.get(ca4CSCrechitClusters_token_ );
  iEvent.getByToken(triggerBitsToken_, triggerBits);

  const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);

  for (unsigned int i = 0, n = triggerBits->size(); i < n; ++i) {
      std::string hltPathNameReq = "HLT_ZeroBias_v";
      if ((names.triggerName(i)).find(hltPathNameReq) == std::string::npos) continue;
      if ((names.triggerName(i)).find_last_of("_") == std::string::npos) continue;
      isHLT_PPZeroBias = triggerBits->accept(i);
  }

  if (debug_){
    for(auto const& cls : clusters){
        std::cout<< "cls : size= "<<cls.size()<< " eta= "<<cls.eta()<<" phi= "<<cls.phi()<<"  time= "<<cls.time()<<" nStation10= "<<cls.nStation()<<std::endl;
    }   
  }
  return (clusters.size()>=1);
}


// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void SimpleCSCshowerFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(SimpleCSCshowerFilter);
