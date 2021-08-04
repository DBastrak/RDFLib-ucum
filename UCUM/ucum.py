'''
This python file holds ucum conversion functions related to RDFLib.
'''



def unitValidation(unitName: str) -> bool:
    '''validates that the unit is real and can be used in the conversion'''

def unitConversion(originalUnit: str, unitValue: float, requiredUnit: str) -> float:
    '''function that will convert the value of the original unit into the required unit'''

def findConversion(originalUnit: str, requiredUnit: str) -> str:
    '''
    function that finds the required conversion in a data structure
    returns a string, string can be lambda methods that hold the conversion

    e.g.
    dir = {'firstMethod':'lambda x: x + 273'}
    x = eval(dir['firstMethod']
    print(x(5)) -> 278
    '''


