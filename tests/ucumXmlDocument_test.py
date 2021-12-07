import pytest
from ucum.ucumXmlDocument import ucumXMLDocument
from ucum.unitTables import unitTablesInstance
from ucum.prefixTables import prefixTablesInstance

class Test_ucumXmlDocument:

    def test_ParseXML(self):
        instance = ucumXMLDocument()
        list = instance.parseXML()
        prefix = list[0]
        base = list[1]
        unit = list[2]
        assert prefix != None
        assert base != None
        assert unit != None

    def test_parsePrefixes(self):
        instance = ucumXMLDocument()
        list = instance.parseXML()
        prefix = list[0]
        prefixTablesInstance.byCode_ = {}
        prefixTablesInstance.byValue_ = {}
        instance.parsePrefixes(prefix)
        assert prefixTablesInstance.byCode_ != None
        assert prefixTablesInstance.byValue_ != None

    def test_BaseUnits(self):
        instance = ucumXMLDocument()
        list = instance.parseXML()
        base = list[1]
        unitTablesInstance.unitCodes_ = {}
        unitTablesInstance.unitCodes_ = {}
        unitTablesInstance.codeOrder_ = []
        unitTablesInstance.unitStrings_ = {}
        unitTablesInstance.unitDimensions_ = {}
        unitTablesInstance.unitSynonyms_ = {}
        unitTablesInstance.massDimIndex_ = 0
        instance.parseBaseUnits(base)

        assert unitTablesInstance.unitCodes_ != None

    def test_parseUnitStrings(self):
        instance = ucumXMLDocument()
        list = instance.parseXML()
        base = list[1]
        unitTablesInstance.unitCodes_ = {}
        unitTablesInstance.unitCodes_ = {}
        unitTablesInstance.codeOrder_ = []
        unitTablesInstance.unitStrings_ = {}
        unitTablesInstance.unitDimensions_ = {}
        unitTablesInstance.unitSynonyms_ = {}
        unitTablesInstance.massDimIndex_ = 0
        instance.parseBaseUnits(base)

        assert unitTablesInstance.unitCodes_ != None