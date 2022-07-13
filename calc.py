# TODO:
#   - Print         DONE
#   - >=, <=, !=    DONE
#   - Input         DONE
#   - Comments      DONE
#   - Strings       DONE
#   - While-Loops   DONE
#   - Errors

#---------------------
from time import sleep
import re
from sys import argv
from sys import version_info
from collections import ChainMap

if version_info.major < 3 or version_info.minor < 10:
    print("This script needs at least Python version 3.10 as it uses structural pattern matching. Please update and try again.")
    input()
    exit()

comment = re.compile("#.*#") # RegEx to filter out comments

def tokenize(program: str) -> list[str]:
    """Tokenizes the program by adding spaces around brackets and splitting it afterwards.
    This also removes comments"""

    program = comment.sub("", program) # remove comments

    return program.replace("(", " ( ").replace(")", " ) ").split()

#---------------------
def parse(tokens: list):
    """Parses tokens into a list to be evaluated"""
    token = tokens.pop(0)
    if token == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(parse(tokens)) # solange parsen bis keine klammer mehr
        tokens.pop(0) # pop closed bracket
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

#--------------------- Builtin Functions
def _input(prompt):
    result = input(f"{prompt} ")
    try:
        return int(result)

    except ValueError:
        try:
            return float(result)

        except ValueError:
            return result

builtins = {
    '+':        lambda a, b : a + b,
    '-':        lambda a, b : a - b,
    '*':        lambda a, b : a * b,
    '/':        lambda a, b : a / b,
    '%':        lambda a, b : a % b,

    '==':       lambda a, b : a == b,
    '!=':       lambda a, b : a != b,
    '>':        lambda a, b : a > b,
    '>=':       lambda a, b : a >= b,
    '<':        lambda a, b : a < b,
    '<=':       lambda a, b : a <= b,
    'expt':     lambda a, b : a ** b,
    
    'input':    _input,
    'sleep':    sleep,
    'print':    print,
}

library = """
(block
    (var e 2.718281828459045)
    (var pi 3.141592653589793)

    (func square (
        (x) 
        (* x x)
    ))

    (func sqrt (
        (x)
        (expt x 0.5)
    ))

    (func factorial (
        (n) 
        (if
            (< n 2)
            1
            (* n (factorial (- n 1)))
        )
    ))

    (func pythagoras (
        (a b) 
        (sqrt (+ (expt a 2) (expt b 2)))
    ))

    (func countdown (
        (x)
        (if 
            (== x 0)
            0
            (block
                (print x)
                (sleep 1)
                (countdown (- x 1))
            )
        )
    ))
)
"""

globalEnv = ChainMap({}, builtins) # ChainMap mit globalen Variablen und Builtins

#---------------------
def evaluate(expr, env=globalEnv):
    """Evaluates the tokenized and parsed expression"""
    match expr:
        case int(num) | float(num):
            return num
        
        case str(name):
            return env[name]

        case ["string", *rest]:
            # joins rest back together while converting anything to strings via list comprehension
            return " ".join(str(element) for element in rest)
        
        case ['var', name, value]:
            value = evaluate(value, env)
            env[name] = value
            return None
        
        case ['+=', name, increment]:
            var = env[name]
            env[name] = var + increment
            return None
        
        case ['-=', name, decrement]:
            var = env[name]
            env[name] = var - decrement
            return None
        
        case ['*=', name, multiplier]:
            var = env[name]
            env[name] = var * multiplier
            return None
        
        case ['/=', name, quotient]:
            var = env[name]
            env[name] = var / quotient
            return None
        
        case ['if', condition, _do, _else]:
            # (if
            #   (== 4 6)        | condition
            #   (+ 2 3)         | return if condition is true
            #   (/ 6 2)         | return if condition is false
            # )

            if evaluate(condition, env):
                return evaluate(_do, env)
            else:
                return evaluate(_else, env)
        
        case ['while', condition, _do]:
            # similar structure as if-statement
            while evaluate(condition, env):
                evaluate(_do, env)

            return None
        
        case ['func', name, [params, body]]:
            # env gets saved for closures
            env[name] = [name, params, body, env]
            return None
        
        case ['block', *statements, _return]:
            # Evaluates multiple statements and returns the result of the last one
            # (block
            #   (var a 5) 
            #   (var b 7)
            #   (* a b)
            # )
            # --> 35

            for statement in statements:
                evaluate(statement, env)
            
            return evaluate(_return, env)
        
        case ['import', filename]:
            try:
                with open(filename) as f:
                    content = f.read()
                    
                return evaluate(parse(tokenize(content)))
            
            except FileNotFoundError:
                return f"No such file or directory: '{filename}'"

        # functions
        case [operator, *args]:
            func = env[operator]
            args = [evaluate(arg, env) for arg in args]

            match func:
                case [funcName, params, body, parentEnv]:
                    # defined functions
                    # create new env with env of potential parent function which includes the global env
                    newEnv = ChainMap({}, parentEnv) 

                    if len(params) != len(args):
                        return f"Error: '{funcName}' takes {len(params)} arguments ({', '.join(params)}), but {len(args)} {'was' if len(args) == 1 else 'were'} given"
                    for p, a in zip(params, args):
                        newEnv[p] = a

                    return evaluate(body, newEnv)
                
                case _:
                    return func(*args)
                

#===================== Input
def repl():
    # load library
    evaluate(parse(tokenize(library)))

    if len(argv) == 2:
        script, filename = argv
        evaluate(parse(tokenize(f"(import {filename})")))

    print("\nType 'quit' or 'exit' to exit program.")
    done = False
    while not done:
        try:
            prog = input('> ').strip()
            if prog.lower() in ('quit', 'exit'):
                done = True

            elif prog != "":
                result = evaluate(parse(tokenize(prog)))
                if result not in ("", None):
                    print(result)

        except Exception as e:
            print('Error', repr(e))

if __name__ == "__main__":
    repl()