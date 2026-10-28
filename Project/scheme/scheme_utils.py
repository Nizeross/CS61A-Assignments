import numbers

from scheme_classes import *

#################
# 类型检查 #
#################

def scheme_procedurep(x):
    return isinstance(x, Procedure)

def scheme_listp(x):
    """返回 x 是否为结构正确的列表。假设不存在环。"""
    while x is not nil:
        if not isinstance(x, Pair):
            return False
        x = x.rest
    return True

def scheme_booleanp(x):
    return x is True or x is False

def scheme_numberp(x):
    return isinstance(x, numbers.Real) and not scheme_booleanp(x)

def is_scheme_true(val):
    """在 Scheme 中，除 False 外的所有值都为真。"""
    return val is not False

def is_scheme_false(val):
    """在 scheme_reader 中，只有 False 为假。"""
    return val is False

def scheme_stringp(x):
    return isinstance(x, str) and x.startswith('"')

def scheme_symbolp(x):
    return isinstance(x, str) and not scheme_stringp(x)

def scheme_nullp(x):
    return type(x).__name__ == 'nil'

def scheme_atomp(x):
    return (scheme_booleanp(x) or scheme_numberp(x) or scheme_symbolp(x) or
            scheme_nullp(x) or scheme_stringp(x))

def self_evaluating(expr):
    """返回 EXPR 的求值结果是否为它自身。"""
    return (scheme_atomp(expr) and not scheme_symbolp(expr)) or expr is None


#######################
# 参数校验 #
#######################

def validate_type(val, predicate, k, name):
    """返回 VAL。如果 PREDICATE(VAL) 为假，则抛出 SchemeError，并用“NAME 的第 K 个参数”描述出错的值。"""
    if not predicate(val):
        msg = "argument {0} of {1} has wrong type ({2})"
        type_name = type(val).__name__
        if scheme_symbolp(val):
            type_name = "symbol"
        raise SchemeError(msg.format(k, name, type_name))
    return val

def validate_procedure(procedure):
    """检查 PROCEDURE 是否为有效的 Scheme 过程。"""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), repl_str(procedure)))

def validate_form(expr, min, max=float('inf')):
    """检查 EXPR 是否为正规列表，且长度不小于 MIN、不大于 MAX（默认无上限）。若不满足，则抛出 SchemeError。

    >>> validate_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + repl_str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif length > max:
        raise SchemeError('too many operands in form')

def validate_formals(formals):
    """检查 FORMALS 是否为有效的形参列表，即由互不相同的符号组成的 Scheme 列表。如果它不是符号列表或包含重复符号，则抛出 SchemeError。

    >>> validate_formals(read_line('(a b c)'))
    """
    symbols = set()
    def validate_and_add(symbol, is_last):
        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        validate_and_add(formals.first, formals.rest is nil)
        formals = formals.rest
