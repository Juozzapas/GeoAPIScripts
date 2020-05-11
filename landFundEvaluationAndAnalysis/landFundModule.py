import json
import sys

from qgis.core import QgsApplication, QgsJsonExporter, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsFeatureRequest,QgsProcessingFeatureSourceDefinition

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

class LandFund:

    def __init__(self):
        pass
    def prepareInputLayer(self, geojson, distance):
        layer = self.getLayerFromFile(geojson)
        layer.setCrs(QgsCoordinateReferenceSystem("EPSG:3346"))
        if (self.isDistanceValid(distance)):
            layer = self.runProcessingNativeBuffer(layer, distance)
        return layer

    def runProcessingNativeSelectByLocation(self,inputLayer, overlayLayer):
        # processing.algorithmHelp("native:selectbylocation")
        rez = processing.run("native:selectbylocation",
                              {'INPUT': inputLayer,
                               'PREDICATE': [0],
                               'INTERSECT': overlayLayer,
                               'METHOD': 0})
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

    def analysisDIRV_DB10LT(self, layerToAnalyze, pathToDIRV_DB10LT):
        evaluationLayer = self.getLayerFromFile(pathToDIRV_DB10LT)
        self.runProcessingNativeSelectByLocation(evaluationLayer,layerToAnalyze)
        if(evaluationLayer.selectedFeatureCount()==0):
            x = {"rezultatas": "plotai nepersidengia"}
            return x;

        selectedFeaturesLayer = evaluationLayer.materialize(QgsFeatureRequest().setFilterFids(evaluationLayer.selectedFeatureIds()))
        intersectedLayer = self.runProcessingNativeIntersectSkipInvalid(selectedFeaturesLayer, layerToAnalyze)

        intersectedLayer = self.runProcessingQgisExportAddGeometryColumns(intersectedLayer)

        layerToAnalyze = self.runProcessingQgisExportAddGeometryColumns(layerToAnalyze)

        features = intersectedLayer.getFeatures()
        array = self.getAreaAndScoreTotal(features)

        features = layerToAnalyze.getFeatures()
        layerToAnalyzeArea = self.getAreaSum(features)
        return self.constructResult(array[0],array[1],layerToAnalyzeArea)

    def constructResult(self,intersectedLayerArea,weightedSum,layerToAnalyzeArea):

        overlaps = intersectedLayerArea * 100 / (layerToAnalyzeArea)
        notOverlaps = 100 - overlaps

        if intersectedLayerArea != 0:
            overlapingLandScore = weightedSum / intersectedLayerArea
        x = {
            "persidengia %": overlaps,
            "nepersidengia %": notOverlaps,
            "persidengiancios dalies dirvozemio nasumas, balais": overlapingLandScore
        }
        return x

    def analysisAZ_PR10LT(self, layerToAnalyze, pathToAZ_PR10LT):
        abandonedLandLayer = self.getLayerFromFile(pathToAZ_PR10LT)

        self.runProcessingNativeSelectByLocation(abandonedLandLayer,layerToAnalyze)
        if(abandonedLandLayer.selectedFeatureCount()==0):
            x = {"rezultatas": "plotai nepersidengia"}
            return x;
        intersectResultLayer = abandonedLandLayer.materialize(QgsFeatureRequest().setFilterFids(abandonedLandLayer.selectedFeatureIds()))
        intersectedAnalysisLayer = self.runProcessingNativeIntersectSkipInvalid(intersectResultLayer,
                                                                                layerToAnalyze)
        intersectedAnalysisLayer = self.runProcessingQgisExportAddGeometryColumns(intersectedAnalysisLayer)

        layerToAnalyze = self.runProcessingQgisExportAddGeometryColumns(layerToAnalyze)

        features = intersectedAnalysisLayer.getFeatures()
        intersectedArea = self.getAreaSum(features)

        features = layerToAnalyze.getFeatures()
        layerToAnalyzeArea = self.getAreaSum(features)

        return self.calculateOverlaping(intersectedArea,layerToAnalyzeArea)

    def calculateOverlaping(self,targetLayerArea,otherLayerArea):
        overlaps = targetLayerArea * 100 / (otherLayerArea)
        notOverlaps = 100 - overlaps

        x = {
            "persidengia %": overlaps,
            "nepersidengia %": notOverlaps,
        }
        return x

    def getAreaAndScoreTotal(self, features):
        layerArea = 0
        weightedSum = 0
        dropedArea = 0
        for feature in features:
            if feature["balas"] != -1:
                layerArea += feature["area"]
                weightedSum += feature["area"] * feature["balas"]
            else:
                dropedArea += feature["area"]
        return [layerArea, weightedSum, dropedArea]

    def getAreaSum(self, features):
        sum = 0
        for feature in features:
            sum += feature["area"]
        return sum

    def getLayerFromFile(self, path):
        return QgsVectorLayer(path, "myLayer", "ogr")

    def exitCall(self):
        qgs.exitQgis()

    def isDistanceValid(self, distance):
        try:
            float(distance)
            return True
        except ValueError:
            return False

    def isPredicateListValid(self,predicateList):
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