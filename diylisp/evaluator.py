# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports,
making your work a bit easier. (We're supposed to get through this thing
in a day, after all.)
"""

def listInList(lst):
    result = False
    for item in lst:
        if isinstance(item, list):
            result = True
            break
    return result

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def divide(a, b):
    return a / b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

def mod(a, b):
    return a % b

def gt(a, b):
    return a > b

theMaths = {
    '+': add,
    '-': subtract,
    '/': divide,
    '*': multiply,
    'mod': mod,
    '>': gt
}

def evaluate(ast, env):

    def evalIfNeeded(thing, e=env):
        if isinstance(thing, (list, str)):
            thing = evaluate(thing, e)
        return thing

    def ensureInt(thing):
        thing = evalIfNeeded(thing)
        if isinstance(thing, int):
            return thing
        else:
            raise LispError()

    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if isinstance(ast, (bool, int)):
        result = ast

    elif ast[0] == 'quote':
        result = ast[1]

    elif ast[0] == 'atom':
        ast[1] = evalIfNeeded(ast[1])
        result = not isinstance(ast[1], list)

    elif ast[0] == 'eq':
        ast[1] = evalIfNeeded(ast[1])
        ast[2] = evalIfNeeded(ast[2])

        # Lists are never equal, because lists are not atoms
        if isinstance(ast[1], list) or isinstance(ast[2], list):
            result = False
        else:
            result = (ast[1] == ast[2])

    elif isinstance(ast[0], str) and ast[0] in theMaths:
        math = theMaths[ast[0]]
        result = math(ensureInt(ast[1]), ensureInt(ast[2]))

    elif ast[0] == 'if':
        ast[1] = evalIfNeeded(ast[1])

        if ast[1]:
            result = evalIfNeeded(ast[2])
        else:
            result = evalIfNeeded(ast[3])

    elif ast[0] == 'define':
        if len(ast) != 3:
            raise LispError("Wrong number of arguments")

        if not isinstance(ast[1], str):
            raise LispError("non-symbol")

        env.set(ast[1], evalIfNeeded(ast[2]))
        result = None

    elif ast[0] == 'lambda':
        if len(ast) != 3:
            raise LispError("Wrong number of arguments")

        if not isinstance(ast[1], list):
            raise LispError("Params must be a list")

        result = Closure(env, ast[1], ast[2])

    elif isinstance(ast[0], Closure):
        params = ast[0].params
        env = ast[0].env
        args = ast[1:]

        argsMap = {}
        for i, param in enumerate(params):
            argsMap[param] = evalIfNeeded(args[i], env)

        result = evaluate(ast[0].body, env.extend(argsMap))

    elif isinstance(ast, list):
        if isinstance(ast[0], list):
            # calling lambda directly
            ast[0] = evaluate(ast[0], env)
        else:
            # ast[0] is assumed to be a function name
            ast[0] = env.lookup(ast[0])

        result = evaluate(ast, ast[0].env)

    else:
        result = env.lookup(ast)

    return result
