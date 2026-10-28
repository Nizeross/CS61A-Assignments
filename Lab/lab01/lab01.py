def digit(n, k):
    """对于正整数 n 和 k，返回 n 从右往左数第 k 位的数字。

    >>> digit(3579, 2)
    5
    >>> digit(3579, 0)
    9
    >>> digit(3579, 10)
    0
    """
    return ____


def middle(a, b, c):
    """返回 a、b、c 中既不是最大值也不是最小值的数。假设三者互不相同。

    >>> middle(3, 5, 4)
    4
    >>> middle(30, 5, 4)
    5
    >>> middle(3, 5, 40)
    5
    >>> middle(3, 5, 40)
    5
    >>> middle(30, 5, 40)
    30
    """
    return ____


def falling(n, k):
    """计算 n 的 k 阶下降阶乘。

    >>> falling(6, 3)  # 6 * 5 * 4
    120
    >>> falling(4, 3)  # 4 * 3 * 2
    24
    >>> falling(4, 1)  # 4
    4
    >>> falling(4, 0)
    1
    """
    "*** YOUR CODE HERE ***"


def divisible_by_k(n, k):
    """
    >>> a = divisible_by_k(10, 2)  # 2、4、6、8 和 10 都能被 2 整除
    2
    4
    6
    8
    10
    >>> a
    5
    >>> b = divisible_by_k(3, 1)  # 1、2 和 3 都能被 1 整除
    1
    2
    3
    >>> b
    3
    >>> c = divisible_by_k(6, 7)  # 不超过 6 的正整数中，没有能被 7 整除的数
    >>> c
    0
    """
    "*** YOUR CODE HERE ***"


def sum_digits(y):
    """求 y 的各位数字之和。

    >>> sum_digits(10) # 1 + 0 = 1
    1
    >>> sum_digits(4224) # 4 + 2 + 2 + 4 = 12
    12
    >>> sum_digits(1234567890)
    45
    >>> a = sum_digits(123) # 确保使用 return，而不是 print
    >>> a
    6
    """
    "*** YOUR CODE HERE ***"


def double_eights(n):
    """如果 n 中存在两个相邻的数字 8，返回真。
    >>> double_eights(8)
    False
    >>> double_eights(88)
    True
    >>> double_eights(2882)
    True
    >>> double_eights(880088)
    True
    >>> double_eights(12345)
    False
    >>> double_eights(80808080)
    False
    """
    "*** YOUR CODE HERE ***"

