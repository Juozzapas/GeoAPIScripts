import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

from landFundEvaliationAndAnalysis import landFundEvaluationAndAnalysisScript


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
        self.assertIn("SCRIPT_ERROR", s)


    def test_Main(self):
        args= [None,None,"array",None]
        self.instance.execute= MagicMock(return_value=None)
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertEqual("", s)


    @patch('landFundEvaliationAndAnalysis.analysisScript.ProcessingAlgorithms')
    @patch('landFundEvaliationAndAnalysis.analysisScript.json.dumps', MagicMock(side_effect=dummy_function))
    def test_Execute(self, MockClass1):
        with redirect_stdout(self.f):
            self.instance.execute(None,"0,1",None)
        s = self.f.getvalue()
        self.assertIn("DIRV_DB10LT", s)

    @patch('landFundEvaliationAndAnalysis.analysisScript.ProcessingAlgorithms')
    def test_ExecuteEmpty(self, MockClass1):
        with redirect_stdout(self.f):
            self.instance.execute(None, "", None)
        s = self.f.getvalue()
        self.assertNotIn("DIRV_DB10LT", s)
        self.assertNotIn("AZ_PR10LT", s)

    @patch('landFundEvaliationAndAnalysis.analysisScript.ProcessingAlgorithms')
    @patch('landFundEvaliationAndAnalysis.analysisScript.json.dumps', MagicMock(side_effect=dummy_function))
    def test_ExecutePredicateDIRV_DV10LT(self, MockClass1):
        with redirect_stdout(self.f):
            self.instance.execute(None, "0", None)
        s = self.f.getvalue()
        self.assertIn("DIRV_DB10LT", s)

    @patch('landFundEvaliationAndAnalysis.analysisScript.ProcessingAlgorithms')
    @patch('landFundEvaliationAndAnalysis.analysisScript.json.dumps', MagicMock(side_effect=dummy_function))
    def test_ExecutePredicateAZ_PR10LT(self, MockClass1):
        with redirect_stdout(self.f):
            self.instance.execute(None,"1", None )
        s = self.f.getvalue()
        self.assertIn("AZ_PR10LT", s)

    @patch('landFundEvaliationAndAnalysis.analysisScript.ProcessingAlgorithms')
    def test_ExecuteUnableToCalculateDIRV_DV10LT(self, MockClass1):
        MockClass1.return_value.analysisDIRV_DB10LT.side_effect = Exception('foo')
        with redirect_stdout(self.f):
            self.instance.execute(None, "0", None)
        s = self.f.getvalue()
        self.assertIn("unableToCalculate", s)

    @patch('landFundEvaliationAndAnalysis.analysisScript.ProcessingAlgorithms')
    def test_ExecuteUnableToCalculateAZ_PR10LT(self, MockClass1):
        MockClass1.return_value.analysisAZ_PR10LT.side_effect = KeyError('foo')
        with redirect_stdout(self.f):
            self.instance.execute(None, "1" ,None)
        s = self.f.getvalue()
        self.assertIn("unableToCalculate", s)


if __name__ == '__main__':
    unittest.main()
