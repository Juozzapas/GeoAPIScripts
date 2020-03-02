import sys
from functionModule import getLayerFromFile, getGeoJsonFromSelectedFeaturesInLayer,exitCall,runProcessingNativeBuffer,isDistanceValid,runProcessingNativeSelectByLocation

def execute(firstGeoJsonFile,SeconGeoJsonFile,predicate,distance):
    if len(sys.argv) == 5:
        layer = getLayerFromFile(firstGeoJsonFile)
        if(isDistanceValid(distance)):
            runProcessingNativeSelectByLocation(layer, bufferedLayer(SeconGeoJsonFile,distance), predicate)
        else:
            runProcessingNativeSelectByLocation(layer, SeconGeoJsonFile)
        getGeoJsonFromSelectedFeaturesInLayer(layer)
    else:
        print("wrong parameters", len(sys.argv))


def bufferedLayer(pathToLayer,distance):
    buffer = runProcessingNativeBuffer(pathToLayer, distance)
    return buffer['OUTPUT']

execute(sys.argv[1], sys.argv[2],sys.argv[3], sys.argv[4])
exitCall()
