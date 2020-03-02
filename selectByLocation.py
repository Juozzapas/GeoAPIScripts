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
# if 4 parameters are right execute with options: distance and predicate
# if 2 parameters are right execute with options: distance = 0 and predicate = 0
def execute():
    if len(sys.argv) == 5:
        vl1 = QgsVectorLayer(sys.argv[1], "mygeojson", "ogr")
        intersection = runProcessingNativeSelectByLocation(vl1, secondLayer(), sys.argv[3])
        print(intersection)
        features = vl1.selectedFeatures()
        exporter = QgsJsonExporter()
        print("GEOJSON", exporter.exportFeatures(features))
    elif len(sys.argv) == 3:
        vl1 = QgsVectorLayer(sys.argv[1], "mygeojson", "ogr")
        intersection = runProcessingNativeSelectByLocation(vl1, sys.argv[2])
        print(intersection)
        features = vl1.selectedFeatures()
        exporter = QgsJsonExporter()
        print("GEOJSON", exporter.exportFeatures(features))
    else:
        print("wrong parameters", len(sys.argv))


def runProcessingNativeBuffer(layer, distance):
    print(distance)
    return processing.run("native:buffer",
                          {'INPUT': layer,
                           'DISTANCE': distance, 'SEGMENTS': 5,
                           'END_CAP_STYLE': 0, 'JOIN_STYLE': 0,
                           'MITER_LIMIT': 2, 'DISSOLVE': False,
                           'OUTPUT': "TEMPORARY_OUTPUT"})


def runProcessingNativeSelectByLocation(inputLayer, overlayLayer, predicate=[0]):
    # processing.algorithmHelp("native:selectbylocation")
    return processing.run("native:selectbylocation",
                          {'INPUT': inputLayer,
                           'PREDICATE': predicate,
                           'INTERSECT': overlayLayer,
                           'METHOD': 0})


def secondLayer():
    distance = sys.argv[4]
    pathToLayer = sys.argv[2]
    if (isInt(distance) and int(distance) > 0):
        buffer = runProcessingNativeBuffer(pathToLayer, distance)
        return buffer['OUTPUT']
    else:
        return pathToLayer


def isInt(object):
    try:
        int(object)
        return True
    except ValueError:
        return False


execute()
# Finally, exitQgis() is called to remove the
# provider and layer registries from memory

qgs.exitQgis()
