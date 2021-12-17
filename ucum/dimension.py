"""

"""
from ucum.ucum_config import UCUM

class Dimension:
    dimVec_ = None


    def __init__(self, dimSetting:(list, int) = None):
        if UCUM['dimLen_'] == 0:
            raise ValueError("Dimension.setDimensionLen must be called before Dimension constructor")
        if dimSetting == None:
            self.assignZero()
        elif isinstance(dimSetting, list):
            if len(dimSetting) != UCUM['dimLen_']:
                raise ValueError(f"Incorrect length of list passed to Dimension, length should be {UCUM['dimLen_']} not {len(dimSetting)}")
            self.dimVec_ = []
            for x in range(UCUM['dimLen_']):
                self.dimVec_.append(dimSetting[x])

        elif type(dimSetting) is int:
            if (dimSetting < 0 or dimSetting >= UCUM['dimLen_']):
                raise ValueError("Parameter error, invalid element number specified for Dimension constructor")
            self.assignZero()
            self.dimVec_[dimSetting] = 1


    def setElementAt(self, indexPos: int, value:int=None):
        if not isinstance(indexPos, int) or indexPos < 0 or indexPos >= UCUM['dimLen_']:
            raise ValueError(f"setElementAt() called with an invalid index position: {indexPos}")
        if not self.dimVec_:
            self.assignZero()
        if isinstance(value, str):
            raise TypeError(f"Value {value} is incorrect it should be a number not a string")
        elif value is None:
            value = 1
        self.dimVec_[indexPos] = value


    def getElementAt(self, indexPos: int) ->int:
        if not isinstance(indexPos, int) or indexPos < 0 or indexPos >= UCUM['dimLen_']:
            raise ValueError(f"getElementAt() called with an invalid index position: {indexPos}")
        ret = None
        if self.dimVec_:
            ret = self.dimVec_[indexPos]
        return  ret


    def toString(self) -> str:
        ret = None
        if self.dimVec_:
            ret = '[' + ",".join([str(x) for x in self.dimVec_ ]) + ']'
        return ret


    def add(self, dim2):
        if not isinstance(dim2, Dimension):
            raise TypeError(f"add() called with an invalid parameter {type(dim2)} instead of Dimension object")
        if self.dimVec_ and dim2.dimVec_:
            for i in range(UCUM['dimLen_']):
                self.dimVec_[i] += dim2.dimVec_[i]
        return self


    def subtract(self, dim2):
        if not isinstance(dim2, Dimension):
            raise TypeError(f"subtract() called with an invalid parameter {type(dim2)} instead of Dimension object")
        if self.dimVec_ and dim2.dimVec_:
            for i in range(UCUM['dimLen_']):
                self.dimVec_[i] -= dim2.dimVec_[i]
        return self


    def invert(self):
        if self.dimVec_:
            for i in range(UCUM['dimLen_']):
                self.dimVec_[i] = -self.dimVec_[i]
        return self


    def mul(self, scalar: int):
        if not isinstance(scalar, int):
            raise TypeError(f"mul() called with an invalid parameter {type(scalar)} instead of a number")
        if self.dimVec_:
            for i in range(UCUM['dimLen_']):
                self.dimVec_[i] *= scalar
        return self


    def equals(self, dim2) -> bool:
        if not isinstance(dim2, Dimension):
            raise TypeError(f"equals() called with an invalid parameter {type(dim2)} instead of Dimension object")
        isEqual = True
        dimVec2 = dim2.dimVec_
        if self.dimVec_ and dim2.dimVec_:
            for i in range(UCUM['dimLen_']):
                isEqual = self.dimVec_[i] == dimVec2[i]
                if not isEqual:
                    break
        else:
            isEqual = self.dimVec_ is None and dimVec2 is None
        return isEqual


    def assignDim(self, dim2):
        if not isinstance(dim2, Dimension):
            raise TypeError(f"assignDim() called with an invalid parameter {type(dim2)} instead of Dimension object")
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
            for i in range(UCUM['dimLen_']):
                allZero = self.dimVec_[i] == 0
                if not allZero:
                    break
        return allZero


    def isNull(self) -> bool:
        return self.dimVec_ is None


    def clone(self):
        that = Dimension()
        that.assignDim(self)
        return that

