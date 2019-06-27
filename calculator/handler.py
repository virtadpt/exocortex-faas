from calculator.simple import SimpleCalculator

help = """
I am a simple calculator.  Send me math problems where the terms and symbols
are separated by spaces, and I'll send back the answer.  For example:

2 + 2

23 - 17

5 fmod 3

I support the following operations:

    + - * / 
    fmod - modulus (floating point output)
    abs - absolute value
    ceil - ceiling
    fabs - absolute value (floating point)

"""

def handle(req):
    if not req:
        return help

    calc = SimpleCalculator()
    calc.run(req)
    return calc.lcd
