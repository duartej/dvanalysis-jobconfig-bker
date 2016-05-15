# My options
readAOD = False

#--------------------------------------------------------------
# control input
#--------------------------------------------------------------
# --- specify input type
if not 'readAOD' in dir():
  readAOD = True
readESD = not readAOD

#--------------------------------------------------------------
# Event related parameters
#--------------------------------------------------------------

from AthenaCommon.AthenaCommonFlags import athenaCommonFlags
  
if readESD:
    athenaCommonFlags.FilesInput = [ 'root://eosatlas.cern.ch//eos/atlas/user/d/duarte/datasets/mc15_13TeV.402721.PythiaRhad_AUET2BCTEQ6L1_gen_gluino_p1_1400_qq_1270_1ns.recon.ESD.e4732_s2770_s2183_r6869/ESD.07397538._000001.pool.root.1'
                    ]
elif readAOD:
  athenaCommonFlags.FilesInput = [ "AOD.pool.root" ]

import AthenaPython.ConfigLib as apcl
cfg = apcl.AutoCfg(name = 'InDetRecExampleAutoConfig', input_files=athenaCommonFlags.FilesInput())
cfg.configure_job()


#--------------------------------------------------------------
# control output (here so RecExCommon via auto-config doesn't delete the global flags)
#--------------------------------------------------------------
# --- controls what is written out. ESD includes AOD, so it's normally enough
doWriteESD = False and readESD
#doWriteAOD = False
doWriteAOD = True

#--------------------------------------------------------------
# control algorithms to be rerun
#--------------------------------------------------------------
# --- run InDetRecStatistics (only possible if readESD = True)
doInDetRecStatistics = True and readESD
# --- refit the EXISTING tracks in ESD (only possible if readESD = True)
doRefitTracks = False and readESD
# --- redo the pattern reco and the tracking (do not use that in conjunction with doRefitTracks above)
redoPatternRecoAndTracking = False and not doRefitTracks and readESD
# --- redo primary vertexing (will be set to true later automatically if you redid the tracking and want to redo the TrackParticle creation)
reDoPrimaryVertexing = False
# --- redo particle creation (recommended after revertexing on ESD, otherwise trackparticles are inconsistent)
reDoParticleCreation = False and readESD and reDoPrimaryVertexing
# --- redo conversion finding
reDoConversions = False
# --- redo V0 finding
reDoV0Finder = False
 
#--------------------------------------------------------------
# Control - standard options (as in jobOptions.py)
#--------------------------------------------------------------
# --- Set output level threshold (2=DEBUG, 3=INFO, 4=WARNING, 5=ERROR, 6=FATAL )
OutputLevel     = INFO
# --- produce an atlantis data file
doJiveXML       = False
# --- run the Virtual Point 1 event visualisation
doVP1           = False
# --- do auditors ?
doAuditors      = True

import os
if os.environ['CMTCONFIG'].endswith('-dbg'):
  # --- do EDM monitor (debug mode only)
  doEdmMonitor    = True
  # --- write out a short message upon entering or leaving each algorithm
  doNameAuditor   = True
else:
  doEdmMonitor    = False
  doNameAuditor   = False

# safety section ... redoing tracking/vertexing is a tricky business to stay consistent ...
if redoPatternRecoAndTracking and reDoParticleCreation:
  reDoPrimaryVertexing = True

if not (readESD or readAOD):
  print "You have to turn on reading of ESD or AOD! That's the purpose of this jobO!"
if readESD and readAOD:
  print "I can either read ESD or AOD but not both at the same time! Turn one or the other off!"
if readESD and reDoPrimaryVertexing and not reDoParticleCreation:
  print "INFO! You are running on ESD, redoing the vertexing but not recreating the TrackParticles!"
  print "INFO! To avoid inconsistencies do not use the old track particles in conjunction with the new vertex!"
  if doWriteESD or doWriteAOD:
    print "INFO! To avoid inconsistencies the old track particle (truth) container will not be in the new ESD/AOD!"
if readAOD and reDoPrimaryVertexing:
  print "INFO! You are running on AOD, and redoing the vertexing. At the moment new track particles cannot be made from old ones."
  print "INFO! To avoid inconsistencies do not use the old track particles in conjunction with the new vertex!"
  if doWriteAOD:
    print "INFO! To avoid inconsistencies the old track particle (truth) container will not be in the new AOD!"
if doRefitTracks and (reDoPrimaryVertexing or reDoParticleCreation):
  print "INFO! You are refitting tracks and also revertex and/or recreate track particles"
  print "INFO! The input for that will be the refitted tracks!"

#--------------------------------------------------------------
# Additional Detector setup
#--------------------------------------------------------------

from RecExConfig.RecFlags import rec
rec.Commissioning=False

# [JDC ADDED]
#rec.doESDReconstruction = True

from AthenaCommon.DetFlags import DetFlags 
# --- switch on InnerDetector
DetFlags.ID_setOn()
# --- and switch off all the rest
DetFlags.Calo_setOff()
DetFlags.Muon_setOff()
# ---- switch parts of ID off/on as follows (always use both lines)
#DetFlags.pixel_setOff()
#DetFlags.detdescr.pixel_setOn()
#DetFlags.SCT_setOff()
#DetFlags.detdescr.SCT_setOn()
#DetFlags.TRT_setOff()
#DetFlags.detdescr.TRT_setOn()

# --- printout
DetFlags.Print()

#--------------------------------------------------------------
# Load Reconstruction configuration for tools only
#--------------------------------------------------------------
#--------------------------------------------------------------
# Load InDet configuration
#--------------------------------------------------------------
import MagFieldServices.SetupField

from AthenaCommon.GlobalFlags import globalflags

# FORCED [JDC]
redoPatternRecoAndTracking = True
reDoParticleCreation = True
# -- FORCED
# --- setup InDetJobProperties
from InDetRecExample.InDetJobProperties import InDetFlags
InDetFlags.doTruth            = (globalflags.DataSource == 'geant4' and globalflags.InputFormat == "pool")
InDetFlags.preProcessing      = redoPatternRecoAndTracking
InDetFlags.doPRDFormation        = False                       # those two will be (later) automatically false if
InDetFlags.doSpacePointFormation = redoPatternRecoAndTracking  # preProcessing is false
InDetFlags.doNewTracking      = redoPatternRecoAndTracking
InDetFlags.doiPatRec          = False
InDetFlags.doxKalman          = False
InDetFlags.doLowPt            = False
InDetFlags.doBackTracking     = False # [JDC]redoPatternRecoAndTracking
InDetFlags.doTRTStandalone    = False # [JDC]redoPatternRecoAndTracking
InDetFlags.doTrtSegments      = redoPatternRecoAndTracking
InDetFlags.postProcessing     = reDoPrimaryVertexing or reDoParticleCreation or reDoConversions or doInDetRecStatistics or reDoV0Finder
InDetFlags.doTrackSegmentsPixel = False
InDetFlags.doTrackSegmentsSCT = False
InDetFlags.doTrackSegmentsTRT = False
InDetFlags.doSlimming         = False
InDetFlags.loadTools          = True
InDetFlags.doVertexFinding    = reDoPrimaryVertexing
#InDetFlags.doParticleCreation = reDoParticleCreation
InDetFlags.doParticleCreation = False # JDC -- Mira arriba
InDetFlags.doConversions      = reDoConversions
InDetFlags.doSecVertexFinder  = False
InDetFlags.doV0Finder         = reDoV0Finder
InDetFlags.doSimpleV0Finder   = False
InDetFlags.doTrkNtuple        = False
InDetFlags.doPixelTrkNtuple   = False
InDetFlags.doSctTrkNtuple     = False
InDetFlags.doTrtTrkNtuple     = False
InDetFlags.doPixelClusterNtuple = False
InDetFlags.doSctClusterNtuple   = False
InDetFlags.doTrtDriftCircleNtuple = False
InDetFlags.doVtxNtuple        = False
InDetFlags.doConvVtxNtuple    = False
InDetFlags.doV0VtxNtuple      = False
InDetFlags.doRefit            = doRefitTracks
InDetFlags.doLowBetaFinder    = False
InDetFlags.doPrintConfigurables = True

# [HIGHD0 TESTING] -- > setting the Large-d0 retracking
InDetFlags.doDVRetracking     = True

# [JDC] ADDED
InDetFlags.doxAOD = True
InDetFlags.doForwardTracks = False
InDetFlags.doTrackSegmentsPixelPrdAssociation = False
##Added to fix bug not finding PixelClustering tools in 17.2.2
from IOVDbSvc.CondDB import conddb
conddb.addFolder("PIXEL_OFL","/PIXEL/PixelClustering/PixelClusNNCalib")
# [JDC] END

# --- activate (memory/cpu) monitoring
InDetFlags.doPerfMon = True

# IMPORTANT NOTE: initialization of the flags and locking them is done in InDetRec_jobOptions.py!
# This way RecExCommon just needs to import the properties without doing anything else!
# DO NOT SET JOBPROPERTIES AFTER THIS LINE! The change will be ignored!

from InDetRecExample.InDetKeys import InDetKeys
if InDetFlags.doVertexFinding() and readAOD:
  InDetKeys.Tracks = InDetKeys.TrackParticles()
# [JDC] ADDED
# Where to put this ? ...  Encuentra que algoritmo usa esto en
# highd0 y activalo ahi, con el "if highD0()"
InDetKeys.TRT_DriftCirclesUncalibrated = "TRT_DriftCircles"
# [JDC] END

# uncomment if you don't want to overwrite the original fits (e.g. for comparison)
# this would also require enabling "pass-through" output mode (see bottom of this file)
# or else manually adding the input collection to the output stream
#if InDetFlags.doVertexFinding():
#  InDetKeys.xAODVertexContainer = "RefitPrimaryVertices" 

if readESD and not redoPatternRecoAndTracking:
    InDetKeys.UnslimmedTracks              = 'Tracks'
    InDetKeys.UnslimmedTracksTruth         = 'TrackTruthCollection'
    InDetKeys.UnslimmedDetailedTracksTruth = 'DetailedTrackTruth'

# Set container names
if doWriteESD:
  InDetKeys.OutputESDFileName = "InDetRecESD_new.root"

if doWriteAOD:
  InDetKeys.OutputAODFileName = "InDetRecAOD_new.root"  

# IMPORTANT! Uncomment this if your input ESD was not slimmed
# See https://its.cern.ch/jira/browse/ATLASRECTS-2698
#InDetKeys.ProcessedESDTracks="CombinedInDetTracks"
#InDetKeys.UnslimmedTracks="CombinedInDetTracksRetracked"
#InDetKeys.UnslimmedTracksTruth = 'CombinedInDetTracksRetrackedTruthCollection'
#InDetKeys.UnslimmedDetailedTracksTruth = 'CombinedInDetTracksRetrackedDetailedTruth'


print "Printing InDetKeys"
InDetKeys.lockAllExceptAlias()
InDetKeys.print_JobProperties()

#--------------------------------------------------------------
# enable statistics for reading ESD testing
#--------------------------------------------------------------

InDetFlags.doStatistics   = doInDetRecStatistics
#TrackCollectionKeys        = [InDetKeys.Tracks()]
#TrackCollectionTruthKeys   = [InDetKeys.TracksTruth()]

# Uncomment to use medical image seeding
# InDetFlags.primaryVertexSetup = "MedImgMultiFinding"
  
#--------------------------------------------------------------
# load master joboptions file
#--------------------------------------------------------------
  
include("InDetRecExample/InDetRec_all.py")

# Not GEN stuff in data
if not globalflags.DataSource() == 'data':
    # --- Not sure if there is another quickest way to create the
    #     MC Truth info needed by the xAODMaker::TrackParticleCnv 
    #     than going through the creation of the AOD ??

    # -- create MC-truth particle info
    #from McParticleAlgs.JobOptCfg import McAodBuilder
    #from RecExConfig.ObjKeyStore import objKeyStore
    #if (cfgKeyStore.isInInput( "McEventCollection", "TruthEvent" ) and \
    #        not objKeyStore.isInInput( "McEventCollection", "GEN_AOD" )): 
    #if (objKeyStore.isInInput( "McEventCollection", "TruthEvent" ) and \
    #        not objKeyStore.isInInput( "McEventCollection", "GEN_AOD" )): 
    #topSequence.insert(0,McAodBuilder())
    from xAODTruthCnv.xAODTruthCnvConf import xAODMaker__xAODTruthCnvAlg
    GEN_AOD2xAOD = xAODMaker__xAODTruthCnvAlg("GEN_AOD2xAOD")
    GEN_AOD2xAOD.AODContainerName = "TruthEvent"
    GEN_AOD2xAOD.WriteInTimePileUpTruth = True
    topSequence.insert(0,GEN_AOD2xAOD)
    # Fix the bug comented in https://its.cern.ch/jira/browse/ATLASRECTS-2062
    topSequence.GEN_AOD2xAOD.ForceRerun=True


# Set to True if you want to write out all input data ("pass-through" mode)
if doWriteESD:
  StreamESD.TakeItemsFromInput = False

if doWriteAOD:
  StreamAOD.TakeItemsFromInput = False
# JCD ADDED
#--------------------------------------------------------------
# Enabling re-writing of the storeGate 

from AthenaCommon.AppMgr import ServiceMgr as svcMgr
StoreGateSvc  = svcMgr.StoreGateSvc
StoreGateSvc.AllowOverwrite = True

#
#
## Do some additional tweaking:
#from AthenaCommon.AppMgr import theApp
#ServiceMgr.MessageSvc.OutputLevel = INFO
#ServiceMgr.MessageSvc.defaultLimit = 10000
#theApp.EvtMax = 200
