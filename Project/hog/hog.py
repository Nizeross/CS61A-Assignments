"""Hog 骰子游戏。"""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100  # Hog 的目标是获得 100 分。

######################
# 第一阶段：模拟器 #
######################


def roll_dice(num_rolls, dice=six_sided):
    """模拟用 DICE 恰好掷 NUM_ROLLS 次（NUM_ROLLS > 0）。若没有任何一次结果为 1，返回所有结果之和；否则返回 1。

    num_rolls：掷骰次数。
    dice：模拟单次掷骰结果的函数，默认为六面骰子。
    """
    # 这些断言确保 num_rolls 是正整数。
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    # END PROBLEM 1


def boar_brawl(player_score, opponent_score):
    """返回根据 Boar Brawl 规则，掷 0 次骰子所获得的分数。

    player_score：当前玩家的总分。
    opponent_score：另一位玩家的总分。

    """
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    # END PROBLEM 2


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """当前玩家已有 PLAYER_SCORE 分、对手已有 OPPONENT_SCORE 分时，返回本回合掷 NUM_ROLLS 次骰子获得的分数。

    num_rolls：掷骰次数。
    player_score：当前玩家的总分。
    opponent_score：另一位玩家的总分。
    dice：模拟单次掷骰结果的函数。
    """
    # 保留这些断言，它们有助于检查错误。
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    # END PROBLEM 3


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """玩家以 PLAYER_SCORE 分开始本回合，然后掷 NUM_ROLLS 次 DICE；返回回合结束后的总分，忽略 Sus Fuss 规则。
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score

def is_prime(n):
    """返回 N 是否为质数。"""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def num_factors(n):
    """返回 N 的因数个数，包括 1 和 N 本身。"""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4

def sus_points(score):
    """返回考虑 Sus Fuss 规则后的玩家新分数。"""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4

def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """玩家以 PLAYER_SCORE 分开始本回合，然后掷 NUM_ROLLS 次 DICE；返回回合结束后的总分，包含 Sus Fuss 规则的影响。
    """
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4


def always_roll_5(score, opponent_score):
    """无论自己或对手得分多少，总是掷 5 次骰子的策略。
    """
    return 5


def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """模拟一局游戏并返回两位玩家的最终得分，玩家 0 的分数在前，玩家 1 的分数在后。

    例如，play(always_roll_5, always_roll_5, sus_update) 模拟一局双方每回合都选择掷 5 次骰子、并启用 Sus Fuss 规则的游戏。

    策略函数（例如 always_roll_5）接受当前玩家和对手的得分，返回当前玩家选择的掷骰次数。

    更新函数（例如 sus_update 或 simple_update）接受掷骰次数、当前玩家得分、对手得分以及用于模拟掷骰的骰子函数，返回当前玩家本回合行动后的新总分。

    strategy0：玩家 0 的策略。
    strategy1：玩家 1 的策略。
    update：双方共用的分数更新函数。
    score0：玩家 0 的初始分数。
    score1：玩家 1 的初始分数。
    dice：模拟掷骰的无参数函数。
    goal：达到该分数时游戏结束，产生胜者。
    """
    who = 0  # 即将行动的玩家：0（第一位）或 1（第二位）
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    # END PROBLEM 5
    return score0, score1


#######################
# 第二阶段：策略 #
#######################


def always_roll(n):
    """返回一个总是掷 N 次骰子的玩家策略。

    玩家策略是一个函数，接受两个总分（当前玩家的分数和对手的分数），返回当前玩家本回合的掷骰次数。

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """通常掷 5 次骰子；如果对手得分更高，则掷 6 次骰子的策略。

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # 多掷一次以追赶对手
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """返回 STRATEGY 在目标为 GOAL 分的游戏中，是否始终选择相同的掷骰次数。

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    # END PROBLEM 7


def make_averaged(original_function, times_called=1000):
    """返回一个函数，用于计算调用 ORIGINAL_FUNCTION 共 TIMES_CALLED 次的返回值平均数。

    实现此函数需要使用 *args 语法。

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # 10 个 4、10 个 2、10 个 5 和 10 个 1 的平均值
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, times_called=1000):
    """返回使单回合平均得分最大的掷骰次数（1 到 10）。假设骰子的结果总为正数。

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """若 strategy0 战胜 strategy1，返回 0，否则返回 1。"""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """返回 STRATEGY 对抗 BASELINE 的平均胜率，取先手（玩家 0）和后手（玩家 1）胜率的平均值。
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """运行一系列策略实验并报告结果。"""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6))) # 接近 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"



def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """若 Boar Brawl 至少能获得 THRESHOLD 分，此策略返回 0，否则返回 NUM_ROLLS。忽略 score 和 Sus Fuss。
    """
    # BEGIN PROBLEM 10
    return num_rolls  # 实现后删除此行。
    # END PROBLEM 10


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """若选择不掷骰子能使你的分数至少增加 threshold，此策略返回 0。"""
    # BEGIN PROBLEM 11
    return num_rolls  # 实现后删除此行。
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """简要描述你的最终策略。

    *** 在这里填写你的策略说明 ***
    """
    # BEGIN PROBLEM 12
    return 6  # 实现后删除此行。
    # END PROBLEM 12


##########################
# 命令行界面 #
##########################

# 注意：本节中的函数不需要修改。它使用了
# 课程中尚未讲到的 Python 特性。

@main
def run(*args):
    """读取命令行参数并调用相应函数。"""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()