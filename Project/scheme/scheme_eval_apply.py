import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# 求值与应用 #
##############

def scheme_eval(expr, env, _=None): # 可选的第三个参数会被忽略
    """在环境帧 ENV 中对 Scheme 表达式 EXPR 求值。

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # 对原子表达式求值
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # 所有非原子表达式都是列表（组合式）
    if not scheme_listp(expr):
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS:
        return scheme_forms.SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """在当前环境帧 ENV 中，将 Scheme 过程 PROCEDURE 应用于参数值 ARGS（一个 Scheme 列表）。"""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            "*** YOUR CODE HERE ***"
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env):
    """在当前环境帧 ENV 中依次对 Scheme 列表 EXPRESSIONS 中的表达式求值，返回最后一个表达式的值。

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    return scheme_eval(expressions.first, env) # 用你自己的代码替换此处
    # END PROBLEM 6


################################
# 附加题：尾递归 #
################################

class Unevaluated:
    """一个表达式及其求值所用的环境。"""

    def __init__(self, expr, env):
        """需要在环境帧 ENV 中求值的表达式 EXPR。"""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """在 env 中将 procedure 应用于 args，并确保结果不是 Unevaluated 对象。"""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """返回求值函数 eval 的一个支持正确尾递归的版本。"""
    def optimized_eval(expr, env, tail=False):
        """在环境帧 ENV 中对 Scheme 表达式 EXPR 求值。若 TAIL 为真，返回一个 Unevaluated 对象，其中包含待进一步求值的表达式。
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# 取消下一行的注释，以启用尾调用优化 #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
