HW_SOURCE_FILE=__file__


def insert_items(s, before, after):
    """在 s 中每次出现的 before 后插入 after，然后返回 s。

    >>> test_s = [1, 5, 8, 5, 2, 3]
    >>> new_s = insert_items(test_s, 5, 7)
    >>> new_s
    [1, 5, 7, 8, 5, 7, 2, 3]
    >>> test_s
    [1, 5, 7, 8, 5, 7, 2, 3]
    >>> new_s is test_s
    True
    >>> double_s = [1, 2, 1, 2, 3, 3]
    >>> double_s = insert_items(double_s, 3, 4)
    >>> double_s
    [1, 2, 1, 2, 3, 4, 3, 4]
    >>> large_s = [1, 4, 8]
    >>> large_s2 = insert_items(large_s, 4, 4)
    >>> large_s2
    [1, 4, 4, 8]
    >>> large_s3 = insert_items(large_s2, 4, 6)
    >>> large_s3
    [1, 4, 6, 4, 6, 8]
    >>> large_s3 is large_s
    True
    """
    "*** YOUR CODE HERE ***"


def group_by(s, fn):
    """返回一个由列表组成的字典，这些列表合起来包含 s 的所有元素。每个列表对应的键，是对该列表中任意元素调用 fn 得到的值。

    >>> group_by([12, 23, 14, 45], lambda p: p // 10)
    {1: [12, 14], 2: [23], 4: [45]}
    >>> group_by(range(-3, 4), lambda x: x * x)
    {9: [-3, 3], 4: [-2, 2], 1: [-1, 1], 0: [0]}
    """
    grouped = {}
    for ____ in ____:
        key = ____
        if key in grouped:
            ____
        else:
            grouped[key] = ____
    return grouped


def count_occurrences(t, n, x):
    """返回迭代器 t 的前 n 个元素中等于 x 的元素个数。

    >>> s = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> count_occurrences(s, 10, 9)
    3
    >>> t = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> count_occurrences(t, 3, 10)
    2
    >>> u = iter([3, 2, 2, 2, 1, 2, 1, 4, 4, 5, 5, 5])
    >>> count_occurrences(u, 1, 3)  # 只迭代经过 3
    1
    >>> count_occurrences(u, 3, 2)  # 只迭代经过 2、2、2
    3
    >>> list(u)                     # 确保迭代器恰好前进了指定步数
    [1, 2, 1, 4, 4, 5, 5, 5]
    >>> v = iter([4, 1, 6, 6, 7, 7, 6, 6, 2, 2, 2, 5])
    >>> count_occurrences(v, 6, 6)
    2
    """
    "*** YOUR CODE HERE ***"


def repeated(t, k):
    """返回迭代器 t 中第一个连续出现 k 次的值，并尽可能少地对 t 调用 next。

    >>> s = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(s, 2)
    9
    >>> t = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(t, 3)
    8
    >>> u = iter([3, 2, 2, 2, 1, 2, 1, 4, 4, 5, 5, 5])
    >>> repeated(u, 3)
    2
    >>> repeated(u, 3)
    5
    >>> v = iter([4, 1, 6, 6, 7, 7, 8, 8, 2, 2, 2, 5])
    >>> repeated(v, 3)
    2
    """
    assert k > 1
    "*** YOUR CODE HERE ***"


def sprout_leaves(t, leaves):
    """在原树 t 的每个叶节点处，添加标签来自 leaves 的新叶节点，返回得到的树。

    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(t1)
    1
      2
      3
    >>> new1 = sprout_leaves(t1, [4, 5])
    >>> print_tree(new1)
    1
      2
        4
        5
      3
        4
        5

    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(t2)
    1
      2
        3
    >>> new2 = sprout_leaves(t2, [6, 1, 2])
    >>> print_tree(new2)
    1
      2
        3
          6
          1
          2
    """
    "*** YOUR CODE HERE ***"


def partial_reverse(s, start):
    """原地反转列表从 start 到末尾的部分。

    >>> a = [1, 2, 3, 4, 5, 6, 7]
    >>> partial_reverse(a, 2)
    >>> a
    [1, 2, 7, 6, 5, 4, 3]
    >>> partial_reverse(a, 5)
    >>> a
    [1, 2, 7, 6, 5, 3, 4]
    """
    "*** YOUR CODE HERE ***"



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

