from ucum.ucum_config import UCUM

class prefix:

    code_ = None
    ciCode_ = None
    name_ = None
    printSymbol_ = None
    value_ = None
    exp_ = None

    def __init__(self, attrs: dict):
        try:
            if attrs['code_'] == None or attrs['ciCode_'] == None or attrs['name_'] == None or \
                   attrs['value_'] == None:
                raise ValueError("Prefix constructor called missing one or more parameters. "
                                "Prefix codes ci, name, value and exponent must all be specified "
                                "and all but the exponent must not be null.")
        except KeyError:
            print("Prefix constructor called missing one or more parameters"
                    "Prefix codes ci, name, value and exponent must all be specified.")


        self.code_ = attrs['code_']

        self.ciCode_ = attrs['ciCode_']

        self.name_ = attrs['name_']

        self.printSymbol_ = attrs['printSymbol_']

        if isinstance(attrs['value_'], str):
            try:
                self.value_ = float(attrs['value_'])
            except TypeError:
                print(f"TypeError value {attrs['value_']} was not a float/int and could not be converted into one")

        else:
            self.value_ = attrs['value_']

        self.exp_ = attrs['exp_']

    def getValue(self) -> float:
        return self.value_

    def getCode(self) -> str:
        return self.code_

    def getCiCode(self) -> str:
        return self.ciCode_

    def getName(self) -> str:
        return self.name_

    def getPrintSymbol(self) -> str:
        return self.printSymbol_

    def getExp(self) -> float:
        return self.exp_

    def equals(self, prefix2) -> bool:
        return (self.code_ == prefix2.code_ and
                self.ciCode_ == prefix2.ciCode_ and
                self.name_ == prefix2.name_ and
                self.printSymbol_ == prefix2.printSymbol_ and
                self.value_ == prefix2.value_ and
                self.exp_ == prefix2.exp_)

