from UCUM.dimension import Dimension

import unittest


class TestDimension(unittest.TestCase):

    def init_test(self):
        baseClass = Dimension()
        self.assertEqual(baseClass, Dimension())
        self.assertRaises(ValueError, Dimension([1,2]))
        self.assertRaises(ValueError, Dimension(-2))

    def setElementAt_test(self):
        pass


    def getElementAt_test(self):
        pass


    def getProperty_test(self):
        pass


    def toString_test(self):
        pass


    def add_test(self):
        pass


    def subtract_test(self):
        pass


    def minus_test(self):
        pass


    def mul_test(self):
        pass


    def equals_test(self):
        pass


    def assignDim_test(self):
        pass


    def assignZero_test(self):
        pass


    def isZero_test(self):
        pass


    def isNull_test(self):
        pass


    def clone_test(self):
        pass

