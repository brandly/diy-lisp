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

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    try:
        if isinstance(ast, (bool, int)):
            result = ast
        elif ast[0] == 'quote':
            result = ast[1]
        elif ast[0] == 'atom':
            if isinstance(ast[1], list):
                result = not listInList(ast[1])
            else:
                result = isinstance(ast[1], (bool, int))

        elif ast[0] == 'eq':
            if isinstance(ast[1], list):
                result = (ast[1] == ast[2]) and not listInList(ast[1])
            else:
                result = (ast[1] == ast[2])

        elif ast[0] == '+':
            result = ast[1] + ast[2]

        elif ast[0] == '-':
            result = ast[1] - ast[2]

        elif ast[0] == '/':
            result = ast[1] / ast[2]

        elif ast[0] == '*':
            result = ast[1] * ast[2]

        elif ast[0] == 'mod':
            result = ast[1] % ast[2]

        elif ast[0] == '>':
            result = ast[1] > ast[2]

        else:
            result = ast
    except TypeError:
        raise LispError()

    return result
