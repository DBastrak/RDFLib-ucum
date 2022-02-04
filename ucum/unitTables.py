from ucum.ucum_config import UCUM

class UnitTablesFactory:

    def __init__(self):
        self.unitNames_ = {}
        self.unitCodes_ = {}
        self.codeOrder_ = []
        self.unitStrings_ = {}
        self.unitDimensions_ = {}
        self.unitSynonyms_ = {}
        self.massDimIndex_ = 0

    def unitsCount(self):
        return len(self.unitCodes_)

    def addUnit(self, theUnit):
        uName = theUnit["name_"]

        if uName:
            self.addUnitName(theUnit)

        self.addUnitCode(theUnit)
        self.addUnitString(theUnit)

        try:
            if theUnit.dim_.dimVec_:
                self.addUnitDimension(theUnit)
        except:
            pass

    def addUnitName(self, theUnit): #todo rework function
        uName = theUnit["name_"]

        if uName:
            try:
                if self.unitNames_[uName]:
                    tempList = [self.unitNames_[uName]].append(theUnit)
                    self.unitNames_[uName] = tempList
            except KeyError:
                self.unitNames_[uName] = theUnit
        else:
            raise ValueError(f"UnitTables.addUnitName called for a unit with no name. Unit code = {theUnit.csCode_}.")

    def addUnitCode(self, theUnit):
        uCode = theUnit["csCode_"]

        if uCode:

            if uCode in self.unitCodes_:
                raise Exception(f"UnitTables.addUnitCode called, already contains entry for unit with code = {uCode}")
            else:
                self.unitCodes_[uCode] = theUnit
                self.codeOrder_.append(uCode)

                if uCode == 'g':
                    dimVec = theUnit["dim_"]["dimVec_"]
                    d = 0
                    for d in range(len(dimVec)):
                        if dimVec[d] >= 1:
                            break
                    self.massDimIndex_ = d
        else:
            raise ValueError(f"UnitTables.addUnitCode called for unit that has no code.")

    def addUnitString(self, theUnit):
        uString = theUnit["csUnitString_"]

        if uString:
            uEntry = {'mag': theUnit["baseFactorStr_"], 'unit': theUnit}
            try:
                if self.unitStrings_[uString]:
                    tempList = [self.unitStrings_[uString]].append(uEntry)
                    self.unitStrings_[uString] = tempList
            except KeyError:
                self.unitStrings_[uString] = uEntry

    def addUnitDimension(self, theUnit):  #todo rework since it is trying to make a key with a list
        uDim = theUnit["dim_"]["dimVec_"]

        if uDim:
            if self.unitDimensions_[uDim]:
                self.unitDimensions_[uDim].append(theUnit)
            else:
                self.unitDimensions_[uDim] = theUnit
        else:
            raise ValueError(f"UnitTables.addUnitDimension called for a unit with no dimension. Unit code = {theUnit.csCode_}.")

    def buildUnitSynonyms(self):

        for code in self.unitCodes_:
            theUnit = self.unitCodes_[code]
            uSyns = theUnit.synonyms_

            if uSyns:
                synsAry = uSyns.split(';')
                if synsAry[0] != '':
                    for a in range(len(synsAry)):
                        theSyn =synsAry[a].strip()
                        self.addSynonymCodes(code, theSyn)
            self.addSynonymCodes(code, theUnit.name_)

    def addSynonymCodes(self, theCode, theSynonyms):
        words = theSynonyms.split(' ')

        for w in range(len(words)):
            word = words[w]

            if self.unitSynonyms_[word]:
                synCodes = self.unitSynonyms_[word]
                if synCodes.find(theCode) == -1:
                    self.unitSynonyms_[word].append(theCode)
            else:
                self.unitSynonyms_[word] = theCode

    def getUnitByCode(self, uCode:str):
        retUnit = None
        if uCode:
            retUnit = self.unitCodes_[uCode]

        return retUnit

    def getUnitByName(self, uName:str):
        if uName == None:
            raise ValueError('Unable to find unit by name because no name was provided.')

        sepPos = uName.find(UCUM['codeSep_'])
        uCode = None
        if sepPos >= 1:
            uCode = uName[sepPos+len(UCUM['codeSep_'])]
            uName = uName[0, sepPos]
        retUnits = self.unitNames_[uName]
        if retUnits:
            uLen = len(retUnits)
            if uCode and uLen > 1:
                i = 0
                for i in range(uLen) and retUnits[i]['csCode_'] != uCode:
                    pass
                if i < uLen:
                    retUnits = retUnits[i]
                else:
                    retUnits = None
        return retUnits

    def getUnitByString(self, uString:str = None):
        retAry = None
        if uString:
            retAry = self.unitStrings_[uString]
            if retAry == None:
                pass
        return retAry

    def getUnitsByDimension(self, uDim):
        unitsArray = None

        if uDim == None:
            raise ValueError('Unable to find unit by because no dimension vector was provided.')

        unitsArray = self.unitDimensions_[uDim]

        if unitsArray == None:
            print(f"Unable to find unit with dimension = {uDim}")

        return unitsArray

    def getUnitBySynonym(self, uSyn):
        retObj = {}
        unitsArray = []
        try:
            if uSyn == None:
                retObj['status'] = 'error'
                raise ValueError("Unable to find unit by synonym because no synonym was provided.")
            if len(self.unitSynonyms_.keys()) == 0:
                self.buildUnitSynonyms()

            foundCodes = []
            foundCodes = self.unitSynonyms_[uSyn]
            if foundCodes:
                retObj['status'] = 'succeeded'
                fLen = len(foundCodes)
                for f in range(fLen):
                    unitsArray.append(self.unitCodes_[foundCodes[f]])
                retObj['units'] = unitsArray

            if len(unitsArray) == 0:
                retObj['status'] = 'failed'
                retObj['msg'] = f'Unable tp find any units with synonym {uSyn}'

        except Exception as e:
            retObj['msg'] = repr(e)
        return retObj

    def getAllUnitNames(self):
        return self.unitNames_.keys()

    def getMassDimensionsIndex(self):
        return self.massDimIndex_

    def compareCode(self,  a, b):#todo check js add regex check if even needed
        a = a.replace('[\[\]]', '')
        a = a.upper()
        b = b.replace('[\[\]]', '')
        b = b.lower()
        return -1 if a < b else 1

    def getAllUnitCodes(self):
        return self.unitCodes_.keys()

    def allUnitsByDef(self):#todo check if needed
        unitsList = []
        uLen = len(self.codeOrder_)
        for u in range(uLen):
            unitsList.append(self.getUnitByCode(self.codeOrder_[u]))
        return unitsList

    def allUnitsByName(self, cols, sep):
        if sep == None:
            sep = '|'
        unitBuff = ''
        unitsList = self.getAllUnitNames()
        uLen = len(unitsList)
        cLen = len(cols)
        for i in range(uLen):
            nameRecs = self.getUnitByName(unitsList[i])
            for u in range(len(nameRecs)):
                rec = nameRecs[u]
                for c in range(cLen):
                    if c > 0:
                        unitBuff += sep
                    if cols[c] == 'dim_':
                        if rec['dim_'] != None and type(rec['dim']['dimVec_']) is list:
                            unitBuff += '[' + rec['dim']['dimVec_'].join(',') + ']'
                        else:
                            unitBuff += ''
                    else:
                        cbuf = rec[cols[c]]
                        if type(cbuf) is str:
                            unitBuff += cbuf.replace('[\n\r]', ' ')
                        else:
                            unitBuff += cbuf
                unitBuff += '\r\n'
        return unitBuff

    def printUnits(self, sep:str = None, doLong: bool = None):
        if doLong == None:
            doLong == False
        if sep == None:
            sep = '|'

        codeList = ''
        uLen = len(self.codeOrder_)
        unitString = 'csCode' + sep

        if doLong:
            unitString += 'ciCode' + sep

        unitString += 'name' + sep

        if doLong:
            unitString += 'isBase' + sep

        unitString += 'magnitude' + sep + 'dimension' + sep + 'from unit(s)' + sep + 'value' + sep + 'function' + sep

        if doLong:
            unitString += 'property' + sep + 'printSymbol' + sep + 'synonyms' + sep + 'source' + sep + 'class' + sep + \
                          'isMetric' + sep + 'variable' + sep + 'isSpecial' + sep + 'isAbitrary' + sep

        unitString += 'comment'
        codeList = unitString + '\n'

        for u in range(uLen):
            curUnit = self.getUnitByCode(self.codeOrder_[u])
            unitString = self.codeOrder_[u] + sep
            if doLong:
                unitString += curUnit.ciCode_ + sep
            unitString+= curUnit.name_ + sep
            if doLong:
                if curUnit.isBase_:
                    unitString += 'true' + sep
                else:
                    unitString += 'false' + sep
            unitString += curUnit.magnitude_ + sep
            curDim = curUnit.dim_
            if curDim:
                unitString += curDim.dimVec_ + sep
            else:
                unitString += 'null' + sep
            if curUnit.csUnitString_:
                unitString += curUnit.csUnitString_ + sep +curUnit.baseFactor_ + sep
            else:
                unitString += 'null' + sep + 'null' +sep

            if curUnit.cnv_:
                unitString += curUnit.cnv_ + sep
            else:
                unitString += 'null' + sep

            if doLong:
                unitString += curUnit.property_ + sep + curUnit.printSymbol_ + sep + curUnit.synonyms_ + sep + \
                    curUnit.source_ + sep + curUnit.class_ + sep + curUnit.isMetric_ + sep + curUnit.gvariable_ + \
                    sep + curUnit.isSpecial_ + sep + curUnit.gisArbitrary_ + sep

            if curUnit.defError_:
                unitString += 'problem parsing this one, deferred to later.'
            codeList += unitString + '\n'

            return codeList

unitTablesInstance = UnitTablesFactory()

def UnitTables():
    return unitTablesInstance