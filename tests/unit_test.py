import pytest
from ucum.unit import Unit

tempUnitDict = {'isBase_': True, 'name_': 'meter', 'csCode_': 'm', 'ciCode_': 'M',
                        'property_': 'length', 'magnitude_': 1,
                        'dim_': {'dimVec_': [1, 0, 0, 0, 0, 0, 0]}, 'printSymbol_': 'm', 'class_': None,
                        'isMetric_': False,
                        'variable_': 'L', 'cnv_': None, 'cnvPfx_': 1,
                        'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                        'synonyms_': ['meters', 'metres', 'distance'],
                        'source_': 'UCUM', 'loincProperty_': 'Len', 'category_': 'Clinical',
                        'guidance_': 'unit of length = 1.09361 yards', 'csUnitString_': None, 'ciUnitString_': None,
                        'baseFactorStr_': None, 'baseFactor_': None, 'defError_': False}
tempUnitDict2 = {'isBase_': False, 'name_': 'meter', 'csCode_': 'm', 'ciCode_': 'M',
                        'property_': 'length', 'magnitude_': 1,
                        'dim_': {'dimVec_': [1, 0, 0, 0, 0, 0, 0]}, 'printSymbol_': 'm', 'class_': None,
                        'isMetric_': False,
                        'variable_': 'L', 'cnv_': None, 'cnvPfx_': 1,
                        'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                        'synonyms_': ['meters', 'metres', 'distance'],
                        'source_': 'UCUM', 'loincProperty_': 'Len', 'category_': 'Clinical',
                        'guidance_': 'unit of length = 1.09361 yards', 'csUnitString_': None, 'ciUnitString_': None,
                        'baseFactorStr_': None, 'baseFactor_': None, 'defError_': False}
tempUnitDictCM = {'isBase_': False, 'name_': 'centimeter', 'csCode_': 'cm', 'ciCode_': 'CM',
                        'property_': 'length', 'magnitude_': 100,
                        'dim_': {'dimVec_': [1, 0, 0, 0, 0, 0, 0]}, 'printSymbol_': 'cm', 'class_': None,
                        'isMetric_': False,
                        'variable_': 'L', 'cnv_': None, 'cnvPfx_': 1,
                        'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                        'synonyms_': ['meters', 'metres', 'distance'],
                        'source_': 'UCUM', 'loincProperty_': 'Len', 'category_': 'Clinical',
                        'guidance_': 'unit of length = 1.09361 yards', 'csUnitString_': None, 'ciUnitString_': None,
                        'baseFactorStr_': None, 'baseFactor_': None, 'defError_': False}
tempUnitDict3 = {'isBase_': True, 'name_': 'meter', 'csCode_': 'm', 'ciCode_': 'M',
                        'property_': 'length', 'magnitude_': 2,
                        'dim_': {'dimVec_': [1, 0, 0, 0, 0, 0, 0]}, 'printSymbol_': 'm', 'class_': None,
                        'isMetric_': False,
                        'variable_': 'L', 'cnv_': None, 'cnvPfx_': 1,
                        'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                        'synonyms_': ['meters', 'metres', 'distance'],
                        'source_': 'UCUM', 'loincProperty_': 'Len', 'category_': 'Clinical',
                        'guidance_': 'unit of length = 1.09361 yards', 'csUnitString_': None, 'ciUnitString_': None,
                        'baseFactorStr_': None, 'baseFactor_': None, 'defError_': False}
tempUnitDictMol = {'isBase_': False, 'name_': 'micro enzyme unit per gram', 'csCode_': 'uU/g', 'ciCode_': 'UU/G',
                        'property_': 'catalytic activity', 'magnitude_': 10036894500,
                        'dim_': {'dimVec_': [0,-1,-1,0,0,0,0]}, 'printSymbol_': 'μU/g', 'class_': "chemical",
                        'isMetric_': True,
                        'variable_': None, 'cnv_': None, 'cnvPfx_': 1,
                        'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 1,
                        'synonyms_': ['uU per gm', 'micro enzyme units per gram', 'micro enzymatic activity per mass',
                                      'enzyme activity'],
                        'source_': 'LOINC', 'loincProperty_': 'CCnt', 'category_': 'Clinical',
                        'guidance_': '1 U is the standard enzyme unit which equals 1 micromole substrate catalyzed per minute (1 umol/min); 1 uU = 1pmol/min',
                        'csUnitString_': 'umol/min', 'ciUnitString_': "UMOL/MIN",
                        'baseFactorStr_': "1", 'baseFactor_': 1, 'defError_': False}

class Test_unit:

    def test_init(self):

        instance = Unit(tempUnitDict)
        assert instance.defError_ == False

    def test_assignUnity(self):
        instance = Unit(tempUnitDict)
        instance.assignUnity()
        assert instance.dim_.dimVec_ == [0,0,0,0,0,0,0]

    def test_assignVals(self):
        instance = Unit(tempUnitDict2)
        instance.assignVals(tempUnitDict)
        assert instance.isBase_ == True

    def test_clone(self):
        instance = Unit(tempUnitDict)
        instance2 = instance.clone()
        assert instance2.name_ == instance.name_

    def test_assign(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2)
        instance2.assign(instance)
        assert instance2.isBase_ == instance.isBase_

    def test_equals(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2)
        assert instance.equals(instance) == True
        assert instance.equals(instance2) == False

    def test_fullEquals(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2)
        assert instance.fullEquals(instance) == True
        assert instance.fullEquals(instance2) == False

    def test_convertTo(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDictCM)

        assert instance2.convertTo(200 ,instance) == 2 #cm to meters 200 -> 2

    def test_convertFrom(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDictCM)
        assert instance2.convertFrom(2, instance) == 200 #meters to cm 2 -> 200

    def test_convertCoherent(self):
        instance = Unit(tempUnitDict)

        assert instance.convertCoherent(2) == 2

    def test_mutateCoherent(self):#change first test mean to work with a different unit check why dim not correctly added
        instance = Unit(tempUnitDict)
        instance.dim_.dimVec_ = [1, 0, 0, 0, 0, 0, 0, 0]

        assert instance.mutateCoherent(1, instance) == 1

    def test_convertMassToMol(self):
        instance = Unit(tempUnitDict) #todo add units for testing with mass to mol
        instance2 = Unit(tempUnitDict)
        assert instance.convertMassToMol(10, instance2, 10.0) == 1

    def test_convertMoltoMass(self):
        instance = Unit(tempUnitDict)  # todo add units for testing with mass to mol
        instance2 = Unit(tempUnitDict)

        assert instance.convertMolToMass(10, instance2, 10.0) == 1

    def test_multiplyThis(self):
        instance = Unit(tempUnitDict)
        x = instance.multiplyThis(2)
        assert x.magnitude_ == 2

    def test_multiplyThese(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2)
        x = instance.multiplyThese(instance2)
        assert x.cnvPfx_ == 1

    def test_divide(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2)
        instance.divide(instance2)
        assert instance.magnitude_ == 1

    def test_invert(self):
        instance = Unit(tempUnitDict)
        instance.invert()
        assert instance.magnitude_ == 1

    def test_invertString(self):
        instance = Unit(tempUnitDict)
        assert instance.invertString("!.") == "/"

    def test_power(self):
        instance = Unit(tempUnitDict3)
        instance.power(2)
        assert instance.magnitude_ == 4


    def test_isMoleMassCommensurable(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2)
        assert instance.isMoleMassCommensurable(instance2) == False


