import json
import sys

from qgis.core import QgsApplication, QgsJsonExporter, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsFeatureRequest

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

Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())


# Write your code here to load some layers, use processing
# algorithms, etc.

class ProcessingAlgorithms:
    def runProcessingNativeBuffer(layer, distance):
        rez = processing.run("native:buffer",
                             {'INPUT': layer,
                              'DISTANCE': distance, 'SEGMENTS': 5,
                              'END_CAP_STYLE': 0, 'JOIN_STYLE': 0,
                              'MITER_LIMIT': 2, 'DISSOLVE': False,
                              'OUTPUT': "TEMPORARY_OUTPUT"})
        return rez['OUTPUT']

    def runProcessingNativeIntersect(inputLayer, overlayLayer):
        processing.algorithmHelp("native:intersection")
        rez = processing.run("native:intersection",
                             {'INPUT': inputLayer,
                              'OVERLAY': overlayLayer,
                              'INPUT_FIELDS': [],
                              'OVERLAY_FIELDS': [],
                              'OVERLAY_FIELDS_PREFIX': '',
                              'OUTPUT': 'TEMPORARY_OUTPUT'})
        return rez['OUTPUT']

    def runProcessingNativeSelectByLocation(inputLayer, overlayLayer, predicate):
        # processing.algorithmHelp("native:selectbylocation")
        print(inputLayer.crs())
        rez = processing.run("native:selectbylocation",
                             {'INPUT': inputLayer,
                              'PREDICATE': predicate,
                              'INTERSECT': overlayLayer,
                              'METHOD': 0})
        return rez['OUTPUT']

    def runProcessingQgisSelectByAttribute(input, field, operator, value):
        return processing.run("qgis:selectbyattribute",
                              {'INPUT': input,
                               'FIELD': field,
                               'OPERATOR': operator,
                               'VALUE': value,
                               'METHOD': 0})

    def runProcessingQgisClip(inputLayer, overlayLayer):
        rez = processing.run("native:clip",
                             {'INPUT': inputLayer,
                              'OVERLAY': overlayLayer,
                              'OUTPUT': 'TEMPORARY_OUTPUT'})
        return rez['OUTPUT']

    def runProcessingMergeVectorLayers(layerList, crs='None'):
        rez = processing.run("native:mergevectorlayers",
                             {'LAYERS': layerList,
                              'CRS': crs,
                              'OUTPUT': 'TEMPORARY_OUTPUT'})
        return rez['OUTPUT']

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

    def runProcessingQgisDeleteColumn(inputLayer, columns):
        return processing.run("qgis:deletecolumn",
                              {'INPUT': inputLayer, 'COLUMN': columns,
                               'OUTPUT': 'TEMPORARY_OUTPUT'})


class LayerManipulation:
    def getQgsVectorLayerArray(objectArray):
        vectorArray = []
        for object in objectArray:
            tempJsonObject = json.dumps(object)
            tempLayer = QgsVectorLayer(tempJsonObject)
            vectorArray.append(tempLayer)
        return vectorArray

    def getGeoJsonFromSelectedFeaturesInLayer(layer):
        features = layer.selectedFeatures()
        exporter = QgsJsonExporter()
        return exporter.exportFeatures(features)

    def getGeoJsonFromFeaturesInLayer(layer):
        features = layer.getFeatures()
        exporter = QgsJsonExporter()
        print("RESULT_GEOJSON", exporter.exportFeatures(features))

    def getLayerFromFile(path):
        return QgsVectorLayer(path, "mygeojson", "ogr")

    def getGeoJsonFromFeaturesOfOutput(output):
        layer = output['OUTPUT']
        features = layer.getFeatures()
        exporter = QgsJsonExporter()
        return exporter.exportFeatures(features)

    def getGeoJsonFromFeaturesFromLayer(layer):
        features = layer.getFeatures()
        exporter = QgsJsonExporter()
        return exporter.exportFeatures(features)

    def layerFromSelectedFeaturesLayer(layer):
        return layer.materialize(QgsFeatureRequest().setFilterFids(layer.selectedFeatureIds()))

    def getResult(output):
        return output['OUTPUT']


class Validation:
    def isSelectedFeaturesEmpty(layer):
        if layer.selectedFeatureCount() == 0:
            return True
        return False

    def isNumber(object):
        try:
            float(object)
            return True
        except ValueError:
            return False

    def isInt(object):
        try:
            int(object)
            return True
        except ValueError:
            return False

    def attributeExists(layer, fieldName):
        field_index = layer.fields().indexFromName(fieldName)

        if field_index == -1:
            return False
        else:
            return True

    def isOperatorValid(operator):
        try:
            x = int(operator)
            if x <= 10 and x >= 0:
                return True
            return False
        except ValueError:
            return False

    def isPredicateValid(predicate):
        try:
            x = predicate.split(',')
            for number in x:
                temp = int(number)
                if temp > 7 or temp < 0:
                    return False
            return True
        except ValueError:
            return False

    def isLayerEmpty(layer):
        if layer.featureCount() == 0:
            return True
        return False

    def isLayerSelectedFeaturesEmpty(layer):
        if layer.selectedFeatureCount() == 0:
            return True
        return False

    def checkIfCrsValid(crs):
        try:
            QgsCrs = QgsCoordinateReferenceSystem(crs)
            if QgsCrs.isValid():
                return True
            else:
                return False
        except:
            print("SCRIPT_ERROR An exception occurred while trying to check crs")
            return False


def exitCall():
    qgs.exitQgis()
