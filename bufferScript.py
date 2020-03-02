from functionModule import runProcessingNativeBuffer, getGeoJsonFromFeaturesOfOutput,exitCall, isDistanceValid
import sys

def myexecute(firstGeoJsonFile,distance):
    if len(sys.argv) == 3 and isDistanceValid(distance):
        ats = runProcessingNativeBuffer(firstGeoJsonFile, distance)
        getGeoJsonFromFeaturesOfOutput(ats)
    else:
        print("wrong parameters", len(sys.argv))
myexecute(sys.argv[1], sys.argv[2])
exitCall