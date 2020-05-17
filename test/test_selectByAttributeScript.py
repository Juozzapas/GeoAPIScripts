import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

from vectorAnalysis import selectByAttributeScript


@patch.object(selectByAttributeScript, 'exitCall', MagicMock())
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.instance = selectByAttributeScript
        self.instance.exitCall = MagicMock()
        self.f = io.StringIO()

    def test_MainNotEnoughArguments(self):
        args = ["Invalid arguments"]
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR", s)

    @patch.object(selectByAttributeScript, 'execute', MagicMock(return_value=None))
    def test_Main(self):
        args = [None, None,None, None,None]
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertEqual("", s)


    @patch.object(selectByAttributeScript.LayerManipulation, 'getLayerFromFile', MagicMock())
    @patch.object(selectByAttributeScript.ProcessingAlgorithms, 'runProcessingQgisSelectByAttribute', MagicMock(side_effect=Exception('Boom!')))
    @patch.object(selectByAttributeScript.LayerManipulation, 'getGeoJsonFromSelectedFeaturesInLayer')
    @patch.object(selectByAttributeScript.Validation, 'isOperatorValid', MagicMock(return_value=True))
    @patch.object(selectByAttributeScript.Validation, 'attributeExists', MagicMock(return_value=True))
    def test_ExecuteError(self,getGeoJSON):
        with redirect_stdout(self.f):
            self.instance.execute(None, None,None, None)
        s = self.f.getvalue()
        getGeoJSON.assert_not_called()
        self.assertIn("SCRIPT_ERROR", s)

    @patch.object(selectByAttributeScript.LayerManipulation, 'getLayerFromFile', MagicMock())
    @patch.object(selectByAttributeScript.ProcessingAlgorithms, 'runProcessingQgisSelectByAttribute', MagicMock())
    @patch.object(selectByAttributeScript.LayerManipulation, 'getGeoJsonFromSelectedFeaturesInLayer', MagicMock())
    @patch.object(selectByAttributeScript.Validation, 'isOperatorValid', MagicMock(return_value=True))
    @patch.object(selectByAttributeScript.Validation, 'attributeExists', MagicMock(return_value=True))
    def test_ExecuteSuccess(self):
        with redirect_stdout(self.f):
            self.instance.execute(None, None,None, None)
        s = self.f.getvalue()
        self.assertIn("RESULT_GEOJSON", s)

if __name__ == '__main__':
    unittest.main()
