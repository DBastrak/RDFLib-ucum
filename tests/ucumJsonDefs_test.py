import pytest
from ucum.ucumJsonDefs import loadJson
from ucum.unitTables import unitTablesInstance

class Test_ucumJson:

    def test_loadJson(self):
        loadJson()
        assert unitTablesInstance != None