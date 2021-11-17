from ucum.dimension import Dimension

import pytest


class TestDimension():

    def test_init(self):
        with pytest.raises(ValueError) as excinfo:
            Dimension([1,2])
        assert "ExceptionInfo" in str(excinfo)

        assert Dimension([1,2,3,4,5,6,7]).dimVec_ == [1,2,3,4,5,6,7]

        with pytest.raises(ValueError) as excinfo:
            Dimension(-2)
        assert "ExceptionInfo" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            Dimension(8)
        assert "ExceptionInfo" in str(excinfo)

    def test_setElementAt(self):
        testInstance = Dimension()
        with pytest.raises(ValueError) as excinfo:
            testInstance.setElementAt("9", 5)
        assert  "ValueError" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            testInstance.setElementAt("9a", 5)
        assert  "ValueError" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            testInstance.setElementAt(-5, 5)
        assert "ValueError" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            testInstance.setElementAt(8, 5)
        assert "ValueError" in str(excinfo)

        with pytest.raises(TypeError) as excinfo:
            testInstance.setElementAt(0, "6")
        assert "TypeError" in str(excinfo)

        testInstance.setElementAt(0)
        assert testInstance.dimVec_[0] == 1

        testInstance.setElementAt(0, 5)
        assert testInstance.dimVec_[0] == 5

    def test_getElementAt(self):
        testInstance = Dimension([1,2,3,4,5,6,7])

        with pytest.raises(ValueError) as excinfo:
            testInstance.getElementAt("9")
        assert "ValueError" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            testInstance.getElementAt("9a")
        assert "ValueError" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            testInstance.getElementAt(-5)
        assert "ValueError" in str(excinfo)
        with pytest.raises(ValueError) as excinfo:
            testInstance.getElementAt(8)
        assert "ValueError" in str(excinfo)

        assert testInstance.getElementAt(5) == 6



    def test_getProperty(self): #todo write test later need to relook at the functions use
        pass


    def test_toString(self):
        testInstance = Dimension([1,2,3,4,5,6,7])

        assert testInstance.toString() == "[1,2,3,4,5,6,7]"

    def test_add(self):
        testInstance = Dimension([1,2,3,4,5,6,7])
        with pytest.raises(TypeError) as excinfo:
            testInstance.add("9")
        assert "TypeError" in str(excinfo)
        with pytest.raises(TypeError) as excinfo:
            testInstance.add(10)
        assert "TypeError" in str(excinfo)
        with pytest.raises(TypeError) as excinfo:
            testInstance.add([123,679,98])
        assert "TypeError" in str(excinfo)

        testInstance2 = Dimension([1,2,3,4,5,6,7])
        testInstance.add(testInstance2)
        assert testInstance.dimVec_ ==  [2,4,6,8,10,12,14]


    def test_subtract(self):
        testInstance = Dimension([1, 2, 3, 4, 5, 6, 7])
        with pytest.raises(TypeError) as excinfo:
            testInstance.subtract("9")
        assert "TypeError" in str(excinfo)
        with pytest.raises(TypeError) as excinfo:
            testInstance.subtract(10)
        assert "TypeError" in str(excinfo)
        with pytest.raises(TypeError) as excinfo:
            testInstance.subtract([123, 679, 98])
        assert "TypeError" in str(excinfo)

        testInstance2 = Dimension([1, 2, 3, 4, 5, 6, 7])
        testInstance.subtract(testInstance2)
        assert testInstance.dimVec_ == [0, 0, 0, 0, 0, 0, 0]


    def test_invert(self):
        testInstance = Dimension([1, 2, 3, 4, 5, 6, 7])
        testInstance.invert()
        assert testInstance.dimVec_ == [-1, -2, -3, -4, -5, -6, -7]


    def test_mul(self):
        testInstance = Dimension([1, 2, 3, 4, 5, 6, 7])
        with pytest.raises(TypeError) as excinfo:
            testInstance.mul("9")
        assert "TypeError" in str(excinfo)
        with pytest.raises(TypeError) as excinfo:
            testInstance.mul([123, 679, 98])
        assert "TypeError" in str(excinfo)
        testInstance.mul(2)
        assert testInstance.dimVec_ == [2, 4, 6, 8, 10, 12, 14]



    def test_equals(self):
        testInstance = Dimension([1, 2, 3, 4, 5, 6, 7])
        testInstance2 = Dimension([1, 2, 3, 4, 5, 6, 7])
        testInstance3 = Dimension([2, 4, 5, 6, 7, 5, 3])
        with pytest.raises(TypeError) as excinfo:
            testInstance.equals("9")
        assert "TypeError" in str(excinfo)
        with pytest.raises(TypeError) as excinfo:
            testInstance.equals(10)
        assert "TypeError" in str(excinfo)
        with pytest.raises(TypeError) as excinfo:
            testInstance.equals([123, 679, 98])
        assert "TypeError" in str(excinfo)

        assert testInstance.equals(testInstance2) == True
        assert testInstance.equals(testInstance3) == False


    def test_assignDim(self):
        testInstance = Dimension([1, 2, 3, 4, 5, 6, 7])
        testInstance2 = Dimension([2, 4, 5, 6, 7, 5, 3])
        with pytest.raises(TypeError) as excinfo:
            testInstance.assignDim("9")
        assert "TypeError" in str(excinfo)
        with pytest.raises(TypeError) as excinfo:
            testInstance.assignDim(10)
        assert "TypeError" in str(excinfo)
        with pytest.raises(TypeError) as excinfo:
            testInstance.assignDim([123, 679, 98])
        assert "TypeError" in str(excinfo)

        testInstance.assignDim(testInstance2)
        assert testInstance.dimVec_ == [2, 4, 5, 6, 7, 5, 3]


    def test_assignZero(self):
        testInstance = Dimension([1, 2, 3, 4, 5, 6, 7])

        testInstance.assignZero()
        assert testInstance.dimVec_ != [0, 0, 0, 0, 0, 0, 0]

        testInstance.dimVec_ = None
        testInstance.assignZero()
        assert  testInstance.dimVec_ == [0, 0, 0, 0, 0, 0, 0]


    def test_isZero(self):
        testInstance = Dimension([1, 2, 3, 4, 5, 6, 7])
        testInstance2 = Dimension([0, 0, 0, 0, 0, 0, 0])

        assert testInstance.isZero() == False
        assert testInstance2.isZero() == True


    def test_isNull(self):
        testInstance = Dimension([1, 2, 3, 4, 5, 6, 7])
        assert testInstance.isNull() == False

        testInstance.dimVec_ = None
        assert testInstance.isNull() == True

    def test_clone(self):
        testInstance = Dimension([1, 2, 3, 4, 5, 6, 7])
        cloneInstance = testInstance.clone()
        assert cloneInstance.dimVec_ == testInstance.dimVec_
