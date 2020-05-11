import sys

from analysisFunctions.functionModule import ProcessingAlgorithms, LayerManipulation, Validation, exitCall


def main(args):
    if len(args) == 3:
        execute(args[1], args[2])
    else:
        print("SCRIPT_ERROR there should be 2 arguments, file and distance. Now there are ", len(args) - 1)

    exitCall()


def execute(firstGeoJsonFile, distance):
    if Validation.isNumber(distance):
        try:
            layer = ProcessingAlgorithms.runProcessingNativeBuffer(firstGeoJsonFile, distance)
            geoJson = LayerManipulation.getGeoJsonFromFeaturesFromLayer(layer)
        except Exception as e:
            print("SCRIPT_ERROR prosessing algorithm error" + str(e))
        else:
            print("RESULT_GEOJSON", geoJson)
    else:
        print("SCRIPT_ERROR distance is not valid")


if __name__ == '__main__':
    sys.exit(main(sys.argv))
