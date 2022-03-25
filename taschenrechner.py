#---------------------
import math
from sys import argv

def tokenize(program):
    return program.replace("(", " ( ").replace(")", " ) ").split()

#---------------------
def parse(tokens):
    token = tokens.pop(0)
    if token == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(parse(tokens)) # solange parsen bis keine klammer mehr
        tokens.pop(0)
        return lst
    else:
        return parse_atom(token)

#---------------------
def parse_atom(token):
    try:
        token = int(token)
    except ValueError:
        try:
            token = float(token)
        except ValueError:
            pass
    return token

#---------------------
def add(a, b):
    return a + b 

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    return a / b

def sqrt(a):
    return math.sqrt(a)

def expt(a, b):
    return a ** b


builtins = {
    '+':    add,
    '-':    sub,
    '*':    mult,
    '/':    div,
    'sqrt': sqrt,
    'expt': expt,
    'e':    2.718281828459045,
    'pi':   3.141592653589793,
}

#---------------------
def evaluate(x):
    if type(x) == float or type(x) == int:
        return x
    elif type(x) == str:
        return builtins[x]
    else:
        operator = x[0]

        # SPECIAL FORMS
        if operator == 'var':
            name, value = x[1:]
            value = evaluate(value) # value evaluieren

            # variable abspeichern
            builtins[name] = value
            # als bestätigung value zurückgeben
            return value

        elif operator == 'func':
            # Funktion: (func f ((a b) (+ a b)))
            name, value = x[1:]

            params = value[0]
            body = value[1]

            builtins[name] = [params, body]

            return f"New function '{name}'"

        else:
            func = builtins[operator]
            args = []

            for arg in x[1:]:
                args.append(evaluate(arg)) # solange evaluieren bis nur noch zahlen

            if type(func) == list: # eigene Funktion: [[p1, p2], [body]]
                params = func[0]
                body = func[1]

                # alle parameter abspeichern in buitins
                for i in range(len(args)):
                    builtins[params[i]] = args[i]

                return evaluate(body)

            else:
                return func(*args)

#===================== Input
def repl():
    print("Press 'q' or 'x' to exit program.")
    done = False
    while not done:
        try:
            prog = input('> ').strip()
            if prog.lower() in ('q', 'quit', 'exit', 'x'):
                done = True

            elif prog.lower()[0:2] == 'f:':
                filename = prog.split(maxsplit=1)[1]

                with open(filename) as f:
                    content = f.read()
                
                print(evaluate(parse(tokenize(content))))

            else:
                print(evaluate(parse(tokenize(prog))))
        except Exception as e:
            print('Error', repr(e))

testScript = False
if len(argv) == 2:
    script, testScript = argv

# test script
if __name__ == '__main__' and testScript:
    tests = [
        (tokenize, ('(+ 1 1)',), ['(', '+', '1', '1', ')']),
        (tokenize, ('(sqrt 36)',), ['(', 'sqrt', '36', ')']),
        (parse, (['(', '+', 1, 1, ')'],), ['+', 1, 1]),
        (parse, (['(', '+', '(', '*', 2, 3, ')', 1, ')'],), ['+', ['*', 2, 3], 1]),
        (parse_atom, ('1.1',), 1.1),
        (add, (1, 1), 2),
        (sub, (2, 1), 1),
        (mult, (2, 3), 6),
        (div, (7, 2), 3.5),
        (sqrt, (64,), 8.0),
        (expt, (2, 5), 32),
        (evaluate, (['*', ['+', 5, 9], ['-', 11, ['/', 128, 16]]],), 42)
    ]
    ok = True
    for func, args, expected_out in tests:
        try:
            actual_out = func(*args)
            if actual_out == expected_out:
                print(func.__name__, 'OK')
            else:
                ok = False
                print(func.__name__, 'not OK!', actual_out, '!=', expected_out)
        except Exception as e:
            ok = False
            print(func.__name__, 'not OK!, Failure:', e)

    if ok:
        print('Everything OK!')
        print()
    else:
        print('\nSomething seems to be wrong. Please correct the above errors.')
repl()