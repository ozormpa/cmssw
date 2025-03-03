from ast import Mod
from modulefinder import Module
from queue import Empty
from L1Trigger.Phase2L1GT.l1tGTScales import scale_parameter
from libL1TriggerPhase2L1GT import L1GTScales as CppScales
l1tGTScales = CppScales(*[param.value() for param in scale_parameter.parameters_().values()])

class Condition:
    """
    Base Class for all EDFilters that correspond to an P2GT condition
    Contains: Cuts, The VHDL Resource usage, Paths corresponding to the Modules in the config
    """
    _ObjectNameConversions = {
        "GTTPromptJets"       : "GTT_PROMPT_JETS_SLOT",
        "GTTDisplacedJets"    : "GTT_DISPLACED_JETS_SLOT",
        "GTTPromptHtSum"      : "GTT_HT_MISS_PROMPT_SLOT",
        "GTTDisplacedHtSum"   : "GTT_HT_MISS_DISPLACED_SLOT",
        "GTTEtSum"            : "GTT_ET_MISS_SLOT",
        "GTTTaus"             : "GTT_TAUS_SLOT",
        "GTTPhiCandidates"    : "GTT_PHI_CANDIDATE_SLOT",
        "GTTRhoCandidates"    : "GTT_RHO_CANDIDATE_SLOT",
        "GTTBsCandidates"     : "GTT_BS_CANDIDATE_SLOT",
        "GTTPrimaryVert"      : "GTT_PRIM_VERT_SLOT",
        "CL2Jets"             : "CL2_JET_SLOT",
        "CL2HtSum"            : "CL2_HT_MISS_SLOT",
        "CL2EtSum"            : "CL2_ET_MISS_SLOT",
        "CL2Taus"             : "CL2_TAU_SLOT",
        "CL2Electrons"        : "CL2_ELECTRON_SLOT",
        "CL2Photons"          : "CL2_PHOTON_SLOT",
        "GCTNonIsoEg"         : "GCT_NON_ISO_EG_SLOT",
        "GCTIsoEg"            : "GCT_ISO_EG_SLOT",
        "GCTJets"             : "GCT_JETS_SLOT",
        "GCTTaus"             : "GCT_TAUS_SLOT",
        "GCTHtSum"            : "GCT_HT_MISS_SLOT",
        "GCTEtSum"            : "GCT_ET_MISS_SLOT",
        "GMTSaPromptMuons"    : "GMT_SA_PROMPT_SLOT",
        "GMTSaDisplacedMuons" : "GMT_SA_DISPLACED_SLOT",
        "GMTTkMuons"          : "GMT_TK_MUON_SLOT",
        "GMTTopo"             : "GMT_TOPO_SLOT"        
    }

    def __init__(self):
        self.Cuts = {}
        self.InputObjects = {}
        self._InputTags = []
        self.Paths = []
        self.ResourceUseage = CutResources()
        self.ResourcesperCut = {
            ('minPt') : CutResources(bram = 0 , dsp = 0, lut = 110),
            ('minEta','maxEta') : CutResources(bram = 0 , dsp = 0, lut = 120),
            ('minPhi','maxPhi') : CutResources(bram = 0 , dsp = 0, lut = 123),
            ('minZ0','maxZ0') : CutResources(bram = 0 , dsp = 0, lut = 123),
            ('qual') : CutResources(bram = 0 , dsp = 0, lut = 40),
            ('iso') : CutResources(bram = 0 , dsp = 0, lut = 40)

        }
        self._HWConversionFunctions = {
            'minPt'  : l1tGTScales.to_hw_pT_floor,
            'maxPt'  : l1tGTScales.to_hw_pT_ceil,
            'minEta' : l1tGTScales.to_hw_eta_floor,
            'maxEta' : l1tGTScales.to_hw_eta_ceil,
	        'minPhi' : l1tGTScales.to_hw_phi_floor,
            'maxPhi' : l1tGTScales.to_hw_phi_ceil,
            'minZ0'  : l1tGTScales.to_hw_z0_floor,
            'maxZ0'  : l1tGTScales.to_hw_z0_ceil,
            'minScalarSumPt' : l1tGTScales.to_hw_pT_floor,
            'maxScalarSumPt' : l1tGTScales.to_hw_pT_ceil,
            'minAbsEta'      : l1tGTScales.to_hw_eta_floor,
            'maxAbsEta'      : l1tGTScales.to_hw_eta_ceil,
            'regionsMinPt'   : l1tGTScales.to_hw_pT_floor,
            # 'minRelIsolationPt'        : l1tGTScales.to_hw_isolationPT_floor, # doesn't exist in l1tGTScales
            # 'maxRelIsolationPt'        : l1tGTScales.to_hw_isolationPT_ceil,
            'minPrimVertDz'  : l1tGTScales.to_hw_z0_floor,
            'maxPrimVertDz'  : l1tGTScales.to_hw_z0_ceil,
            'regionsMaxRelIsolationPt' : l1tGTScales.to_hw_relative_isolationPT_ceil,
            'regionsAbsEtaLowerBounds' : l1tGTScales.to_hw_eta_ceil,
        }

        self._cut_aliases = {

        }
    def booltostring(self,x):
        # print(f"❌ x is: {x}")
        if x == True:
            return True
        else: 
            return False

    def addResources(self,knowncut):
        for k in list(self.ResourcesperCut.keys()):
            if knowncut in k:
                if k in self.ResourcesperCut.keys():
                    self.ResourceUseage.addCutResources(self.ResourcesperCut.pop(k))

    def _setInputObject(self,condition,value):
        # self.InputObjects[condition] = self._ObjectNameConversions.get(value)
        self.InputObjects[condition] = value

    def setCut(self, key, physvalue, collection="", numberofparameters=0):
        """
        Sets a cut value, ensuring the correct type propagation for hardware (hwcut) 
        and physics (physcut) values.
        """
        needs_conversion = key in self._HWConversionFunctions
        print(f"🚀 Key in setcut is: {key} - needs conversion? {needs_conversion}")
        if isinstance(physvalue, list):
            print(f"\t\tWe are in a list {physvalue}")
            if needs_conversion:
                hwvalue = [self._HWConversionFunctions[key](v) for v in physvalue]
                print(f"\t\t\tNeeds conversion: hwvalue: {hwvalue}")
            else:
                hwvalue = physvalue  # No conversion needed
                print(f"\t\t\tDoesn't need conversion: hwvalue: {hwvalue} = {physvalue}")
        else:
            hwvalue = self._HWConversionFunctions[key](physvalue) if needs_conversion else physvalue
            print(f"\t\tWe are not in a list - needs conversion? {needs_conversion} - hw: {hwvalue} phys: {physvalue}")
        if collection != "":
            print(f"\t\tWe are in a collection!")
            if self.getHWCut(key) not in self.Cuts.keys():
                cut = _Cut()
                cut.setNumberofvalues(numberofparameters, physvalue, hwvalue)  
                if needs_conversion and key in ['ss', 'os']: 
                    cut.setforBooleanCut(numberofparameters)
                cut.setCutat(hwvalue, physvalue, collection)
                self.Cuts[self.getHWCut(key)] = cut
                print(f"\t\t\tWe are not in self.Cuts.keys - cut: {self.getHWCut(key)}")
            else:
                self.Cuts[self.getHWCut(key)].setCutat(hwvalue, physvalue, collection)
                print(f"\t\t\tWe are in self.Cuts.keys - cut: {self.getHWCut(key)}")
        else:
            print(f"\t\tWe are not in a collection!")
            cut = _Cut()
            cut.setNumberofvalues(numberofparameters, physvalue, hwvalue) 
            cut.setCut(hwvalue, physvalue)
            self.Cuts[self.getHWCut(key)] = cut
            print(f"\t\t\tcut: {self.getHWCut(key)}")
        print("\t\t\tAll cuts are  : ")
        for cut in self.Cuts:
            print(f"\t\t\t\t\t{cut}")
        print(f"😊😊 {key} {hwvalue} {physvalue}")

    def setName(self,name):
        self.Name = name
    def addPath(self,path):
        self.Paths.append(path)

    def getHWCut(self, cut, collection = ""):
        if cut in self._cut_aliases:
            return self._cut_aliases[cut].format(collection)
        return cut

    def getCollections(self, object):
        return {}

    def setInputObjects(self, **inobjs):
        for name, value in inobjs.items():
            if name in self._InputTags:
                self.InputObjects[name] = value
    def _setHWConversionFunctions(self,indict):
           self._HWConversionFunctions = indict

class DoubleObjCond(Condition):
    """
    Class for to the L1GTDoubleObjectCond 
    """
    Label = "L1GTDoubleObjectCond"
    Template = "double.template"
    NumberOfCollections = 2 
    NumberOfCorrelations = 2
    def __init__(self):
        Condition.__init__(self)
        
        self._HWConversionFunctions.update({
            'minDEta'     : l1tGTScales.to_hw_eta_floor,
            'maxDEta'     : l1tGTScales.to_hw_eta_ceil,
            'minDPhi'     : l1tGTScales.to_hw_phi_floor,
            'maxDPhi'     : l1tGTScales.to_hw_phi_ceil,
            'minDR'       : l1tGTScales.to_hw_dRSquared_floor,
            'maxDR'       : l1tGTScales.to_hw_dRSquared_ceil,
            'minInvMass'  : l1tGTScales.to_hw_InvMassSqrDiv2,
            'maxInvMass'  : l1tGTScales.to_hw_InvMassSqrDiv2,
            'minTransMass': l1tGTScales.to_hw_TransMassSqrDiv2,
            'maxTransMass': l1tGTScales.to_hw_TransMassSqrDiv2,
            'minCombPt'   : l1tGTScales.to_hw_PtSquared,
            'maxCombPt'   : l1tGTScales.to_hw_PtSquared,
            'minDz'       : l1tGTScales.to_hw_z0_floor, # same as Z0??
            'maxDz'       : l1tGTScales.to_hw_z0_ceil,
            # 'minQualityScore' : l1tGTScales.to_hw_z0_ceil,
            # 'maxQualityScore' : l1tGTScales.to_hw_z0_ceil,
            # 'minInvMassSqrOver2DRSqr' : l1tGTScales.to_hw_,
            # 'maxInvMassSqrOver2DRSqr' : l1tGTScales.to_hw_,
            'regionsAbsEtaLowerBounds' : l1tGTScales.to_hw_eta_ceil,
            'os'          : self.booltostring,
            'ss'          : self.booltostring        
        })

        self._cut_aliases.update({ 
            'minPt'  : 'minPT_cuts',
            'maxPt'  : 'maxPT_cuts',
            'minEta' : 'minEta_cuts',
            'maxEta' : 'maxEta_cuts',
            'minPhi' : 'minPhi_cuts',
            'maxPhi' : 'maxPhi_cuts',
            'minZ0'  : 'minZ0_cuts',
            'maxZ0'  : 'maxZ0_cuts',
            'minScalarSumPt'    : 'minScalarSumPT_cuts',
            'maxScalarSumPt'    : 'maxScalarSumPT_cuts',
            'minQualityScore'   : 'minQualityScore_cuts',
            'maxQualityScore'   : 'maxQualityScore_cuts',
            'qualityFlags'      : 'qualityFlags_cuts',
            'minIsolationPt'    : 'minIsolationPT_cuts',
            'maxIsolationPt'    : 'maxIsolationPT_cuts',
            'minAbsEta'         : 'minAbsEta_cuts',
            'maxAbsEta'         : 'maxAbsEta_cuts',
            'minRelIsolationPt' : 'minRelIsolationPT_cuts',
            'maxRelIsolationPt' : 'maxRelIsolationPT_cuts',
            'primVertex'        : 'primVertIdcs',
            'minPrimVertDz'     : 'minPrimVertDz_cuts',
            'maxPrimVertDz'     : 'maxPrimVertDz_cuts',
            'regionsAbsEtaLowerBounds' : 'regionsAbsEtaLowerBounds',
            'regionsMinPt'             : 'regionsMinPt_cuts',
            'regionsMaxRelIsolationPt' : 'regionsMaxRelIsolationPT_cuts',
            'regionsQualityFlags'      : 'regionsQualityFlags_cuts',
            'minPtMultiplicityN'       : 'minPtMultiplicityNs',
            'minPtMultiplicityCut'     : 'minPtMultiplicity_cuts',
            'os'           : 'os_cut',
            'ss'           : 'ss_cut',
            'minCombPt'    : 'minPTSqr_cut',
            'maxCombPt'    : 'maxPTSqr_cut',
            'minDEta'      : 'minDEta_cut',
            'maxDEta'      : 'maxDEta_cut',
            'minDPhi'      : 'minDPhi_cut',
            'maxDPhi'      : 'maxDPhi_cut',
            'minDz'        : 'minDZ_cut',
            'maxDz'        : 'maxDZ_cut',
            'minDR'        : 'minDRSquared_cut',
            'maxDR'        : 'maxDRSquared_cut',
            'minInvMass'   : 'minInvMassSqrDiv2_cut',
            'maxInvMass'   : 'maxInvMassSqrDiv2_cut',
            'minTransMass' : 'minTransMassSqrDiv2_cut',
            'maxTransMass' : 'maxTransMassSqrDiv2_cut',
            # 'minInvMassSqrOver2DRSqr' : 'minInvMassSqrOver2DRSqr_cut',
            # 'maxInvMassSqrOver2DRSqr' : 'maxInvMassSqrOver2DRSqr_cut'
        })
        self.ResourcesperCut.update({
            ('minDEta','maxDEta') : CutResources(bram = 0 , dsp = 0, lut = 800),
            ('minDPhi','maxDPhi') : CutResources(bram = 0 , dsp = 0, lut = 800),
            ('minDR','maxDR') : CutResources(bram = 0 , dsp = 24, lut = 1800),
            ('minInvMass','maxInvMass') : CutResources(bram = 24 , dsp = 36, lut = 2000),
            ('minTransMass','maxTransMass') : CutResources(bram = 24 , dsp = 36, lut = 2000)
        })


    def getCollections(self, object):
        collections = {1: object.getParameter('collection1'), 2: object.getParameter('collection2')}
        for col in collections.values():
            self._InputTags += [col.getParameter("tag")]
            print(f"🔹🔹 DoubleObjCond: {self._InputTags}")
        return collections

class SingleObjCond(Condition):
    """
    Class for to the L1GTSingleObjectCond 
    """
    def __init__(self):
        Condition.__init__(self)

        self._cut_aliases.update({ 
            'minPt'  : 'minPT_cut',
            'maxPt'  : 'maxPT_cut',
            'minEta' : 'minEta_cut',
            'maxEta' : 'maxEta_cut',
            'minPhi' : 'minPhi_cut',
            'maxPhi' : 'maxPhi_cut',
            'minZ0'  : 'minZ0_cut',
            'maxZ0'  : 'maxZ0_cut',
            # 'qual'   : 'qual_cut',
            # 'iso'    : 'iso_cut',
            # 'non existent' : 'minDz_cut',
            # 'non existent' : 'maxDz_cut',
            'minScalarSumPt'    : 'minScalarSumPT_cut',
            'maxScalarSumPt'    : 'maxScalarSumPT_cut',
            'minQualityScore'   : 'minQualityScore_cut',
            'maxQualityScore'   : 'maxQualityScore_cut',
            'qualityFlags'      : 'qualityFlags_cut',
            'minIsolationPt'    : 'minIsolationPT_cut',
            'maxIsolationPt'    : 'maxIsolationPT_cut',
            'minAbsEta'         : 'minAbsEta_cut',
            'maxAbsEta'         : 'maxAbsEta_cut',
            'minRelIsolationPt' : 'minRelIsolationPT_cut',
            'maxRelIsolationPt' : 'maxRelIsolationPT_cut',
            'primVertex'        : 'primVertIdx',
            'minPrimVertDz'     : 'minPrimVertDz_cut',
            'maxPrimVertDz'     : 'maxPrimVertDz_cut',
            'regionsMinPt'      : 'regionsMinPt_cut',
            'regionsAbsEtaLowerBounds' : 'regionsAbsEtaLowerBounds',
            'regionsMaxRelIsolationPt' : 'regionsMaxRelIsolationPT_cut',
            'regionsQualityFlags'      : 'regionsQualityFlags_cut',
            'minPtMultiplicityN'       : 'minPtMultiplicityN',
            'minPtMultiplicityCut'     : 'minPtMultiplicity_cut',
        })
    Label = "L1GTSingleObjectCond"
    Template = "single.template"


    def getCollections(self, object):
        self._InputTags += [object.getParameter("tag")]
        print(f"🔹 SingleObjCond: {self._InputTags}")
        return {}

class QuadObjCond(Condition):
    """
    Class for to the L1GTQuadObjectCond 
    """
    def __init__(self):
        Condition.__init__(self)

        self._cut_aliases.update({
            'minPt'  : 'minPT_cuts',
            'maxPt'  : 'maxPT_cuts',
            'minEta' : 'minEta_cuts',
            'maxEta' : 'maxEta_cuts',
            'minPhi' : 'minPhi_cuts',
            'maxPhi' : 'maxPhi_cuts',
            'minZ0'  : 'minZ0_cuts',
            'maxZ0'  : 'maxZ0_cuts',
            'minScalarSumPt'    : 'minScalarSumPT_cuts',
            'maxScalarSumPt'    : 'maxScalarSumPT_cuts',
            'minQualityScore'   : 'minQualityScore_cuts',
            'maxQualityScore'   : 'maxQualityScore_cuts',
            'qualityFlags'      : 'qualityFlags_cuts',
            'minIsolationPt'    : 'minIsolationPT_cuts',
            'maxIsolationPt'    : 'maxIsolationPT_cuts',
            'minAbsEta'         : 'minAbsEta_cuts',
            'maxAbsEta'         : 'maxAbsEta_cuts',
            'minRelIsolationPt' : 'minRelIsolationPT_cuts',
            'maxRelIsolationPt' : 'maxRelIsolationPT_cuts',
            'primVertex'        : 'primVertIdcs',
            'minPrimVertDz'     : 'minPrimVertDz_cuts',
            'maxPrimVertDz'     : 'maxPrimVertDz_cuts',
            'regionsAbsEtaLowerBounds' : 'regionsAbsEtaLowerBounds',
            'regionsMinPt'             : 'regionsMinPt_cuts',
            'regionsMaxRelIsolationPt' : 'regionsMaxRelIsolationPT_cuts',
            'regionsQualityFlags'      : 'regionsQualityFlags_cuts',
            'minPtMultiplicityN'       : 'minPtMultiplicityNs',
            'minPtMultiplicityCut'     : 'minPtMultiplicity_cuts',
            'os'           : 'os_cuts',
            'ss'           : 'ss_cuts',
            'minCombPt'    : 'minPTSqr_cuts',
            'maxCombPt'    : 'maxPTSqr_cuts',
            'minDEta'      : 'minDEta_cuts',
            'maxDEta'      : 'maxDEta_cuts',
            'minDPhi'      : 'minDPhi_cuts',
            'maxDPhi'      : 'maxDPhi_cuts',
            'minDz'        : 'minDZ_cuts',
            'maxDz'        : 'maxDZ_cuts',
            'minDR'        : 'minDRSquared_cuts',
            'maxDR'        : 'maxDRSquared_cuts',
            'minInvMass'   : 'minInvMassSqrDiv2_cuts',
            'maxInvMass'   : 'maxInvMassSqrDiv2_cuts',
            'minTransMass' : 'minTransMassSqrDiv2_cuts',
            'maxTransMass' : 'maxTransMassSqrDiv2_cuts',
            # 'minInvMassSqrOver2DRSqr' : 'minInvMassSqrOver2DRSqr_cuts',
            # 'maxInvMassSqrOver2DRSqr' : 'maxInvMassSqrOver2DRSqr_cuts'
        })

        self._HWConversionFunctions.update({
            'minDEta'     : l1tGTScales.to_hw_eta_floor,
            'maxDEta'     : l1tGTScales.to_hw_eta_ceil,
            'minDPhi'     : l1tGTScales.to_hw_phi_floor,
            'maxDPhi'     : l1tGTScales.to_hw_phi_ceil,
            'minDR'       : l1tGTScales.to_hw_dRSquared_floor,
            'maxDR'       : l1tGTScales.to_hw_dRSquared_ceil,
            'minInvMass'  : l1tGTScales.to_hw_InvMassSqrDiv2,
            'maxInvMass'  : l1tGTScales.to_hw_InvMassSqrDiv2,
            'minTransMass': l1tGTScales.to_hw_TransMassSqrDiv2,
            'maxTransMass': l1tGTScales.to_hw_TransMassSqrDiv2,
            'minCombPt'   : l1tGTScales.to_hw_PtSquared,
            'maxCombPt'   : l1tGTScales.to_hw_PtSquared,
            'minDz'       : l1tGTScales.to_hw_z0_floor, # same as Z0??
            'maxDz'       : l1tGTScales.to_hw_z0_ceil,
            # 'minInvMassSqrOver2DRSqr' : l1tGTScales.to_hw_,
            # 'maxInvMassSqrOver2DRSqr' : l1tGTScales.to_hw_,
            'regionsAbsEtaLowerBounds' : l1tGTScales.to_hw_eta_ceil,
            'os'          : self.booltostring,
            'ss'          : self.booltostring
        })

    Label = "L1GTQuadObjectCond"
    Template = "quad.template"
    NumberOfCollections = 4
    NumberOfCorrelations = 6
    def getCollections(self, object):
        collections = {1: object.getParameter('collection1'), 2: object.getParameter('collection2'),3: object.getParameter('collection3'),4: object.getParameter('collection4')}
        for col in collections.values():
            self._InputTags += [col.getParameter("tag")]
            print(f"🔹🔹🔹🔹 QuadObjCond: {self._InputTags}")
        return collections


    # def getCollections(self, object):
    #     collections = {1: object.getParameter('collection1'), 2: object.getParameter('collection2'),3: object.getParameter('collection3'),4: object.getParameter('collection4')}
    #     for col in collections.values():
    #         self._InputTags += [col.getParameter("tag")]
    #     return collections
    
    def getCorrelations(self, object):
        correlations = { 1: object.getParameter('correl12'), 2: object.getParameter('correl13'), 3 : object.getParameter('correl23'),4: object.getParameter('correl14'), 5: object.getParameter('correl24'), 6 : object.getParameter('correl34')}
        return correlations

class TripleObjCond(Condition):
    """
    Class for to the L1GTTripleObjectCond 
    """
    Label = "L1GTTripleObjectCond"
    Template = "triple.template"
    NumberOfCollections = 3
    NumberOfCorrelations = 3
    def __init__(self):
        Condition.__init__(self)
        
        self._HWConversionFunctions.update({
            'minDEta'     : l1tGTScales.to_hw_eta_floor,
            'maxDEta'     : l1tGTScales.to_hw_eta_ceil,
            'minDPhi'     : l1tGTScales.to_hw_phi_floor,
            'maxDPhi'     : l1tGTScales.to_hw_phi_ceil,
            'minDR'       : l1tGTScales.to_hw_dRSquared_floor,
            'maxDR'       : l1tGTScales.to_hw_dRSquared_ceil,
            'minInvMass'  : l1tGTScales.to_hw_InvMassSqrDiv2,
            'maxInvMass'  : l1tGTScales.to_hw_InvMassSqrDiv2,
            'minTransMass': l1tGTScales.to_hw_TransMassSqrDiv2,
            'maxTransMass': l1tGTScales.to_hw_TransMassSqrDiv2,
            'minCombPt'   :   l1tGTScales.to_hw_PtSquared,
            'maxCombPt'   :   l1tGTScales.to_hw_PtSquared,
            'minDz'       : l1tGTScales.to_hw_z0_floor, # same as Z0??
            'maxDz'       : l1tGTScales.to_hw_z0_ceil,
            # 'minInvMassSqrOver2DRSqr' : l1tGTScales.to_hw_,
            # 'maxInvMassSqrOver2DRSqr' : l1tGTScales.to_hw_,
            'os'   : self.booltostring,
            'ss'   : self.booltostring
        })

        
        self._cut_aliases.update({ 
            'minPt'  : 'minPT_cuts',
            'maxPt'  : 'maxPT_cuts',
            'minEta' : 'minEta_cuts',
            'maxEta' : 'maxEta_cuts',
            'minPhi' : 'minPhi_cuts',
            'maxPhi' : 'maxPhi_cuts',
            'minZ0'  : 'minZ0_cuts',
            'maxZ0'  : 'maxZ0_cuts',
            'minScalarSumPt'    : 'minScalarSumPT_cuts',
            'maxScalarSumPt'    : 'maxScalarSumPT_cuts',
            'minQualityScore'   : 'minQualityScore_cuts',
            'maxQualityScore'   : 'maxQualityScore_cuts',
            'qualityFlags'      : 'qualityFlags_cuts',
            'minIsolationPt'    : 'minIsolationPT_cuts',
            'maxIsolationPt'    : 'maxIsolationPT_cuts',
            'minAbsEta'         : 'minAbsEta_cuts',
            'maxAbsEta'         : 'maxAbsEta_cuts',
            'minRelIsolationPt' : 'minRelIsolationPT_cuts',
            'maxRelIsolationPt' : 'maxRelIsolationPT_cuts',
            'primVertex'        : 'primVertIdcs',
            'minPrimVertDz'     : 'minPrimVertDz_cuts',
            'maxPrimVertDz'     : 'maxPrimVertDz_cuts',
            'regionsAbsEtaLowerBounds' : 'regionsAbsEtaLowerBounds',
            'regionsMinPt'             : 'regionsMinPt_cuts',
            'regionsMaxRelIsolationPt' : 'regionsMaxRelIsolationPT_cuts',
            'regionsQualityFlags'      : 'regionsQualityFlags_cuts',
            'minPtMultiplicityN'       : 'minPtMultiplicityNs',
            'minPtMultiplicityCut'     : 'minPtMultiplicity_cuts',
            'os' : 'os_cuts',
            'ss' : 'ss_cuts',
            'minCombPt'    : 'minPTSqr_cuts',
            'maxCombPt'    : 'maxPTSqr_cuts',
            'minDEta'      : 'minDEta_cuts',
            'maxDEta'      : 'maxDEta_cuts',
            'minDPhi'      : 'minDPhi_cuts',
            'maxDPhi'      : 'maxDPhi_cuts',
            'minDz'        : 'minDZ_cuts',
            'maxDz'        : 'maxDZ_cuts',
            'minDR'        : 'minDRSquared_cuts',
            'maxDR'        : 'maxDRSquared_cuts',
            'minInvMass'   : 'minInvMassSqrDiv2_cuts',
            'maxInvMass'   : 'maxInvMassSqrDiv2_cuts',
            'minTransMass' : 'minTransMassSqrDiv2_cuts',
            'maxTransMass' : 'maxTransMassSqrDiv2_cuts',
            # 'minInvMassSqrOver2DRSqr' : 'minInvMassSqrOver2DRSqr_cuts',
            # 'maxInvMassSqrOver2DRSqr' : 'maxInvMassSqrOver2DRSqr_cuts'
        })
        self.ResourcesperCut.update({
            ('minDEta','maxDEta') : CutResources(bram = 0 , dsp = 0, lut = 800),
            ('minDPhi','maxDPhi') : CutResources(bram = 0 , dsp = 0, lut = 800),
            ('minDR','maxDR') : CutResources(bram = 0 , dsp = 24, lut = 1800),
            ('minInvMass','maxInvMass') : CutResources(bram = 24 , dsp = 36, lut = 2000),
            ('minTransMass','maxTransMass') : CutResources(bram = 24 , dsp = 36, lut = 2000)
        })


    def getCollections(self, object):
        collections = {1: object.getParameter('collection1'), 2: object.getParameter('collection2'),3: object.getParameter('collection3')}
        for col in collections.values():
            self._InputTags += [col.getParameter("tag")]
            print(f"🔹🔹🔹 TripleObjCond: {self._InputTags}")
        return collections
    
    def getCorrelations(self, object):
        correlations = { 1: object.getParameter('correl12'), 2: object.getParameter('correl13'), 3 : object.getParameter('correl23')}
        return correlations

class CutResources:
    def __init__(self,bram = 0,dsp = 0,lut = 0):
        self.bram = bram
        self.dsp = dsp
        self.lut = lut
    def addCutResources(self,cutResources):
        self.bram = self.bram + cutResources.bram
        self.dsp = self.dsp + cutResources.dsp
        self.lut = self.lut + cutResources.lut
    def printResources(self):
        print("bram:{}".format(self.bram))
        print("dsp:{}".format(self.dsp))
        print("lut:{}".format(self.lut))
        return 0

class DefineAlgoBits:
    def __init__(self):
        self.Assignment = {}
    def SetBit(self,Name,Algobit):
        self.Assignment[Name] = Algobit
    
class _Cut:
    def __init__(self):
        self.hwcut = []
        self.physcut = []
        self.enablecut = []
    def setCut(self,hwcut,physcut):
        self.hwcut.append(hwcut)
        self.physcut.append(physcut)
        self.enablecut.append(True)        
 
    # def setNumberofvalues(self,value): # 0.0 should be added here and True/False should be added here
    #     self.hwcut = [0] * (value )
    #     self.physcut = [0] * (value)
    #     self.enablecut = [False] * (value)

    # def setNumberofvalues(self, value, cut_type):  
    #     if cut_type == float:
    #         self.hwcut = [0.0] * value  # Use 0.0 for real values
    #         self.physcut = [0.0] * value
    #     elif cut_type == bool:
    #         self.hwcut = [False] * value  # Use False for boolean values
    #         self.physcut = [False] * value
    #     elif cut_type == list:
    #         self.hwcut = [[0]] * value  # Use [0] for lists - to be replaced with `(others=>0)` in jinja
    #         self.physcut = [False] * value
    #     else:
    #         self.hwcut = [0] * value  # Default to int (as before)
    #         self.physcut = [0] * value

    #     self.enablecut = [False] * value  # Keep enablecut as string

    def setNumberofvalues(self, numparam, physvalue, hwvalue):  
        """
        Ensures that self.hwcut and self.physcut match the types of hwvalue and physvalue respectively.
        Handles lists, booleans, and single values correctly. Mode can be either "phys" or "hw" in order 
        to facilitate the (others => 0) for hwvalue or list of zeros for physvalue. Jinja template replaces
        the quotes for others.
        """
        # Initialize default values based on input type
        def get_default(v, mode):
            if isinstance(v, bool):
                print(f"\t\t🔥🔥 value {v} is {type(v)} == bool")
                return False
            elif isinstance(v, float):
                print(f"\t\t🔥🔥 value {v} is {type(v)} == float")
                return 0.0
            elif isinstance(v, list) and mode == "hw":
                print(f"\t\t🔥🔥 value {v} is {type(v)} == list")
                return '(others => 0)' if v else []
            elif isinstance(v, list) and mode == "phys":
                print(f"\t\t🔥🔥 value {v} is {type(v)} == list")
                return [get_default(v[0], "phys")] * len(v) if v else []
            else:
                print(f"\t\t🔥🔥 value {v} is {type(v)} == other")
                return 0  # Default to int
        self.hwcut = [get_default(hwvalue, "hw")] * numparam
        self.physcut = [get_default(physvalue, "phys")] * numparam
        self.enablecut = [False] * numparam  # Enable cut flags (always boolean)

    def setforBooleanCut(self,value):
        self.hwcut = [False] * (value)
        # print(f"      Self.hwcut: {self.hwcut}")
    def setCutat(self, hwcut, physcut, position):
        self.hwcut[position - 1] = hwcut
        self.physcut[position - 1] = physcut
        self.enablecut[position - 1] = True  # Keep boolean logic unchanged
        
    def __str__(self) -> str:
        pass

class LogicalFilter:
    def __init__(self,pathname,expression,modulenames):
        self.pathname = pathname 
        self.expression = expression
        self.modulenames = modulenames

class AlgorithmBlock:
    """
    Class that groups the algorithms in a way that all codependent conditions are grouped   
    """
    def __init__(self):
        self.ResourceUseage = CutResources(0,0,0)
        self.Modules = set()
        self.Paths  = set()
        self.Collections = set()
        self.LogicalPath = set()

    def addlogical(self,paths,modules):
        self.Modules.update(modules.modulenames)
        self.LogicalPath.add(paths)
    def checklogical(self,modules):
        """
        checks if a module in a logical combination is already present in modules
        """
        if(self.Modules.intersection(modules.modulenames) == set()):
            return 0
        else:
            return 1
    def Combineblocks(self,algoblock):
        self.ResourceUseage.addCutResources(algoblock.ResourceUseage) 
        self.Modules.update(algoblock.Modules) 
        self.Paths.update(algoblock.Paths)  
        self.LogicalPath.update(algoblock.LogicalPath)
        self.Collections.update(set(algoblock.Collections))

    def addCondition(self,knownfilterkey,knownfiltervalue):
        self.Modules.add(knownfilterkey)
        self.Paths.update(knownfiltervalue.Paths)
        self.ResourceUseage.addCutResources(knownfiltervalue.ResourceUseage)
        self.Collections.update(set(knownfiltervalue.InputObjects.values()))
    def checkCondition(self,knownfilterkey):
        """
        checks if module is already present in modules, needed to combine logical filters and conditions
        """
        if  knownfilterkey in self.Modules:
            return 1
        else:
            return 0 

class Algorithmsdict:
    def __init__(self):
        self.algoblocks = []

    def addLogicalFilters(self,logicalcombinations):
        for key, value in logicalcombinations.items():
            for algoblock in self.algoblocks:
                # if algoblock.checklogical(key, value):
                if algoblock.checklogical(value):
                    # print("here here!")
                    break
            else:
                newblock  = AlgorithmBlock()
                newblock.addlogical(key, value)
                self.algoblocks.append(newblock)
    def addConditions(self,conditions):
        for key in conditions.keys():
            for algoblock in self.algoblocks:
                if algoblock.checkCondition(key) == 1:
                    algoblock.addCondition(key,conditions[key])
                    break
            else:
                newblock  = AlgorithmBlock()
                newblock.addCondition(key,conditions[key])
                self.algoblocks.append(newblock)


    def popMaxalgoblock(self):

        if self.algoblocks == []:
            return 0
        else:
           brammax = max(item.ResourceUseage.bram for item in self.algoblocks)

           if brammax!=0 :
                for item, value in enumerate(self.algoblocks):
                    if value.ResourceUseage.bram == brammax:
                        return self.algoblocks.pop(item)

           dspmax = max(item.ResourceUseage.dsp for item in self.algoblocks)
           if dspmax!=0 :
                for item, value in enumerate(self.algoblocks):
                    if value.ResourceUseage.dsp == dspmax:
                        return self.algoblocks.pop(item)
           lutmax = max(item.ResourceUseage.lut for item in self.algoblocks)
           for item, value in enumerate(self.algoblocks):
                if value.ResourceUseage.lut == lutmax:
                    return self.algoblocks.pop(item)

            


