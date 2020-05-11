import sys

from analysisFunctions.functionModule import ProcessingAlgorithms, LayerManipulation, Validation, exitCall


def main(args):
    if len(args) == 3:
        execute(args[1], args[2])
    else:
        print("SCRIPT_ERROR there should be 2 arguments, inputFile1, inputFile2. Now there are ", len(args) - 1)
    exitCall()


def execute(firstGeoJsonFile, SeconGeoJsonFile):
    try:
        inputLayer = LayerManipulation.getLayerFromFile(firstGeoJsonFile)
        ProcessingAlgorithms.runProcessingNativeSelectByLocation(inputLayer, SeconGeoJsonFile, [0])
        layerToExport = LayerManipulation.layerFromSelectedFeaturesLayer(inputLayer)
        if not Validation.isSelectedFeaturesEmpty(inputLayer):
            layerToExport = ProcessingAlgorithms.runProcessingNativeIntersect(layerToExport, SeconGeoJsonFile)

        geoJson = LayerManipulation.getGeoJsonFromFeaturesFromLayer(layerToExport)
    except Exception as e:
        print("SCRIPT_ERROR prosessing algorithm error" + str(e))
    else:
        print("RESULT_GEOJSON", geoJson)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
