
from unittest.mock import patch, MagicMock
import unittest
from vectorAnalysis.vectorAnalysisModule import Validation
from random import seed
from random import random
from random import randint
class TestValidator(unittest.TestCase):

    def setUp(self):
        seed(1)

    def test_isStringNumber(self):
        valid = isNumber("string")
        self.assertEqual(valid, False)

    def test_isNumberinStringIsNumber(self):
        valid = isNumber("50")
        self.assertEqual(valid, True)

    def test_isRandomNumberIsNumber(self):
        valid = isNumber(random())
        self.assertEqual(valid, True)

    def test_isStringInt(self):
        valid = isInt("string")
        self.assertEqual(valid, False)

    def test_isNumberinStringIsInt(self):
        valid = isInt("50")
        self.assertEqual(valid, True)

    def test_isRandomNumberIsInt(self):
        valid = isInt(random())
        self.assertEqual(valid, True)

    def test_ifCrsValid(self):
        valid = checkIfCrsValid(3346)
        self.assertEqual(valid, False)

    def test_ifCrsValid2(self):
        valid = checkIfCrsValid("EPSG:3346")
        self.assertEqual(valid, True)


if __name__ == '__main__':
    unittest.main()
