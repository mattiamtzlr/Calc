#---------------------
import math
from sys import argv
from sys import version_info

if version_info.major != 3 or version_info.minor != 10:
    print("This script needs at least Python version 3.10 as it uses structural pattern matching. Please update and try again.")
    input()
    exit()

def tokenize(program: str) -> list[str]:
    """Tokenizes the program by adding spaces around brackets and splitting it afterwards"""
    return program.replace("(", " ( ").replace(")", " ) ").split()

#---------------------
def parse(tokens: list):
    """Parses tokens into a list to be evaluated"""
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
    """Parses single tokens into numbers, floats or strings"""
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
    """Evaluates the tokenized and parsed program"""
    match x:
        case int(num) | float(num):
            return num
        
        case str(name):
            return builtins[name]
        
        case ['var', name, value]:
            value = evaluate(value)
            builtins[name] = value
            return value
        
        case ['func', name, [params, body]]:
            builtins[name] = [params, body]
            return f"New function '{name}'"
        
        case [operator, *args]:
            func = builtins[operator]
            args = [evaluate(arg) for arg in args]

            if callable(func):
                # Eingebaute Funktion
                return func(*args)

            else:
                # eigene Funktion: [[p1, p2], [body]]
                params = func[0]
                body = func[1]

                # alle parameter abspeichern in buitins
                for p, a in zip(params, args):
                    builtins[p] = a

                return evaluate(body)
                

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