# NOT USE THIS FILE DIRECTLY! 
# INTENDED TO BE USED AS COMMAND LINE

# Perform the Large-d0 retracking and the vertexing (VrtSecInclusive)

Reco_tf.py --fileValidation False --ignoreErrors 'True' --autoConfiguration 'everything' --preExec 'from InDetRecExample.InDetJobProperties import InDetFlags;InDetFlags.disableInDetReco.set_Value_and_Lock(False);InDetFlags.disableTracking.set_Value_and_Lock(False);InDetFlags.doDVRetracking.set_Value(True)' --postExec 'from AthenaCommon.AppMgr import ServiceMgr;import MuonRPC_Cabling.MuonRPC_CablingConfig;ServiceMgr.MuonRPC_CablingSvc.RPCMapfromCool=False;ServiceMgr.MuonRPC_CablingSvc.CorrFileName="LVL1confAtlasRUN2_ver016.corr";ServiceMgr.MuonRPC_CablingSvc.ConfFileName="LVL1confAtlasRUN2_ver016.data";from IOVDbSvc.CondDB import conddb;conddb.addFolderSplitOnline("INDET","/Indet/Onl/IBLDist","/Indet/IBLDist");ServiceMgr.StoreGateSvc.AllowOverwrite=True' --postInclude ScheduleVrtSecInclusive.py --inputESD YOUR_ESD_INPUT.pool.root --outputDAOD_RPVLL YOUR_DAOD_OUTPUTNAME.root 2>&1 | tee outlog.txt
