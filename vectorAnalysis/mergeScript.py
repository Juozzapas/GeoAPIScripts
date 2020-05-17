import json
import sys

from vectorAnalysis.vectorAnalysisModule import ProcessingAlgorithms, LayerManipulation, Validation, exitCall


def execute(file, crs):

    if crs != 'None' and not Validation.checkIfCrsValid(crs):
       print("SCRIPT_ERROR Invalid crs: " + crs)
    else:
        try:
            with open(file) as f:
                objectArray = json.loads(f.read())
            vectorLayerArray = LayerManipulation.getQgsVectorLayerArray(objectArray)
            ats = ProcessingAlgorithms.runProcessingMergeVectorLayers(vectorLayerArray, crs)
            ats = ProcessingAlgorithms.runProcessingQgisDeleteColumn(ats,['layer','path'])
            geoJson = LayerManipulation.getGeoJsonFromFeaturesOfOutput(ats)
        except Exception as s:
            print("SCRIPT_ERROR processing algorithm error" + str(s))
        else:
            print("RESULT_GEOJSON", geoJson)


def main(args):
    if len(args) == 3:
        execute(args[1], args[2])
    else:
        print("SCRIPT_ERROR there should be 2 arguments, file, crs. Now there are", len(args) - 1)
    exitCall()
if __name__ == '__main__':
    sys.exit(main(sys.argv))