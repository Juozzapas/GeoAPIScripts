import json
import sys

from qgis.core import QgsApplication, QgsJsonExporter, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsFeatureRequest

print("dsdsdsd")
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
from processing.tools import dataobjects
from processing.core.Processing import Processing

print("dsdsdsd")
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())


# Write your code here to load some layers, use processing
# algorithms, etc.

class ProcessingAlgorithms:
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

    def runProcessingQgisSelectByAttribute(input, field, operator, value):
        return processing.run("qgis:selectbyattribute",
                              {'INPUT': input,
                               'FIELD': field,
                               'OPERATOR': operator,
                               'VALUE': value,
                               'METHOD': 0})

    def runProcessingQgisClip(inputLayer, overlayLayer):
        return processing.run("native:clip",
                              {'INPUT': inputLayer,
                               'OVERLAY': overlayLayer,
                               'OUTPUT': 'TEMPORARY_OUTPUT'})

    def runProcessingMergeVectorLayers(layerList, crs='None'):
        return processing.run("native:mergevectorlayers",
                              {'LAYERS': layerList,
                               'CRS': crs,
                               'OUTPUT': 'TEMPORARY_OUTPUT'})

    def runProcessingQgisExportAddGeometryColumns(layer):
        return processing.run("qgis:exportaddgeometrycolumns",
                              {'INPUT': layer, 'CALC_METHOD': 0,
                               'OUTPUT': 'TEMPORARY_OUTPUT'})

    def runProcessingNativeIntersectSkipInvalid(inputLayer, overlayLayer):
        context = dataobjects.createContext()
        context.setInvalidGeometryCheck(QgsFeatureRequest.GeometrySkipInvalid)
        processing.algorithmHelp("native:intersection")
        return processing.run("native:intersection",
                              {'INPUT': inputLayer,
                               'OVERLAY': overlayLayer,
                               'INPUT_FIELDS': [],
                               'OVERLAY_FIELDS': [],
                               'OVERLAY_FIELDS_PREFIX': '',
                               'OUTPUT': 'TEMPORARY_OUTPUT'}, context=context)


def analysisDIRV_DB10LT1(inputFile):
    info_layer = getLayerFromFile("C:\\Users\\Username\\Desktop\\New folder (2)\\vertinimas.shp")
    input_layer = getLayerFromFile(inputFile)

    ats = ProcessingAlgorithms.runProcessingNativeIntersectSkipInvalid(info_layer, input_layer)
    layer = ats['OUTPUT']
    ats = ProcessingAlgorithms.runProcessingQgisExportAddGeometryColumns(layer)
    layer = ats['OUTPUT']

    layerArea = 0
    weightedSum = 0
    dropedArea = 0
    features = layer.getFeatures()
    for feature in features:
        if feature["BALAS"] != -1:
            layerArea += feature["area"]
            weightedSum += feature["area"] * feature["Balas"]
        else:
            dropedArea += feature["area"]

    ats2 = ProcessingAlgorithms.runProcessingQgisExportAddGeometryColumns(input_layer)
    input_layer = ats2['OUTPUT']
    plotas2 = 0
    for feature in input_layer.getFeatures():
        plotas2 += feature["area"]

    sutampa = layerArea * 100 / (plotas2)
    nesutampa = 100 - sutampa
    x = {
        "sutampa": sutampa,
        "nesutampa": nesutampa,
        "svertinas vidurkis": weightedSum / layerArea,
    }
    print(x)


def analysisAZ_PR10LT(inputFile):
    info_layer = getLayerFromFile("C:\\Users\\Username\\Desktop\\apleistos_zemes.shp")
    input_layer = getLayerFromFile(inputFile)

    ats = ProcessingAlgorithms.runProcessingNativeIntersectSkipInvalid(info_layer, input_layer)
    layer = ats['OUTPUT']
    ats = ProcessingAlgorithms.runProcessingQgisExportAddGeometryColumns(layer)
    layer = ats['OUTPUT']

    layerArea = 0
    features = layer.getFeatures()
    for feature in features:
        layerArea += feature["area"]

    ats2 = ProcessingAlgorithms.runProcessingQgisExportAddGeometryColumns(input_layer)
    input_layer = ats2['OUTPUT']
    plotas2 = 0
    for feature in input_layer.getFeatures():
        plotas2 += feature["area"]

    sutampa = layerArea * 100 / (plotas2)
    nesutampa = 100 - sutampa
    x = {
        "sutampa": sutampa,
        "nesutampa": nesutampa,
    }
    print(x)


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

def getQgsVectorLayerArray(objectArray):
    vectorArray = []
    for object in objectArray:
        tempJsonObject = json.dumps(object)
        tempLayer = QgsVectorLayer(tempJsonObject, "mygeojson", "ogr")
        vectorArray.append(tempLayer)
    return vectorArray
