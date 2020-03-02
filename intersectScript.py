import sys
from functionModule import runProcessingNativeIntersect, getGeoJsonFromFeaturesOfOutput,exitCall
def execute(firstGeoJsonFile,SeconGeoJsonFile):
    if len(sys.argv) == 3:
        ats = runProcessingNativeIntersect(firstGeoJsonFile, SeconGeoJsonFile)
        getGeoJsonFromFeaturesOfOutput(ats)
    else:
        print("wrong parameters", len(sys.argv))

execute(sys.argv[1], sys.argv[2])
exitCall()

