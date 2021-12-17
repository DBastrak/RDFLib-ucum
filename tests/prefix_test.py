from ucum.prefix import prefix
import pytest

class TestPrefix():


    def test_init(self):
        dictionary1 = {'code_': "001", 'ciCode_': "001", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
        dictionary2 = {'code_': "001", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': "a", 'exp_': 1}


        with pytest.raises(KeyError) as excinfo:
            instance1 = prefix(dictionary1)
        assert "KeyError" in str(excinfo)

        with pytest.raises(ValueError) as excinfo:
            instance2 = prefix(dictionary2)
        assert "ValueError" in str(excinfo)


    def test_getValue(self):
        dictionary = {'code_': "001", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
        instance = prefix(dictionary)
        assert instance.getValue() == 1

    def test_getCode(self):
        dictionary = {'code_': "001", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
        instance = prefix(dictionary)
        assert instance.getCode() == "001"

    def test_getCiCode(self):
        dictionary = {'code_': "001", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
        instance = prefix(dictionary)
        assert instance.getCiCode() == "001"

    def test_getName(self):
        dictionary = {'code_': "001", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
        instance = prefix(dictionary)
        assert instance.getName() == "Meters"

    def test_getPrintSymbol(self):
        dictionary = {'code_': "001", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
        instance = prefix(dictionary)
        assert instance.getPrintSymbol() == "M"

    def test_getExp(self):
        dictionary = {'code_': "001", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
        instance = prefix(dictionary)
        assert instance.getExp() == 1

    def test_equals(self):
        dictionary = {'code_': "001", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
        instance = prefix(dictionary)
        instance2 = prefix(dictionary)
        dictionary2 = {'code_': "111", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
        instance3 = prefix(dictionary2)
        assert instance.equals(instance2) == True
        assert instance.equals(instance3) == False
