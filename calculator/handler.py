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

def handle(event, context):

    # Assume that no payload in the request means the user is asking for
    # help.
    if not event.body:
        response = {}
        response["statusCode"] = 400
        response["body"] = help
        return(response)

    calc = SimpleCalculator()
    calc.run(event.body)

    response = {}
    response["statusCode"] = 200
    response["body"] = str(calc.lcd)
    return(response)

