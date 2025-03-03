import FWCore.ParameterSet.Config as cms
import re   # regular expressions


TYPE_STANDARD_PHYSICS = cms.vint32(1) # TODO

algorithms = cms.VPSet()    # vector of parameter sets - config for multiple algos?

l1tGTAlgoBlockProducer = cms.EDProducer(
    "L1GTAlgoBlockProducer",
    algorithms = algorithms
)

# cms.Process as input --> tuple of algo paths from algorithms as output
def collectAlgorithmPaths(process) -> "tuple[cms.Path]":
    str_paths = set()   # create a str_path set, to avoid duplicates?
    for algorithm in algorithms:
        algo_paths = re.sub(r'[()]'," " , algorithm.expression.value()).split() # remove parentheses and split the expression
        for algo in algo_paths:
            if algo in process.pathNames() :    # if the algo matches the path name in process.pathNames() it is added in str_paths
                str_paths.add(algo)
    paths = set()

    for str_path in str_paths:
        paths.add(getattr(process, str_path))   # get the value of the str_path property, of the process object

    return tuple(paths)


