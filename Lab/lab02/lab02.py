
def composite_identity(f, g):
    """
    返回一个只有参数 x 的函数：当 f(g(x)) 等于 g(f(x)) 时返回 True。可以假定 g(x) 的结果是 f 的有效输入，反之亦然。

    >>> add_one = lambda x: x + 1        # 将 x 加一
    >>> square = lambda x: x**2          # 将 x 平方（返回 x^2）
    >>> b1 = composite_identity(square, add_one)
    >>> b1(0)                            # (0 + 1) ** 2 == 0 ** 2 + 1
    True
    >>> b1(4)                            # (4 + 1) ** 2 != 4 ** 2 + 1
    False
    """
    "*** YOUR CODE HERE ***"


def sum_digits(y):
    """返回非负整数 y 的各位数字之和。"""
    total = 0
    while y > 0:
        total, y = total + y % 10, y // 10
    return total

def is_prime(n):
    """返回正整数 n 是否为质数。"""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def count_cond(condition):
    """返回一个只有参数 N 的函数，用于统计 1 到 N 中满足双参数谓词函数 Condition 的数的个数。调用 Condition 时，第一个参数为 N，第二个参数为 1 到 N 中当前检查的数。

    >>> count_fives = count_cond(lambda n, i: sum_digits(n * i) == 5)
    >>> count_fives(10)   # 50 (10 * 5)
    1
    >>> count_fives(50)   # 50 (50 * 1), 500 (50 * 10), 1400 (50 * 28), 2300 (50 * 46)
    4

    >>> is_i_prime = lambda n, i: is_prime(i) # 需要向 count_cond 传入一个接受两个参数的函数
    >>> count_primes = count_cond(is_i_prime)
    >>> count_primes(2)    # 2
    1
    >>> count_primes(3)    # 2, 3
    2
    >>> count_primes(4)    # 2, 3
    2
    >>> count_primes(5)    # 2, 3, 5
    3
    >>> count_primes(20)   # 2, 3, 5, 7, 11, 13, 17, 19
    8
    """
    "*** YOUR CODE HERE ***"


def multiple(a, b):
    """返回同时是 a 和 b 的倍数的最小数 n。

    >>> multiple(3, 4)
    12
    >>> multiple(14, 21)
    42
    """
    "*** YOUR CODE HERE ***"



def cycle(f1, f2, f3):
    """返回一个本身也是高阶函数的函数。

    >>> def add1(x):
    ...     return x + 1
    >>> def times2(x):
    ...     return x * 2
    >>> def add3(x):
    ...     return x + 3
    >>> my_cycle = cycle(add1, times2, add3)
    >>> identity = my_cycle(0)
    >>> identity(5)
    5
    >>> add_one_then_double = my_cycle(2)
    >>> add_one_then_double(1)
    4
    >>> do_all_functions = my_cycle(3)
    >>> do_all_functions(2)
    9
    >>> do_more_than_a_cycle = my_cycle(4)
    >>> do_more_than_a_cycle(2)
    10
    >>> do_two_cycles = my_cycle(6)
    >>> do_two_cycles(1)
    19
    """
    "*** YOUR CODE HERE ***"

