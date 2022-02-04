from ucum.unitTables import UnitTables
import re

def isNumericString(theString: str = None) -> bool:
    num = "" + theString
    try:
        return num is not None and float(num) is not None
    except TypeError:
        return False

def isIntegerUnit(theString: str = None) -> bool :
    pattern = '^\d+$'
    try:
        return re.match(pattern, theString)[0]
    except TypeError:
        return None

def getSynonyms( theSyn:str) -> dict:
    retObj = {}
    utab = UnitTables()
    resp = utab.getUnitBySynonym(theSyn)
    print(resp)

    if "units" not in resp:
        retObj['status'] = resp['status']
        retObj['msg]'] = resp['msg']
    else:
        retObj['status'] = 'succeeded'
        retObj['units'] = []
        for a in range(len(resp['units'])):
            theUnit = resp['units'][a]
            retObj['units'][a] = {
                'code':theUnit["csCode_"],
                'name':theUnit["name_"],
                'guidance':theUnit["guidance_"]
            }
    return retObj