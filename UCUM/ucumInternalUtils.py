from UCUM.unitTables import UnitTables

def isNumericString(theString: str) -> bool:
    num = "" + theString
    return num is not None and float(num) is not None

def isIntegerUnit(theString: str) -> bool :
    try:
        return type(int(theString)) is int
    except TypeError:
        return False

def getSynonyms( theSyn:str) -> dict:
    retObj = {}
    utab = UnitTables()
    resp = {}
    resp = utab.getUnitBySynonym(theSyn)

    if not resp['units']:
        retObj['status'] = resp['status']
        retObj['msg]'] = resp['msg']
    else:
        retObj['status'] = 'succeeded'
        retObj['units'] = []
        for a in range(len(resp['units'])):
            theUnit = resp['units'][a]
            retObj['units'][a] = {
                'code':theUnit.csCode_,
                'name':theUnit.name_,
                'guidance':theUnit.guidance_
            }
    return retObj