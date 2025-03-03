import L1Trigger.Phase2L1GT.VHDLWriter.Conversions as conversions
import L1Trigger.Phase2L1GT.VHDLWriter.Writer as writer
import FWCore.ParameterSet.Config as cms

# Create a dummy process, to be able to retrieve algorithms, moduleNames, filters
menu = cms.Process('VHDLWriter')
menu.load("L1Trigger.Phase2L1GT.l1tGTMenu_cff")

# They must be deleted to avoid unnecessary objects in the menu process
del(menu.l1tGTSingleObjectCond)
del(menu.l1tGTDoubleObjectCond)
del(menu.l1tGTTripleObjectCond)
del(menu.l1tGTQuadObjectCond)

knownfilters = dict()
logicalcombinations = dict()
distributedalgos = dict()

algobitmap = conversions.sortAlgodictWithIndices(menu)  # will loop over all algos, extract the expression, remove the '_',
                                                        # save them in a dict (original, modified), sort the dictionary
                                                        # assign an algobit to each algo. 
knownfilters = conversions.getConditionsfromConfig(menu)  # takes in a cmssw process object and checks if filter 
                                                        # is a known gt condition converts it to corresponding 
                                                        # Condition object defined in Conditions.py
logicalcombinations = conversions.getLogicalFilters(menu, knownfilters) # For each module in a path:
                                                                        # Check if it’s a filter and of type "PathStatusFilter". Retrieve its logical expression.
                                                                        # Analyze the modules, If any of these modules are in knownfilters, update combinatorialfilters.
                                                                        # Return a dictionary summarizing the combinatorial filters for each path.
algoblocks = conversions.writeAlgoblocks(knownfilters, logicalcombinations)
distributedalgos = conversions.distributeAlgos(algoblocks, 4)    # 4 is the number of slrs. Distributes algos in all slrs
conversions.writeAlgounits(distributedalgos, algobitmap, knownfilters, logicalcombinations) # handles the writing of the algos in vhdl file
distributed_algomap = conversions.getAlgobits(algobitmap, distributedalgos, [0, 24, 32, 48]) 
