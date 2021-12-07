import math



class UcumFunctions:

    def __init__(self):
        self.funcs = {}

        self.funcs['cel'] = {'cnvTo': lambda x: x - 273.15, 'cnvFrom' : lambda x: x+ 273.15}

        self.funcs['degf'] = {'cnvTo': lambda x: x - 459.67, 'cnvFrom': lambda x: x + 459.67}

        self.funcs['degre'] = {'cnvTo': lambda x: x - 273.15, 'cnvFrom': lambda x: x + 273.15}

        self.funcs['ph'] = {'cnvTo': lambda x:  - math.log(x) / math.log10(), 'cnvFrom': lambda x: math.pow(10, -x)}

        self.funcs['ln'] = {'cnvTo': lambda x: math.log(x), 'cnvFrom': lambda x: math.exp(x)}

        self.funcs['2ln'] = {'cnvTo': lambda x: 2 * math.log(x), 'cnvFrom': lambda x: math.exp(x/2)}

        self.funcs['lg'] = {'cnvTo': lambda x: math.log(x) / math.log10(), 'cnvFrom': lambda x: math.pow(10, x)}

        self.funcs['10lg'] = {'cnvTo': lambda x: 10 * math.log(x) / math.log10(), 'cnvFrom': lambda x: math.pow(10, x/10)}

        self.funcs['20lg'] = {'cnvTo': lambda x: 20 * math.log(x) / math.log10(), 'cnvFrom': lambda x: math.pow(10, x/20)}

        self.funcs['2lg'] = {'cnvTo': lambda x: 2 * math.log(x) / math.log10(), 'cnvFrom': lambda x: math.pow(10, x/2)}

        self.funcs['lgtimes2'] = self.funcs['2lg']

        self.funcs['ld'] = {'cnvTo': lambda x: math.log(x) / math.log2(), 'cnvFrom': lambda x: math.pow(2, x)}

        self.funcs['100tan'] = {'cnvTo': lambda x: math.tan(x) * 100, 'cnvFrom': lambda x: math.atan(x/100)}

        self.funcs['tanTimes100'] = self.funcs['100tan']

        self.funcs['sqrt'] = {'cnvTo': lambda x: math.sqrt(x), 'cnvFrom': lambda x: x*x}

        self.funcs['inv'] = {'cnvTo': lambda x: 1.0 / x, 'cnvFrom': lambda x: 1.0 / x}

        self.funcs['hpX'] = {'cnvTo': lambda x: -(math.log(x) / math.log10()), 'cnvFrom': lambda x: math.pow(10, -x)}

        self.funcs['hpC'] = {'cnvTo': lambda x: -(self.func['ln'](x))/self.funcs['ln'](100),
                             'cnvFrom': lambda x: math.pow(100, -x)}

        self.funcs['hpM'] = {'cnvTo': lambda x: -(self.funcs['ln'](x))/self.funcs['ln'](1000),
                             'cnvFrom': lambda x: math.pow(1000, -x)}

        self.funcs['hpQ'] = {'cnvTo': lambda x: -(self.funcs['ln'](x))/self.funcs['ln'](50000),
                             'cnvFrom': lambda x: math.pow(50000, -x)}

    def forName(self, fname) -> dict:
        fname.lower()
        try:
            f = self.funcs[fname]
            return f
        except KeyError:
            print(f"Requested function {fname} is not defined")
            return False

    def isDefined(self, fname) -> bool:
        fname.lower()
        try:
            return self.funcs[fname] != None
        except KeyError:
            return False

