def hailstone(n):
    """
    依次生成从 n 开始的冰雹序列元素。到达序列末尾后，无限生成 1。

    >>> hail_gen = hailstone(10)
    >>> [next(hail_gen) for _ in range(10)]
    [10, 5, 16, 8, 4, 2, 1, 1, 1, 1]
    >>> next(hail_gen)
    1
    """
    "*** YOUR CODE HERE ***"


def merge(a, b):
    """
    返回一个生成器，按递增顺序生成生成器 a 和 b 的全部元素，且不重复。

    >>> def sequence(start, step):
    ...     while True:
    ...         yield start
    ...         start += step
    >>> a = sequence(2, 3) # 2, 5, 8, 11, 14, ...
    >>> b = sequence(3, 2) # 3, 5, 7, 9, 11, 13, 15, ...
    >>> result = merge(a, b) # 2, 3, 5, 7, 8, 9, 11, 13, 14, 15
    >>> [next(result) for _ in range(10)]
    [2, 3, 5, 7, 8, 9, 11, 13, 14, 15]
    """
    a_val, b_val = next(a), next(b)
    while True:
        if a_val == b_val:
            "*** YOUR CODE HERE ***"
        elif a_val < b_val:
            "*** YOUR CODE HERE ***"
        else:
            "*** YOUR CODE HERE ***"


def stair_ways(n):
    """
    生成爬上 n 级台阶的所有方案，每次爬 1 级或 2 级。

    >>> list(stair_ways(0))
    [[]]
    >>> s_w = stair_ways(4)
    >>> sorted([next(s_w) for _ in range(5)])
    [[1, 1, 1, 1], [1, 1, 2], [1, 2, 1], [2, 1, 1], [2, 2]]
    >>> list(s_w) # 确保没有生成多余的值
    []
    """
    "*** YOUR CODE HERE ***"


def yield_paths(t, value):
    """
    生成 t 中从根节点到标签为 value 的节点的所有路径，每条路径用列表表示。

    >>> t1 = tree(1, [tree(2, [tree(3), tree(4, [tree(6)]), tree(5)]), tree(5)])
    >>> print_tree(t1)
    1
      2
        3
        4
          6
        5
      5
    >>> next(yield_paths(t1, 6))
    [1, 2, 4, 6]
    >>> path_to_5 = yield_paths(t1, 5)
    >>> sorted(list(path_to_5))
    [[1, 2, 5], [1, 5]]

    >>> t2 = tree(0, [tree(2, [t1])])
    >>> print_tree(t2)
    0
      2
        1
          2
            3
            4
              6
            5
          5
    >>> path_to_2 = yield_paths(t2, 2)
    >>> sorted(list(path_to_2))
    [[0, 2], [0, 2, 1, 2]]
    """
    if label(t) == value:
        yield ____
    for b in branches(t):
        for ____ in ____:
            yield ____



# 树的数据抽象

def tree(label, branches=[]):
    """用给定的标签值和分支列表构造一棵树。"""
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    """返回树的标签值。"""
    return tree[0]

def branches(tree):
    """返回给定树的分支列表。"""
    return tree[1:]

def is_tree(tree):
    """如果给定对象是有效的树，返回 True，否则返回 False。"""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    """如果给定树的分支列表为空，返回 True，否则返回 False。
    """
    return not branches(tree)

def print_tree(t, indent=0):
    """打印树的表示形式；每个节点的缩进空格数为它距根节点的深度乘以二。

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def copy_tree(t):
    """返回 t 的副本。仅用于测试。

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

