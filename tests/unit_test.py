import pytest
from ucum.unit import Unit

tempUnitDict = {'isBase_': True, 'name_': 'meter', 'csCode_': 'm', 'ciCode_': 'M',
                        'property_': 'length', 'magnitude_': 1,
                        'dim_': {'dimVec_': [1, 0, 0, 0, 0, 0, 0, 0]}, 'printSymbol_': 'm', 'class_': None,
                        'isMetric_': False,
                        'variable_': 'L', 'cnv_': None, 'cnvPfx_': 1,
                        'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                        'synonyms_': ['meters', 'metres', 'distance'],
                        'source_': 'UCUM', 'loincProperty_': 'Len', 'category_': 'Clinical',
                        'guidance_': 'unit of length = 1.09361 yards', 'csUnitString_': None, 'ciUnitString_': None,
                        'baseFactorStr_': None, 'baseFactor_': None, 'defError_': False}
tempUnitDict2 = {'isBase_': False, 'name_': 'meter', 'csCode_': 'm', 'ciCode_': 'M',
                        'property_': 'length', 'magnitude_': 1,
                        'dim_': {'dimVec_': [1, 0, 0, 0, 0, 0, 0, 0]}, 'printSymbol_': 'm', 'class_': None,
                        'isMetric_': False,
                        'variable_': 'L', 'cnv_': None, 'cnvPfx_': 1,
                        'isSpecial_': False, 'isArbitrary_': False, 'moleExp_': 0,
                        'synonyms_': ['meters', 'metres', 'distance'],
                        'source_': 'UCUM', 'loincProperty_': 'Len', 'category_': 'Clinical',
                        'guidance_': 'unit of length = 1.09361 yards', 'csUnitString_': None, 'ciUnitString_': None,
                        'baseFactorStr_': None, 'baseFactor_': None, 'defError_': False}

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

        assert instance.equals(instance2) == True

    def test_fullEquals(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2)

        assert instance.fullEquals(instance2) == True

    def test_convertFrom(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2) #todo add cm unit

        assert instance.convertFrom(200 ,instance2) == 2 #cm to meters 200 -> 2

    def test_convertTo(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2) #todo add cm unit

        assert instance.convertTo(2 , instance2) == 200 #meters to cm 2 -> 200

    def test_convertCoherent(self):
        instance = Unit(tempUnitDict)

        assert instance.convertCoherent(2) == 2

    def test_mutateCoherent(self):
        instance = Unit(tempUnitDict)

        assert instance.mutateCoherent(1) == 1

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
        assert instance.multiplyThis(2).cnvPfx_ == 2

    def test_multiplyThese(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2)
        assert instance.multiplyThese(instance2).cnvPfx_ == 2

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
        instance = Unit(tempUnitDict)
        instance.power(2)
        assert instance.magnitude_ == 4


    def test_isMoleMassCommensurable(self):
        instance = Unit(tempUnitDict)
        instance2 = Unit(tempUnitDict2)
        assert instance.isMoleMassCommensurable(instance2) == False


