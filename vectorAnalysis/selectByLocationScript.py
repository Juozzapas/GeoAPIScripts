import sys

from analysisFunctions.functionModule import ProcessingAlgorithms, LayerManipulation, Validation, exitCall

def execute(firstGeoJsonFile, SeconGeoJsonFile, predicate, distance):
    if not Validation.isPredicateListValid(predicate):
        print("SCRIPT_ERROR Incorrect parameter value for PREDICATE")
        return
    try:
        layer = LayerManipulation.getLayerFromFile(firstGeoJsonFile)
        layer2 = LayerManipulation.getLayerFromFile(SeconGeoJsonFile)
        if (Validation.isNumber(distance)):
            layer2= ProcessingAlgorithms.runProcessingNativeBuffer(layer2, distance)
        ProcessingAlgorithms.runProcessingNativeSelectByLocation(layer, layer2, predicate)
    except:
        print("SCRIPT_ERROR prosessing algorithm error")
    else:
        geoJson = LayerManipulation.getGeoJsonFromSelectedFeaturesInLayer(layer)
        print("RESULT_GEOJSON", geoJson)

def main(args):
    if len(args) == 5:
        execute(args[1], args[2], args[3], args[4])
    elif len(args) == 4:
        execute(args[1], args[2], args[3], "InvalidDistance")
    else:
        print("SCRIPT_ERROR there should be 4 or 3 arguments, inputFile1, inputFile2, predicate with optional distance. Now there are ",
              len(args) - 1)
    exitCall()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
