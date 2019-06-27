from calculator.simple import SimpleCalculator

def handle(req):
    calc = SimpleCalculator()
    calc.run(req)
    return calc.lcd
