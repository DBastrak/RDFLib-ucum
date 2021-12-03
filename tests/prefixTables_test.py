import pytest
from ucum.prefix import prefix
from ucum.prefixTables import PrefixTablesFactory

prefix1 = {'code_': "001", 'ciCode_': "001", 'name_': "Meters", 'printSymbol_': "M", 'value_': 1, 'exp_': 1}
prefix2 = {'code_': "002", 'ciCode_': "002", 'name_': "Centimeters", 'printSymbol_': "CM", 'value_': 1, 'exp_': 1/100}
prefix3 = {'code_': "003", 'ciCode_': "003", 'name_': "Kilometers", 'printSymbol_': "KM", 'value_': 1, 'exp_': 10}
prefixObj1 = prefix(prefix1)
prefixObj2 = prefix(prefix2)
prefixObj3 = prefix(prefix3)

class TestPrefixTable():

    def test_prefixCount(self):
        obj = PrefixTablesFactory()
        assert obj.prefixCount() == 0
        obj.add(prefixObj1)
        assert obj.prefixCount() == 1

    def test_allPrefixesByValue(self):
        obj = PrefixTablesFactory()
        obj.add(prefixObj1)
        assert obj.allPrefixesByValue() == "001,Meters,,1\r\n"


    def test_allPrefixesByCode(self):
        obj = PrefixTablesFactory()
        obj.add(prefixObj1)
        assert obj.allPrefixesByValue() == "001,Meters,,1\r\n"

    def test_add(self):
        pass

    def test_isDefined(self):
        obj = PrefixTablesFactory()
        obj.add(prefixObj1)
        assert obj.isDefined("001") == True
        assert obj.isDefined("002") == False

    def test_getPrefixByCode(self):
        obj = PrefixTablesFactory()
        obj.add(prefixObj1)
        assert obj.getPrefixByCode("001").getName() == "Meters"
        assert obj.getPrefixByValue("123") == None

    def test_getPrefixByValue(self):
        obj = PrefixTablesFactory()
        obj.add(prefixObj1)
        assert obj.getPrefixByValue(1).getName() == "Meters"
        assert obj.getPrefixByValue(123) == None
