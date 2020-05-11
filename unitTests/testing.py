import unittest
from analysisFunctions import bufferScript, intersectScript

from contextlib import redirect_stdout
import io

class TestBuffer(unittest.TestCase):
    def setUp(self):
        self.f=io.StringIO()
    def test_DecentInput(self):
        with redirect_stdout(self.f):
            bufferScript.execute("C:\\Users\\Username\\Desktop\\Extra\\Darbas\\d\\Inter1.geojson", 50)
        s = self.f.getvalue()
        self.assertIn("RESULT_GEOJSON",s)

    def test_negativeDistance(self):
        with redirect_stdout(self.f):
            bufferScript.execute("C:\\Users\\Username\\Desktop\\Extra\\Darbas\\d\\Inter1.geojson", -50)
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR",s)
    def test_TestProcessingError(self):
        with redirect_stdout(self.f):
            bufferScript.execute("C:\\Users\\Username\\Desktop\\Extra\\Darbas\\d\\Inter1a", 50)
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR",s)

class TestIntersect(unittest.TestCase):
    def setUp(self):
        self.f=io.StringIO()
    def test_DecentInput(self):
        with redirect_stdout(self.f):
            intersectScript.execute("C:\\Users\\Username\\Desktop\\Extra\\Darbas\\d\\Inter1.geojson", "C:\\Users\\Username\\Desktop\\Extra\\Darbas\\d\\Inter1.geojson")
        s = self.f.getvalue()
        self.assertIn("RESULT_GEOJSON",s)

    def test_TestProcessingError(self):
        with redirect_stdout(self.f):
            intersectScript.execute("C:\\Users\\Username\\Desktop\\Extra\\Darbas\\d\\Inter1a", "C:\\Users\\Username\\Desktop\\Extra\\Darbas\\d\\Inter1.geojson")
        s = self.f.getvalue()
        self.assertIn("SCRIPT_ERROR",s)

if __name__ == '__main__':
    unittest.main()