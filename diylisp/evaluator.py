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

    def evalIfList(thing):
        if isinstance(thing, list):
            thing = evaluate(thing, env)
        return thing

    @evalIfList
    def ensureInt(thing):
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
        if isinstance(ast[1], list):
            potentialAtom = evaluate(ast[1], env)
            result = not isinstance(potentialAtom, list)
        else:
            result = isinstance(ast[1], (bool, int))

    elif ast[0] == 'eq':
        if isinstance(ast[1], list):
            result = (ast[1] == ast[2]) and not listInList(ast[1])
        else:
            result = (ast[1] == ast[2])
        # result = (evalIfList(ast[1]) == evalIfList(ast[2]))

    elif ast[0] in theMaths:
        math = theMaths[ast[0]]
        result = math(ensureInt(ast[1]), ensureInt(ast[2]))

    else:
        result = ast

    return result
