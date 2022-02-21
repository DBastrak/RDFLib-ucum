from ucum.unitTables import UnitTables
from ucum.unit import Unit
from ucum.prefixTables import prefixTable
from ucum.ucum_config import UCUM

import ucum.ucumInternalUtils as uI
import math
import re

class UnitString:

    def __init__(self):
        self.utabs = UnitTables()
        self.pfxTabs_ = prefixTable()

        self.openEmph_ = UCUM["openEmph_"]
        self.closeEmph_ = UCUM["closeEmph_"]

        self.braceMsg_ = ''

        self.parensFlag_ = "parens_placeholder";
        self.pFlagLen_ = len(self.parensFlag_)
        self.braceFlag_ = "braces_placeholder";
        self.bFlagLen_ = len(self.braceFlag_)

        self.vcMsgStart_ = None
        self.vcMsgEnd_ = None

        self.retMsg_ = []
        self.parensUnits_ = []
        self.annotations_ = []
        self.suggestions_ = []


    def useBraceMsgForEachString(self, use:bool):
        if use == True:
            self.braceMsg_ = UCUM["bracesMsg_"]
        else:
            self.braceMsg_ = ''

    def parseString(self, uStr: str = None, valConv: str = "validate", suggest: bool = False) -> dict:
        uStr.strip()
        if uStr == None or uStr == '':
            raise ValueError("Please specify a unit expression to be validated.")
        if valConv == 'validate':
            self.vcMsgStart_ = UCUM["valMsgStart_"]
            self.vcMsgEnd_ =UCUM["valMsgEnd_"]
        else:
            self.vcMsgStart_ = UCUM["cnvMsgStart_"]
            self.vcMsgEnd_ = UCUM["cnvMsgEnd_"]

        if suggest == False:
            self.suggestions_ = None
        else:
            self.suggestions_ = []

        self.retMsg_ = []
        self.parensUnits_ = []
        self.annotations_ = []
        origString = uStr
        retObj = []

        uStr = self._getAnnotations(uStr)
        if len(self.retMsg_) > 0:
            retObj[0] = None
            retObj[1] = None
        else:
            endProcessing = len(self.retMsg_) > 0
            for sUnit in UCUM["specUnits_"]:
                while (uStr.find(sUnit) != -1):
                    uStr = uStr.replace(sUnit, UCUM["specUnits_"][sUnit])

            if uStr.find(' ') != -1:
                raise ValueError("Blank spaces are not allowed in unit expressions.")

            retObj = self._parseTheString(uStr, origString)
            finalUnit = retObj[0]
            if type(finalUnit) is int or type(finalUnit) is float:
                finalUnit = Unit({
                    'csCode_': origString,
                    'magnitude_': finalUnit,
                    'name_': origString
                })
                retObj[0] = finalUnit
        print(retObj)
        retObj.append(self.retMsg_)
        if self.suggestions_ and len(self.suggestions_) > 0:
            retObj[3] = self.suggestions_
        return retObj

    def _parseTheString(self, uStr:str, origString:str) -> list:
        finalUnit = None


        parensResp = self._processParens(uStr, origString)
        endProcessing = parensResp[2]

        uArray = []
        if not(endProcessing):
            uStr = parensResp[0]
            origString = parensResp[1]
            mkUArray = self._makeUnitsArray(uStr, origString)

            endProcessing = mkUArray[2]
            if not(endProcessing):
                uArray = mkUArray[0]
                origString = mkUArray[1]
                uLen = len(uArray)

                for u1 in range(uLen):
                    curCode = uArray[u1]['un']

                    if type(curCode) is int or type(curCode) is float:
                        pass
                    else:
                        if curCode.find(self.parensFlag_) >= 0:
                            parenUnit = self._getParensUnit(curCode, origString)
                            if not(endProcessing):
                                uArray[u1]['un'] = parenUnit[0]

                        else:
                            uRet = self._makeUnit(curCode, origString)

                            if uRet[0] == None:
                                endProcessing = True
                            else:
                                uArray[u1]['un'] = uRet[0]
                                origString = uRet[1]
        if not(endProcessing):
            if (uArray[0] == None or uArray[0] == ' ' or uArray[0]['un'] == None) and len(self.retMsg_) == 0:
                self.retMsg_.append(f"Unit string ({origString}) did not contain anything that could be used to "
                                    f"create a unit, or else it is something that is not handled yet by this package. Sorry")
                endProcessing = True

        if not (endProcessing):
            finalUnit =self._performUnitArithmetic(uArray, origString)

        return [finalUnit, origString]

    def _getAnnotations(self, uString) -> str:
        openBrace = uString.find("{")
        while (openBrace >= 0):
            closeBrace = uString.find("}")
            if closeBrace < 0:
                self.retMsg_.append("Missing closing brace for annotation starting at "+self.openEmph_+
                                    uString[openBrace:] +self.closeEmph_)
                openBrace = -1
            else:
                braceStr = uString[openBrace, closeBrace+1]
                aIdx = str(len(self.annotations_))
                uString = uString.replace(braceStr, self.braceFlag_+aIdx+self.braceFlag_)
                self.annotations_.append(braceStr)
                openBrace = uString.find('{')
        closeBrace = uString.find('}')
        if closeBrace >= 0:
            self.retMsg_.append('Missing opening brace for closing brace found at '+ self.openEmph_ +
                                uString.substring(0, closeBrace + 1) + self.closeEmph_)
        return uString


    def _processParens(self, uString:str, origString:str) -> list:
        uStrArray = []
        uStrAryPos = 0
        stopProcessing = False

        pu = len(self.parensUnits_)

        trimmedCt = 0

        while uString != "" and not stopProcessing:
            openCt =  0
            closeCt = 0
            openPos = int(uString.find('('))

            if openPos < 0:
                closePos = uString.find(')')
                if closePos >=0:
                    theMsg = f"Missing open parenthesis for close parenthesis at {uString[0, closePos+trimmedCt]}" \
                             f"{self.openEmph_}{uString[closePos, 1]}{self.closeEmph_}"
                    if (closePos < len(uString) - 1 ):
                        theMsg += f"{uString[closePos+1]}"
                    self.retMsg_.append(theMsg)
                    uStrArray[uStrAryPos] = uString
                    stopProcessing = True

                else:
                    openCt += 1
                    uLen =len(uString)
                    if openPos > 0:
                        uStrArray[uStrAryPos+1] = uString[0, openPos]

                    closePos = 0
                    c = openPos + 1
                    for c in range(uLen):
                        if openCt == closeCt:
                            break
                        if uString[c] == '(':
                            openCt += 1
                        elif uString[c] == ')':
                            closeCt += 1

                    if openCt == closePos:
                        closePos = c
                        uStrArray[uStrAryPos] = self.parensFlag_ + str(pu) +self.parensFlag_
                        parseResp = self._parseTheString(uString[openPos+1, closePos-1], origString)
                        if parseResp[0] == None:
                            stopProcessing = True
                        else:
                            origString = parseResp[1]
                            self.parensUnits_[pu+1] = parseResp[0]
                            uString = uString[closePos]
                            trimmedCt = closePos

                    else:
                        uStrArray.append(origString[openPos])
                        self.retMsg_.append(f"Missing close parenthesis for open parenthesis at "
                                            f"{origString[0: openPos + trimmedCt]}"
                                            f"{self.openEmph_}{origString[openPos: 1]}"
                                            f"{self.closeEmph_}{origString[openPos + 1]}")
                        stopProcessing = True
        if stopProcessing:
            self.parensUnits_ = []
        return [''.join(uStrArray), origString, stopProcessing]

    def _makeUnitsArray(self, uStr:str, origString:str) -> list:

        uArray1 = re.search("/([./]|[^./]+)/g", uStr) #regex
        endProcessing = False
        uArray = []
        startNumCheck = "/(^[0-9]+)(\[?[a-zA-Z\_0-9a-zA-Z\_]+\]?$)/" #regex

        if uArray1[0] == "/":
            uArray1.insert(0, "1")

        elif uArray1[0] == ".":
            self.retMsg_.append(f"{origString} is not a valid UCUM code. The multiplication operator at the beginning"
                                f" of the expression is not valid. A multiplication operator must appear only "
                                f"between two codes.")
            endProcessing = True

        if not endProcessing:
            if not uI.isNumericString(uArray1[0]):
                numRes = re.search(startNumCheck, uArray[0])
                if numRes and len(numRes) == 3 and numRes[1] != '' and numRes[2] != '' and \
                    numRes[2].find(self.braceFlag_) != 0:
                    dispVal = numRes[2]

                    if not endProcessing and numRes[2].find(self.parensFlag_) != -1:
                        parensback = self._getParensUnit(numRes[2], origString)
                        numRes[2] = parensback[0]['csCode_']
                        dispVal = f"({numRes[2]})"
                        endProcessing = parensback[1]
                    if not endProcessing:
                        self.retMsg_.append(f"{numRes[1]}{dispVal} is not a valid UCUM code. {self.vcMsgStart_}"
                                            f"{numRes[1]}.{dispVal}{self.vcMsgEnd_}")
                        origString = origString.replace(f"{numRes[1]}{dispVal}",f"{numRes[1]}.{dispVal}")
                        uArray1[0] = numRes[2]
                        uArray1.insert(0, numRes[1]).insert(0, '.')

        if not endProcessing:
            u1 = len(uArray1)
            uArray = [{"op" : "", "un": uArray1[0]}]
            n = 1
            for n in range(u1):
                theOp = uArray1[n+1]

                if not uArray1[n]:
                    self.retMsg_.append(f"{origString} is not a valid UCUM code. It is terminated with the "
                                        f"operator {self.openEmph_}{theOp}{self.closeEmph_}.")
                    n = u1
                    endProcessing = True
                elif UCUM["validOps_"].find(uArray1[n]) != -1:
                    self.retMsg_.append(f"{origString} is not a valid UCUM code. A unit code is missing"
                                        f" between{self.openEmph_}{theOp}{self.closeEmph_}and{self.openEmph_}"
                                        f"{uArray1[n]}{self.closeEmph_}in{self.openEmph_}{theOp}"
                                        f"{uArray1[n]}{self.closeEmph_}.")
                    n = u1
                    endProcessing = True

                else:
                    if not uI.isNumericString(uArray1[n]):
                        numRes2 = re.search(startNumCheck, uArray1[n])
                        if numRes2 and len(numRes2) == 2 and numRes2[1] != '' \
                            and numRes2[2] != '' and numRes2.find(self.braceFlag_) != 0:
                            invalidString = numRes2[0]

                            if not endProcessing and numRes2[2].find(self.parensFlag_) != -1:
                                parensback = self._getParensUnit(numRes2[2], origString)
                                numRes2[2] = parensback[0]['csCode_']
                                invalidString = f"{numRes2[2]}"
                                endProcessing = parensback[1]

                                if not endProcessing:
                                    self.retMsg_.appned(f"{numRes2[1]}{invalidString} is not a valid UCUM code. "
                                                        f"{self.vcMsgStart_}{numRes2[1]}.{invalidString}{self.vcMsgEnd_}")
                                    parensString = f"({numRes2[1]}.{invalidString})"
                                    origString = origString.replace(f"{numRes2[1]}{invalidString}", parensString)
                                    nextParens = self._processParens(parensString, origString)
                                    endProcessing = nextParens[2]

                                    if not endProcessing:
                                        uArray.append({"op": theOp, "un":nextParens[0]})
                            else:
                                parensStr = '(' + numRes2[1] + '.' + numRes2[2] + ')'
                                parensResp = self._processParens(parensStr, origString)

                                if parensResp[2]:
                                    n = u1
                                    endProcessing = True
                                else:
                                    self.retMsg_.append(f"{numRes2[0]} is not a valid UCUM code. "
                                                        f"{self.vcMsgStart_}{numRes2[1]}.{numRes2[2]}{self.vcMsgEnd_}")
                                    origString = origString.replace(numRes2[0], parensStr)
                                    uArray.append({"op": theOp, "un":parensResp[0]})
                        else:
                            uArray.append({"op": theOp, "un":uArray[n]})
                    else:
                        uArray.append({"op": theOp, "un": uArray[n]})
        return [uArray, origString, endProcessing]

    def _getParensUnit(self, pStr:str, origString:str)->list:
        endProcessing = False
        retAry = []
        retUnit = None
        befAnnoText = None
        aftAnnoText = None

        psIdx = pStr.find(self.parensFlag_)
        befText = None
        if psIdx > 0:
            befText = pStr[0, psIdx-1]

        peIdx = max(index for index, item in enumerate(pStr) if item == self.parensFlag_) #finding index of final instance
        aftText = None

        if peIdx + self.pFlagLen_ < len(pStr):
            aftText = pStr[peIdx + self.pFlagLen_]

        pNumText = pStr[psIdx + self.pFlagLen_, peIdx]

        if uI.isNumericString(pNumText):
            retUnit = self.parensUnits_[float(pNumText)]
            if not uI.isIntegerUnit(retUnit):
                pStr = retUnit.csCode_ #todo
            else:
                pStr = retUnit

        else:
            raise ValueError(f"Processing error - invalid parens number {pNumText} found in {pStr}.")

        if befText:
            if uI.isNumericString(befText):
                nMag = retUnit.getProperty('magnitude_')
                nMag *= float(befText)
                retUnit.assignVals({"magnitude_":nMag})
                pStr = f"{befText}.{pStr}"
                self.retMsg_.append(f"{befText}{pStr} is not a valid UCUM code.\n{self.vcMsgStart_}"
                                    f"{pStr}{self.vcMsgEnd_}")
            else:
                if befText.find(self.braceFlag_) >= 0:
                    annoRet = self._getAnnoText(befText, origString)
                    try: #todo rework this
                        if annoRet[1] or annoRet[2]:
                            raise ValueError(f"Text found before the parentheses ({befText}) included an annotation"
                                  f" along with other text for parenthetical unit {retUnit.csCode_}")
                    except IndexError:
                        print(f"Text found before the parentheses ({befText}) included an annotation"
                              f" along with other text for parenthetical unit {retUnit.csCode_}")
                    pStr += annoRet[0]
                    self.retMsg_.append(f"The annotation {annoRet[0]} before the unit code is invalid.\n "
                                        f"{self.vcMsgStart_}{pStr}{self.vcMsgEnd_}")

                elif not self.suggestions_:
                    self.retMsg_.append(f"{befText} preceding the unit code {pStr} is invalid."
                                        f" Unable to make a substitution.")
                    endProcessing = True

                else:
                    suggestStat = self._getSuggestions(befText)
                    endProcessing = (suggestStat != 'succeeded')
        if aftText:
            if aftText.find(self.braceFlag_) >= 0:
                annoRet = self._getAnnoText(aftText, origString)

                try:  # todo rework this
                    if annoRet[1] or annoRet[2]:
                        raise ValueError(f"Text found before the parentheses ({aftText}) included an annotation"
                                         f" along with other text for parenthetical unit {retUnit.csCode_}")
                except IndexError:
                    print(f"Text found before the parentheses ({aftText}) included an annotation"
                          f" along with other text for parenthetical unit {retUnit.csCode_}")
                pStr += annoRet[0]

            else:
                if uI.isNumericString(aftText):
                    pStr += aftText
                    retUnit = retUnit.power(float(aftText))
                    self.retMsg_.append(f"An exponent ({aftText}) following a parenthesis is "
                                        f"invalid as of revision 1.9 of the UCUM Specification.\n"
                                        f"{self.vcMsgStart_}{pStr}{self.vcMsgEnd_}")
                elif not self.suggestions_:
                    self.retMsg_.append(f"Text {aftText} following the unit code {pStr} "
                                        f"is invalid.  Unable to make a substitution.")
                    endProcessing = True

                else:
                    suggestStat = self._getSuggestions(befText)
                    endProcessing = (suggestStat != 'succeeded')
        if not endProcessing:
            if not retUnit:
                retUnit = Unit({'csCode_': pStr, 'magnitude_': 1, 'name_': pStr})
            elif uI.isIntegerUnit(retUnit):
                retUnit = Unit({'csCode_': retUnit, 'magnitude_': retUnit, 'name_': retUnit})
            else:
                retUnit.csCode_ = pStr

        return [retUnit, endProcessing]

    def _getAnnoText(self, pStr: str, origString: str)-> str:
        asIdx = pStr.find(self.braceFlag_)
        startText = pStr[0, asIdx] if asIdx > 0 else None
        if asIdx != 0:
            pStr = pStr[asIdx]

        aeIdx = pStr[pStr.find(self.braceFlag_):]
        endText = f"{aeIdx}{self.bFlagLen_}" if len(f"{aeIdx}{self.bFlagLen_}") < len(pStr) else None

        idx = pStr[self.bFlagLen_: aeIdx]
        try:
            idxNum = float(idx)
            if idxNum >= len(self.annotations_):
                raise ValueError(f"Processing Error - invalid annotation index {idx} found "
                                 f"in {pStr} that was created from {origString}")
        except ValueError:
            print(f"Processing Error - invalid annotation index {idx} found in {pStr} that was created from {origString}")

        pStr = self.annotations_[idxNum]
        return [pStr, startText, endText]

    def _getSuggestions(self, pStr:str)->str:
        retObj = uI.getSynonyms(pStr)
        if retObj['status'] == 'succeeded':
            suggSet = {}
            suggSet['msg'] = f"{pStr} is not a valid UCUM code.  We found possible units that might be what was meant:"
            suggSet['invalidUnit'] = pStr
            synLen = len(retObj['units'])
            suggSet['units'] = []
            for s in range(synLen):
                unit = retObj['units'][s]
                unitArray = [unit['code'], unit['name'], unit['guidance']]
                suggSet['units'].append(unitArray)
            self.suggestions_.append(suggSet)

        else:
            self.retMsg_.append(f"{pStr} is not a valid UCUM code. No alternatives were found.")
        return retObj['status']

    def _makeUnit(self, uCode:str, origString:str)->list:
        retUnit = self.utabs.getUnitByCode(uCode)
        if retUnit:
            retUnit = retUnit.clone()
        elif uCode.find(self.braceFlag_) >= 0:
            getAnnoRet = self._getUnitWithAnnotation(uCode, origString)
            retUnit = getAnnoRet[0]
            if retUnit:
                origString = getAnnoRet[1]
            else:
                if uCode.find('^') > -1:
                    tryCode = uCode.replace('^','*')
                    retUnit = self.utabs.getUnitByCode(tryCode)
                    if retUnit:
                        retUnit = retUnit.clone()
                        retUnit.csCode_ = retUnit.csCode_.replace('*', '^')
                        retUnit.ciCode_ = retUnit.ciCode_.replace('*', '^')

                if not retUnit:
                    addBrackets = f'[{uCode}]'
                    retUnit = self.utabs.getUnitByCode(addBrackets)
                    if retUnit:
                        retUnit = retUnit.clone()
                        origString = origString.replace(uCode, addBrackets)
                        self.retMsg_.append(f"{uCode} is not a valid unit expression, but {addBrackets} is.\n"
                                            f"{self.vcMsgStart_}{addBrackets} ({retUnit.name_}){self.vcMsgEnd_}")

                if not retUnit:
                    retUnitAry = self.utabs.getUnitByName(uCode)
                    if retUnitAry and len(retUnitAry) > 0:
                        retUnit = retUnitAry[0].clone()
                        mString =f"The UCUM code for {uCode} is {retUnit.csCode_}.\n{self.vcMsgStart_}" \
                                 f"{retUnit.csCode_}{self.vcMsgEnd_}"
                        dupMsg = False
                        for r in range(len(self.retMsg_)) and not dupMsg:
                            dupMsg = self.retMsg_[r] == mString
                        if not dupMsg:
                            self.retMsg_.append(mString)
                        rStr = '(^|[.\/({])(' + uCode + ')($|[.\/)}])'
                        res = re.findall(origString, rStr)
                        origString = origString.replace(rStr, res[1]+retUnit.csCode_+res[3])
                        uCode = retUnit.csCode_

                if not retUnit:
                    sUnit = None
                    for sUnit in UCUM["specUnits_"]:
                        if uCode.find(UCUM['specUnits_'][sUnit]) != -1:
                            uCode = uCode.replace(UCUM['specUnits_'][sUnit], sUnit)
                    retUnit = self.utabs.getUnitByCode(uCode)
                    if retUnit:
                        retUnit = retUnit.clone()
                if not retUnit:
                    origCode = uCode
                    origUnit = None
                    exp = None
                    pfxCode = None
                    pfxObj = None
                    pfxVal = None
                    pfxExp = None

                    codeAndExp = self.isCodeWithExponent(uCode)
                    if codeAndExp:
                        uCode = codeAndExp[0]
                        exp = codeAndExp[1]
                        origUnit = self.utabs.getUnitByCode(uCode)

                    if not origUnit:
                        pfxCode = uCode[0]
                        pfxObj = self.pfxTabs_.getPrefixByCode(pfxCode)

                        if pfxObj:
                            pfxVal = pfxObj.getValue()
                            pfxExp = pfxObj.getExp()
                            pCodeLen = len(pfxCode)
                            uCode = uCode[pCodeLen:]

                            origUnit = self.utabs.getUnitByCode(uCode)

                            if not origUnit and pfxCode == 'd' and uCode[0, 1] == 'a':
                                pfxCode = 'da'
                                pfxObj = self.pfxTabs_.getPrefixByCode(pfxCode)
                                pfxVal = pfxObj.getValue()
                                uCode = uCode[1:]
                                origUnit = self.utabs.getUnitByCode(uCode)

                    if not origUnit:
                        retUnit = None
                        if self.suggestions_:
                            suggestStat = self._getSuggestions(origCode)
                        else:
                            self.retMsg_.append(f"{origCode} is not a valid UCUM code.")
                    else:
                        retUnit = origUnit.clone()
                        retUnit.guidance_ = ''
                        theDim = retUnit.getProperty('dim_')
                        theMag = retUnit.getProperty('magnitude_')
                        theName = retUnit.getProperty('name_')
                        theCiCode = retUnit.getProperty('ciCode_')
                        thePrintSymbol = retUnit.getProperty('printSymbol_')

                        if exp:
                            exp = int(exp)
                            expMul = exp
                            if theDim:
                                theDim = theDim.mul(exp)
                            theMag = math.pow(theMag, exp)
                            retUnit.assignVals({'magnitude_': theMag})

                            if pfxObj:
                                if pfxExp:
                                    expMul *= pfxObj.getExp()
                                    pfxVal = math.pow(10, expMul)
                        if pfxObj:
                            if retUnit.cnv_:
                                retUnit.assignVals({'cnvPfx_': pfxVal})
                            else:
                                theMag *= pfxVal
                                retUnit.assignVals({'magnitude_': theMag})
                        theCode = retUnit.csCode_
                        if pfxObj:
                            theName = pfxObj.getName() + theName
                            theCode = pfxCode + theCode
                            theCiCode = pfxObj.getCiCode() + theCiCode
                            thePrintSymbol = pfxObj.getPrintSymbol() + thePrintSymbol
                            retUnit.assignVals({'name_': theName, 'csCode_': theCode,
                                'ciCode_': theCiCode, 'printSymbol_': thePrintSymbol})

                        if exp:
                            expStr = str(exp)
                            retUnit.assignVals({'name_': theName + '<sup>' + expStr + '</sup>',
                                  'csCode_': theCode + expStr, 'ciCode_': theCiCode + expStr,
                                  'printSymbol_': thePrintSymbol + '<sup>' + expStr + '</sup>'})
        return [retUnit, origString]

    def _getUnitWithAnnotation(self, uCode:str, origString:str)->list:
        retUnit = None
        annoRet = self._getAnnoText(uCode, origString)
        annoText = annoRet[0]
        befAnnoText = annoRet[1]
        aftAnnoText = annoRet[2]

        if self.braceMsg_ and self.retMsg_.find(self.braceMsg_) == -1:
            self.retMsg_.append(self.braceMsg_)
            
        msgLen = len(self.retMsg_)

        if not befAnnoText and not aftAnnoText:
            tryBrackets = '[' + annoText[1, len(annoText)-1] + ']'
            mkUnitRet = self._makeUnit(tryBrackets, origString)

            if mkUnitRet[0]:
                retUnit = mkUnitRet[0]
                self.retMsg_.append(f"{annoText} is not a valid unit expression, but {tryBrackets} is.\n"
                                    f"{self.vcMsgStart_}{tryBrackets} ({retUnit.name_})${self.vcMsgEnd_}")
            else:
                if len(self.retMsg_) > msgLen:
                    self.retMsg_.pop()
                uCode = 1
                retUnit = 1

        else:
            if befAnnoText and not aftAnnoText:
                if uI.isIntegerUnit(befAnnoText):
                    retUnit = befAnnoText
                else:
                    mkUnitRet = self._makeUnit(befAnnoText, origString)

                    if mkUnitRet[0]:
                        retUnit = mkUnitRet[0]
                        retUnit.csCode_ += annoText
                        origString = mkUnitRet[1]

                    else:
                        self.retMsg_.append(f"Unable to find a unit for ${befAnnoText} that "
                                            f"precedes the annotation {annoText}.")

            elif not befAnnoText and aftAnnoText:
                if uI.isIntegerUnit(aftAnnoText):

                    retUnit = aftAnnoText
                    self.retMsg_.append(f"The annotation {annoText} before the {aftAnnoText} is invalid.\n"
                                        f"t{self.vcMsgStart_}{retUnit}{self.vcMsgEnd_}")

                else:
                    mkUnitRet = self._makeUnit(aftAnnoText, origString)

                    if mkUnitRet[0]:
                        retUnit = mkUnitRet[0]
                        retUnit.csCode_ += annoText
                        origString = retUnit.csCode_
                        self.retMsg_.append(f"The annotation {annoText} before the unit code is invalid.\n"
                                            f"{self.vcMsgStart_}{retUnit.csCode_}{self.vcMsgEnd_}")


                    else:
                        self.retMsg_.append(f"Unable to find a unit for {befAnnoText} that "
                                            f"follows the annotation {annoText}.")

            else:
                self.retMsg_.append(f"Unable to find a unit for {befAnnoText}{annoText}{aftAnnoText}. \n"
                                    f"We are not sure how to interpret text both before and after the annotation.")

        return [retUnit, origString]

    def _performUnitArithmetic(self, uArray, origString):
        finalUnit = uArray[0]['un']
        if uI.isIntegerUnit(finalUnit):
            finalUnit = Unit({'csCode_':finalUnit, "magnitude_":float(finalUnit), "name_": finalUnit})

        uLen = len(uArray)
        endProcessing = False

        u2 =1
        for u2 in range(uLen) and not endProcessing:

            nextUnit = uArray[u2]['un']

            if uI.isIntegerUnit(nextUnit):
                nextUnit = Unit({'csCode_': nextUnit, "magnitude_": float(nextUnit), "name_": nextUnit})
            if nextUnit == None or type(nextUnit) is not float and not nextUnit.getProperty():
                msgString = f"Unit string ({origString}) contains unrecognized element"

                if nextUnit:
                    msgString += f" ({self.openEmph_}{str(nextUnit)}{self.closeEmph_}"

                msgString + "; could not parse full string. Sorry"
                self.retMsg_.append(msgString)
                endProcessing = True
            else:
                try:
                    thisOp = uArray[u2]['op']
                    isDiv = thisOp == '/'

                    finalUnit = finalUnit.divide(nextUnit) if  isDiv else finalUnit.multiplyThese(nextUnit)
                except Exception as err:
                    self.retMsg_.insert(0, err)
                    endProcessing = True
                    finalUnit = None

        return finalUnit

    def _isCodeWithExponent(self, uCode: str):
        ret = []
        res = re.findall("/(^[^\-\+]+?)([\-\+\d]+)$/", uCode)

        if res and res[2] and res[2] != "":
            ret.append(res[1])
            ret.append(res[2])
        else:
            ret = None
        return ret

def UnitStringInstance():
    return UnitString()

