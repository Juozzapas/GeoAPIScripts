import sys

from functionModule import getLayerFromFile, getGeoJsonFromSelectedFeaturesInLayer, exitCall, runProcessingNativeBuffer, \
    isDistanceValid, runProcessingNativeSelectByLocation


def execute(firstGeoJsonFile, SeconGeoJsonFile, predicate, distance):
    layer = getLayerFromFile(firstGeoJsonFile)
    if (isDistanceValid(distance)):
        runProcessingNativeSelectByLocation(layer, bufferedLayer(SeconGeoJsonFile, distance), predicate)
    else:
        runProcessingNativeSelectByLocation(layer, SeconGeoJsonFile)
    getGeoJsonFromSelectedFeaturesInLayer(layer)


def bufferedLayer(pathToLayer, distance):
    buffer = runProcessingNativeBuffer(pathToLayer, distance)
    return buffer['OUTPUT']


if len(sys.argv) == 5:
    execute(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
else:
    print("SCRIPT_ERROR there should be 4 arguments, inputFile1, inputFile2, predicate, distance. Now there are ",
          len(sys.argv) - 1)
exitCall()
