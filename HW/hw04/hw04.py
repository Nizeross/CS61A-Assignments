def shuffle(s):
    """返回一个新列表，将 s 的前半部分和后半部分交错排列。

    >>> shuffle(range(6))
    [0, 3, 1, 4, 2, 5]
    >>> letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    >>> shuffle(letters)
    ['a', 'e', 'b', 'f', 'c', 'g', 'd', 'h']
    >>> shuffle(shuffle(letters))
    ['a', 'c', 'e', 'g', 'b', 'd', 'f', 'h']
    >>> letters  # 不应修改原列表
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    """
    assert len(s) % 2 == 0, 'len(seq) must be even'
    "*** YOUR CODE HERE ***"


def deep_map(f, s):
    """在嵌套列表 s 中，将所有非列表元素 x 替换为 f(x)。

    >>> six = [1, 2, [3, [4], 5], 6]
    >>> deep_map(lambda x: x * x, six)
    >>> six
    [1, 4, [9, [16], 25], 36]
    >>> # 检查是否没有创建新列表
    >>> s = [3, [1, [4, [1]]]]
    >>> s1 = s[1]
    >>> s2 = s1[1]
    >>> s3 = s2[1]
    >>> deep_map(lambda x: x + 1, s)
    >>> s
    [4, [2, [5, [2]]]]
    >>> s1 is s[1]
    True
    >>> s2 is s1[1]
    True
    >>> s3 is s2[1]
    True
    """
    "*** YOUR CODE HERE ***"


HW_SOURCE_FILE=__file__


def planet(mass):
    """构造一个具有指定质量的星球。"""
    assert mass > 0
    "*** YOUR CODE HERE ***"

def mass(p):
    """选取星球的质量。"""
    assert is_planet(p), 'must call mass on a planet'
    "*** YOUR CODE HERE ***"

def is_planet(p):
    """判断 p 是否为星球。"""
    return type(p) == list and len(p) == 2 and p[0] == 'planet'

def examples():
    t = mobile(arm(1, planet(2)),
               arm(2, planet(1)))
    u = mobile(arm(5, planet(1)),
               arm(1, mobile(arm(2, planet(3)),
                             arm(3, planet(2)))))
    v = mobile(arm(4, t), arm(2, u))
    return t, u, v

def total_mass(m):
    """返回 m 的总质量，m 可以是星球或活动雕塑。

    >>> t, u, v = examples()
    >>> total_mass(t)
    3
    >>> total_mass(u)
    6
    >>> total_mass(v)
    9
    """
    if is_planet(m):
        return mass(m)
    else:
        assert is_mobile(m), "must get total mass of a mobile or a planet"
        return total_mass(end(left(m))) + total_mass(end(right(m)))

def balanced(m):
    """返回 m 是否平衡。

    >>> t, u, v = examples()
    >>> balanced(t)
    True
    >>> balanced(v)
    True
    >>> p = mobile(arm(3, t), arm(2, u))
    >>> balanced(p)
    False
    >>> balanced(mobile(arm(1, v), arm(1, p)))
    False
    >>> balanced(mobile(arm(1, p), arm(1, v)))
    False
    >>> from construct_check import check
    >>> # 通过禁止索引操作，检查是否违反抽象屏障
    >>> check(HW_SOURCE_FILE, 'balanced', ['Index'])
    True
    """
    "*** YOUR CODE HERE ***"


def berry_finder(t):
    """若 t 包含值为 'berry' 的节点，返回 True，否则返回 False。

    >>> scrat = tree('berry')
    >>> berry_finder(scrat)
    True
    >>> sproul = tree('roots', [tree('branch1', [tree('leaf'), tree('berry')]), tree('branch2')])
    >>> berry_finder(sproul)
    True
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> berry_finder(numbers)
    False
    >>> t = tree(1, [tree('berry',[tree('not berry')])])
    >>> berry_finder(t)
    True
    """
    "*** YOUR CODE HERE ***"


HW_SOURCE_FILE=__file__


def max_path_sum(t):
    """返回树中从根到叶节点的最大路径和。
    >>> t = tree(1, [tree(5, [tree(1), tree(3)]), tree(10)])
    >>> max_path_sum(t) # 1, 10
    11
    >>> t2 = tree(5, [tree(4, [tree(1), tree(3)]), tree(2, [tree(10), tree(3)])])
    >>> max_path_sum(t2) # 5, 2, 10
    17
    """
    "*** YOUR CODE HERE ***"


def mobile(left, right):
    """用左臂和右臂构造一个活动雕塑（mobile）。"""
    assert is_arm(left), "left must be an arm"
    assert is_arm(right), "right must be an arm"
    return ['mobile', left, right]

def is_mobile(m):
    """返回 m 是否为活动雕塑。"""
    return type(m) == list and len(m) == 3 and m[0] == 'mobile'

def left(m):
    """选取活动雕塑的左臂。"""
    assert is_mobile(m), "must call left on a mobile"
    return m[1]

def right(m):
    """选取活动雕塑的右臂。"""
    assert is_mobile(m), "must call right on a mobile"
    return m[2]

def arm(length, mobile_or_planet):
    """构造一个臂：一根末端悬挂活动雕塑或星球的定长杆。"""
    assert is_mobile(mobile_or_planet) or is_planet(mobile_or_planet)
    return ['arm', length, mobile_or_planet]

def is_arm(s):
    """返回 s 是否为臂。"""
    return type(s) == list and len(s) == 3 and s[0] == 'arm'

def length(s):
    """选取臂的长度。"""
    assert is_arm(s), "must call length on an arm"
    return s[1]

def end(s):
    """选取臂末端悬挂的活动雕塑或星球。"""
    assert is_arm(s), "must call end on an arm"
    return s[2]



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

