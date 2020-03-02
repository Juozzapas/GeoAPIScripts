import sys
from functionModule import runProcessingQgisSelectByAttribute, exitCall,getLayerFromFile,getGeoJsonFromSelectedFeaturesInLayer

def execute(input,field,operator,value):
    layer = getLayerFromFile(input)
    runProcessingQgisSelectByAttribute(layer,field,operator,value)
    getGeoJsonFromSelectedFeaturesInLayer(layer)

execute(sys.argv[1], sys.argv[2],sys.argv[3], sys.argv[4])
exitCall()
