import sys

from functionModule import runProcessingNativeIntersect, getGeoJsonFromFeaturesOfOutput, exitCall


def execute(firstGeoJsonFile, SeconGeoJsonFile):
    ats = runProcessingNativeIntersect(firstGeoJsonFile, SeconGeoJsonFile)
    getGeoJsonFromFeaturesOfOutput(ats)


if len(sys.argv) == 3:
    execute(sys.argv[1], sys.argv[2])
else:
    print("SCRIPT_ERROR there should be 2 arguments, inputFile1, inputFile2. Now there are ", len(sys.argv) - 1)
exitCall()
