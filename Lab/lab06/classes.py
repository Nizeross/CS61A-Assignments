# Lambda 魔法卡牌游戏！

import random

class Card:
    cardtype = 'Staff'

    def __init__(self, name, attack, defense):
        """
        创建一个具有名称、攻击力和防御力的 Card 对象。
        >>> staff_member = Card('staff', 400, 300)
        >>> staff_member.name
        'staff'
        >>> staff_member.attack
        400
        >>> staff_member.defense
        300
        >>> other_staff = Card('other', 300, 500)
        >>> other_staff.attack
        300
        >>> other_staff.defense
        500
        """
        "*** YOUR CODE HERE ***"

    def power(self, opponent_card):
        """
        威力的计算方式：（己方卡牌的攻击力）减去（对方卡牌的防御力）
        >>> staff_member = Card('staff', 400, 300)
        >>> other_staff = Card('other', 300, 500)
        >>> staff_member.power(other_staff)
        -100
        >>> other_staff.power(staff_member)
        0
        >>> third_card = Card('third', 200, 400)
        >>> staff_member.power(third_card)
        0
        >>> third_card.power(staff_member)
        -100
        """
        "*** YOUR CODE HERE ***"


    def effect(self, opponent_card, player, opponent):
        """
        卡牌默认没有特殊效果。
        """
        return

    def __repr__(self):
        """
        返回卡牌的可读字符串，格式为：<cardname>: <cardtype>, [<attack>, <defense>]
        """
        return '{}: {}, [{}, {}]'.format(self.name, self.cardtype, self.attack, self.defense)

    def copy(self):
        """
        返回此卡牌的副本。
        """
        return Card(self.name, self.attack, self.defense)

class Player:
    def __init__(self, deck, name):
        """初始化 Player 对象。玩家在游戏开始时从牌堆抽取 5 张牌。每轮再抽一张牌，并选择一张打出。
        >>> test_card = Card('test', 100, 100)
        >>> test_deck = Deck([test_card.copy() for _ in range(6)])
        >>> test_player = Player(test_deck, 'tester')
        >>> len(test_deck.cards)
        1
        >>> len(test_player.hand)
        5
        """
        self.deck = deck
        self.name = name
        "*** YOUR CODE HERE ***"

    def draw(self):
        """从玩家的牌堆抽一张牌，加入手牌。
        >>> test_card = Card('test', 100, 100)
        >>> test_deck = Deck([test_card.copy() for _ in range(6)])
        >>> test_player = Player(test_deck, 'tester')
        >>> test_player.draw()
        >>> len(test_deck.cards)
        0
        >>> len(test_player.hand)
        6
        """
        assert not self.deck.is_empty(), 'Deck is empty!'
        "*** YOUR CODE HERE ***"

    def play(self, index):
        """移除并返回玩家手牌中给定 INDEX 处的卡牌。
        >>> from cards import *
        >>> test_player = Player(standard_deck, 'tester')
        >>> ta1, ta2 = TACard("ta_1", 300, 400), TACard("ta_2", 500, 600)
        >>> tutor1, tutor2 = TutorCard("t1", 200, 500), TutorCard("t2", 600, 400)
        >>> test_player.hand = [ta1, ta2, tutor1, tutor2]
        >>> test_player.play(0) is ta1
        True
        >>> test_player.play(2) is tutor2
        True
        >>> len(test_player.hand)
        2
        """
        "*** YOUR CODE HERE ***"


    def display_hand(self):
        """
        向用户显示玩家当前的手牌。
        """
        print('Your hand:')
        for card_index, displayed_card in zip(range(len(self.hand)),[str(card) for card in self.hand]):
            indent = ' '*(5 - len(str(card_index)))
            print(card_index, indent + displayed_card)

    def play_random(self):
        """
        随机打出一张手牌。
        """
        return self.play(random.randrange(len(self.hand)))

######################
# 选做题 #
######################

class AICard(Card):
    cardtype = 'AI'

    def effect(self, opponent_card, player, opponent):
        """
        通过抽牌将牌堆顶部的两张牌加入手牌。完成本题代码后，将 implemented 设置为 True，以便打出 AICard 时打印说明文字。

        >>> from cards import *
        >>> player1, player2 = Player(standard_deck.copy(), 'p1'), Player(standard_deck.copy(), 'p2')
        >>> opponent_card = Card("other", 500, 500)
        >>> test_card = AICard("AI Card", 500, 500)
        >>> initial_deck_length = len(player1.deck.cards)
        >>> initial_hand_size = len(player1.hand)
        >>> test_card.effect(opponent_card, player1, player2)
        AI Card allows me to draw two cards!
        >>> initial_hand_size == len(player1.hand) - 2
        True
        >>> initial_deck_length == len(player1.deck.cards) + 2
        True
        """
        "*** YOUR CODE HERE ***"
        implemented = False
        # 你应在此行上方添加自己的实现。
        if implemented:
            print(f"{self.name} allows me to draw two cards!")

    def copy(self):
        """
        创建此卡牌的副本。
        """
        return AICard(self.name, self.attack, self.defense)

class TutorCard(Card):
    cardtype = 'Tutor'

    def effect(self, opponent_card, player, opponent):
        """
        以输掉本轮为代价，将手牌中第一张牌的副本加入手牌。如果没有手牌，则不添加卡牌，但仍输掉本轮。为实现后一个效果，Tutor 卡的威力应小于所有非 Tutor 卡。

        >>> from cards import *
        >>> player1, player2 = Player(standard_deck.copy(), 'p1'), Player(standard_deck.copy(), 'p2')
        >>> opponent_card = Card("other", 500, 500)
        >>> test_card = TutorCard("Tutor Card", 10000, 10000)
        >>> player1.hand = [Card("card1", 0, 100), Card("card2", 100, 0)]
        >>> test_card.effect(opponent_card, player1, player2)
        Tutor Card allows me to add a copy of a card to my hand!
        >>> print(player1.hand)
        [card1: Staff, [0, 100], card2: Staff, [100, 0], card1: Staff, [0, 100]]
        >>> player1.hand[0] is player1.hand[2] # 必须添加副本！
        False
        >>> player1.hand = []
        >>> test_card.effect(opponent_card, player1, player2)
        >>> print(player1.hand) # 没有可用卡牌时，不得添加卡牌
        []
        >>> test_card.power(opponent_card) < opponent_card.power(test_card)
        True
        """
        "*** YOUR CODE HERE ***"
        added = False
        # 你应在此行上方添加自己的实现。
        if added:
            print(f"{self.name} allows me to add a copy of a card to my hand!")

    "*** YOUR CODE HERE ***"


    def copy(self):
        """
        创建此卡牌的副本。
        """
        return TutorCard(self.name, self.attack, self.defense)

class TACard(Card):
    cardtype = 'TA'

    def effect(self, opponent_card, player, opponent, arg=None):
        """
        丢弃手牌中 power 最高的卡牌，并将被丢弃卡牌的攻击力和防御力分别加到此卡牌的对应属性上。

        >>> from cards import *
        >>> player1, player2 = Player(standard_deck.copy(), 'p1'), Player(standard_deck.copy(), 'p2')
        >>> opponent_card = Card("other", 500, 500)
        >>> test_card = TACard("TA Card", 500, 500)
        >>> player1.hand = []
        >>> test_card.effect(opponent_card, player1, player2) # 如果没有手牌，则不产生效果。
        >>> print(test_card.attack, test_card.defense)
        500 500
        >>> player1.hand = [Card("card1", 0, 100), TutorCard("tutor", 10000, 10000), Card("card3", 100, 0)]
        >>> test_card.effect(opponent_card, player1, player2) # 必须使用卡牌的 power 方法。
        TA Card discards card3 from my hand to increase its own power!
        >>> print(player1.hand)
        [card1: Staff, [0, 100], tutor: Tutor, [10000, 10000]]
        >>> print(test_card.attack, test_card.defense)
        600 500
        """
        "*** YOUR CODE HERE ***"
        best_card = None
        # 你应在此行上方添加自己的实现。
        if best_card:
            print(f"{self.name} discards {best_card.name} from my hand to increase its own power!")


    def copy(self):
        """
        创建此卡牌的副本。
        """
        return TACard(self.name, self.attack, self.defense)

class InstructorCard(Card):
    cardtype = 'Instructor'

    def effect(self, opponent_card, player, opponent, arg=None):
        """
        只要本轮结束时攻击力或防御力非负，该卡牌就能继续存活。在每轮开始时，它的攻击力和防御力各永久减少 1000。若存活，则重新加入手牌。

        >>> from cards import *
        >>> player1, player2 = Player(standard_deck.copy(), 'p1'), Player(standard_deck.copy(), 'p2')
        >>> opponent_card = Card("other", 500, 500)
        >>> test_card = InstructorCard("Instructor Card", 1000, 1000)
        >>> player1.hand = [Card("card1", 0, 100)]
        >>> test_card.effect(opponent_card, player1, player2)
        Instructor Card returns to my hand!
        >>> print(player1.hand) # 攻击力非负时存活
        [card1: Staff, [0, 100], Instructor Card: Instructor, [0, 0]]
        >>> player1.hand = [Card("card1", 0, 100)]
        >>> test_card.effect(opponent_card, player1, player2)
        >>> print(player1.hand)
        [card1: Staff, [0, 100]]
        >>> print(test_card.attack, test_card.defense)
        -1000 -1000
        """
        "*** YOUR CODE HERE ***"
        re_add = False
        # 你应在此行上方添加自己的实现。
        if re_add:
            print(f"{self.name} returns to my hand!")

    def copy(self):
        return InstructorCard(self.name, self.attack, self.defense)


########################################
# 请勿修改此行以下的任何内容 #
########################################

class Deck:
    def __init__(self, cards):
        """
        根据输入的卡牌列表创建牌堆。牌堆需要记录其中的卡牌，并支持随机抽出和移除一张牌。
        """
        self.cards = cards

    def draw(self):
        """
        从牌堆中随机选取并移除一张牌。
        """
        assert self.cards, 'The deck is empty!'
        rand_index = random.randrange(len(self.cards))
        return self.cards.pop(rand_index)

    def is_empty(self):
        return len(self.cards) == 0

    def copy(self):
        """
        创建此牌堆的副本。
        """
        return Deck([card.copy() for card in self.cards])

class Game:
    win_score = 8

    def __init__(self, player1, player2):
        """
        初始化一局 Lambda 魔法卡牌游戏。
        """
        self.player1, self.player2 = player1, player2
        self.p1_score = 0
        self.p2_score = 0

    def play_round(self, p1_card, p2_card):
        """
        两位玩家各选一张牌后，让这两张牌进行对战。
        """
        p1_card.effect(p2_card, self.player1, self.player2)
        p2_card.effect(p1_card, self.player2, self.player1)
        p1_power = p1_card.power(p2_card)
        p2_power = p2_card.power(p1_card)
        if p1_power > p2_power:
            # 玩家 1 赢得本轮。
            self.p1_score += 1
            result = 'won'
        elif p2_power > p1_power:
            # 玩家 2 赢得本轮。
            self.p2_score += 1
            result = 'lost'
        else:
            # 本轮平局。
            result = 'tied'
        # 向用户显示结果。
        print('You {} this round!'.format(result))
        print('{}\'s card: {}; Power: {}'.format(self.player1.name, p1_card, p1_power))
        print('Opponent\'s card: {}; Power: {}'.format(p2_card, p2_power))

    def game_won(self):
        """
        检查游戏是否结束；若已结束，确定获胜玩家。
        """
        if self.p1_score < self.win_score and self.p2_score < self.win_score:
            return 0
        return 1 if self.p1_score > self.p2_score else 2

    def display_scores(self):
        """
        向用户显示玩家的分数。
        """
        print('{}\'s score: {}'.format(self.player1.name, self.p1_score))
        print('Opponent\'s score: {}'.format(self.p2_score))