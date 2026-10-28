passphrase = 'REPLACE_THIS_WITH_PASSPHRASE'

def midsem_survey(p):
    """
    你不需要理解这段代码。
    >>> midsem_survey(passphrase)
    '2bf925d47c03503d3ebe5a6fc12d479b8d12f14c0494b43deba963a0'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()


class VendingMachine:
    """以指定价格售卖某种商品的自动售货机。

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Nothing left to vend. Please restock.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'Please add $10 more funds.'
    >>> v.add_funds(7)
    'Current balance: $7'
    >>> v.vend()
    'Please add $3 more funds.'
    >>> v.add_funds(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.add_funds(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.add_funds(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    def __init__(self, product, price):
        """设置商品、价格和其他实例属性。"""
        "*** YOUR CODE HERE ***"

    def restock(self, n):
        """将库存增加 n，返回描述更新后库存的消息。

        例如：Current candy stock: 3（当前糖果库存：3）
        """
        "*** YOUR CODE HERE ***"

    def add_funds(self, n):
        """若机器缺货，返回一条提示用户补货并退还其 n 美元的消息。

        例如：Nothing left to vend. Please restock. Here is your $4.（已售罄，请补货，退还您 4 美元。）

        否则，将余额增加 n，返回描述更新后余额的消息。

        例如：Current balance: $4（当前余额：4 美元）
        """
        "*** YOUR CODE HERE ***"

    def vend(self):
        """若库存和余额充足，则售出商品并返回消息，同时更新库存和余额。

        例如：Here is your candy and $2 change.（这是您的糖果及 2 美元找零。）

        否则，返回提示如何解决问题的消息。

        例如：Nothing left to vend. Please restock. 或 Please add $3 more funds.（已售罄，请补货；或请再投入 3 美元。）
        """
        "*** YOUR CODE HERE ***"


def store_digits(n):
    """将正整数 n 的各位数字存入链表。

    >>> s = store_digits(1)
    >>> s
    Link(1)
    >>> store_digits(2345)
    Link(2, Link(3, Link(4, Link(5))))
    >>> store_digits(876)
    Link(8, Link(7, Link(6)))
    >>> store_digits(2450)
    Link(2, Link(4, Link(5, Link(0))))
    >>> store_digits(20105)
    Link(2, Link(0, Link(1, Link(0, Link(5)))))
    >>> # 检查是否使用了受限函数
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(store_digits)))
    >>> print("Do not use str or reversed!") if any([r in cleaned for r in ["str", "reversed"]]) else None
    """
    "*** YOUR CODE HERE ***"


def deep_map_mut(func, s):
    """原地修改深层嵌套链表 s，将其中每个元素替换为对该元素调用 func 的结果。不得创建新的 Link 节点（因此不能使用 Link 的构造函数）。

    不返回修改后的 Link 对象。

    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> print(link1)
    <3 <4> 5 6>
    >>> # 在调用 deep_map_mut 之前，禁止创建新的 Link 节点
    >>> Link.__init__, hold = lambda *args: print("Do not create any new Links."), Link.__init__
    >>> try:
    ...     deep_map_mut(lambda x: x * x, link1)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(link1)
    <9 <16> 25 36>
    """
    "*** YOUR CODE HERE ***"


def two_list(vals, counts):
    """
    根据传入的两个列表返回链表。假设 vals 和 counts 等长；vals 中的元素表示值，counts 中对应元素表示该值应在最终链表中出现的次数。假设 counts 中所有元素均大于 0，两个列表均至少有一个元素。
    >>> a = [1, 3]
    >>> b = [1, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(3))
    >>> a = [1, 3, 2]
    >>> b = [2, 2, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(1, Link(3, Link(3, Link(2)))))
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

