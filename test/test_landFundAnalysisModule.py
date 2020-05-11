import unittest
from unittest.mock import MagicMock

from landFundEvaliationAndAnalysis.landFundModule import LandFund


def createFeatures():
    feature1 = {"area": 5, "balas": 3, }
    feature2 = {"area": 5, "balas": 3, }
    feature3 = {"area": 5, "balas": 3, }
    return [feature1, feature2, feature3]


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.isntance = Validation()

    def test_isDistanceValidMoreThanZero(self):
        self.isntance.isInt = MagicMock(return_value=True)
        valid = self.isntance.isDistanceValid(1)
        self.assertEqual(valid, True)


    def test_isIntString(self):
        valid = self.isntance.isInt("string")
        self.assertEqual(valid, False)

    def test_isIntInt(self):
        valid = self.isntance.isInt(0)
        self.assertEqual(valid, True)
    def test_isFloatString(self):
        valid = self.isntance.isFloat("string")
        self.assertEqual(valid, False)

    def test_isFloatInt(self):
        valid = self.isntance.isFloat(0)
        self.assertEqual(valid, True)


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.isntance = ProcessingAlgorithms(MagicMock())

    def test_AreaSumZero(self):
        arr = []
        sum = self.isntance.getAreaSum(arr)
        self.assertEqual(sum, 0)

    def test_AreaSum(self):
        arr = createFeatures()
        sum = self.isntance.getAreaSum(arr)
        self.assertEqual(sum, 15)

    def test_AreaSumAndScore(self):
        arr = createFeatures()
        sum = self.isntance.getAreaAndScoreTotal(arr)
        self.assertEqual(sum[0], 15)
        self.assertEqual(sum[1], 45)

    def test_AZPR10LTOverlapsEqual(self):
        ans = self.isntance.calculateOverlaping(50, 100)
        self.assertEqual(ans["persidengia %"], 50)
        self.assertEqual(ans["nepersidengia %"], 50)

    def test_AZPR10LTOverlapsNone(self):
        ans = self.isntance.calculateOverlaping(0, 20)
        self.assertEqual(ans["persidengia %"], 0)
        self.assertEqual(ans["nepersidengia %"], 100)


if __name__ == '__main__':
    unittest.main()
