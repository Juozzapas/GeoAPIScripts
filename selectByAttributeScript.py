import sys

from functionModule import runProcessingQgisSelectByAttribute, exitCall, getLayerFromFile, \
    getGeoJsonFromSelectedFeaturesInLayer


def execute(input, field, operator, value):
    layer = getLayerFromFile(input)
    runProcessingQgisSelectByAttribute(layer, field, operator, value)
    getGeoJsonFromSelectedFeaturesInLayer(layer)


if len(sys.argv) == 5:
    execute(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
else:
    print("there should be 4 arguments, inputFile1, field, operator, value. Now there are ", len(sys.argv) - 1)

exitCall()
