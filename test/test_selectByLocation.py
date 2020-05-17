import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

from vectorAnalysis import selectByLocationScript

@patch.object(selectByLocationScript, 'exitCall', MagicMock())
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.instance = selectByLocationScript
        self.instance.exitCall = MagicMock()
        self.f = io.StringIO()

    def test_MainNotEnoughArguments(self):
        args = ["Invalid arguments"]
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR", s)

    @patch.object(selectByLocationScript, 'execute', MagicMock(return_value=None))
    def test_Main(self):
        args = [None, None, None, None, None]
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertEqual("", s)

    @patch.object(selectByLocationScript.LayerManipulation, 'getLayerFromFile', MagicMock())
    @patch.object(selectByLocationScript.ProcessingAlgorithms, 'runProcessingNativeSelectByLocation',MagicMock(side_effect=Exception('Boom!')))
    @patch.object(selectByLocationScript.Validation, 'isNumber', MagicMock(return_value=True))
    @patch.object(selectByLocationScript.Validation, 'isPredicateValid', MagicMock(return_value=True))
    def test_ExecuteError(self):
        with redirect_stdout(self.f):
            self.instance.execute(None, None, None, None)
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR", s)

    @patch.object(selectByLocationScript.ProcessingAlgorithms, 'runProcessingNativeSelectByLocation', MagicMock())
    @patch.object(selectByLocationScript.ProcessingAlgorithms, 'runProcessingNativeBuffer', MagicMock())
    @patch.object(selectByLocationScript.LayerManipulation, 'getGeoJsonFromSelectedFeaturesInLayer', MagicMock())
    @patch.object(selectByLocationScript.Validation, 'isNumber', MagicMock(return_value=False))
    @patch.object(selectByLocationScript.Validation, 'isPredicateValid', MagicMock(return_value=True))
    def test_ExecuteSuccess(self):
        with redirect_stdout(self.f):
            self.instance.execute(None, None, None, None)
        s = self.f.getvalue()
        self.assertIn("RESULT_GEOJSON", s)


if __name__ == '__main__':
    unittest.main()
