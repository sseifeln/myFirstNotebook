import os, sys ,stat, fnmatch ,subprocess ,math , random ,time, fileinput, numpy
import Utils 


TMTT_defRt_bits = 12 
TMTT_defZ_bits = 14
TMTT_defBend_bits = 6
TMTT_defPhiSector_bits = 6
TMTT_defPhiS_bits = 13
TMTT_defPhiO_bits = 15
TMTT_defPhi_bits = 14 

TMTT_KF_defd0_bits = 12
TMTT_KF_defoneOver2r_bits = 18
TMTT_KF_defphi0_bits = 18
TMTT_KF_defz0_bits = 18
TMTT_KF_deftanlambda_bits = 18 
TMTT_KF_defchisquared_bits = 17

cStats_UseBinomial=True
TMTT_defVariables_ResolutionPlots = ["QinvPt","Phi","D0" , "Z0" ,"Eta"]
TMTT_defVariables_EfficiencyPlots = ["invpt","eta","phi" , "d0" ,"z0"]
TMTT_defXVariables_ResolutionPlots = ["Eta","InvPt"]

testFile = "data/Hists_10RtBits_14ZBits_6BendBits_6PhiSectorBits_13PhiSBits_15PhiOBits.root"
testHistName = "TMTrackProducer/InputData/StubsVsEta"
testFitter = "KF5ParamsComb"
testVariable = "Z0"
testXVariable = "Eta"


# fitters are either KF5ParamsComb or KF4ParamsComb
# variables are QinvPt , Phi , D0 , Z0 , Eta 
def getFoldedResolution(pFileName, pVarName, pFitter) : 
	cObjName = 'TMTrackProducer/%s/Fit%sRes__%s' % (pFitter , pVarName, pFitter )
	cHist = Utils.getObject( pFileName , cObjName )
	return cHist

def getResolution(pFileName, pVarName, pVarName_x ,  pFitter) : 
	cObjName = 'TMTrackProducer/%s/%sResVsTrue%s__%s' % ( pFitter, pVarName, pVarName_x, pFitter )
	return Utils.getObject( pFileName , cObjName )

def getTrueTracks_Fitter(pFileName, pVarName) : 
	cObjName = 'TMTrackProducer/TrackCands_HT/TP%sForAlgEff_HT' % (pVarName)
	return Utils.getObject( pFileName , cObjName )

def getAlgTracks_Fitter(pFileName, pVarName, pFitter) : 
	cObjName = 'TMTrackProducer/%s/FitTP%sForAlgEff__%s' % ( pFitter, pVarName, pFitter )
	return Utils.getObject( pFileName , cObjName )

def getAbsoluteAlgEfficiency(pFileName, pVarName, pFitter) : 
	cAlgTracks_Fitter = getAlgTracks_Fitter(pFileName, pVarName, pFitter)
	cTrueTracks_Fitter = getTrueTracks_Fitter(pFileName, pVarName)
	if( cStats_UseBinomial ) : 
		return Utils.getBinomialEfficiency(cAlgTracks_Fitter.GetEntries(), cTrueTracks_Fitter.GetEntries())
	else : 
		return Utils.getBayesianEfficiency(cAlgTracks_Fitter.GetEntries(), cTrueTracks_Fitter.GetEntries())
		
def getAlgEfficiency(pFileName, pVarName, pFitter) : 
	cAlgTracks_Fitter = getAlgTracks_Fitter(pFileName, pVarName, pFitter)
	cTrueTracks_Fitter = getTrueTracks_Fitter(pFileName, pVarName)
	cEff = Utils.TEfficiency(cAlgTracks_Fitter, cTrueTracks_Fitter)
	cTitle = 'Tracking efficiency vs. %s; %s; Efficiency' % ( pVarName , pVarName )
	cEff.SetTitle(cTitle)
	return cEff
