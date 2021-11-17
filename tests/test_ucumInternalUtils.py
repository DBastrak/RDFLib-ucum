import ucum.ucumInternalUtils as uI
import pytest

class TestUtils:

    def test_isNumericString(self):
        assert uI.isNumericString("10") == True
        with pytest.raises(TypeError) as excinfo:
            uI.isNumericString()
        assert "NoneType" in str(excinfo.value)
        with pytest.raises(ValueError) as excinfo:
            uI.isNumericString("a10")
        assert "could not convert string to float" in str(excinfo.value)

    def test_isIntegerUnit(self):
        assert uI.isIntegerUnit("10") == "10"
        assert uI.isIntegerUnit() == None
        assert uI.isIntegerUnit("a10") == None

    def test_getSynonyms(self):
        pass
