from ucum.ucum_config import UCUM
from ucum.dimension import Dimension
from ucum.ucumFunctions import UcumFunctions
from ucum.unitTables import UnitTables
from ucum.ucumInternalUtils import *
import copy
import math

class Unit:

    def __init__(self, attrs: dict):
        self.isBase_ = attrs['isBase_']

        try:
            self.name_ = attrs['name_']
        except KeyError:
            self.name_ = False


        try:
            self.csCode_ = attrs['csCode_']
        except KeyError:
            self.csCode_ = ''

        try:
            self.ciCode_ = attrs['ciCode_']
        except KeyError:
            self.ciCode_ = ''

        try:
            self.property_ = attrs['property_']
        except KeyError:
            self.property_ = ''

        try:
            self.magnitude_ = attrs['magnitude_']
        except KeyError:
            self.magnitude_ = 1

        if attrs['dim_'] == None:
            self.dim_ = Dimension()

        elif attrs['dim_']['dimVec_'] == None:
            self.dim_ = Dimension(attrs['dim_']['dimVec_'])

        elif type(attrs['dim_']) is Dimension:
            self.dim_ = attrs['dim_']

        elif type(attrs['dim_']) is list or type(attrs['dim_']) is int:
            self.dim_ = Dimension(attrs['dim_'])
        else:
            self.dim_ = Dimension()

        try:
            self.printSymbol_ = attrs['printSymbol_']
        except KeyError:
            self.printSymbol_ = None

        try:
            self.class_ = attrs['class_']
        except KeyError:
            self.class_ = None

        try:
            self.isMetric_ = attrs['isMetric_']
        except KeyError:
            self.isMetric_ = False

        try:
            self.variable_ = attrs['variable_']
        except KeyError:
            self.variable_ = None

        try:
            self.cnv_ = attrs['cnv_']
        except KeyError:
            self.cnv_ = None

        try:
            self.cnvPfx_ = attrs['cnvPfx_']
        except KeyError:
            self.cnvPfx_ = 1

        try:
            self.isSpecial_ = attrs['isSpecial_']
        except KeyError:
            self.isSpecial_ = False

        try:
            self.isArbitrary_ = attrs['isArbitrary_']
        except KeyError:
            self.isArbitrary_ = False

        try:
            self.moleExp_ = attrs['moleExp_']
        except KeyError:
            self.moleExp_ = 0

        try:
            self.synonyms_ = attrs['synonyms_']
        except KeyError:
            self.synonyms_ = None

        try:
            self.source_ = attrs['source_']
        except KeyError:
            self.source_ = None

        try:
            self.loincProperty_ = attrs['loincProperty_']
        except KeyError:
            self.loincProperty_ = None

        try:
            self.category_ = attrs['category_']
        except KeyError:
            self.category_ = None

        try:
            self.guidance_ = attrs['guidance_']
        except KeyError:
            self.guidance_ = None

        try:
            self.csUnitString_ = attrs['csUnitString_']
        except KeyError:
            self.csUnitString_ = None

        try:
            self.ciUnitString_ = attrs['ciUnitString_']
        except KeyError:
            self.ciUnitString_ = None

        try:
            self.baseFactorStr_ = attrs['baseFactorStr_']
        except KeyError:
            self.baseFactorStr_ = None

        try:
            self.baseFactor_ = attrs['baseFactor_']
        except KeyError:
            self.baseFactor_ = None

        try:
            self.defError_ = attrs['defError_']
        except KeyError:
            self.defError_ = False

    def assignUnity(self):
        self.name_ = ""
        self.magnitude_ = 1
        if not self.dim_:
            self.dim_= Dimension()
        self.dim_.assignZero()
        self.cnv_ = None
        self.cnvPfx_ = 1
        return self

    def assignVals(self, vals: list):
        for key in vals:
            uKey = key+'-' if key[-1] != '-' else key
            if eval(f'self.{uKey}'):
                self[uKey] = vals[key]
            else:
                raise KeyError(f'{key} is not a property of a Unit')

    def clone(self):
        retUnit = copy.deepcopy(self)
        return retUnit

    def assign(self, unit2):
        self = copy.deepcopy(unit2)

    def equals(self,unit2) -> bool:
        return( self.magnitude_ == unit2.magnitude_ and self.cnv_ == unit2.cnv_ and self.cnvPfx_ == unit2.cnvPfx_ and
                (self.dim_ == None and unit2.dim_ == None) or self.dim_ == unit2.dim_)

    def fullEquals(self, unit2) -> bool:
        thisAttr = self.keys().sort()
        u2Attr = unit2.keys().sort()
        keyLen = len(thisAttr)
        match = (keyLen == len(u2Attr))
        k = 0
        for k in range(keyLen) and match:
            if thisAttr[k] == u2Attr[k]:
                if thisAttr[k] == 'dim_':
                    match = self.dim_ == unit2.dim_
                else:
                    match = eval(f"self.{thisAttr[k]} == unit2.{thisAttr[k]}")
            else:
                match = False
        return match

    def getProperty(self, propertyName:str = None) -> str:
        uProp = propertyName + '-' if propertyName[-1] != '-' else propertyName
        return eval(f"self.{uProp}")

    def convertFrom(self, num, fromUnit):
        newNum = 0.0
        if self.isArbitrary_:
            raise (f"Attempt to convert arbitrary unit {self.name_}")
        if fromUnit.isArbitrary:
            raise(f"Attempt to convert to arbitrary unit {fromUnit.name_}")

        if fromUnit.dim_ and self.dim_ and not fromUnit.dim_ == self.dim_:
            if self.isMoleMassCommensurable(fromUnit):
                raise(UCUM['needMoleWeightMsg_'])
            else:
                raise (f"Sorry. {fromUnit.csCode_} cannot be converted to {self.csCode_}")

        if fromUnit.dim_ and (not self.dim_ or self.dim_ == None):
            raise (f"Sorry. {fromUnit.csCode_} cannot be converted to {self.csCode_}")

        if self.dim_ and (not fromUnit.dim_ or fromUnit.dim_ == None):
            raise (f"Sorry. {fromUnit.csCode_} cannot be converted to {self.csCode_}")

        fromCnv = fromUnit.cnv_
        fromMag = fromUnit.magnitude_

        if fromCnv == self.cnv_:
            newNum = (num * fromMag)/self.magnitude_

        else:
            x = 0.0
            funcs = UcumFunctions
            if fromCnv != None:

                fromFunc = funcs.forName(fromCnv)
                x = fromFunc['cnvFrom'](num * fromUnit.cnvPfx_) * fromMag
            else:
                x = num * fromMag

            if self.cnv_ != None:
                toFunc = funcs.forName(self.cnv_)
                newNum = toFunc['cnvTo'](x/ self.magnitude_)/self.cnvPfx_
            else:
                newNum = x/ self.magnitude_
        return newNum

    def convertTo(self, num, toUnit):
        return toUnit.convertFrom(num, self)

    def convertCoherent(self, num) -> float: #todo come back to this function
        if self.cnv_ == None:
            num = (num / self.cnvPfx_) * self.magnitude_
        return num

    def mutateCoherent(self, num):
        num = self.convertFrom(num)
        self.magnitude_ = 1
        self.cnv_ = None
        self.cnvPfx_ = 1
        self.name_ = ""


        for i in range(7): #todo (max = Dimension.getMax() not sure how to translate this into python)
            elem = self.dim_.getElementAt(i)
            tabs = UnitTables()
            uA = tabs.getUnitsByDimension(Dimension(i))
            if uA == None:
                raise(f"Can't find base unit for dimensions {i}")
            self.name_ = uA.name + elem #todo not sure how this works

        return num

    """
    param amt the quantity of this unit to be converted
    param molUnit the target/to unit for which the converted # is wanted
    param molecularWeight the molecular weight of the substance for which the conversion is being made
    """
    def convertMassToMol(self, amt: float,  molUnit, molecularWeight:float) -> float:
        molAmt = (self.magnitude_ * amt)/molecularWeight

        tabs = UnitTables()
        avoNum = (tabs.getUnitByCode('mol')).magnitude_
        molesFactor = molUnit.magnitude_ / avoNum

        return molAmt/molesFactor

    def convertMolToMass(self, amt: float, massUnit, molecularWeight):

        tabs = UnitTables()
        avoNum = (tabs.getUnitByCode('mol')).magnitude_
        molesFactor = self.magnitude_ / avoNum
        massAmt = (molesFactor * amt) * molecularWeight
        return massAmt/massUnit.magnitude_

    def mutateRaito(self, num):
        if self.cnv_ == None:
            return self.mutateCoherent(num)
        else:
            return num

    def multiplyThis(self, s):
        retUnit = self.clone()
        if retUnit.cnv_ != None:
            retUnit.cnvPfx_ *= s
        else:
            retUnit.magnitude_ *= s
        mulVal = str(s)
        retUnit.name_ = f"[{mulVal}*{self.name_}]"
        retUnit.csCode_ = f"({mulVal}.{self.csCode_})"
        retUnit.ciCode_ = f"({mulVal}.{self.ciCode_})"
        retUnit.printSymbol_ = f"({mulVal}.{self.printSymbol_})"

        return retUnit

    def multiplyThese(self, unit2):
        retUnit = self.clone()
        if retUnit.cnv_ != None:
            if unit2.cnv_ == None and (not (unit2.dim_) or unit2.dim_ == 0):
                retUnit.cnvPfx_ *= unit2.magnitude_
            else:
                raise TypeError(f"Attempt to multiply non-ratio unit {retUnit.name_} failed")

        elif unit2.cnv_ != None:
            if not(retUnit.dim_ or retUnit.dim_ == 0):
                retUnit.cnvPfx_ = unit2.cnvPfx_ * retUnit.magnitude_
                retUnit.cnv_ = unit2.cnv_
            else:
                raise TypeError(f"Attempt to multiple non-ratio unit {unit2.name_}")

        else:
            retUnit.magnitude_ *= unit2.magnitude_

        if (not (retUnit.dim_) or (retUnit.dim_ and not(retUnit.dim_.dimVec_))):
            if unit2.dim_:
                retUnit.dim_ = unit2.dim_.clone()
            else:
                retUnit.dim_ = unit2.dim_
        elif unit2.dim_ and type(unit2.dim_) is Dimension:
            retUnit.dim_.add(unit2.dim_)

        retUnit.name_ = f"[{retUnit.name_}]*[{unit2.name_}]"
        retUnit.csCode_ = f"({retUnit.csCode_}).({unit2.csCode_})"

        if (retUnit.ciCode_ and unit2.ciCode_):
            retUnit.ciCode_ = f"({retUnit.ciCode_}).({unit2.ciCode_})"

        elif unit2.ciCode_:
            retUnit.ciCode_ = unit2.ciCode_

        retUnit.guidance_ = ''
        if retUnit.printSymbol_ and unit2.printSymbol_:
            retUnit.printSymbol_ = f"({retUnit.printSymbol_}).({unit2.printSymbol_})"

        retUnit.moleExp_ =retUnit.moleExp_ + unit2.moleExp_
        if not(retUnit.isArbitrary_):
            retUnit.isArbitrary_ = unit2.isArbitrary

        return retUnit

    def divide(self, unit2):
        retUnit = self.clone()
        if retUnit.cnv_ != None:
            raise(f"Attempt to divide non-ratio unit {retUnit.name_}")
        if unit2.cnv_ != None:
            raise (f"Attempt to divide non-ratio unit {unit2.name_}")

        if retUnit.name_ and unit2.name_:
            retUnit.name_ = f"[{retUnit.name_}]/[{unit2.name_}]"
        elif unit2.name_:
            retUnit.name_ = unit2.invertString(unit2.name_)

        retUnit.csCode_ = f"({retUnit.csCode_})/({unit2.csCode_})"

        if (retUnit.ciCode_ and unit2.ciCode_):
            retUnit.ciCode_ = f"({retUnit.ciCode_})/({unit2.ciCode_})"
        elif unit2.csCode_:
            retUnit.ciCode_ = unit2.invertString(unit2.ciCode_)

        retUnit.guidance_ = ''
        retUnit.magnitude_ /= unit2.magnitude_

        if retUnit.printSymbol_ and unit2.printSymbol_:
            retUnit.printSymbol_ = f"({retUnit.printSymbol_})/({unit2.printSymbol_})"
        elif unit2.printSymbol_:
            retUnit.printSymbol_ = unit2.invertString(unit2.printSymbol_)

        if unit2.dim_:
            if retUnit.dim_:
                if retUnit.dim_ == None:
                    retUnit.dim_.assignZero()
                retUnit.dim_ = unit2.dim_.sub(unit2.dim_)
            else:
                retUnit.dim_ = unit2.dim_.clone().minus()

        retUnit.moleExp_ = retUnit.moleExp_ = unit2.moleExp_

        if not (retUnit.isArbitrary_):
            retUnit.isArbitrary_ = unit2.isArbitrary

        return retUnit

    def invert(self):
        if self.cnv_ != None:
            raise (f"Attempt to invert a non-ratio unit {self.name_}")
        self.name_ = self.invertString(self.name_)
        self.magnitude_ = 1/self.magnitude_
        self.dim_.minus()
        return self

    def invertString(self, theString):
        if len(theString) > 0:
            stringRep = theString.replace('/', '!').replace('.', '/').replace('!','.')
            if stringRep[0] == '.':
                theString = stringRep[1]
            if stringRep[0] == '/':
                theString = stringRep
            else:
                theString = "/" + stringRep
        return theString

    def power(self, p):
        if self.cnv_ != None:
            raise(f"Attempt to raise a non-ratio unit, {self.name_} to a power")
        uStr = self.csCode_
        uArray = uStr #todo convert regex .match(/([./]|[^./]+)/g)
        arLen = len(uArray)

        for i in range(arLen):
            un = len(uArray)
            if un != '/' and un != '.':
                try:
                    nun = int(un)
                    if type(nun) is int:
                        uArray[i] = str(math.pow(nun, p))
                except:
                    uLen = len(un)
                    u = uLen - 1
                    for i in range(u, 0, -1):
                        try:
                            uChar = int(un[u])
                            if type(uChar) is not int:
                                if un[u] == '-' or un[u] == '+':
                                    u -= 1
                                if u < uLen -1:
                                    exp = int(un[u])
                                    exp = math.pow(exp, p)
                                    uArray[i] = un[0,u] + str(exp)
                                    u = -1
                                else:
                                    uArray[i] += str(p)
                                    u = -1
                                u =-1
                        except:
                            pass
        self.csCode_ = uArray.join('')
        self.magnitude_ = math.pow(self.magnitude_, p)
        if self.dim_:
            self.dim_.mul(p)

        return self

    def isMoleMassCommensurable(self, unit2):
        tabs = UnitTables()
        d = tabs.getMassDimensionsIndex()
        commensurable = False
        if self.moleExp_ == 1 and unit2.moleExp_ == 0:
            testDim = self.dim_.clone()
            curVal = testDim.getElementAt(d)
            testDim.setElementAt(d, (curVal + unit2.moleExp_))
            commensurable = testDim.equals(self.dim_)
        elif unit2.moleExp_ == 1 and self.moleExp_ == 0:
            testDim = unit2.dim_.clone()
            curVal = testDim.getElementAt(d)
            testDim.setElementAt(d, (curVal + unit2.moleExp_))
            commensurable = testDim.equals(self.dim_)

        return commensurable
