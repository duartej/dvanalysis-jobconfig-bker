# Post-Include file to feed the Reco_tf
# these lines schedules the vertexing algo after the 
# retracking

# MC-truth stuff
if not globalflags.DataSource() == 'data':
    # -- create MC-truth particle info
    from McParticleAlgs.JobOptCfg import McAodBuilder
    topSequence.insert(0,McAodBuilder())
    from xAODTruthCnv.xAODTruthCnvConf import xAODMaker__xAODTruthCnvAlg
    GEN_AOD2xAOD = xAODMaker__xAODTruthCnvAlg("GEN_AOD2xAOD")
    GEN_AOD2xAOD.AODContainerName = "TruthEvent"
    GEN_AOD2xAOD.WriteInTimePileUpTruth = True
    topSequence.insert(1,GEN_AOD2xAOD)
    # Fix the bug comented in https://its.cern.ch/jira/browse/ATLASRECTS-2062
    topSequence.GEN_AOD2xAOD.ForceRerun=True

from AthenaCommon.AppMgr import ServiceMgr as svcMgr
StoreGateSvc=svcMgr.StoreGateSvc
StoreGateSvc.AllowOverwrite=True

from VrtSecInclusive.VrtSecInclusive import VrtSecInclusive
topSequence.insert(-1, VrtSecInclusive())

#print "OHM: topSequence contents below"
#print topSequence

# testing Dominik's new option
topSequence.VrtSecInclusive.ImpactWrtBL = True

# Dominik fixes to kazuki's
topSequence.VrtSecInclusive.doTRTPixCut=True
topSequence.VrtSecInclusive.doMergeFinalVerticesDistance=True

# New Kazuki's cuts
topSequence.VrtSecInclusive.a0TrkPVDstMaxCut=300.0 
topSequence.VrtSecInclusive.zTrkPVDstMinCut=0.0 
topSequence.VrtSecInclusive.zTrkPVDstMaxCut=1500.0 


# Kazuki's options, untouched so far
topSequence.VrtSecInclusive.CutPixelHits = 0
topSequence.VrtSecInclusive.CutSctHits = 2
topSequence.VrtSecInclusive.TrkA0ErrCut = 200000
topSequence.VrtSecInclusive.TrkZErrCut = 200000
topSequence.VrtSecInclusive.a0TrkPVDstMinCut = 2.0
topSequence.VrtSecInclusive.TrkPtCut = 1000
topSequence.VrtSecInclusive.SelVrtChi2Cut=5
topSequence.VrtSecInclusive.CutSharedHits=2
topSequence.VrtSecInclusive.TrkChi2Cut=50
topSequence.VrtSecInclusive.TruthTrkLen=1
topSequence.VrtSecInclusive.SelTrkMaxCutoff=300
topSequence.VrtSecInclusive.DoSAloneTRT=False
topSequence.VrtSecInclusive.DoTruth = (globalflags.DataSource == 'geant4' and globalflags.InputFormat == "pool")
topSequence.VrtSecInclusive.RemoveFake2TrkVrt = True

from TrkVKalVrtFitter.TrkVKalVrtFitterConf import Trk__TrkVKalVrtFitter
InclusiveVxFitterTool = Trk__TrkVKalVrtFitter(name                = "InclusiveVxFitter",
                                              Extrapolator        = ToolSvc.AtlasExtrapolator,
                                              IterationNumber     = 30,
                                              AtlasMagFieldSvc    = "AtlasFieldSvc"
                                             )
ToolSvc +=  InclusiveVxFitterTool;
InclusiveVxFitterTool.OutputLevel = INFO
topSequence.VrtSecInclusive.VertexFitterTool=InclusiveVxFitterTool
topSequence.VrtSecInclusive.Extrapolator = ToolSvc.AtlasExtrapolator

# Tell VrtSecInclusive the interface name for Trk::IVertexMapper
from TrkDetDescrTestTools.TrkDetDescrTestToolsConf import Trk__VertexMapper
HadronicVertexMapper = Trk__VertexMapper("HadronicVertexMapper")
ToolSvc += HadronicVertexMapper
topSequence.VrtSecInclusive.VertexMapper = HadronicVertexMapper

# Now add the new vertex collection to the output DAOD_RPVLL file
from OutputStreamAthenaPool.MultipleStreamManager import MSMgr
MSMgr.GetStream("StreamDAOD_RPVLL").AddItem( [ 'xAOD::TrackParticleContainer#VrtSecInclusive*',
                                               'xAOD::TrackParticleAuxContainer#VrtSecInclusive*',
                                               'xAOD::VertexContainer#VrtSecInclusive*',
                                               'xAOD::VertexAuxContainer#VrtSecInclusive*'] )

print "OHM: list of items in output stream:"
print MSMgr.GetStream("StreamDAOD_RPVLL").GetItems()
