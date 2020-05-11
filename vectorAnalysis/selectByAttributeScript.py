import sys

from analysisFunctions.functionModule import ProcessingAlgorithms, LayerManipulation, Validation, exitCall

def main(args):
    if len(args) == 5:
        execute(args[1], args[2], args[3], args[4])
    elif len(args) == 4:
        execute(args[1], args[2], args[3], "")
    else:
        print(
            "SCRIPT_ERROR there should be 3 or 4 arguments, inputFile1, field, operator and optional value. Now there are ",
            len(args) - 1)

    exitCall()


def execute(input, field, operator, value):
    try:
        if not Validation.isOperatorValid(operator):
            print("SCRIPT_ERROR Incorrect parameter value for OPERATOR")
            return;
        layer = LayerManipulation.getLayerFromFile(input)
        if not Validation.attributeExists(layer, field):
            print("SCRIPT_ERROR Incorrect parameter value for FIELD, The FIELD {} does not exist!".format(field))
            return;
        ProcessingAlgorithms.runProcessingQgisSelectByAttribute(layer, field, operator, value)
        geoJson = LayerManipulation.getGeoJsonFromSelectedFeaturesInLayer(layer)
    except Exception as e:
        print("SCRIPT_ERROR prosessing algorithm error " + str(e))
    else:
        print("RESULT_GEOJSON", geoJson)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
