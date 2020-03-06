import sys

from functionModule import runProcessingQgisClip, getGeoJsonFromFeaturesOfOutput, exitCall


def execute(firstGeoJsonFile, SeconGeoJsonFile):
    ats = runProcessingQgisClip(firstGeoJsonFile, SeconGeoJsonFile)
    getGeoJsonFromFeaturesOfOutput(ats)


if len(sys.argv) == 3:
    execute(sys.argv[1], sys.argv[2])
else:
    print("there should be 2 arguments, inputFile1, inputFile2. Now there are ", len(sys.argv) - 1)
exitCall()
