



class PrefixTablesFactory:

    def __init__(self):
        self.byCode_ = {}
        self.byValue_ = {}

    def prefixCount(self) -> int:
        return len(self.byCode_)

    def allPrefixesByValue(self) -> str:
        prefixBuff = ''

        for key in self.byValue_:
            pfx = self.getPrefixByValue(key)
            prefixBuff += pfx.code_ + ',' + pfx.name_ + ',,' + f"{pfx.value_}" + '\r\n'
        return prefixBuff

    def allPrefixesByCode(self) -> list:
        prefixList = []
        for key in self.byCode_:
            prefixList.append(self.getPrefixByCode(key))
        return prefixList

    def add(self, prefixObj):
        self.byCode_[prefixObj.getCode()] = prefixObj
        self.byValue_[prefixObj.getValue()] = prefixObj

    def isDefined(self, code:str) -> bool:
        try:
            return self.byCode_[code] != None
        except KeyError:
            return False

    def getPrefixByCode(self,code):
        try:
            return self.byCode_[code]
        except KeyError:
            print("This code doesn't exist")
            return None

    def getPrefixByValue(self, value):
        try:
            return self.byValue_[value]
        except KeyError:
            print("This value doesn't exist")
            return None

prefixTablesInstance = PrefixTablesFactory()

def prefixTable():
    return prefixTablesInstance