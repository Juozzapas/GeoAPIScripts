import sys

from analysisFunctions.functionModule import ProcessingAlgorithms, LayerManipulation, exitCall


def main(args):
    if len(args) == 3:
        execute(args[1], args[2])
    else:
        print("SCRIPT_ERROR there should be 2 arguments, inputFile1, inputFile2. Now there are ", len(args) - 1)
    exitCall()


def execute(firstGeoJsonFile, SeconGeoJsonFile):
    try:
        layer = ProcessingAlgorithms.runProcessingQgisClip(firstGeoJsonFile, SeconGeoJsonFile)
        geoJson = LayerManipulation.getGeoJsonFromFeaturesFromLayer(layer)
    except:
        print("SCRIPT_ERROR prosessing algorithm error")
    else:
        print("RESULT_GEOJSON", geoJson)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
