
from ucum.unitTables import UnitTablesFactory
from ucum.unit import Unit
import pytest

unitDict = {'isBase_': True, 'name_': 'meter', 'csCode_': 'm', 'ciCode_': 'M',
                             'property_': 'length', 'magnitude_': 1,
                             'dim_': {'dimVec_': [1, 0, 0, 0, 0, 0, 0]}, 'printSymbol_': 'm', 'class_': None,
                             'isMetric_': False,
                             'variable_': 'L', 'cnv_': None, 'cnvPfx_': 1,
                             'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                             'synonyms_': ['meters', 'metres', 'distance'],
                             'source_': 'UCUM', 'loincProperty_': 'Len', 'category_': 'Clinical',
                             'guidance_': 'unit of length = 1.09361 yards', 'csUnitString_': None,
                             'ciUnitString_': None,
                             'baseFactorStr_': None, 'baseFactor_': None, 'defError_': False}

unitDictUnitString = {'isBase_': False, 'name_': 'newton', 'csCode_': 'N', 'ciCode_': 'N',
                             'property_': 'force', 'magnitude_': 1000,
                             'dim_': {'dimVec_': [1, -2, 0, 0, 0, 0, 0]}, 'printSymbol_': 'N', 'class_': "si",
                             'isMetric_': True,
                             'variable_': None, 'cnv_': None, 'cnvPfx_': 1,
                             'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                             'synonyms_': ['Newtons'],
                             'source_': 'UCUM', 'loincProperty_': 'Force', 'category_': 'Clinical',
                             'guidance_': 'unit of force with base units kg.m/s2', 'csUnitString_': "kg.m/s2",
                             'ciUnitString_': "KG.M/S2",
                             'baseFactorStr_': "1", 'baseFactor_': 1, 'defError_': False}


class TestUnitTables():


    def test_unitsCount(self):
        instance = UnitTablesFactory()
        assert instance.unitsCount() == 0

    def test_addUnit(self):
        instance = UnitTablesFactory()
        instance.addUnit(unitDict)
        assert instance.unitsCount() == 1

    def test_addUnitName(self):
        instance = UnitTablesFactory()
        instance.addUnitName(unitDict)
        assert len(instance.unitNames_) == 1

    def test_addUnitCode(self):
        instance = UnitTablesFactory()
        instance.addUnitCode(unitDict)
        assert len(instance.unitCodes_) == 1

    def test_addUnitString(self):
        instance = UnitTablesFactory()
        instance.addUnitString(unitDictUnitString)
        assert len(instance.unitStrings_) == 1

    def test_addUnitDimension(self):
        instance = UnitTablesFactory()
        instance.addUnitDimension(unitDict)
        assert len(instance.unitDimensions_) == 1

    def test_buildUnitSynonyms(self):
        pass

    def test_addSynonymCodes(self):
        pass

    def test_getUnitByCode(self):
        instance = UnitTablesFactory()
        instance.addUnit(unitDict)
        assert instance.getUnitByCode('m') == unitDict

    def test_getUnitByName(self):
        instance = UnitTablesFactory()
        instance.addUnit(unitDict)
        assert instance.getUnitByName('meter') == unitDict

    def test_getUnitByString(self):
        instance = UnitTablesFactory()
        instance.addUnit(unitDictUnitString)
        assert instance.getUnitByString('kg.m/s2') == {'mag': '1', 'unit':unitDictUnitString}

    def test_getUnitsByDimension(self):
        instance = UnitTablesFactory()
        instance.addUnit(unitDict)
        assert instance.getUnitsByDimension([1,0,0,0,0,0,0]) == [unitDict]

    def test_getUnitBySynonym(self):
        instance = UnitTablesFactory()
        instance.addUnit(unitDict)
        assert instance.getUnitByName('meter') == unitDict

    def test_getAllUnitNames(self):
        instance = UnitTablesFactory()
        instance.addUnit(unitDict)
        assert list(instance.getAllUnitNames()) == ['meter']

    def test_getMassDimensionsIndex(self):
        instance = UnitTablesFactory()
        instance.addUnit(unitDict)
        assert instance.getMassDimensionsIndex() == 0

    def test_compareCode(self):
        pass

    def test_getAllUnitCodes(self):
        instance = UnitTablesFactory()
        instance.addUnit(unitDict)
        assert list(instance.getAllUnitCodes()) == ['m']

    def test_allUnitsByDef(self):
        pass

    def test_allUnitsByName(self):
        pass

    def test_printUnits(self):
        pass

    def test_UnitTables(self):
        pass
