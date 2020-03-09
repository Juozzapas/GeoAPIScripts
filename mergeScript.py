import json
import sys

from functionModule import runProcessingMergeVectorLayers, getGeoJsonFromFeaturesOfOutput, exitCall, \
    getQgsVectorLayerArray, checkIfCrsValid, isInt


def execute(file, crs):
    if (isInt(crs)):
        crs = int(crs)
    if (crs == 'None' or checkIfCrsValid("EPSG:4326")):
        with open(file) as f:
            objectArray = json.loads(f.read())
        vectorLayerArray = getQgsVectorLayerArray(objectArray)
        ats = runProcessingMergeVectorLayers(vectorLayerArray, crs)
        getGeoJsonFromFeaturesOfOutput(ats)
    else:
        print("SCRIPT_ERROR Invalid crs: " + crs)


if len(sys.argv) == 3:
    execute(sys.argv[1], sys.argv[2])
else:
    print("SCRIPT_ERROR there should be 2 arguments, file, crs. Now there are", len(sys.argv) - 1)

exitCall()
