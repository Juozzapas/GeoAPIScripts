import sys
import json

from landFundEvaliationAndAnalysis.landFundModule import exitCall, \
    LandFund

def main(args):
    if len(args) == 4:
        execute(args[1], args[2], args[3])
    elif len(args) == 3:
        execute(args[1], args[2], "Invalid")
    else:
        print("SCRIPT_ERROR there should be 2 or 3 arguments, inputFilePath, distance, predicate (optional). Now there are",
              len(args) - 1)

def execute(firstGeoJsonFile, predicate, distance):
    instance = LandFund()
    predicateList = predicate.split(',')
    x = {}
    if instance.isPredicateListValid(predicateList):
        layer = instance.prepareInputLayer(firstGeoJsonFile, distance)
        try:
            if '0' in predicateList:
                answer = instance.analysisDIRV_DB10LT(layer,
                                                      "C:\\Users\\Username\\Desktop\\New folder (2)\\vertinimas.shp")
                x.update(DIRV_DB10LT=answer)
        except:
            x.update(DIRV_DB10LT="unableToCalculate")
        try:
            if '1' in predicateList:
                answer = instance.analysisAZ_PR10LT(layer, "C:\\Users\\Username\\Desktop\\apleistos_zemes.shp")
                x.update(AZ_PR10LT=answer)
        except:
            x.update(AZ_PR10LT="unableToCalculate")
        x = getJson(x)
        print("RESULT_GEOJSON", x)
    else:
        print("SCRIPT_ERROR predicate list does not contain values representing existing operations")


def getJson(str):
    return json.dumps(str)
if __name__ == '__main__':
    sys.exit(main(sys.argv))

