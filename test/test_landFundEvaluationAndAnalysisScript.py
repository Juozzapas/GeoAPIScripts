import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

from landFundEvaluationAndAnalysis import landFundEvaluationAndAnalysisScript


def createFeatures():
    feature1 = {"area": 5, "balas": 3, }
    feature2 = {"area": 5, "balas": 3, }
    feature3 = {"area": 5, "balas": 3, }
    return [feature1, feature2, feature3]


def dummy_function(value):
    "Will return same value as value passed to the function"
    return value


class TestAnalysis(unittest.TestCase):

    def setUp(self):
        self.instance = landFundEvaluationAndAnalysisScript
        self.f = io.StringIO()
        self.instance.exitCall = MagicMock()

    def test_MainWrongArguments(self):
        args = ['Wrong arguments']
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertIn(
            "SCRIPT_ERROR there should be 2 or 3 arguments, inputFilePath, distance, predicate (optional). Now there are",
            s)

    def test_Main(self):
        args = [None, None, "array", None]
        self.instance.execute = MagicMock(return_value=None)
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertEqual("", s)

    @patch.object(landFundEvaluationAndAnalysisScript.LandFundAnalysis, 'isPredicateListValid', MagicMock(return_value=False))
    def test_ExecuteInvalidPredicateList(self):
        with redirect_stdout(self.f):
            self.instance.execute(None, "", None)
        s = self.f.getvalue()
        self.assertNotIn("DIRV_DB10LT", s)
        self.assertNotIn("AZ_PR10LT", s)
        self.assertIn("SCRIPT_ERROR predicate list does not contain values representing existing operations", s)

    @patch.object(landFundEvaluationAndAnalysisScript.LandFundAnalysis, 'isPredicateListValid', MagicMock(return_value=True))
    @patch.object(landFundEvaluationAndAnalysisScript.LandFundAnalysis, 'prepareInputLayer', MagicMock())
    @patch.object(landFundEvaluationAndAnalysisScript.LandFundAnalysis, 'processInputLayer', MagicMock())
    @patch('landFundEvaluationAndAnalysis.landFundEvaluationAndAnalysisScript.json.dumps',
           MagicMock(side_effect=dummy_function))
    def test_Execute(self):
        with redirect_stdout(self.f):
            self.instance.execute(None, "0", None)
        s = self.f.getvalue()
        self.assertIn("RESULT_GEOJSON", s)

    @patch('landFundEvaluationAndAnalysis.landFundEvaluationAndAnalysisScript.LandFundAnalysis')
    @patch('landFundEvaluationAndAnalysis.landFundEvaluationAndAnalysisScript.json.dumps',
           MagicMock(side_effect=dummy_function))
    def test_ExecuteDIRV_DB10LaandAZ_PR10LT(self, MockClass):
        with redirect_stdout(self.f):
            self.instance.execute(None, "0,1", None)
        s = self.f.getvalue()
        self.assertIn("DIRV_DB10LT", s)
        self.assertIn("AZ_PR10LT", s)

    @patch('landFundEvaluationAndAnalysis.landFundEvaluationAndAnalysisScript.LandFundAnalysis')
    @patch('landFundEvaluationAndAnalysis.landFundEvaluationAndAnalysisScript.json.dumps',
           MagicMock(side_effect=dummy_function))
    def test_ExecuteUnableToCalculateDIRV_DV10LT(self, MockClass):
        MockClass.return_value.startAnalyzis.side_effect = Exception('foo')
        with redirect_stdout(self.f):
            self.instance.execute(None, "0", None)
        s = self.f.getvalue()
        self.assertIn("DIRV_DB10LT", s)
        self.assertIn("unableToCalculate", s)

    @patch('landFundEvaluationAndAnalysis.landFundEvaluationAndAnalysisScript.LandFundAnalysis')
    @patch.object(landFundEvaluationAndAnalysisScript.LandFundAnalysis, 'processInputLayer', MagicMock())
    @patch('landFundEvaluationAndAnalysis.landFundEvaluationAndAnalysisScript.json.dumps',
           MagicMock(side_effect=dummy_function))
    def test_ExecuteUnableToCalculateAZ_PR10LT(self, MockClass):
        MockClass.return_value.startAnalyzis.side_effect = KeyError('foo')
        with redirect_stdout(self.f):
            self.instance.execute(None, "1", None)
        s = self.f.getvalue()
        self.assertIn("AZ_PR10LT", s)
        self.assertIn("unableToCalculate", s)

    @patch('landFundEvaluationAndAnalysis.landFundEvaluationAndAnalysisScript.LandFundAnalysis')
    @patch.object(landFundEvaluationAndAnalysisScript.LandFundAnalysis, 'processInputLayer', MagicMock())
    @patch('landFundEvaluationAndAnalysis.landFundEvaluationAndAnalysisScript.json.dumps',
           MagicMock(side_effect=dummy_function))
    @patch.object(landFundEvaluationAndAnalysisScript.LandFundAnalysis, 'isPredicateListValid', MagicMock(return_value=True))
    def test_BaseAnalysisResult(self, MockClass):
        with redirect_stdout(self.f):
            self.instance.execute(None, "", None)
        s = self.f.getvalue()
        self.assertNotIn("AZ_PR10LT", s)
        self.assertNotIn("DIRV_DB10LT", s)
        self.assertIn("baseAnalysis", s)

if __name__ == '__main__':
    unittest.main()
