class Transaction:
    def __init__(self, id, before, after):
        self.id = id
        self.before = before
        self.after = after

    def changed(self):
        """返回该笔交易是否改变了余额。"""
        "*** YOUR CODE HERE ***"

    def report(self):
        """返回描述该笔交易的字符串。

        >>> Transaction(3, 20, 10).report()
        '3: decreased 20->10'
        >>> Transaction(4, 20, 50).report()
        '4: increased 20->50'
        >>> Transaction(5, 50, 50).report()
        '5: no change'
        """
        msg = 'no change'
        if self.changed():
            "*** YOUR CODE HERE ***"
        return str(self.id) + ': ' + msg

class BankAccount:
    """记录交易历史的银行账户。

    >>> a = BankAccount('Eric')
    >>> a.deposit(100)    # a 的第 0 笔交易
    100
    >>> b = BankAccount('Erica')
    >>> a.withdraw(30)    # a 的第 1 笔交易
    70
    >>> a.deposit(10)     # a 的第 2 笔交易
    80
    >>> b.deposit(50)     # b 的第 0 笔交易
    50
    >>> b.withdraw(10)    # b 的第 1 笔交易
    40
    >>> a.withdraw(100)   # a 的第 3 笔交易
    'Insufficient funds'
    >>> len(a.transactions)
    4
    >>> len([t for t in a.transactions if t.changed()])
    3
    >>> for t in a.transactions:
    ...     print(t.report())
    0: increased 0->100
    1: decreased 100->70
    2: increased 70->80
    3: no change
    >>> b.withdraw(100)   # b 的第 2 笔交易
    'Insufficient funds'
    >>> b.withdraw(30)    # b 的第 3 笔交易
    10
    >>> for t in b.transactions:
    ...     print(t.report())
    0: increased 0->50
    1: decreased 50->40
    2: no change
    3: decreased 40->10
    """

    # *** 你需要修改此类中的多个位置 ***

    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        """将账户余额增加 amount，把存款记入交易历史，并返回新余额。
        """
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        """将账户余额减少 amount，把取款记入交易历史，并返回新余额。
        """
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance


class Email:
    """电子邮件具有以下实例属性：

        msg（str）：邮件内容；sender（Client）：发送邮件的客户端；recipient_name（str）：收件人（另一个客户端）的名称。
    """
    def __init__(self, msg, sender, recipient_name):
        self.msg = msg
        self.sender = sender
        self.recipient_name = recipient_name

class Server:
    """每个 Server 都有一个名为 clients 的实例属性，它是从客户端名称到客户端对象的字典。
    """
    def __init__(self):
        self.clients = {}

    def send(self, email):
        """将邮件添加到收件客户端的收件箱。email 是 Email 类的实例。
        """
        ____.inbox.append(email)

    def register_client(self, client):
        """将客户端添加到 clients 映射（从客户端名称到客户端实例的字典）。client 是 Client 类的实例。
        """
        ____[____] = ____

class Client:
    """客户端包含服务器 server、名称 name（str）和收件箱 inbox（list）。

    >>> s = Server()
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> a.compose('Hello, World!', 'Bob')
    >>> b.inbox[0].msg
    'Hello, World!'
    >>> a.compose('CS 61A Rocks!', 'Bob')
    >>> len(b.inbox)
    2
    >>> b.inbox[1].msg
    'CS 61A Rocks!'
    >>> b.inbox[1].sender.name
    'Alice'
    """
    def __init__(self, server, name):
        self.inbox = []
        self.server = server
        self.name = name
        server.register_client(____)

    def compose(self, message, recipient_name):
        """向收件人发送内容为给定消息的邮件。"""
        email = Email(message, ____, ____)
        self.server.send(email)


class Mint:
    """铸币厂通过压印年份来制造硬币。

    update 方法将铸币厂的年份印记设置为 Mint.present_year。

    >>> mint = Mint()
    >>> mint.year
    2024
    >>> dime = mint.create(Dime)
    >>> dime.year
    2024
    >>> Mint.present_year = 2104  # 时间流逝
    >>> nickel = mint.create(Nickel)
    >>> nickel.year     # 铸币厂尚未更新年份印记
    2024
    >>> nickel.worth()  # 5 美分 +（80 - 50 年）
    35
    >>> mint.update()   # 铸币厂的年份更新为 2104
    >>> Mint.present_year = 2179     # 又过了一段时间
    >>> mint.create(Dime).worth()    # 10 美分 +（75 - 50 年）
    35
    >>> Mint().create(Dime).worth()  # 新的铸币厂使用当前年份
    10
    >>> dime.worth()     # 10 美分 +（155 - 50 年）
    115
    >>> Dime.cents = 20  # 提升所有 dime 硬币的面值！
    >>> dime.worth()     # 20 美分 +（155 - 50 年）
    125
    """
    present_year = 2024

    def __init__(self):
        self.update()

    def create(self, coin):
        "*** YOUR CODE HERE ***"

    def update(self):
        "*** YOUR CODE HERE ***"

class Coin:
    cents = None # 由子类提供，而非由 Coin 类本身提供

    def __init__(self, year):
        self.year = year

    def worth(self):
        "*** YOUR CODE HERE ***"

class Nickel(Coin):
    cents = 5

class Dime(Coin):
    cents = 10

