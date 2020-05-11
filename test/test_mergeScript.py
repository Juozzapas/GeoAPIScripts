import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock,mock_open
import unittest
from vectorAnalysis import mergeScript
@patch.object(mergeScript, 'exitCall', MagicMock())
class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.instance = mergeScript
        self.f = io.StringIO()

    def test_MainWrongArguments(self):
        args = ['WrongArguments']
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR", s)

    @patch.object(mergeScript, 'execute', MagicMock(return_value=None))
    def test_MainPass(self):
        args = [None, None,None]
        with redirect_stdout(self.f):
            self.instance.main(args)
        s = self.f.getvalue()
        self.assertEqual("", s)

    @patch.object(mergeScript.Validation, 'checkIfCrsValid', MagicMock(return_value=False))
    @patch.object(mergeScript.Validation, 'isInt', MagicMock(return_value=False))
    def test_InvalidCrsError(self):
        with redirect_stdout(self.f):
            self.instance.execute(None, "InvalidCrs")
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR", s)


    @patch.object(mergeScript.Validation, 'isInt', MagicMock(return_value=False))
    @patch.object(mergeScript.Validation, 'checkIfCrsValid', MagicMock(return_value=True))
    @patch.object(mergeScript.ProcessingAlgorithms, 'runProcessingQgisDeleteColumn')
    def test_ExecuteError(self, deleteColumn):
        with patch("vectorAnalysis.mergeScript.open", mock_open(read_data="data")) as mock_file:
            mock_file=MagicMock(side_effect=Exception('Boom!'))
            with redirect_stdout(self.f):
                self.instance.execute("path/to/open", MagicMock())
            mock_file.assert_not_called()
        deleteColumn.assert_not_called()
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR", s)

    @patch.object(mergeScript.Validation, 'checkIfCrsValid', MagicMock(return_value=True))
    @patch.object(mergeScript.Validation, 'isInt', MagicMock(return_value=False))
    @patch.object(mergeScript.json, 'loads', MagicMock())
    @patch.object(mergeScript.ProcessingAlgorithms, 'runProcessingMergeVectorLayers', MagicMock())
    @patch.object(mergeScript.ProcessingAlgorithms, 'runProcessingQgisDeleteColumn', MagicMock())
    @patch.object(mergeScript.LayerManipulation, 'getQgsVectorLayerArray', MagicMock())
    @patch.object(mergeScript.LayerManipulation, 'getGeoJsonFromFeaturesOfOutput', MagicMock())
    def test_ExecuteSuccess(self):
        with patch("vectorAnalysis.mergeScript.open", mock_open(read_data="data")) as mock_file:
            with redirect_stdout(self.f):
                self.instance.execute("path/to/open", MagicMock())
            mock_file.assert_called_once_with("path/to/open")
        s = self.f.getvalue()
        self.assertIn("RESULT_GEOJSON", s)

if __name__ == '__main__':
    unittest.main()
