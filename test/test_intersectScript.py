import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock
import unittest
from vectorAnalysis import intersectScript
@patch.object(intersectScript, 'exitCall', MagicMock())
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.instance = intersectScript
        self.f = io.StringIO()

    def test_MainWrongArguments(self):
        args = ['WrongArguments'];
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR", s)

    @patch.object(intersectScript, 'execute', MagicMock(return_value=None))
    def test_MainPass(self):
        args = [None, None,None]
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertEqual("", s)

    @patch.object(intersectScript.LayerManipulation, 'getLayerFromFile', MagicMock(side_effect=Exception('Boom!')))
    @patch.object(intersectScript.LayerManipulation, 'getGeoJsonFromFeaturesFromLayer')
    def test_Error(self,getGeoJSON):
        with redirect_stdout(self.f):
            self.instance.execute(None, None)
        s = self.f.getvalue()
        getGeoJSON.assert_not_called()
        self.assertIn("SCRIPT_ERROR", s)

    @patch.object(intersectScript.LayerManipulation, 'getLayerFromFile', MagicMock())
    @patch.object(intersectScript.ProcessingAlgorithms, 'runProcessingNativeSelectByLocation', MagicMock())
    @patch.object(intersectScript.LayerManipulation, 'layerFromSelectedFeaturesLayer', MagicMock())
    @patch.object(intersectScript.ProcessingAlgorithms, 'runProcessingNativeIntersect')
    @patch.object(intersectScript.Validation, 'isSelectedFeaturesEmpty', MagicMock(return_value=True))
    @patch.object(intersectScript.LayerManipulation, 'getGeoJsonFromFeaturesFromLayer', MagicMock())
    def test_NotOverlapingLayers(self,intersect):
        with redirect_stdout(self.f):
            self.instance.execute(None, None)
        intersect.assert_not_called()
        s = self.f.getvalue()
        self.assertIn("RESULT_GEOJSON", s)


    @patch.object(intersectScript.LayerManipulation, 'getLayerFromFile', MagicMock())
    @patch.object(intersectScript.ProcessingAlgorithms, 'runProcessingNativeSelectByLocation', MagicMock())
    @patch.object(intersectScript.LayerManipulation, 'layerFromSelectedFeaturesLayer', MagicMock())
    @patch.object(intersectScript.LayerManipulation, 'getGeoJsonFromFeaturesFromLayer', MagicMock())
    @patch.object(intersectScript.ProcessingAlgorithms, 'runProcessingNativeIntersect')
    @patch.object(intersectScript.Validation, 'isSelectedFeaturesEmpty', MagicMock(return_value=False))
    def test_OverlapingLayers(self, intersect):
        with redirect_stdout(self.f):
            self.instance.execute(None, None)
        intersect.assert_called_once()
        s = self.f.getvalue()
        self.assertIn("RESULT_GEOJSON", s)

if __name__ == '__main__':
    unittest.main()
