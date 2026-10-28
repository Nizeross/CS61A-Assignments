LAB_SOURCE_FILE = __file__


def print_if(s, f):
    """打印 s 中每个使 f 返回真值的元素。

    >>> print_if([3, 4, 5, 6], lambda x: x > 4)
    5
    6
    >>> result = print_if([3, 4, 5, 6], lambda x: x % 2 == 0)
    4
    6
    >>> print(result)  # print_if 应返回 None
    None
    """
    for x in s:
        "*** YOUR CODE HERE ***"


def close(s, k):
    """返回 s 中与自身索引的差的绝对值不超过 k 的元素个数。

    >>> t = [6, 2, 4, 3, 5]
    >>> close(t, 0)  # 只有 3 等于其索引
    1
    >>> close(t, 1)  # 2、3 和 5 与各自索引的差的绝对值不超过 1
    3
    >>> close(t, 2)  # 2、3、4 和 5 与各自索引的差的绝对值都不超过 2
    4
    >>> close(list(range(10)), 0)
    10
    """
    count = 0
    for i in range(len(s)):  # 使用 range 遍历索引
        "*** YOUR CODE HERE ***"
    return count


def close_list(s, k):
    """返回一个列表，包含 s 中与自身索引的差的绝对值不超过 k 的元素。

    >>> t = [6, 2, 4, 3, 5]
    >>> close_list(t, 0)  # 只有 3 等于其索引
    [3]
    >>> close_list(t, 1)  # 2、3 和 5 与各自索引的差的绝对值不超过 1
    [2, 3, 5]
    >>> close_list(t, 2)  # 2、3、4 和 5 与各自索引的差的绝对值都不超过 2
    [2, 4, 3, 5]
    """
    return [___ for i in range(len(s)) if ___]


from math import sqrt

def squares(s):
    """返回一个新列表，包含原列表中所有完全平方数的平方根。

    >>> seq = [8, 49, 8, 9, 2, 1, 100, 102]
    >>> squares(seq)
    [7, 3, 1, 10]
    >>> seq = [500, 30]
    >>> squares(seq)
    []
    """
    return [___ for n in s if ___]


def double_eights(n):
    """返回 n 中是否存在两个相邻的数字 8。

    >>> double_eights(1288)
    True
    >>> double_eights(880)
    True
    >>> double_eights(538835)
    True
    >>> double_eights(284682)
    False
    >>> double_eights(588138)
    True
    >>> double_eights(78)
    False
    >>> # 禁止迭代
    >>> from construct_check import check
    >>> check(LAB_SOURCE_FILE, 'double_eights', ['While', 'For'])
    True
    """
    "*** YOUR CODE HERE ***"


def make_onion(f, g):
    """返回函数 can_reach(x, y, limit)，判断能否仅用 f、g 和 x 构造一个调用表达式，在调用次数不超过 limit 的情况下得到 y。

    >>> up = lambda x: x + 1
    >>> double = lambda y: y * 2
    >>> can_reach = make_onion(up, double)
    >>> can_reach(5, 25, 4)      # 25 = up(double(double(up(5))))
    True
    >>> can_reach(5, 25, 3)      # 无法实现
    False
    >>> can_reach(1, 1, 0)      # 1 = 1
    True
    >>> add_ing = lambda x: x + "ing"
    >>> add_end = lambda y: y + "end"
    >>> can_reach_string = make_onion(add_ing, add_end)
    >>> can_reach_string("cry", "crying", 1)      # "crying" = add_ing("cry")
    True
    >>> can_reach_string("un", "unending", 3)     # "unending" = add_ing(add_end("un"))
    True
    >>> can_reach_string("peach", "folding", 4)   # 无法实现
    False
    """
    def can_reach(x, y, limit):
        if limit < 0:
            return ____
        elif x == y:
            return ____
        else:
            return can_reach(____, ____, limit - 1) or can_reach(____, ____, limit - 1)
    return can_reach

