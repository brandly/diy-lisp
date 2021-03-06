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

    # quotes don't need evaluating
    elif ast[0] == 'quote':
        result = ast[1]

    # checks if item is an atom
    # lists are not atoms
    elif ast[0] == 'atom':
        ast[1] = evalIfNeeded(ast[1])
        result = not isinstance(ast[1], list)

    elif ast[0] == 'eq':
        left = evalIfNeeded(ast[1])
        right = evalIfNeeded(ast[2])

        # Lists are never equal, because lists are not atoms
        if isinstance(left, list) or isinstance(right, list):
            result = False
        else:
            result = (left == right)

    # ensure we have a hashable object to lookup on theMaths
    elif isinstance(ast[0], str) and ast[0] in theMaths:
        math = theMaths[ast[0]]
        result = math(ensureInt(ast[1]), ensureInt(ast[2]))

    elif ast[0] == 'if':
        comparison = evalIfNeeded(ast[1])

        if comparison:
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

    # prepend to list
    elif ast[0] == 'cons':
        ast[1] = evalIfNeeded(ast[1])
        ast[2] = evalIfNeeded(ast[2])

        ast[2].insert(0, ast[1])
        result = ast[2]

    # extract first element from list
    elif ast[0] == 'head':
        theList = evalIfNeeded(ast[1])

        if len(theList) < 1:
            raise LispError("cannot call `head` on empty list")

        result = theList.pop(0)

    # the list after removing first element
    elif ast[0] == 'tail':
        theList = evalIfNeeded(ast[1])

        if len(theList) < 1:
            raise LispError("cannot call `pop` on empty list")

        theList.pop(0)
        result = theList

    elif ast[0] == 'empty':
        theList = evalIfNeeded(ast[1])
        result = len(theList) < 1

    elif isinstance(ast[0], Closure):
        params = ast[0].params
        env = ast[0].env
        args = ast[1:]

        if len(params) != len(args):
            raise LispError("wrong number of arguments, expected " + `len(params)` + " got " + `len(args)`)

        argsMap = {}
        for i, param in enumerate(params):
            argsMap[param] = evalIfNeeded(args[i], env)

        result = evaluate(ast[0].body, env.extend(argsMap))

    elif isinstance(ast, list):
        if isinstance(ast[0], list):
            # calling lambda directly
            closure = evaluate(ast[0], env)
        else:
            try:
                # ast[0] is assumed to be a function name
                closure = env.lookup(ast[0])
            except LispError:
                raise LispError("not a function")

        withClosure = ast[1:]
        withClosure.insert(0, closure)
        result = evaluate(withClosure, closure.env)

    else:
        result = env.lookup(ast)

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
