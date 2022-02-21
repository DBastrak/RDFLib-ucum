import pytest
from ucum.ucumLhcUtils import ucumLhcUtils
from ucum.unitTables import unitTablesInstance
from ucum.ucum_config import UCUM
from ucum.ucumJsonDefs import loadJson

loadJson()

class Test_ucumLhcUtils:

    def test_init(self):
        instance = ucumLhcUtils()
        assert instance.uStrParser_ != None and unitTablesInstance != None

    def test_useBraceMsg(self):
        instance = ucumLhcUtils()
        instance.useBraceMsgForEachString()
        assert instance.uStrParser_.braceMsg_ == UCUM["bracesMsg_"]

        instance.useBraceMsgForEachString(False)
        assert instance.uStrParser_.braceMsg_ == ""

    def test_validateUnitString(self):
        instance = ucumLhcUtils()
        ret = instance.validateUnitString("m")
        assert ret["status"] == "valid"

    def test_convertUnitTo(self):
        loadJson()
        unitTablesInstance.buildUnitSynonyms()
        instance = ucumLhcUtils()
        ret = instance.convertUnitTo(1, "cm", "m")
        assert ret["toVal"] == 100
        ret = instance.convertUnitTo(1, "g", "kg")
        assert ret["toVal"] == 1000


    def test_checkSynonyms(self):
        loadJson()
        unitTablesInstance.buildUnitSynonyms()
        instance = ucumLhcUtils()
        ret = instance.checkSynonyms("m")
        assert ret['status'] != 'error'

    def test_getSpecifiedUnit(self):
        loadJson()
        unitTablesInstance.buildUnitSynonyms()
        instance = ucumLhcUtils()
        ret = instance.checkSynonyms("m")
        assert 'error' not in ret['status']

    def test_commensurablesList(self):
        loadJson()
        unit = unitTablesInstance.getUnitByName("meter")
        unitTablesInstance.addUnitDimension(unit)
        instance = ucumLhcUtils()
        retList = instance.commensurablesList("meter")
        assert retList[0] != None
