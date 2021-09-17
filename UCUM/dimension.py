"""

"""
from UCUM.ucum_config import UCUM

class Dimension:
    dimVec_ = None
    def __init__(self, dimSetting:(list, int) = None):
        if UCUM['dimLen_'] == 0:
            raise ValueError("Dimension.setDimensionLen must be called before Dimension constructor")
        if dimSetting == None:
            self.assignZero()
        elif type(dimSetting) is list:
            if len(dimSetting) != UCUM['dimLen_']:
                raise ValueError(f"Incorrect length of list passed to Dimension, length should be {UCUM['dimLen_']} not {len(dimSetting)}")
            self.dimVec_ = []
            for x in range(len(UCUM['dimLen_'])):
                self.dimVec_.append(dimSetting[x])

        elif type(dimSetting) is int:
            if (dimSetting < 0 or dimSetting >= UCUM['dimLen_']):
                raise ValueError("Parameter error, invalid element number specified for Dimension constructor")
            self.assignZero()
            self.dimVec_[dimSetting] = 1

    def setElementAt(self, indexPos: int, value:int=None):
        if type(indexPos) is not int or indexPos < 0 or indexPos >= UCUM['dimLen_']:
            raise ValueError(f"setElementAt() called with an invalid index position: {indexPos}")
        if not self.dimVec_:
            self.assignZero()
        if value is None:
            value = 1
        self.dimvec_[indexPos] = value

    def getElementAt(self, indexPos: int) ->int:
        if type(indexPos) is not int or indexPos < 0 or indexPos >= UCUM['dimLen_']:
            raise ValueError(f"getElementAt() called with an invalid index position: {indexPos}")
        ret = None
        if self.dimVec_:
            ret = self.dimVec_[indexPos]
        return  ret

    def getProperty(self, propertyName:str) -> str:
        uProp = propertyName if propertyName[-1] == '_' else propertyName + '_'
        return uProp

    def toString(self) -> str:
        ret = None
        if self.dimVec_:
            ret = '[' + self.dimVec_.join(',') + ']'
        return ret

    def add(self, dim2):
        if isinstance(not dim2, Dimension):
            raise ValueError(f"add() called with an invalid parameter {type(dim2)} instead of Dimension object")
        if self.dimVec_ and dim2.dimVec_:
            for i in range(UCUM['dimLen_']):
                self.dimVec_[i] += dim2.dimVec_[i]
        return self

    def subtract(self, dim2):
        if isinstance(not dim2, Dimension):
            raise ValueError(f"add() called with an invalid parameter {type(dim2)} instead of Dimension object")
        if self.dimVec_ and dim2.dimVec_:
            for i in range(UCUM['dimLen_']):
                self.dimVec_[i] -= dim2.dimVec_[i]
        return self

    def minus(self):
        if self.dimVec_:
            for i in range(UCUM['dimLen_']):
                self.dimVec_[i] = -self.dimVec_[i]
        return self

    def mul(self, scalar: int):
        if type(scalar) is not int:
            raise TypeError(f"mul() called with an invalid parameter {type(scalar)} instead of a number")
        if self.dimVec_:
            for i in range(UCUM['dimLen_']):
                self.dimVec_ *= scalar
        return self

    def equals(self, dim2) -> bool:
        if isinstance(not dim2, Dimension):
            raise ValueError(f"add() called with an invalid parameter {type(dim2)} instead of Dimension object")
        isEqual = True
        dimVec2 = dim2.dimVec_
        if self.dimVec_ and dim2.dimVec_:
            for i in range(UCUM['dimLen_']) and isEqual:
                isEqual = self.dimVec_[i] == dimVec2[i]
        else:
            isEqual = self.dimVec_ is None and dimVec2 is None
        return isEqual

    def assignDim(self, dim2):
        if isinstance(not dim2, Dimension):
            raise ValueError(f"add() called with an invalid parameter {type(dim2)} instead of Dimension object")
        if dim2.dimVec_ is None:
            self.dimVec_ = None
        else:
            if self.dimVec_ is None:
                self.dimVec_ = []
            for i in range(UCUM['dimLen_']):
                self.dimVec_[i] = dim2.dimVec_[i]
        return self

    def assignZero(self):
        if self.dimVec_ is None:
            self.dimVec_ = []
        for i in range(UCUM['dimLen_']):
            self.dimVec_.append(0)
        return self

    def isZero(self) -> bool:
        allZero = self.dimVec_ != None
        if self.dimVec_:
            for i in range(UCUM['dimLen_']) and allZero:
                allZero = self.dimVec_[i] == 0
        return allZero

    def isNull(self) -> bool:
        return self.dimVec_ is None

    def clone(self):
        that = Dimension()
        that.assignDim(self)
        return that

