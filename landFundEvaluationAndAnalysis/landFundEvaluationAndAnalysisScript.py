import sys
import json
import os
from landFundEvaluationAndAnalysis.landFundModule import exitCall, \
    LandFundAnalysis,ResultAZ_PR10LT,ResultDIRV_DB10LT


DIRV_DB10LTFilePath=os.path.join(os.getcwd(),"Data_sets\\vertinimas.shp")
AZ_PR10LTFilePath=os.path.join(os.getcwd(),"Data_sets\\apleistos_zemes.shp")
def main(args):

    if len(args) == 4:
        execute(args[1], args[2], args[3])
    elif len(args) == 3:
        execute(args[1], args[2], "Invalid")
    else:
        print("SCRIPT_ERROR there should be 2 or 3 arguments, inputFilePath, distance, predicate (optional). Now there are",
              len(args) - 1)

def execute(firstGeoJsonFile, predicate, distance):
    instance = LandFundAnalysis()
    predicateList = predicate.split(',')
    x = {}
    if instance.isPredicateListValid(predicateList):
        layer = instance.prepareInputLayer(firstGeoJsonFile, distance)
        try:
            if '0' in predicateList:
                answer = instance.startAnalyzis(layer,DIRV_DB10LTFilePath
                                                      ,ResultDIRV_DB10LT())
                x.update(DIRV_DB10LT=answer)
        except:
            x.update(DIRV_DB10LT="unableToCalculate")
        try:
            if '1' in predicateList:
                answer = instance.startAnalyzis(layer,AZ_PR10LTFilePath,ResultAZ_PR10LT())
                x.update(AZ_PR10LT=answer)
        except:
            x.update(AZ_PR10LT="unableToCalculate")
        x.update(baseAnalysis=instance.processInputLayer(layer))
        x = json.dumps(x)
        print("RESULT_GEOJSON", x)
    else:
        print("SCRIPT_ERROR predicate list does not contain values representing existing operations")
if __name__ == '__main__':
    sys.exit(main(sys.argv))
exitCall()

