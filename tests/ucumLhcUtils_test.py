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
        ret = instance.convertUnitTo(1, "m", "cm")
        assert ret["toVal"] == 100
        ret = instance.convertUnitTo(0.025400000000000002, "m", "[in_i]")
        assert ret["toVal"] == 1
        ret = instance.convertUnitTo(0.3048, "m", "[ft_i]")
        assert ret["toVal"] == 1
        ret = instance.convertUnitTo(1000, "m", "km")
        assert ret["toVal"] == 1
        ret = instance.convertUnitTo(1000, "g", "kg")
        assert ret["toVal"] == 1
        ret = instance.convertUnitTo(1, "J", "W")
        assert ret["toVal"] == 1
        ret = instance.convertUnitTo(60, "s", "min")
        assert ret["toVal"] == 1
        ret = instance.convertUnitTo(60, "min", "h")
        assert ret["toVal"] == 1


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
        instance = ucumLhcUtils()
        retList = instance.commensurablesList("meter")
        assert retList[0] != None
