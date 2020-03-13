import sys

from functionModule import ProcessingAlgorithms, getGeoJsonFromFeaturesOfOutput, exitCall, isDistanceValid


def myexecute(firstGeoJsonFile, distance):
    if isDistanceValid(distance):
        ats = ProcessingAlgorithms.runProcessingNativeBuffer(firstGeoJsonFile, distance)
        getGeoJsonFromFeaturesOfOutput(ats)
    else:
        print("SCRIPT_ERROR distance is not valid")

if len(sys.argv) == 3:
    myexecute(sys.argv[1], sys.argv[2])
else:
    print("SCRIPT_ERROR there should be 2 arguments, file and distance. Now there are ", len(sys.argv) - 1)

exitCall()
