#####################################
# 可选：添加用户界面 #
#####################################

from hog import *

########################
# 打印游戏事件 #
########################


def play_and_print(strategy0, strategy1):
    """模拟一局游戏，并打印模拟过程中发生的事件。"""
    final0, final1 = play(printing_strategy(0, strategy0),
                          printing_strategy(1, strategy1),
                          sus_update_and_print, 0, 0,
                          printing_dice(six_sided))
    print('The final score is Player 0:', final0, 'vs Player 1:', final1)


def printing_strategy(who, strategy):
    """返回一个同时打印玩家分数和选择的策略。

    （这里可能打印出语法不规范的 "rolls 1 dice..."，但没有关系。）

    >>> strategy0 = printing_strategy(0, always_roll_5)
    >>> strategy0(10, 20)
    The score is 10 to 20 and Player 0 rolls 5 dice...
    5
    >>> strategy1 = printing_strategy(1, always_roll_5)
    >>> strategy1(8, 16)
    The score is 16 to 8 and Player 1 rolls 5 dice...
    5
    """
    assert who == 0 or who == 1, 'the player must be 0 or 1'

    def choose_and_print(score, opponent_score):
        "A strategy function that also prints."
        if who == 0:
            score0, score1 = score, opponent_score
        else:
            score0, score1 = opponent_score, score
        num_rolls = strategy(score, opponent_score)
        print('The score is', score0, 'to', score1, 'and Player', who,
              'rolls', num_rolls, 'dice...')
        return num_rolls
    return choose_and_print


def printing_dice(dice):
    """返回一个骰子函数，它还会打印结果和一个空格。"""
    def dice_and_print():
        "A dice function that also prints."
        outcome = dice()
        print(outcome, end=' ')
        return outcome
    return dice_and_print


def sus_update_and_print(num_rolls, player_score, opponent_score, dice):
    """返回更新后的分数，打印分数变化，并在触发 Sus Fuss 时打印提示。

    >>> d = printing_dice(make_test_dice(4, 5, 3))
    >>> sus_update_and_print(3, 9, 99, d)
      [ 4 5 3 ] => 12; 9 + 12 = 21 triggering **Sus Fuss**, increasing to 23
    23
    """
    print('  [', end=" ")
    turn_score = take_turn(num_rolls, player_score, opponent_score, dice)  # 打印骰子结果
    print('] =>', turn_score, end='; ')
    print(player_score, '+', turn_score, '=', player_score + turn_score, end='')
    score = turn_score + player_score
    sus_score = sus_points(score)
    if sus_score != score:
        score = sus_score
        print(' triggering **Sus Fuss**, increasing to', score)
    else:
        print()  # 此 print 结束当前行，不添加额外文字
    return score


########################
# 接收用户输入 #
########################


def get_int(prompt, lower, upper):
    """返回满足 lower <= i <= upper 的整数 i。"""
    choice = input(prompt)
    while not choice.isnumeric() or int(choice) < lower or int(choice) > upper:
        print('Please enter an integer from', lower, 'to', upper)
        choice = input(prompt)
    return int(choice)


def interactive_strategy(who):
    """返回一个由用户输入掷骰次数的策略。"""
    def strategy(score, opponent_score):
        print('Player', who, ', you have', score, 'and your opponent has', opponent_score)
        choice = get_int('How many dice will you roll? ', 0, 10)
        return choice
    return strategy


####################
# 进行游戏 #
####################


def play_with(num_players):
    """进行一局有 NUM_PLAYERS 位真人交互玩家的游戏。"""
    if num_players == 0:
        play_and_print(always_roll_5, always_roll_5)
    elif num_players == 1:
        play_and_print(interactive_strategy(0), always_roll_5)
    elif num_players == 2:
        play_and_print(interactive_strategy(0), interactive_strategy(1))
    else:
        print('num_players must be 0, 1, or 2.')


@main
def run(*args):
    """选择玩家人数并开始游戏。"""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--num_players', '-n', type=int, default=0,
                        help='How many interactive players (0, 1, or 2)')
    args = parser.parse_args()
    play_with(args.num_players)