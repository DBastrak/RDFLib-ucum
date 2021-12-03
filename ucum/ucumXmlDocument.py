from ucum.prefix import prefix
from ucum.unitTables import unitTablesInstance
from ucum.unit import Unit
from ucum.unitString import UnitStringInstance
from ucum.prefixTables import prefixTablesInstance
import json
from bs4 import BeautifulSoup as bs
import math

class ucumXMLDocument:

    def __init__(self):

        with open(r"G:\PythonProjects\RDFLib-ucum\data\ucum-essence.xml", 'r') as xmlFile:
            data = xmlFile.read()
        self.bs_data = bs(data)
        self.moleCodes_ = ['mol', 'eq', 'osm', 'kat', 'U']


    def parseXML(self):
        prefix = self.bs_data.find_all("prefix")
        base_unit = self.bs_data.find_all("base-unit")
        unit = self.bs_data.find_all("unit")

        return [prefix, base_unit, unit]

    def parsePrefixes(self, prefixes):


        for p in prefixes:
            attrs = {}

            attrs["code_"] = p.get("code")
            attrs["ciCode_"] = p.get("cicode")
            attrs["name_"] = p.find("name").text
            attrs["printSymbol_"] = p.find("printsymbol").text

            pValNode = p.find("value")
            attrs["value_"] = None
            attrs["exp_"] = pValNode.find("sup").text
            if attrs["exp_"] != None:
                attrs["value_"] = math.pow(10, attrs["exp_"])
            else:
                attrs["value_"] = pValNode.get("value")
                attrs["exp_"] = None

            if prefixTablesInstance.isDefined(attrs["code_"]):
                raise Exception(f'Prefix constructor called for prefix already defined; code = {attrs["code_"]}')
            else:
                newPref = prefix(attrs)
                prefixTablesInstance.add(newPref)


    def parseBaseUnits(self, baseUnit):

        for b in range(len(baseUnit)):
            attrs = {}
            attrs['isBase_'] = True
            attrs['name_'] = baseUnit[b].find("name").text
            attrs['csCode_'] = baseUnit[b].get("code")
            attrs['ciCode_'] = baseUnit[b].get("cicode")
            attrs['property_'] = baseUnit[b].find("property").text
            attrs['variable_'] = baseUnit[b].get("dim")
            attrs['printSymbol_'] = baseUnit[b].find("printsymbol").text
            attrs['dim_'] = b
            attrs['source_'] = "UCUM"

            newUnit = Unit(attrs)
            unitTablesInstance.addUnit(newUnit)

    def parseUnitStrings(self, unitStrings):
        utab = unitTablesInstance
        uStrParser = UnitStringInstance()
        stopNow = False
        aLen = len(unitStrings)

        for a in range(aLen):
            if stopNow:
                break
            haveUnit = True
            attrs = {}
            attrs['isBase_'] = False
            attrs['source_'] = 'UCUM'
            attrs['name_'] = unitStrings[a].find("name").text
            attrs['csCode_'] = unitStrings[a].get("code")
            if unitStrings[a].get("cicode"):
                attrs['ciCode_'] = unitStrings[a].get("cicode")
            else:
                attrs['ciCode_'] = unitStrings[a].get("code").toUpper()
            attrs['property_'] = unitStrings[a].find("property").text

            if unitStrings[a].find("printsymbol").text:
                sym = unitStrings[a].find("printsymbol")
                symVal = unitStrings[a].find("printsymbol").text
                symVal = symVal.replace(/\n/g, "") #todo add regex
                symVal = symVal.strip()
                symI = sym.find('i')

                if symI:
                    symVal = symI.text
                sub = sym.find("sub")
                sup = sym.find("sup")

                if sub:
                    symVal += sub.text
                if sup:
                    symVal += sym.text

                attrs['printSymbol_'] = symVal

            if unitStrings[a].find("ismetric_").text == "yes":
                attrs['isMetric_'] = True
            else:
                attrs['isMetric_'] = False

            if unitStrings[a].find("isarbitrary"):
                attrs['isArbitrary_'] = True
            else:
                attrs['isArbitrary_'] = False

            if unitStrings[a].find("class"):
                attrs['class_'] = unitStrings[a].find("class").text
            valNode = unitStrings[a].find("value")
            if self.moleCodes_.find(unitStrings[a].get("code")) != -1:
                attrs['moleExp_'] = 1
            else:
                attrs['moleExp_'] = 0

            if unitStrings[a].find("isspecial"):
                attrs['isSpecial_'] = unitStrings[a].find("isspecial").text == "yes"
                funcNode = valNode.find('function')
                attrs['cnv_'] = funcNode.find("name").text
                attrs['csUnitString_'] = funcNode.find("Unit").text
                if attrs['csUnitString_'] == '1':
                    attrs['baseFactor_'] = 1
                elif attrs['csCode_'] == '[pH]':
                    attrs['baseFactor_'] = float(funcNode.find("value").text)
                else:
                    slashPos = attrs['csUnitString_'].find('/')
                    ar = []

                    if slashPos >= 0:
                        ar = attrs['csUnitString_'].split('/')
                    if slashPos >= 0 and len(ar) == 2:
                        attrs['csUnitString_'] = ar[0]
                        attrs['baseFactor_'] = float(funcNode.find("value").text) / float(ar[2])

                    elif attrs['csCode_'] == 'B[SPL]':
                        attrs['baseFactor_'] = math.pow(10, -5) * 2
                        attrs['csUnitString_'] = "Pa"

                    else:
                        attrs['baseFactor_'] = float(funcNode.find("value").text)

            else:

                attrs['csUnitString_'] = unitStrings[a].find("unit").text
                attrs['ciUnitString_'] = unitStrings[a].find("unitci").text
                attrs['baseFactor_'] = unitStrings[a].find("value").get("value")
                if attrs['csCode_'] == '[pi]':
                    attrs['baseFactor_'] = float(attrs['baseFactor_'])
                elif unitStrings[a].find("sup"):
                    attrs['baseFactor_'] = float(unitStrings[a].find("value").get("value"))
                else:
                    attrs['baseFactor_'] = float(unitStrings[a].find("value").text)

            if attrs['isArbitrary_'] == True:
                attrs['magnitude_'] = 1
                attrs['dim_'] = None

            elif attrs['class'] == 'dimless' or attrs['csCode_'] == 'mol':
                attrs['dim_'] = None

                if attrs['csUnitString_'] == '1':
                    attrs['magnitude_'] = attrs['baseFactor_']

                elif attrs['csUnitString_'][0:3] == "10*":
                    exp = int(attrs['csUnitString_'][3:]) #todo add int parser
                    attrs['magnitude_'] = math.pow(10, exp)
                    if attrs['baseFactor_'] != 1:
                        attrs['magnitude_'] *= attrs['baseFactor_']

                else:
                    attrs['defError_'] = True
                    print(f"unexpected dimless unit definition, unit code is {attrs['csCode_']}")
            elif attrs['csCode_'] == "[car_Au]":
                attrs['magnitude_'] = 1/24
                attrs['dim_'] = None
            else:
                if attrs['csUnitString_'] and attrs['csUnitString_'] != '1' and attrs['csUnitString_'] != 1:
                    haveUnit = False

                    if attrs['csCode_'] == 'Oe':
                        attrs['baseFactor_'] = 250 / math.pi
                        attrs['csUnitString_'] = "A/m"

                    elif attrs['csUnitString_'][0] == '/':
                        attrs['cnv_'] = "inv"
                        attrs['csUnitString_'] = 's'

                    elif attrs['csCode_'] == '[mu_0]':
                        attrs['baseFactor_'] = 4 * math.pi * math.pow(10, -7)
                        attrs['csUnitString_'] = 'N/A2'

                    try:
                        retObj = uStrParser.parseString((attrs['csUnitString_'], 'validate', False))
                        ret = retObj[0]
                        retString = retObj[1]
                        retMsg = retObj[2]

                        if ret:
                            attrs['dim_'] = ret.dim_
                            newMag = ret.magnitude_
                            newMag *= attrs['baseFactor_']
                            attrs['magnitude_'] = newMag
                            haveUnit = True

                        else:
                            attrs['defError_'] = True
                            print(f"unit definition error; code = {attrs['csCode_']}; msg = {retMsg}")
                            attrs['dim_'] = None
                            attrs['magnitude_'] = None

                    except Exception as e:
                        print(f"error thrown from unit parsing code for unit name {attrs['name_']}\n{str(e)}")
                        stopNow = True
            if haveUnit:
                newUnit = Unit(attrs)
                utab.addUnit(newUnit)
                uList = utab.printUnits()


