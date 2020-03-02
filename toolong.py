from qgis.core import *
import sys
import json
# Supply path to qgis install location
QgsApplication.setPrefixPath('C:/OSGEO4W1/apps/qgis', True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()
sys.path.append('C:\\OSGeo4W64\\apps\\qgis\\python\\plugins')
from qgis.analysis import QgsNativeAlgorithms
import processing
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
# Write your code here to load some layers, use processing
# algorithms, etc.

from qgis.PyQt.QtCore import QVariant
# create layer
vl = QgsVectorLayer("Polygon", "poly", "memory")
pr = vl.dataProvider()

# add fields
pr.addAttributes([QgsField("name", QVariant.String),
                    QgsField("age",  QVariant.Int),
                    QgsField("size", QVariant.Double)])
vl.updateFields() # tell the vector layer to fetch changes from the provider

# add a feature
fet = QgsFeature()
points = [QgsPointXY(50,50),QgsPointXY(50,150),QgsPointXY(100,150),QgsPointXY(100,50)]
fet.setGeometry(QgsGeometry.fromPolygonXY([points]))
fet.setAttributes(["Johny", 2, 0.3])
pr.addFeatures([fet])

# update layer's extent when new features have been added
# because change of extent in provider is not propagated to the layer
vl.updateExtents()
QgsProject.instance().addMapLayers([vl])

#print('\n'.join(map(str, [alg.id() for alg in QgsApplication.processingRegistry().algorithms()])))

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

print(sys.argv[1])
#geoString={"type":"MultiPolygon","coordinates":[[[[540776.621887207,5912792.64251709],[540773.4404907227,5912798.570678711],[540774.3524780273,5912833.500305176],[540773.7451171875,5912839.8787231445],
#                                                  [540781.3389282227,5912846.864685059],[540789.8435058594,5912855.673095703],[540800.170715332,5912865.088500977],[540805.637878418,5912877.541870117],
#                                                  [540806.8529052734,5912887.261291504],[540804.4237060547,5912900.322509766],[540796.8306884766,5912932.8220825195],[540795.3120727539,5912966.841308594],
#                                                  [540800.7799072266,5912984.76171875],[540803.6392822266,5912983.147521973],[540799.428527832,5912964.180908203],[540801.6641235352,5912931.578491211],
#                                                 [540808.3139038086,5912901.5205078125],[540812.0502929688,5912888.047912598],[540810.8626708984,5912876.851501465],[540805.3167114258,5912862.604125977]
#                                                    ,[540796.9296875,5912854.176513672],[540787.0308837891,5912844.229919434],[540777.3010864258,5912836.084289551],[540776.621887207,5912792.64251709]]]]}

#geoString=json.dumps(geoString)

vl = QgsVectorLayer(sys.argv[1],"mygeojson","ogr")

def runProcessingNativeBuffer(inputGeoJson, distance):
    processing.algorithmHelp("native:buffer")
    return processing.run("native:buffer",
                         {'INPUT': inputGeoJson,
                          'DISTANCE': distance, 'SEGMENTS': 5,
                          'END_CAP_STYLE': 0, 'JOIN_STYLE': 0,
                          'MITER_LIMIT': 2, 'DISSOLVE': False,
                          'OUTPUT': "TEMPORARY_OUTPUT"})

ats = runProcessingNativeBuffer(vl, sys.argv[2])

vl1=ats['OUTPUT']
#print ("ATS",ats)
#features = vl1.getFeatures()
#print ("layer",vl1)

features = vl1.getFeatures()
exporter = QgsJsonExporter()
print("GEOJSON",exporter.exportFeatures(features))

#exporting features
#for fet in features:
#   print("F:", fet.id(), fet.attributes(), fet.geometry())
#    print(fet.geometry())

# Finally, exitQgis() is called to remove the
# provider and layer registries from memory

qgs.exitQgis()