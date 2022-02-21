from ucum.unitString import UnitString
import pytest
from ucum.ucumJsonDefs import loadJson
from ucum.unitTables import unitTablesInstance

loadJson()
unitTablesInstance.buildUnitSynonyms()

class Test_unitString:

    def test_useBraceMsgForEachString(self):
        instance = UnitString()
        instance.useBraceMsgForEachString(True)
        assert instance.braceMsg_ == 'FYI - annotations (text in curly braces {}) are ignored, except that an annotation without a leading symbol implies the default unit 1 (the unity).'

        instance.useBraceMsgForEachString(False)
        assert instance.braceMsg_ == ''

    def test_parseString(self):
        instance = UnitString()
        assert instance.parseString("String") != None

    def test_parseTheString(self):
        instance = UnitString()
        assert instance._parseTheString("String", "String") != None

    def test_getAnnotations(self):
        instance = UnitString()
        assert instance._parseTheString("String", "String") != None

    def test_processParens(self):
        instance = UnitString()
        assert instance._processParens("String", "String") != None

    def test_makeUnitsArray(self):
        instance = UnitString()
        assert instance._makeUnitsArray("String", "String") != None

    def test_getParensUnit(self):
        instance = UnitString()
        assert instance._getParensUnit("String", "String") != None

    def test_getAnnoText(self):
        instance = UnitString()
        assert instance._getAnnoText("String", "String") != None

    def test_getSuggestions(self):
        instance = UnitString()
        assert instance._getSuggestions("String") != None

    def test_makeUnit(self):
        instance = UnitString()
        assert instance._makeUnit("m", "String") != None

    def test_getUnitWithAnnotation(self):
        instance = UnitString()
        assert instance._getUnitWithAnnotation("String", "String") != None

    def test_performUnitArithmetic(self):
        instance = UnitString()
        assert instance._performUnitArithmetic("String", "String") != None

    def test_isCodeWithExponent(self):
        instance = UnitString()
        assert instance._isCodeWithExponent("String") != None
