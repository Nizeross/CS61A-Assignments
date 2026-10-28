HW_SOURCE_FILE = __file__


def num_eights(n):
    """返回 n 的十进制表示中数字 8 出现的次数。

    >>> num_eights(3)
    0
    >>> num_eights(8)
    1
    >>> num_eights(88888888)
    8
    >>> num_eights(2638)
    1
    >>> num_eights(86380)
    2
    >>> num_eights(12345)
    0
    >>> num_eights(8782089)
    3
    >>> from construct_check import check
    >>> # 禁止所有赋值语句
    >>> check(HW_SOURCE_FILE, 'num_eights',
    ...       ['Assign', 'AnnAssign', 'AugAssign', 'NamedExpr', 'For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n == 0:
        return 0
    elif n % 10 == 8:
        return 1 + num_eights(n // 10)
    else:
        return num_eights(n // 10)


def digit_distance(n):
    """计算 n 的数字距离（相邻位数字差的绝对值之和）。

    >>> digit_distance(3)
    0
    >>> digit_distance(777) # 0 + 0
    0
    >>> digit_distance(314) # 2 + 3
    5
    >>> digit_distance(31415926535) # 2 + 3 + 3 + 4 + ... + 2
    32
    >>> digit_distance(3464660003)  # 1 + 2 + 2 + 2 + ... + 3
    16
    >>> from construct_check import check
    >>> # 禁止所有循环
    >>> check(HW_SOURCE_FILE, 'digit_distance',
    ...       ['For', 'While'])
    True
    """
    "*** YOUR CODE HERE ***"
    if n < 10:
        return 0
    else:
        a = n % 10
        b = n // 10 % 10
        return digit_distance(n // 10) + abs(a - b)


def interleaved_sum(n, odd_func, even_func):
    """计算 odd_func(1) + even_func(2) + odd_func(3) + ...，直到 n。

    >>> identity = lambda x: x
    >>> square = lambda x: x * x
    >>> triple = lambda x: x * 3
    >>> interleaved_sum(5, identity, square) # 1   + 2*2 + 3   + 4*4 + 5
    29
    >>> interleaved_sum(5, square, identity) # 1*1 + 2   + 3*3 + 4   + 5*5
    41
    >>> interleaved_sum(4, triple, square)   # 1*3 + 2*2 + 3*3 + 4*4
    32
    >>> interleaved_sum(4, square, triple)   # 1*1 + 2*3 + 3*3 + 4*3
    28
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'interleaved_sum', ['While', 'For', 'Mod']) # 禁止循环和 % 运算符
    True
    >>> check(HW_SOURCE_FILE, 'interleaved_sum', ['BitAnd', 'BitOr', 'BitXor']) # 禁止位运算符；如果你还不知道它们是什么，不用担心
    True
    """
    "*** YOUR CODE HERE ***"
    def helper(i, n, f, g):
        if i > n:
            return 0
        else:
            return f(i) + helper(i+1, n, g, f)
    return helper(1, n, odd_func, even_func)



def next_smaller_dollar(bill):
    """返回面额序列中下一个更小的纸币面额。"""
    if bill == 100:
        return 50
    if bill == 50:
        return 20
    if bill == 20:
        return 10
    elif bill == 10:
        return 5
    elif bill == 5:
        return 1

def count_dollars(total):
    """返回换零钱的方案数。

    >>> count_dollars(15)  # 15 张 1 美元，10 张 1 美元加 1 张 5 美元，……，1 张 5 美元加 1 张 10 美元
    6
    >>> count_dollars(10)  # 10 张 1 美元，5 张 1 美元加 1 张 5 美元，2 张 5 美元，10 张 1 美元
    4
    >>> count_dollars(20)  # 20 张 1 美元，15 张 1 美元加 1 张 5 美元，……，1 张 20 美元
    10
    >>> count_dollars(45)  # 45 美元有多少种换零钱的方案？
    44
    >>> count_dollars(100) # 100 美元有多少种换零钱的方案？
    344
    >>> count_dollars(200) # 200 美元有多少种换零钱的方案？
    3274
    >>> from construct_check import check
    >>> # 禁止迭代
    >>> check(HW_SOURCE_FILE, 'count_dollars', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"



def next_larger_dollar(bill):
    """返回面额序列中下一个更大的纸币面额。"""
    if bill == 1:
        return 5
    elif bill == 5:
        return 10
    elif bill == 10:
        return 20
    elif bill == 20:
        return 50
    elif bill == 50:
        return 100

def count_dollars_upward(total):
    """返回使用纸币换零钱的方案数。

    >>> count_dollars_upward(15)  # 15 张 1 美元，10 张 1 美元加 1 张 5 美元，……，1 张 5 美元加 1 张 10 美元
    6
    >>> count_dollars_upward(10)  # 10 张 1 美元，5 张 1 美元加 1 张 5 美元，2 张 5 美元，10 张 1 美元
    4
    >>> count_dollars_upward(20)  # 20 张 1 美元，15 张 1 美元加 1 张 5 美元，……，1 张 20 美元
    10
    >>> count_dollars_upward(45)  # 45 美元有多少种换零钱的方案？
    44
    >>> count_dollars_upward(100) # 100 美元有多少种换零钱的方案？
    344
    >>> count_dollars_upward(200) # 200 美元有多少种换零钱的方案？
    3274
    >>> from construct_check import check
    >>> # 禁止迭代
    >>> check(HW_SOURCE_FILE, 'count_dollars_upward', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"


def print_move(origin, destination):
    """打印移动一个圆盘的指令。"""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """打印将 n 个圆盘从 start 柱移到 end 柱所需的步骤，且不能违反汉诺塔规则。

    n：圆盘数量。
    start：起始柱的位置，为 1、2 或 3。
    end：目标柱的位置，为 1、2 或 3。

    总共只有三根柱子，且 start 和 end 必须不同。假定起始柱至少有 n 个从上到下依次增大的圆盘；目标柱为空，或其顶部圆盘比起始柱顶部的 n 个圆盘都大。

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    "*** YOUR CODE HERE ***"


from operator import sub, mul

def make_anonymous_factorial():
    """返回一个用于计算阶乘的表达式的值。

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> # 禁止任何赋值或递归
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial',
    ...     ['Assign', 'AnnAssign', 'AugAssign', 'NamedExpr', 'FunctionDef', 'Recursion'])
    True
    """
    return 'YOUR_EXPRESSION_HERE'

