class Account:
    """账户包含余额 balance 和持有人 holder。

    >>> a = Account('John')
    >>> a.deposit(10)
    10
    >>> a.balance
    10
    >>> a.interest
    0.02
    >>> a.time_to_retire(10.25)  # 10 -> 10.2 -> 10.404
    2
    >>> a.balance                # 调用 time_to_retire 方法不应改变余额
    10
    >>> a.time_to_retire(11)     # 10 -> 10.2 -> ... -> 11.040808032
    5
    >>> a.time_to_retire(100)
    117
    """
    max_withdrawal = 10
    interest = 0.02

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds"
        if amount > self.max_withdrawal:
            return "Can't withdraw that amount"
        self.balance = self.balance - amount
        return self.balance

    def time_to_retire(self, amount):
        """返回余额增长到 amount 所需的年数。"""
        assert self.balance > 0 and amount > 0 and self.interest > 0
        "*** YOUR CODE HERE ***"


class FreeChecking(Account):
    """取款收费的银行账户，但前两次取款免费！

    >>> ch = FreeChecking('Jack')
    >>> ch.balance = 20
    >>> ch.withdraw(100)  # 第一次免费。虽然取款失败，仍占用一次免费取款机会
    'Insufficient funds'
    >>> ch.withdraw(3)    # 第二次取款也免费
    17
    >>> ch.balance
    17
    >>> ch.withdraw(3)    # 现在需要收费，因为 free_withdrawals 只有 2 次
    13
    >>> ch.withdraw(3)
    9
    >>> ch2 = FreeChecking('John')
    >>> ch2.balance = 10
    >>> ch2.withdraw(3) # 不收手续费
    7
    >>> ch.withdraw(3)  # ch 仍然收取手续费
    5
    >>> ch.withdraw(5)  # 余额不足以支付手续费和取款金额
    'Insufficient funds'
    """
    withdraw_fee = 1
    free_withdrawals = 2

    "*** YOUR CODE HERE ***"


def without(s, i):
    """返回一个与 s 相似的新链表，但去掉索引 i 处的元素。

    >>> s = Link(3, Link(5, Link(7, Link(9))))
    >>> without(s, 0)
    Link(5, Link(7, Link(9)))
    >>> without(s, 2)
    Link(3, Link(5, Link(9)))
    >>> without(s, 4)           # 索引 4 不存在，因此保留 s 的全部元素。
    Link(3, Link(5, Link(7, Link(9))))
    >>> without(s, 4) is not s  # 确保创建了副本
    True
    """
    "*** YOUR CODE HERE ***"


def duplicate_link(s, val):
    """原地修改 s，使每个等于 val 的元素后面都再跟一个 val。

    >>> x = Link(5, Link(4, Link(5)))
    >>> duplicate_link(x, 5)
    >>> x
    Link(5, Link(5, Link(4, Link(5, Link(5)))))
    >>> y = Link(2, Link(4, Link(6, Link(8))))
    >>> duplicate_link(y, 10)
    >>> y
    Link(2, Link(4, Link(6, Link(8))))
    >>> z = Link(1, Link(2, (Link(2, Link(3)))))
    >>> duplicate_link(z, 2) # 确保相邻的两个值为 val 的节点都被复制
    >>> z
    Link(1, Link(2, Link(2, Link(2, Link(2, Link(3))))))
    """
    "*** YOUR CODE HERE ***"


class Link:
    """一个链表。

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # 显示 repr(s) 的内容
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # 打印 str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

