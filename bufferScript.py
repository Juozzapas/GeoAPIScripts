import sys

from functionModule import runProcessingNativeBuffer, getGeoJsonFromFeaturesOfOutput, exitCall, isDistanceValid


def myexecute(firstGeoJsonFile, distance):
    if isDistanceValid(distance):
        ats = runProcessingNativeBuffer(firstGeoJsonFile, distance)
        getGeoJsonFromFeaturesOfOutput(ats)
    else:
        print("distance is not valid")


if len(sys.argv) == 3:
    myexecute(sys.argv[1], sys.argv[2])
else:
    print("there should be 2 arguments, file and distance. Now there are ", len(sys.argv) - 1)

exitCall()
