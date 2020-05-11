
from unittest.mock import patch, MagicMock
import unittest
from vectorAnalysis.vectorAnalysisModule import Validation
from random import random
from random import randint
from random import randrange
from vectorAnalysis import vectorAnalysisModule

Validation = vectorAnalysisModule.Validation
class TestValidaton(unittest.TestCase):

    def setUp(self):
        pass

    def test_isStringNumber(self):
        valid = Validation.isNumber("string")
        self.assertEqual(valid, False)

    def test_isNumberinStringIsNumber(self):
        valid = Validation.isNumber("50")
        self.assertEqual(valid, True)

    def test_isRandomNumberIsNumber(self):
        valid = Validation.isNumber(random())
        self.assertEqual(valid, True)

    def test_isStringInt(self):
        valid = Validation.isInt("string")
        self.assertEqual(valid, False)

    def test_isNumberinStringIsInt(self):
        valid = Validation.isInt("50")
        self.assertEqual(valid, True)

    def test_isRandomNumberIsInt(self):
        valid = Validation.isInt(random())
        self.assertEqual(valid, True)
    # ne unit testas
    def test_ifCrsValid2(self):

        valid = Validation.checkIfCrsValid("EPSG:3346")
        self.assertEqual(valid, True)

    def test_TestDecentPredicate(self):
        predicateList = []
        s = ","
        for x in range(6):
            predicateList.append(str(randint(0,7)))
        s = s.join(predicateList)
        valid = Validation.isPredicateValid(s)
        self.assertEqual(valid, True)

    def test_InvalidPredicate(self):
        predicateList = []
        s = ","
        r = randrange(-1000, 0) + randrange(7 + 1, 1000)
        for x in range(6):
            predicateList.append(str(r))
        s = s.join(predicateList)
        valid = Validation.isPredicateValid(s)
        self.assertEqual(valid, False)

    def test_DecentOperator(self):
        valid = Validation.isOperatorValid(randint(0,10))
        self.assertEqual(valid, True)

    def test_InvalidOperator(self):
        r = randrange(-1000,0) + randrange(10+1, 1000)
        valid = Validation.isOperatorValid(r)
        self.assertEqual(valid, False)


if __name__ == '__main__':
    unittest.main()
