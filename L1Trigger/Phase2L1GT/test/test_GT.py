# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --conditions 125X_mcRun4_realistic_v2 -n 2 --era Phase2C17I13M9 --eventcontent FEVTDEBUGHLT -s RAW2DIGI,L1TrackTrigger,L1 --datatier GEN-SIM-DIGI-RAW-MINIAOD --fileout file:test.root --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring,L1Trigger/Configuration/customisePhase2.addHcalTriggerPrimitives,L1Trigger/Configuration/customisePhase2FEVTDEBUGHLT.customisePhase2FEVTDEBUGHLT,L1Trigger/Configuration/customisePhase2TTNoMC.customisePhase2TTNoMC --geometry Extended2026D88 --nThreads 8 --filein /store/mc/Phase2Fall22DRMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2_ext1-v1/30000/000c5e5f-78f7-44ee-95fe-7b2f2c2e2312.root --mc --customise_commands=process.source.inputCommands = cms.untracked.vstring("keep *", "drop l1tPFJets_*_*_*")
import FWCore.ParameterSet.Config as cms  # Import CMS python class definitions such as Process, Source, and EDProducer

# Import contents of a file
from Configuration.Eras.Era_Phase2C17I13M9_cff import Phase2C17I13M9
from L1Trigger.Phase2L1GT.l1tGTSingleObjectCond_cfi import l1tGTSingleObjectCond
from L1Trigger.Phase2L1GT.l1tGTDoubleObjectCond_cfi import l1tGTDoubleObjectCond
from L1Trigger.Phase2L1GT.l1tGTTripleObjectCond_cfi import l1tGTTripleObjectCond
from L1Trigger.Phase2L1GT.l1tGTQuadObjectCond_cfi import l1tGTQuadObjectCond
from L1Trigger.Phase2L1GT.l1tGTAlgoBlockProducer_cff import algorithms

# Set up a process, named L1TEmulation in this case
process = cms.Process('L1TEmulation',Phase2C17I13M9)

# import of standard 
# they live in /cvmfs/cms.cern.ch/el8_amd64_gcc12/cms/cmssw/CMSSW_14_2_1/src/Configuration/Geometry/python
# they are python modules that serve as configuration fragments files is CMSSW
# they are python modules that serve as configuration initializer files is CMSSW
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
# process.load('Configuration.Geometry.GeometryExtended2025Reco_cff')
# process.load('Configuration.Geometry.GeometryExtended2026D110Reco_cff')   # D110 is (Current Phase-2 baseline from CMSSW_14_1_0_pre2) not sure if it's ok to use with CMSSW 14-2-1 
                                                                            # Benjamin suggested to replace *2026* with *Run4* and go for it
process.load('Configuration.Geometry.GeometryExtendedRun4D110Reco_cff') 
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Configure the object that reads the input file
# The following files are probably not working, replaced them with new ones
# process.source = cms.Source("PoolSource",
#                             fileNames=cms.untracked.vstring(
# "/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_L1TFix_Trk1GeV_131X_mcRun4_realistic_v9-v1/50000/005bc30b-cf79-4b3b-9ec1-a80e13072afd.root",
#             "/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_L1TFix_Trk1GeV_131X_mcRun4_realistic_v9-v1/50000/009bd7ba-4295-46ef-a5bc-9eb3d2cd3cf7.root",
#             "/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_L1TFix_Trk1GeV_131X_mcRun4_realistic_v9-v1/50000/017a99d2-4636-4584-97d0-d5499c3b453c.root",
#             "/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_L1TFix_Trk1GeV_131X_mcRun4_realistic_v9-v1/50000/02020287-a16f-41db-8021-f9bcd272f6c9.root",
#             "/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_L1TFix_Trk1GeV_131X_mcRun4_realistic_v9-v1/50000/02ca41cb-9638-4703-88b7-799c30fd2656.root",
#             "/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_L1TFix_Trk1GeV_131X_mcRun4_realistic_v9-v1/50000/03171e00-8880-4c09-807a-0c1d5bac2797.root",
#             "/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_L1TFix_Trk1GeV_131X_mcRun4_realistic_v9-v1/50000/04c836c3-66f4-44d5-a8fd-2faf5e4aa623.root",                            ),
# )
process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring(
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/00c7f40e-b44e-4eea-a86b-def8f7d82b0e.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/02504470-83bc-49bf-adc4-b74306efbd0d.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/033d49d4-2f2d-44d4-9b27-9f3edd36cef3.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/039e692f-3423-4290-b9ce-5c55d00de1f1.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/04c30a1a-dc16-4711-bde4-bdbd1d919b8c.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/0e1e8cf8-d4ac-4402-aed3-dc3464acfaaf.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/0f1f8047-b0c9-4360-9b83-2f74b9ce4acf.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/11d0767a-8328-427b-ba64-87e63b2f76e7.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/16a7dad1-a5ab-41a3-8689-f2adae908172.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/19fb47dd-a610-49f9-9b8f-369c5519a6d4.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/1b03b34d-1807-4aaf-818a-0bf548de10ef.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/23c66f66-4daa-411b-958e-41ec2111d927.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/27437ae0-e9b6-40ee-9dca-a6bb81a2d133.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/27718d3a-01f6-41f1-a0f4-09f39e3461c5.root",
"/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/130000/2910f2cc-44a6-489d-b913-b98fe4577678.root",                          
                            ),
)

# maximum number of events to process during the job.
# PSet = parameter set = container for parameter config in CMSSW
# untracked --> not tracked in the metadata
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(10000)) # number of events



process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step1 nevts:2'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition - Configure the object that writes an output file
process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW-MINIAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:test.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
# Configure an object that produces a new data object

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '125X_mcRun4_realistic_v2', '')

# Path and EndPath definitions - Configure a path and endpath to run the producer and output modules
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)


#GT emulator
process.load('L1Trigger.Configuration.GTemulator_cff')
process.GTemulation_step = cms.Path(process.GTemulator)

process.load('L1Trigger.Phase2L1GT.l1tGTMenu_cff')
from L1Trigger.Phase2L1GT.l1tGTAlgoBlockProducer_cff import collectAlgorithmPaths

# # !! implement a single CL2JetsSC8 algorithm with a p_T > 25
# # avoid underscore symbol in processes - illegal
# process.CL2JetsSC825 = l1tGTSingleObjectCond.clone(
#     # No ambiguities, thus everything in the top level PSet
#     tag = cms.InputTag("l1tGTProducer", "CL2JetsSC8"),
#     maxAbsEta = cms.double(2.4),
#     minPt = cms.double(25)
# )

# # here underscore is legal. create the path and append it in the algorithms.
# # don't forget to add it in the schedule definition part
# process.pCL2JetsSC8_25 = cms.Path(process.CL2JetsSC825) # create the path
# algorithms.append(cms.PSet(expression=cms.string("pCL2JetsSC8_25")))

process.GToutput = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('drop *',
       #'keep *_l1ctLayer2*_*',
       #'keep *_l1tLayer2EG_*_*',
       #'keep *l1tLayer2EG*_*_*_L1TEmulation',
       'keep *P2GT*_*_*_L1TEmulation',
    ),
    fileName=cms.untracked.string("l1t_emulation.root")
    )

process.pGToutput = cms.EndPath(process.GToutput) 

process.load('L1Trigger.Phase2L1GT.l1tGTBoardWriterVU13P_cff')

process.pBoardDataInputVU13P = cms.EndPath(process.BoardDataInputVU13P)
process.pBoardDataOutputObjectsVU13P = cms.EndPath(process.BoardDataOutputObjectsVU13P)
process.pAlgoBitBoardDataVU13P = cms.EndPath(process.AlgoBitBoardDataVU13P)

process.BoardDataInputVU13P.maxEvents = cms.untracked.uint32(96) # number of output events per file
process.BoardDataOutputObjectsVU13P.maxEvents = cms.untracked.uint32(96)  # number of output events per file
process.AlgoBitBoardDataVU13P.maxEvents = cms.untracked.uint32(96)  # number of output events per file


# Schedule definition
# in the process.schedule you can add the process.pCL2JetsSC8_25 part, unless it includes the *collectAlgorithmPaths(process) statement,
# because this automatically include all the paths and if you also include it manually, it will crash because you've added it twice
process.schedule = cms.Schedule(process.raw2digi_step,process.L1simulation_step,process.GTemulation_step, *collectAlgorithmPaths(process), process.pGToutput,
                                process.pBoardDataInputVU13P, process.pBoardDataOutputObjectsVU13P, process.pAlgoBitBoardDataVU13P, process.endjob_step)

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
# process.options.numberOfThreads = 4
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.aging
from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000 

#call to customisation function customise_aging_1000 imported from SLHCUpgradeSimulations.Configuration.aging
process = customise_aging_1000(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customisePhase2
from L1Trigger.Configuration.customisePhase2 import addHcalTriggerPrimitives 

#call to customisation function addHcalTriggerPrimitives imported from L1Trigger.Configuration.customisePhase2
process = addHcalTriggerPrimitives(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customisePhase2FEVTDEBUGHLT
from L1Trigger.Configuration.customisePhase2FEVTDEBUGHLT import customisePhase2FEVTDEBUGHLT 

#call to customisation function customisePhase2FEVTDEBUGHLT imported from L1Trigger.Configuration.customisePhase2FEVTDEBUGHLT
process = customisePhase2FEVTDEBUGHLT(process)

# Automatic addition of the customisation function from L1Trigger.Configuration.customisePhase2TTNoMC
from L1Trigger.Configuration.customisePhase2TTNoMC import customisePhase2TTNoMC 

#call to customisation function customisePhase2TTNoMC imported from L1Trigger.Configuration.customisePhase2TTNoMC
process = customisePhase2TTNoMC(process)

# End of customisation functions


# Customisation from command line

process.source.inputCommands = cms.untracked.vstring("keep *", "drop l1tPFJets_*_*_*", "drop l1tTkPrimaryVertexs_L1TkPrimaryVertex_*_*")
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
