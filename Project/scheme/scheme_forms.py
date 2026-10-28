from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# 特殊形式 #
#################

# 以下各个 do_xxx_form 函数以特殊形式的 cdr 作为
# 第一个参数：它是去掉开头标识符的 Scheme 列表，
# 这些标识符包括 if、lambda、quote 等。第二个参数是
# 对该形式求值时所用的环境。

def do_define_form(expressions, env):
    """对 define 形式求值。
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env) # 对 (define x 2) 求值
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env) # 对 (define x (+ 2 8)) 求值
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # 第 10 题
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env) # 对 (define (f x) (+ x 8)) 求值
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2) # 检查 expressions 是否为长度至少为 2 的列表
    signature = expressions.first
    if scheme_symbolp(signature):
        # 将名称绑定到一个值，例如 (define x (+ 1 2))
        validate_form(expressions, 2, 2) # 检查 expressions 是否为长度恰好为 2 的列表
        # BEGIN PROBLEM 4
        "*** YOUR CODE HERE ***"
        # END PROBLEM 4
    elif isinstance(signature, Pair) and scheme_symbolp(signature.first):
        # 定义具名过程，例如 (define (f x y) (+ x y))
        # BEGIN PROBLEM 10
        "*** YOUR CODE HERE ***"
        # END PROBLEM 10
    else:
        bad_signature = signature.first if isinstance(signature, Pair) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))

def do_quote_form(expressions, env):
    """对 quote 形式求值。

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env) # 对 (quote (+ x 2)) 求值
    Pair('+', Pair('x', Pair(2, nil)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    # END PROBLEM 5

def do_begin_form(expressions, env):
    """对 begin 形式求值。

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env) # 对 (begin (print 2) 3) 求值
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):
    """对 lambda 形式求值。

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env) # 对 (lambda (x) (+ x 2)) 求值
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    # END PROBLEM 7

def do_if_form(expressions, env):
    """对 if 形式求值。

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # 对 (if #t (print 2) (print 3)) 求值
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # 对 (if #f (print 2) (print 3)) 求值
    3
    """
    validate_form(expressions, 2, 3)
    if is_scheme_true(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env)
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env)

def do_and_form(expressions, env):
    """对具有短路行为的 and 形式求值。

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env) # 对 (and #f (print 1)) 求值
    False
    >>> # 对 (and (print 1) (print 2) (print 4) 3 #f) 求值
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    "*** YOUR CODE HERE ***"
    # END PROBLEM 12

def do_or_form(expressions, env):
    """对具有短路行为的 or 形式求值。

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env) # 对 (or 10 (print 1)) 求值
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env) # 对 (or #f 2 3 #t #f) 求值
    2
    >>> # 对 (or (begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7)) 求值
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    "*** YOUR CODE HERE ***"
    # END PROBLEM 12

def do_cond_form(expressions, env):
    """对 cond 形式求值。

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    while expressions is not nil:
        clause = expressions.first
        validate_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.rest != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if is_scheme_true(test):
            # BEGIN PROBLEM 13
            "*** YOUR CODE HERE ***"
            # END PROBLEM 13
        expressions = expressions.rest

def do_let_form(expressions, env):
    """对 let 形式求值。

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)

def make_let_frame(bindings, env):
    """创建环境帧 ENV 的子帧，其中包含 BINDINGS 给出的定义。Scheme 列表 BINDINGS 必须具有 let 表达式中合法绑定列表的形式：每项都是包含一个符号和一个 Scheme 表达式的列表。"""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names = vals = nil
    # BEGIN PROBLEM 14
    "*** YOUR CODE HERE ***"
    # END PROBLEM 14
    return env.make_child_frame(names, vals)



def do_quasiquote_form(expressions, env):
    """在环境帧 ENV 中，对参数为 EXPRESSIONS 的 quasiquote 形式求值。"""
    def quasiquote_item(val, env, level):
        """在环境帧 ENV 中，对嵌套在 quasiquote 形式内、深度为 LEVEL 的 Scheme 表达式 VAL 求值。"""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)

def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


#################
# 动态作用域 #
#################

def do_mu_form(expressions, env):
    """对 mu 形式求值。"""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 11
    "*** YOUR CODE HERE ***"
    # END PROBLEM 11



SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'mu': do_mu_form,
}