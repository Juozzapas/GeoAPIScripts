import sys
import json
import os
from landFundEvaluationAndAnalysis.landFundModule import exitCall, \
    LandFundAnalysis,ResultAZ_DR10LT,ResultDIRV_DR10LT

path= os.path.dirname(os.path.abspath(__file__))
parent = os.path.join(path, os.pardir)
absParent=os.path.abspath(parent)
DIRV_DR10LTFilePath=os.path.join(absParent,"Data_sets\\vertinimas.shp")
AZ_DR10LTFilePath=os.path.join(absParent,"Data_sets\\apleistos_zemes.shp")
print (DIRV_DR10LTFilePath)
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
                answer = instance.startAnalyzis(layer, DIRV_DR10LTFilePath
                                                , ResultDIRV_DR10LT())
                x.update(DIRV_DR10LT=answer)
        except:
            x.update(DIRV_DR10LT="unableToCalculate")
        try:
            if '1' in predicateList:
                answer = instance.startAnalyzis(layer, AZ_DR10LTFilePath, ResultAZ_DR10LT())
                x.update(AZ_DR10LT=answer)
        except:
            x.update(AZ_DR10LT="unableToCalculate")
        x.update(baseAnalysis=instance.processInputLayer(layer))
        x = json.dumps(x)
        print("RESULT_GEOJSON", x)
    else:
        print("SCRIPT_ERROR predicate list does not contain values representing existing operations")
if __name__ == '__main__':
    sys.exit(main(sys.argv))
exitCall()

