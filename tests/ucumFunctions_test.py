import pytest
from ucum.ucumFunctions import UcumFunctions

class TestUcumFunctions():


    def test_forName(self):

        instance = UcumFunctions()
        func = instance.forName('cel')
        assert func['cnvFrom'](5) == 278.15

        assert instance.forName('celll') == False

        with pytest.raises(AttributeError) as excinfo:
            instance.forName(111)
        assert "AttributeError" in str(excinfo)

    def test_isDefined(self):

        instance = UcumFunctions()

        assert instance.isDefined('cel') == True

        assert instance.isDefined('celll') == False

        with pytest.raises(AttributeError) as excinfo:
            instance.isDefined(111)
        assert "AttributeError" in str(excinfo)

