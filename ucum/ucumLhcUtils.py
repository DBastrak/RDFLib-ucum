from ucum.ucum_config import UCUM
from ucum.unitTables import unitTablesInstance
from ucum.unitString import UnitStringInstance
from ucum.ucumInternalUtils import *
from ucum.ucumJsonDefs import loadJson
from ucum.unit import Unit

class ucumLhcUtils:

    def __init__(self):
        if unitTablesInstance.unitsCount() == 0:
            loadJson()
        self.uStrParser_ = UnitStringInstance()

    def useBraceMsgForEachString(self, use:bool = None):
        if use == None:
            use = True
        self.uStrParser_.useBraceMsgForEachString(use)

    def validateUnitString(self, uStr, suggest:bool = False, valConv: str = 'validate') ->dict:

        resp = self.getSpecifiedUnit(uStr, valConv, suggest)
        theUnit = resp['unit']
        retObj = {}
        if not theUnit:
            retObj = {'status': 'error' if not resp['origString'] or resp['origString'] == None else 'invalid',
                      'ucumCode': None}

        else:
            retObj = {'status': 'valid' if resp['origString'] == uStr else 'invalid', 'ucumCode': resp['origString'],
                      'unit' : {'code': theUnit["csCode_"], 'name_': theUnit["name_"], 'guidance': theUnit["guidance_"]}}

        try:
            retObj['suggestions'] = resp['suggestions']
        except KeyError:
            pass

        retObj['msg'] = resp['retMsg']
        return retObj

    def convertUnitTo(self, fromVal, fromUnitCode:str = '', toUnitCode: str = '', suggest:bool = False, molecularWeight = False)-> dict:
        retObj = {'status': 'failed', 'toVal': None, 'msg' : []}

        if fromUnitCode:
            fromUnitCode = fromUnitCode.strip()

        if not fromUnitCode or fromUnitCode == '':
            retObj['status'] = 'error'
            retObj['msg'].append('No "from" value, or an invalid "from" value, was specified.')

        if toUnitCode:
            toUnitCode = toUnitCode.strip()

        if not toUnitCode or toUnitCode == '':
            retObj['status'] = 'error'
            retObj['msg'].append('No "to" value, or an invalid "to" value, was specified.')

        if retObj['status'] != 'error':
            try:
                fromUnit = unitTablesInstance.getUnitByCode(fromUnitCode)
                fromUnit = Unit(fromUnit)
                parseResp = self.getSpecifiedUnit(fromUnitCode, 'convert', suggest)
                #fromUnit = parseResp['unit']

                if 'retMsg' in parseResp:
                    retObj['msg'] = retObj['msg'].append(parseResp['retMsg'])

                if 'suggestions' in parseResp:
                    retObj['suggestions'] = {}
                    retObj['suggestions']['from'] = parseResp['suggestions']

                if not fromUnit:
                    retObj['msg'].append(f"Unable to find a unit for {fromUnitCode}, "
                                         f"so no conversion could be performed.")

                toUnit = unitTablesInstance.getUnitByCode(toUnitCode)
                toUnit = Unit(toUnit)
                parseResp = self.getSpecifiedUnit(toUnitCode, 'convert', suggest)
                #toUnit = parseResp['unit']
                if parseResp['retMsg']:
                    retObj['msg'] = retObj['msg'].append(parseResp['retMsg'])
                if 'suggestions' in parseResp:
                    if not retObj['suggestions']:
                        retObj['suggestions'] = {}
                    retObj['suggestions']['to'] = parseResp['suggestions']

                if fromUnit and toUnit:
                    try:
                        if not molecularWeight:
                            retObj['toVal'] = toUnit.convertFrom(fromVal, fromUnit)
                        else:

                            if fromUnit.moleExp_ != 0 and toUnit.moleExp_ != 0:
                                raise TypeError('A molecular weight was specified but a mass <-> mole conversion '
                                                'cannot be executed for two mole-based units.'
                                                ' No conversion was attempted.')
                            if fromUnit.moleExp_ == 0 and toUnit.moleExp_ == 0:
                                raise TypeError('A molecular weight was specified but a mass <-> mole conversion '
                                                'cannot be executed when neither unit is mole-based. '
                                                'No conversion was attempted.')
                            if not fromUnit.isMoleMassCommensurable(toUnit):
                                raise TypeError(f'Sorry. {fromUnitCode} cannot be converted to {toUnitCode}.')

                            if fromUnit.moleExp_ != 0:
                                retObj['toVal'] = fromUnit.convertMolToMass(fromVal, toUnit, molecularWeight)
                            else:
                                retObj['toVal'] = fromUnit.convertMassToMol(fromVal, toUnit, molecularWeight)

                        retObj['status'] = 'succeeded'
                        retObj['fromUnit'] = fromUnit
                        retObj['toUnit'] = toUnit

                    except Exception as e:
                        retObj['status'] = 'failed'
                        retObj['msg'] = str(e)

            except Exception as e:
                if e == UCUM["needMoleWeightMsg_"]:
                    retObj['status'] = 'failed'
                else:
                    retObj['status'] = 'error';
                retObj['msg'].append(str(e))

        return retObj

    def checkSynonyms(self, theSyn:str = None)->dict:
        retObj = {}
        if theSyn == None:
            retObj['status'] = 'error'
            retObj['msg'] = 'No term specified for synonym search.'

        else:
            retObj = getSynonyms(theSyn)
        print(retObj)
        return retObj

    def getSpecifiedUnit(self, uName:str ,valConv: str , suggest:bool = False):
        retObj = {}
        retObj['retMsg'] = []

        if not uName:
            retObj['retMsg'].append("No unit string specified.")
        else:
            utab = unitTablesInstance
            uName = uName.strip()

            theUnit = utab.getUnitByCode(uName)

            if theUnit:
                retObj['unit'] = theUnit
                retObj['origString'] = uName
            else:
                try:
                    resp = self.uStrParser_.parseString(uName, valConv, suggest)
                    retObj['unit'] = resp[0]
                    retObj['origString'] = resp[1]
                    if resp[2]:
                        retObj['retMsg'] = resp[2]
                    retObj['suggestions'] = resp[3]
                except Exception as e:
                    print(f"Unit requested fro unit string {uName}. request unsuccessful; error throw = {str(e)}")
                    retObj['retMsg'].insert(0, f"{uName} is not a valid unit. {str(e)}")
        return retObj

    def getSpecifiedUnitByName(self, uName:str ,valConv: str , suggest:bool = False):
        retObj = {}
        retObj['retMsg'] = []

        if not uName:
            retObj['retMsg'].append("No unit string specified.")
        else:
            utab = unitTablesInstance
            uName = uName.strip()

            theUnit = utab.getUnitByName(uName)

            if theUnit:
                retObj['unit'] = theUnit
                retObj['origString'] = uName
            else:
                try:
                    resp = self.uStrParser_.parseString(uName, valConv, suggest)
                    retObj['unit'] = resp[0]
                    retObj['origString'] = resp[1]
                    if resp[2]:
                        retObj['retMsg'] = resp[2]
                    retObj['suggestions'] = resp[3]
                except Exception as e:
                    print(f"Unit requested fro unit string {uName}. request unsuccessful; error throw = {str(e)}")
                    retObj['retMsg'].insert(0, f"{uName} is not a valid unit. {str(e)}")
        return retObj

    def commensurablesList(self, fromName:str)->list:
        retMsg = []
        commUnits = None

        fromUnit = unitTablesInstance.getUnitByName(fromName)

        if not fromUnit:
            retMsg.append(f"Could not find unit {fromName}")
        else:
            fromDim = fromUnit['dim_']['dimVec_']

            if not fromDim:
                retMsg.append(f"No commensurable units were found for {fromName}")
            if fromDim:
                commUnits = unitTablesInstance.getUnitsByDimension(fromDim)
        return [commUnits, retMsg]
