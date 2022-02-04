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
        instance = ucumLhcUtils()
        ret = instance.convertUnitTo(1, "cm", "m")
        assert ret["status"] == 'succeeded'

    def test_checkSynonyms(self):
        instance = ucumLhcUtils()
        ret = instance.checkSynonyms("m")
        assert ret['status'] != 'error'

    def test_getSpecifiedUnit(self):
        instance = ucumLhcUtils()
        ret = instance.checkSynonyms("m")
        assert 'error' not in ret["retMsg"][0]

    def test_commensurablesList(self):
        instance = ucumLhcUtils()
        retList = instance.commensurablesList("m")
        assert retList[0] != None