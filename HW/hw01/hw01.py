from operator import add, sub

def a_plus_abs_b(a, b):
    """返回 a+abs(b)，但不能调用 abs。

    >>> a_plus_abs_b(2, 3)
    5
    >>> a_plus_abs_b(2, -3)
    5
    >>> a_plus_abs_b(-1, 4)
    3
    >>> a_plus_abs_b(-1, -4)
    3
    """
    if b < 0:
        f = a - b
    else:
        f = a + b
    return f

def a_plus_abs_b_syntax_check():
    """检查你是否没有修改 a_plus_abs_b 的 return 语句。

    >>> # 你不需要理解此测试的代码。
    >>> import inspect, re
    >>> re.findall(r'^\s*(return .*)', inspect.getsource(a_plus_abs_b), re.M)
    ['return f(a, b)']
    """
    # 你不需要修改此函数。它只是用来检查你的答案。


def two_of_three(i, j, k):
    """返回 m*m + n*n，其中 m 和 n 是正数 i、j、k 中最小的两个数。

    >>> two_of_three(1, 2, 3)
    5
    >>> two_of_three(5, 3, 1)
    10
    >>> two_of_three(10, 2, 8)
    68
    >>> two_of_three(5, 5, 5)
    50
    """
    return i * i + j * j + k * k - max(i, j, k) ** 2

def two_of_three_syntax_check():
    """检查 two_of_three 的代码是否只有一条 return 语句。

    >>> # 你不需要理解此测试的代码。
    >>> import inspect, ast
    >>> [type(x).__name__ for x in ast.parse(inspect.getsource(two_of_three)).body[0].body]
    ['Expr', 'Return']
    """
    # 你不需要修改此函数。它只是用来检查你的答案。


def largest_factor(n):
    """返回 n 的小于 n 的最大因数。

    >>> largest_factor(15) # 因数为 1、3、5
    5
    >>> largest_factor(80) # 因数为 1、2、4、5、8、10、16、20、40
    40
    >>> largest_factor(13) # 因为 13 是质数，所以因数只有 1
    1
    """
    "*** YOUR CODE HERE ***"
    k = n - 1
    while n % k != 0:
        k -= 1
    return k


def hailstone(n):
    """打印从 n 开始的冰雹序列，并返回其长度。

    >>> a = hailstone(10)
    10
    5
    16
    8
    4
    2
    1
    >>> a
    7
    >>> b = hailstone(1)
    1
    >>> b
    1
    """
    "*** YOUR CODE HERE ***"
    length = 1
    print(n)
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = n * 3 + 1
        print(n)
        length += 1
    return length

