import FWCore.ParameterSet.Config as cms

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/cvmfs/cms-griddata.cern.ch/phys_generator/gridpacks_tarball/pp/13TeV/madgraphMLM/TT_EFT/TT01j2lBSMRef_slc7_amd64_gcc10_CMSSW_12_4_25_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(False)
)

#Link to datacards:
# https://github.com/HephyAnalysisSW/genproductions/tree/mg265UL/bin/MadGraph5_aMCatNLO/addons/cards/SMEFTsim_topU3l_MwScheme_UFO/TT01j2lCARef


import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:doShowerKt = off',
            'JetMatching:qCut = 30.',
            'JetMatching:nQmatch = 5',
            'JetMatching:nJetMax = 1',
            'TimeShower:mMaxGamma = 1.0'
        ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'processParameters',
            'pythia8PSweightsSettings'
        )
    ),
    comEnergy = cms.double(13000),
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(1),
)

LHE_Mtt_700to900_filter = cms.EDFilter("LHEmttFilter",
 ptMin = cms.double(0.0),
 MinInvMass = cms.double(700),
 MaxInvMass = cms.double(900),
 src = cms.InputTag("externalLHEProducer")
)

ProductionFilterSequence = cms.Sequence(generator*LHE_Mtt_700to900_filter)

