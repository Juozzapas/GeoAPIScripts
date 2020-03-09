import json
import sys

from qgis.core import QgsApplication, QgsJsonExporter, QgsVectorLayer, QgsCoordinateReferenceSystem

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

def execute():
    if len(sys.argv) == 3:

        ats = runProcessingNativeBuffer(sys.argv[1], sys.argv[2])
        print(ats)
        vl1 = ats['OUTPUT']

        features = vl1.getFeatures()
        exporter = QgsJsonExporter()
        print("RESULT_GEOJSON", exporter.exportFeatures(features))
    else:
        print("SCRIPT_ERROR wrong parameters", len(sys.argv))

def runProcessingNativeBuffer(layer, distance):
    return processing.run("native:buffer",
                          {'INPUT': layer,
                           'DISTANCE': distance, 'SEGMENTS': 5,
                           'END_CAP_STYLE': 0, 'JOIN_STYLE': 0,
                           'MITER_LIMIT': 2, 'DISSOLVE': False,
                           'OUTPUT': "TEMPORARY_OUTPUT"})

def runProcessingNativeIntersect(inputLayer, overlayLayer):
    processing.algorithmHelp("native:intersection")
    return processing.run("native:intersection",
                          {'INPUT': inputLayer,
                           'OVERLAY': overlayLayer,
                           'INPUT_FIELDS': [],
                           'OVERLAY_FIELDS': [],
                           'OVERLAY_FIELDS_PREFIX': '',
                           'OUTPUT': 'TEMPORARY_OUTPUT'})

def runProcessingNativeSelectByLocation(inputLayer, overlayLayer, predicate=[0]):
    # processing.algorithmHelp("native:selectbylocation")
    return processing.run("native:selectbylocation",
                          {'INPUT': inputLayer,
                           'PREDICATE': predicate,
                           'INTERSECT': overlayLayer,
                           'METHOD': 0})

def isInt(object):
    try:
        int(object)
        return True
    except ValueError:
        return False


def getGeoJsonFromFeaturesOfOutput(output):
    layer = output['OUTPUT']
    features = layer.getFeatures()
    exporter = QgsJsonExporter()
    print("RESULT_GEOJSON", exporter.exportFeatures(features))


def getGeoJsonFromSelectedFeaturesInLayer(layer):
    features = layer.selectedFeatures()
    exporter = QgsJsonExporter()
    print("RESULT_GEOJSON", exporter.exportFeatures(features))


def getGeoJsonFromFeaturesInLayer(layer):
    features = layer.getFeatures()
    exporter = QgsJsonExporter()
    print("RESULT_GEOJSON", exporter.exportFeatures(features))


def getLayerFromFile(path):
    return QgsVectorLayer(path, "mygeojson", "ogr")


def isDistanceValid(distance):
    if (isInt(distance) and int(distance) > 0):
        return True
    else:
        return False


def exitCall():
    qgs.exitQgis()


def runProcessingQgisSelectByAttribute(input, field, operator, value):
    return processing.run("qgis:selectbyattribute",
                          {'INPUT': input,
                           'FIELD': field,
                           'OPERATOR': operator,
                           'VALUE': value,
                           'METHOD': 0})


def checkIfCrsValid(crs):
    try:
        QgsCrs = QgsCoordinateReferenceSystem(crs)
        if QgsCrs.isValid():
            return True
        else:
            return False
    except:
        print("SCRIPT_ERROR An exception occurred")
        return False


def runProcessingMergeVectorLayers(layerList, crs='None'):
    return processing.run("native:mergevectorlayers",
                          {'LAYERS': layerList,
                           'CRS': crs,
                           'OUTPUT': 'TEMPORARY_OUTPUT'})


def getQgsVectorLayerArray(objectArray):
    vectorArray = []
    for object in objectArray:
        tempJsonObject = json.dumps(object)
        tempLayer = QgsVectorLayer(tempJsonObject, "mygeojson", "ogr")
        vectorArray.append(tempLayer)
    return vectorArray


def runProcessingQgisClip(inputLayer, overlayLayer):
    return processing.run("native:clip",
                          {'INPUT': inputLayer,
                           'OVERLAY': overlayLayer,
                           'OUTPUT': 'TEMPORARY_OUTPUT'})
