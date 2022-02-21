from ucum.prefix import prefix
from ucum.prefixTables import prefixTable
from ucum.unit import Unit
from ucum.unitTables import unitTablesInstance
import json

def loadJson():

    with open(r"G:\PythonProjects\RDFLib-ucum\data\ucumDefs.json", encoding="utf8") as jsonFile:
        jsonDefs = json.load(jsonFile)
        jsonPrefix = jsonDefs["prefixes"]
        jsonUnits = jsonDefs["units"]

    jsonPrefix = jsonPrefix['data']
    jsonUnits = jsonUnits['data']

    if unitTablesInstance.unitsCount() == 0:
        pTab = prefixTable()

        for x in jsonPrefix:
            tempDict = {"code_": x[0], "ciCode_": x[1], 'name_': x[2],
                        'printSymbol_': x[3], 'value_': x[4], 'exp_': x[5]}
            newPref = prefix(tempDict)
            pTab.add(newPref)

        unitTable = unitTablesInstance

        for unit in jsonUnits:
            tempUnitDict = {'isBase_': unit[0], 'name_': unit[1], 'csCode_': unit[2], 'ciCode_': unit[3],
                            'property_': unit[4], 'magnitude_': unit[5],
                            'dim_': {'dimVec_': unit[6]}, 'printSymbol_': unit[7], 'class_': unit[8], 'isMetric_': unit[9],
                            'variable_': unit[10], 'cnv_': unit[11], 'cnvPfx_': unit[12],
                            'isSpecial_': unit[13], 'isArbitrary_': unit[14], 'moleExp_': unit[15], 'synonyms_': unit[16],
                            'source_': unit[17], 'loincProperty_': unit[18], 'category_': unit[19],
                            'guidance_': unit[20], 'csUnitString_': unit[21], 'ciUnitString_': unit[22],
                            'baseFactorStr_': unit[23], 'baseFactor_': unit[24], 'defError_': unit[25]}
            unitTable.addUnit(tempUnitDict)






if __name__ == "__main__":
    loadJson()
    print(unitTablesInstance.unitCodes_)