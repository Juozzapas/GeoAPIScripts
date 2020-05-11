import unittest
from random import random, randint, randrange
from unittest.mock import MagicMock

from landFundEvaluationAndAnalysis.landFundModule import BaseResult, ResultDIRV_DB10LT, ResultAZ_PR10LT, \
    LandFundAnalysis


def createFeatures():
    feature1 = {"area": 5, "balas": 3, "perimeter": 2}
    feature2 = {"area": 5, "balas": 3, "perimeter": 2}
    feature3 = {"area": 5, "balas": 3, "perimeter": 2}
    return [feature1, feature2, feature3]


class TestBaseResult(unittest.TestCase):
    def setUp(self):
        self.isntance = BaseResult()

    def test_aggregateField(self):
        arr = createFeatures()
        sum = self.isntance.aggregateField(arr, "area")
        self.assertEqual(sum, 15)

    def test_aggregateFieldZero(self):
        arr = []
        sum = self.isntance.aggregateField(arr, "area")
        self.assertEqual(sum, 0)

    def test_calculateOverlapping(self):
        self.isntance.calculateOverlapping(40, 100)
        self.assertEqual(self.isntance.overlapping, 40)

    def test_calculateInputArea(self):
        arr = createFeatures()
        self.isntance.calculateInputArea(arr)
        self.assertEqual(self.isntance.inputArea, 15)

    def test_calculateGeometryInfoCalled(self):
        arr = createFeatures()
        self.isntance.calculateGeometryInfo = MagicMock()
        self.isntance.calculateGeometryInfo(arr)
        self.isntance.calculateGeometryInfo.assert_called_once()

    def test_getResultCalled(self):
        arr = createFeatures()
        self.isntance.getResult = MagicMock()
        self.isntance.getResult()
        self.isntance.getResult.assert_called_once()


class TestResultDIRV_DB10LT(unittest.TestCase):
    def setUp(self):
        self.isntance = ResultDIRV_DB10LT()

    def test_calculateGeometryInfo(self):
        arr = createFeatures()
        self.isntance.calculateGeometryInfo(arr)
        self.assertEqual(self.isntance.area, 15)
        self.assertEqual(self.isntance.perimeter, 6)
        self.assertEqual(self.isntance.weightedSum, 45)

    def test_calculateGeometryInfoEmpty(self):
        arr = []
        self.isntance.calculateGeometryInfo(arr)
        self.assertEqual(self.isntance.area, 0)
        self.assertEqual(self.isntance.perimeter, 0)
        self.assertEqual(self.isntance.weightedSum, 0)

    def test_getResult(self):
        self.isntance.calculateOverlapping = MagicMock()
        self.isntance.calculatedWeightedAverage = MagicMock()
        result = self.isntance.getResult(0, 0)
        for value in result:
            self.assertEqual(result[value], 0)


class TestResultAZ_PR10LT(unittest.TestCase):
    def setUp(self):
        self.isntance = ResultAZ_PR10LT()

    def test_calculateGeometryInfo(self):
        arr = createFeatures()
        self.isntance.calculateGeometryInfo(arr)
        self.assertEqual(self.isntance.area, 15)
        self.assertEqual(self.isntance.perimeter, 6)

    def test_calculateGeometryInfoEmpty(self):
        arr = []
        self.isntance.calculateGeometryInfo(arr)
        self.assertEqual(self.isntance.area, 0)
        self.assertEqual(self.isntance.perimeter, 0)

    def test_getResult(self):
        self.isntance.calculateOverlapping = MagicMock()
        self.isntance.calculatedWeightedAverage = MagicMock()
        result = self.isntance.getResult(0, 0)
        for value in result:
            self.assertEqual(result[value], 0)


class TestLandFundModule(unittest.TestCase):
    def setUp(self):
        self.isntance = LandFundAnalysis()

    def test_isDistanceValidFloatOrIntTrue(self):
        valid = self.isntance.isDistanceValid(random())
        self.assertEqual(valid, True)

    def test_isDistanceValidFloatOrIntFalse(self):
        valid = self.isntance.isDistanceValid("string")
        self.assertEqual(valid, False)

    def test_TestDecentPredicate(self):
        predicateList = []
        for x in range(10):
            predicateList.append(str(randint(0, 1)))
        valid = self.isntance.isPredicateListValid(predicateList)
        self.assertEqual(valid, True)

    def test_InvalidPredicate(self):
        predicateList = []
        r = randrange(-1000, 0) + randrange(1 + 1, 1000)
        for x in range(6):
            predicateList.append(str(randrange(-10, 0) + randrange(1 + 1, 20)))
        print(predicateList)
        valid = self.isntance.isPredicateListValid(predicateList)
        self.assertEqual(valid, False)


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.isntance = LandFundAnalysis()
        self.isntance.alg=MagicMock()

    def test_getGeoJsonFromLayerNoAttributesIncludedCalled(self):
        self.isntance.getGeoJsonFromLayerNoAttributesIncluded = MagicMock()
        self.isntance.getGeoJsonFromLayerNoAttributesIncluded()
        self.isntance.getGeoJsonFromLayerNoAttributesIncluded.assert_called_once()

    def test_getGeoJsonFromLayer(self):
        self.isntance.getGeoJsonFromLayer = MagicMock()
        self.isntance.getGeoJsonFromLayer()
        self.isntance.getGeoJsonFromLayer.assert_called_once()

    def test_getLayerFromFile(self):
        self.isntance.getLayerFromFile = MagicMock()
        self.isntance.getLayerFromFile()
        self.isntance.getLayerFromFile.assert_called_once()

    def test_deleteAllFields(self):
        self.isntance.deleteAllFields = MagicMock()
        self.isntance.deleteAllFields()
        self.isntance.deleteAllFields.assert_called_once()

    def test_setLayerCrs(self):
        self.isntance.setLayerCrs = MagicMock()
        self.isntance.setLayerCrs()
        self.isntance.setLayerCrs.assert_called_once()

    def test_addFieldsToLayer(self):
        self.isntance.addFieldsToLayer = MagicMock()
        self.isntance.addFieldsToLayer()
        self.isntance.addFieldsToLayer.assert_called_once()

    def test_calculateVerticesAndCentroid(self):
        mock =MagicMock()
        miniMock1 =MagicMock()
        miniMock2 = MagicMock()
        mock.getFeatures.return_value = [miniMock1,miniMock2]
        self.isntance.calculateVerticesAndCentroid(mock)
        mock.startEditing.assert_called_once()
        mock.getFeatures.assert_called_once()
        miniMock1.geometry.assert_called()

    def test_processInputLayer(self):
        self.isntance.addFieldsToLayer = MagicMock()
        self.isntance.calculateVerticesAndCentroid = MagicMock()
        self.isntance.getGeoJsonFromLayer = MagicMock()
        self.isntance.processInputLayer(None)
        self.isntance.addFieldsToLayer.assert_called_once()
        self.isntance.calculateVerticesAndCentroid.assert_called_once()
        self.isntance.alg.runProcessingQgisExportAddGeometryColumns.assert_called_once()
        self.isntance.getGeoJsonFromLayer.assert_called_once()



    def test_prepareInputLayer(self):
        self.isntance.getLayerFromFile = MagicMock(return_value = 'layer')
        self.isntance.deleteAllFields = MagicMock()
        self.isntance.setLayerCrs = MagicMock()
        self.isntance.isDistanceValid = MagicMock(return_value = True)
        self.isntance.prepareInputLayer(None,None)
        self.isntance.getLayerFromFile.assert_called_once()
        self.isntance.deleteAllFields.assert_called_once()
        self.isntance.setLayerCrs.assert_called_once_with('layer',"EPSG:3346")
        self.isntance.isDistanceValid.assert_called_once()
        self.isntance.alg.runProcessingNativeBuffer.assert_called_once()

if __name__ == '__main__':
    unittest.main()
