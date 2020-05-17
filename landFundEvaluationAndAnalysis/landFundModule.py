import sys
from qgis.core import QgsApplication, QgsJsonExporter, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsFeatureRequest,QgsField
from abc import ABC

from qgis.PyQt.QtCore import QVariant


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
    def __init__(self):
        pass

    def runProcessingNativeSelectByLocation(self, inputLayer, overlayLayer):
        # processing.algorithmHelp("native:selectbylocation")
        rez = processing.run("native:selectbylocation",
                             {'INPUT': inputLayer,
                              'PREDICATE': [0],
                              'INTERSECT': overlayLayer,
                              'METHOD': 0})
        return rez['OUTPUT']

    def runProcessingCentroids(self, inputLayer):
        # processing.algorithmHelp("native:selectbylocation")
        rez = processing.run("native:centroids",
                             {'INPUT': inputLayer, 'ALL_PARTS': False, 'OUTPUT': 'TEMPORARY_OUTPUT'})
        return rez['OUTPUT']

    def runProcessingSimplifyGeometries(self, inputLayer):
        # processing.algorithmHelp("native:selectbylocation")
        rez = processing.run("native:simplifygeometries",
                             {'INPUT': inputLayer, 'METHOD': 0, 'TOLERANCE': 1000, 'OUTPUT': 'TEMPORARY_OUTPUT'})
        return rez['OUTPUT']

    def runProcessingNativeBuffer(self, layer, distance):
        rez = processing.run("native:buffer",
                             {'INPUT': layer,
                              'DISTANCE': distance, 'SEGMENTS': 5,
                              'END_CAP_STYLE': 0, 'JOIN_STYLE': 0,
                              'MITER_LIMIT': 2, 'DISSOLVE': False,
                              'OUTPUT': "TEMPORARY_OUTPUT"})
        return rez['OUTPUT']

    def runProcessingQgisExportAddGeometryColumns(self, layer):
        rez = processing.run("qgis:exportaddgeometrycolumns",
                             {'INPUT': layer, 'CALC_METHOD': 0,
                              'OUTPUT': 'TEMPORARY_OUTPUT'})
        return rez['OUTPUT']

    def runProcessingQgisDeleteColumn(self, inputLayer, columns):
        return processing.run("qgis:deletecolumn",
                              {'INPUT': inputLayer, 'COLUMN': columns,
                               'OUTPUT': 'TEMPORARY_OUTPUT'})

    def runProcessingNativeIntersectSkipInvalid(self, inputLayer, overlayLayer):
        context = dataobjects.createContext()
        context.setInvalidGeometryCheck(QgsFeatureRequest.GeometrySkipInvalid)
        processing.algorithmHelp("native:intersection")
        rez = processing.run("native:intersection",
                             {'INPUT': inputLayer,
                              'OVERLAY': overlayLayer,
                              'INPUT_FIELDS': [],
                              'OVERLAY_FIELDS': [],
                              'OVERLAY_FIELDS_PREFIX': '',
                              'OUTPUT': 'TEMPORARY_OUTPUT'}, context=context)
        return rez['OUTPUT']

class BaseResult(ABC):
    def __init__(self):
        self.inputArea = 0
        self.area = 0
        self.perimeter = 0
        self.overlapping = 0

    def aggregateField(self, features, field):
        temp = 0
        for feature in features:
            temp+= feature[field]
        return temp

    def calculateOverlapping(self, dividend, divisor):
        if divisor != 0:
            self.overlapping = dividend * 100 / divisor

    def calculateInputArea(self, features):
        for feature in features:
            self.inputArea += feature["area"]

    def calculateGeometryInfo(self, features):
        pass

    def getResult(self, featureCount, geoJson):
        pass

class ResultDIRV_DR10LT(BaseResult):
    def __init__(self):
        BaseResult.__init__(self)
        self.weightedSum = 0
        self.weightedAverage = 0

    def calculateGeometryInfo(self, features):
        for feature in features:
            if feature["balas"] != -1:
                self.area += feature["area"]
                self.weightedSum += feature["area"] * feature["balas"]
                self.perimeter += feature["perimeter"]

    def calculatedWeightedAverage(self):
        if self.area != 0:
            self.weightedAverage = self.weightedSum / self.area

    def getResult(self, featureCount, geoJson):
        self.calculateOverlapping(self.area, self.inputArea)
        self.calculatedWeightedAverage()
        x = {
            "areaHa": round(self.inputArea / 1000, 2),
            "overlappingAreaHa": round(self.area / 1000, 2),
            "overlappingAreaProc": round(self.overlapping, 2),
            "overlappingPerimeterM": round(self.perimeter, 2),
            "overlappingFeatureCount": featureCount,
            "soilFertilityScore": round(self.weightedAverage, 2),
            "overlappingFeatureGeoJson": geoJson
        }
        return x

class ResultAZ_DR10LT(BaseResult):
    def __init__(self):
        BaseResult.__init__(self)

    def calculateGeometryInfo(self, features):
        for feature in features:
            self.area += feature["area"]
            self.perimeter += feature["perimeter"]

    def getResult(self, featureCount, geoJson):
        self.calculateOverlapping(self.area, self.inputArea)
        x = {
            "areaHa": round(self.inputArea / 1000, 2),
            "overlappingAreaHa": round(self.area / 1000, 2),
            "overlappingAreaProc": round(self.overlapping, 2),
            "overlappingPerimeterM": round(self.perimeter, 2),
            "overlappingFeatureCount": featureCount,
            "overlappingFeatureGeoJson": geoJson
        }
        return x

class LandFundAnalysis:
    def __init__(self):
        self.alg = ProcessingAlgorithms()

    def attributeExists(self,layer, fieldName):
        field_index = layer.fields().indexFromName(fieldName)

        if field_index == -1:
            return False
        else:
            return True

    def getGeoJsonFromLayerNoAttributesIncluded(self, layer):
        features = layer.getFeatures()
        exporter = QgsJsonExporter()
        if self.attributeExists(layer,'BALAS'):
            exporter.setAttributes([ layer.fields().indexFromName('BALAS')])
        else:
            exporter.setIncludeAttributes(False)
        return exporter.exportFeatures(features)

    def getGeoJsonFromLayer(self, layer):
        features = layer.getFeatures()
        exporter = QgsJsonExporter()
        return exporter.exportFeatures(features)

    def getLayerFromFile(self, path):
        return QgsVectorLayer(path, "myLayer", "ogr")

    def deleteAllFields(self, layer):
        layer.startEditing()
        layer.deleteAttributes(layer.dataProvider().attributeIndexes())
        layer.commitChanges()

    def setLayerCrs(self,layer,crs):
        layer.setCrs(QgsCoordinateReferenceSystem(crs))

    def prepareInputLayer(self, path, distance):
        layer = self.getLayerFromFile(path)
        self.deleteAllFields(layer)
        self.setLayerCrs(layer,"EPSG:3346")
        if self.isDistanceValid(distance):
            layer = self.alg.runProcessingNativeBuffer(layer, distance)
        return layer

    def addFieldsToLayer(self, layer, fieldList):
        layer.startEditing()
        layer.dataProvider().addAttributes(fieldList)
        layer.commitChanges()

    def calculateVerticesAndCentroid(self, layer):
        layer.startEditing()
        vertices = 0
        for feature in layer.getFeatures():
            point = feature.geometry().centroid().asPoint()
            for vertice in feature.geometry().vertices():
                vertices += 1
            feature.setAttribute("vertices", vertices - 1)
            feature.setAttribute("centroid", str(point.x()) + " " + str(point.y()))
            layer.updateFeature(feature)

    def processInputLayer(self, layer):
        self.addFieldsToLayer(layer, [QgsField("vertices", QVariant.String), QgsField("centroid", QVariant.String)])
        self.calculateVerticesAndCentroid(layer)
        resultLayer = self.alg.runProcessingQgisExportAddGeometryColumns(layer)
        return self.getGeoJsonFromLayer(resultLayer)

    def startAnalyzis(self, layerToAnalyze, pathToDataSet, analysisObject):

        evaluationLayer = self.getLayerFromFile(pathToDataSet)

        self.alg.runProcessingNativeSelectByLocation(evaluationLayer, layerToAnalyze)
        if evaluationLayer.selectedFeatureCount() == 0:
            x = {"results": "not overlaping"}
            return x;

        selectedFeatureLayer = evaluationLayer.materialize(
            QgsFeatureRequest().setFilterFids(evaluationLayer.selectedFeatureIds()))

        intersectResultLayer = self.alg.runProcessingNativeIntersectSkipInvalid(selectedFeatureLayer,
                                                                                    layerToAnalyze)
        intersectResultLayer = self.alg.runProcessingQgisExportAddGeometryColumns(intersectResultLayer)
        layerToAnalyze = self.alg.runProcessingQgisExportAddGeometryColumns(layerToAnalyze)
        features = intersectResultLayer.getFeatures()
        analysisObject.calculateGeometryInfo(features)
        features = layerToAnalyze.getFeatures()
        analysisObject.calculateInputArea(features)

        return {"results": analysisObject.getResult(intersectResultLayer.featureCount(),
                                                       self.getGeoJsonFromLayerNoAttributesIncluded(
                                                           intersectResultLayer))}

    def exitCall(self):
        qgs.exitQgis()

    def isDistanceValid(self, distance):
        try:
            float(distance)
            return True
        except ValueError:
            return False

    def isPredicateListValid(self, predicateList):
        try:
            for number in predicateList:
                temp = int(number)
                if temp > 2 or temp < 0:
                    return False
            return True
        except ValueError:
            return False


# Finally, exitQgis() method removes provider and layer registries from memory
def exitCall():
    qgs.exitQgis()
