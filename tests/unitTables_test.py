from ucum.dimension import Dimension
from ucum.unitTables import UnitTablesFactory
from ucum.unit import Unit
import pytest

unitDict = {'isBase_': True, 'name_': 'meter', 'csCode_': 'm', 'ciCode_': 'M',
                             'property_': 'length', 'magnitude_': 1,
                             'dim_': {'dimVec_': [1, 0, 0, 0, 0, 0, 0, 0]}, 'printSymbol_': 'm', 'class_': None,
                             'isMetric_': False,
                             'variable_': 'L', 'cnv_': None, 'cnvPfx_': 1,
                             'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                             'synonyms_': ['meters', 'metres', 'distance'],
                             'source_': 'UCUM', 'loincProperty_': 'Len', 'category_': 'Clinical',
                             'guidance_': 'unit of length = 1.09361 yards', 'csUnitString_': None,
                             'ciUnitString_': None,
                             'baseFactorStr_': None, 'baseFactor_': None, 'defError_': False}

class TestUnitTables():


    def test_unitsCount(self):
        instance = UnitTablesFactory()
        assert instance.unitsCount() == 0

    def test_addUnit(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnit(instanceUnit)
        assert instance.unitsCount() == 1

    def test_addUnitName(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnitName(instanceUnit)
        assert len(instance.unitNames_) == 1

    def test_addUnitCode(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnitName(instanceUnit)
        assert len(instance.unitCodes_) == 1

    def test_addUnitString(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnitName(instanceUnit)
        assert len(instance.unitStrings_) == 1

    def test_addUnitDimension(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnitName(instanceUnit)
        assert len(instance.unitDimensions_) == 1

    def test_buildUnitSynonyms(self):
        pass

    def test_addSynonymCodes(self):
        pass

    def test_getUnitByCode(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnit(instanceUnit)
        assert instance.getUnitByCode('m') == instanceUnit

    def test_getUnitByName(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit()
        instance.addUnit(instanceUnit)
        assert instance.getUnitByName('meter') == instanceUnit

    def test_getUnitByString(self):
        instance = UnitTablesFactory()
        #unit class edited for this instance
        instanceUnit = Unit({'isBase_': True, 'name_': 'meter', 'csCode_': 'm', 'ciCode_': 'M',
                             'property_': 'length', 'magnitude_': 1,
                             'dim_': {'dimVec_': [1, 0, 0, 0, 0, 0, 0, 0]}, 'printSymbol_': 'm', 'class_': None,
                             'isMetric_': False,
                             'variable_': 'L', 'cnv_': None, 'cnvPfx_': 1,
                             'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                             'synonyms_': ['meters', 'metres', 'distance'],
                             'source_': 'UCUM', 'loincProperty_': 'Len', 'category_': 'Clinical',
                             'guidance_': 'unit of length = 1.09361 yards', 'csUnitString_': 'meter',
                             'ciUnitString_': None,
                             'baseFactorStr_': None, 'baseFactor_': None, 'defError_': False})
        instance.addUnit(instanceUnit)
        assert instance.getUnitByString('meter') == instanceUnit

    def test_getUnitsByDimension(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnit(instanceUnit)
        assert instance.getUnitsByDimension(1) == instanceUnit

    def test_getUnitBySynonym(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnit(instanceUnit)
        assert instance.getUnitByName('meters') == instanceUnit

    def test_getAllUnitNames(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnit(instanceUnit)
        assert instance.getAllUnitNames() == ['meter']

    def test_getMassDimensionsIndex(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnit(instanceUnit)
        assert instance.getMassDimensionsIndex() == 0

    def test_compareCode(self):
        pass

    def test_getAllUnitCodes(self):
        instance = UnitTablesFactory()
        instanceUnit = Unit(unitDict)
        instance.addUnit(instanceUnit)
        assert instance.getAllUnitCodes() == ['m']

    def test_allUnitsByDef(self):
        pass

    def test_allUnitsByName(self):
        pass

    def test_printUnits(self):
        pass

    def test_UnitTables(self):
        pass
