"""打字测试的实现"""

from utils import (
    lower,
    split,
    remove_punctuation,
    lines_from_file,
    count,
    deep_convert_to_tuple,
)
from ucb import main, interact, trace
from datetime import datetime
import random


###########
# 第一阶段 #
###########


def pick(paragraphs, select, k):
    """返回 PARAGRAPHS 中使 SELECT 返回 True 的第 K 个段落（从索引 0 开始）。如果符合条件的段落不足以取到该索引，则返回空字符串。

    参数：
    paragraphs：表示段落的字符串列表。
    select：对满足条件的段落返回 True 的函数。
    k：整数索引。

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    # END PROBLEM 1


def about(subject):
    """返回一个函数，接受一个段落，并判断该段落是否包含 SUBJECT 中的某个单词。

    参数：subject：与某个主题相关的单词列表。

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in subject]), "subjects should be lowercase."

    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    # END PROBLEM 2


def accuracy(typed, source):
    """比较 TYPED 与 SOURCE 中对应的单词，返回准确率（正确输入的单词百分比）。

    参数：
    typed：可能含有输入错误的字符串。
    source：没有错误的参考字符串。

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    # END PROBLEM 3


def wpm(typed, elapsed):
    """返回 TYPED 字符串的每分钟打字词数（WPM）。

    参数：
    typed：输入的字符串。
    elapsed：经过的时间，单位为秒。

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, "Elapsed time must be positive"
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    # END PROBLEM 4


################
# 第四阶段（附加题）#
################


def memo(f):
    """通用的记忆化缓存装饰器。"""
    cache = {}

    def memoized(*args):
        immutable_args = deep_convert_to_tuple(args)  # 将 *args 转换为元组表示
        if immutable_args not in cache:
            result = f(*immutable_args)
            cache[immutable_args] = result
            return result
        return cache[immutable_args]

    return memoized


def memo_diff(diff_function):
    """记忆化缓存函数。"""
    cache = {}

    def memoized(typed, source, limit):
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        # END PROBLEM EC

    return memoized


###########
# 第二阶段 #
###########


def autocorrect(typed_word, word_list, diff_function, limit):
    """根据 DIFF_FUNCTION，返回 WORD_LIST 中与 TYPED_WORD 差异最小的元素。若多个单词并列，则返回在 WORD_LIST 中最靠前的一个。若差异大于 LIMIT，则返回 TYPED_WORD。

    参数：
    typed_word：可能存在拼写错误的单词字符串。
    word_list：参考单词的字符串列表。
    diff_function：量化两个单词差异的函数。
    limit：数值上限。

    >>> ten_diff = lambda w1, w2, limit: 10 # 始终返回 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # 检查首字符是否相同
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    # END PROBLEM 5


def furry_fixes(typed, source, limit):
    """用于自动纠错的差异函数：统计将 TYPED 变为 SOURCE 需要替换的字母数，再加上两者长度之差的绝对值，返回结果。

    参数：
    typed：起始单词。
    source：期望得到的目标单词字符串。
    limit：需要修改的字符数上限。

    >>> big_limit = 10
    >>> furry_fixes("nice", "rice", big_limit)    # 替换：n -> r
    1
    >>> furry_fixes("range", "rungs", big_limit)  # 替换：a -> u、e -> s
    2
    >>> furry_fixes("pill", "pillage", big_limit) # 无需替换，长度相差 3。
    3
    >>> furry_fixes("roses", "arose", big_limit)  # 替换：r -> a、o -> r、s -> o、e -> s、s -> e
    5
    >>> furry_fixes("rose", "hello", big_limit)   # 替换：r -> h、o -> e、s -> l、e -> l；长度相差 1。
    5
    """
    # BEGIN PROBLEM 6
    assert False, 'Remove this line'
    # END PROBLEM 6


def minimum_mewtations(typed, source, limit):
    """用于自动纠错的差异函数，计算从 TYPED 到 SOURCE 的编辑距离。接受字符串 TYPED、字符串 SOURCE 和数值 LIMIT。

    参数：
    typed：起始单词。
    source：期望得到的目标单词字符串。
    limit：编辑次数上限。

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    assert False, 'Remove this line'
    if ___________: # 在这里处理基本情况；可以根据需要增加其他基本情况。
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END
    # 在下面处理递归情况
    if ___________: # 可以自行删除或添加其他情况
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END
    else:
        add = ... # 补全这些行
        remove = ...
        substitute = ...
        # BEGIN
        "*** YOUR CODE HERE ***"
        # END


# 忽略下面这一行
minimum_mewtations = count(minimum_mewtations)


def final_diff(typed, source, limit):
    """接受字符串 TYPED、字符串 SOURCE 和数值 LIMIT 的差异函数。如果实现此函数，系统将使用它。"""
    assert False, "Remove this line to use your final_diff function."


FINAL_DIFF_LIMIT = 6  # 在此填写你的 LIMIT 值


###########
# 第三阶段 #
###########


def report_progress(typed, source, user_id, upload):
    """向多人服务器上传你的 id 和当前进度报告，并返回当前进度。

    参数：
    typed：目前已输入的单词列表。
    source：参考文本的单词列表。
    user_id：当前用户的数值标识。
    upload：向多人服务器上传进度的函数。

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # 上面的函数按 ID: __, Progress: __ 的格式显示进度
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    # END PROBLEM 8


def time_per_word(words, timestamps_per_player):
    """返回字典 {'words': words, 'times': times}，其中 times 是列表的列表，记录每位玩家输入 words 中每个单词所用的时长。

    参数：
    words：按输入顺序排列的单词列表。
    timestamps_per_player：时间戳列表的列表，包含每位玩家开始输入的时刻，以及完成每个单词的时刻。

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> result = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> result['words']
    ['collar', 'plush', 'blush', 'repute']
    >>> result['times']
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    tpp = timestamps_per_player  # 使用更短的名称以便书写
    # BEGIN PROBLEM 9
    times = []  # 可以删除此行
    # END PROBLEM 9
    return {'words': words, 'times': times}


def fastest_words(words_and_times):
    """返回列表的列表，分别表示每位玩家在哪些单词上输入最快。

    参数：words_and_times：字典 {'words': words, 'times': times}，其中 words 是输入的单词列表，times 是每位玩家输入各单词所用时长组成的列表的列表。

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words({'words': ['Just', 'have', 'fun'], 'times': [p0, p1]})
    [['have', 'fun'], ['Just']]
    >>> p0  # 不得修改输入列表
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    check_words_and_times(words_and_times)  # 检查输入的结构是否正确
    words, times = words_and_times['words'], words_and_times['times']
    player_indices = range(len(times))  # 包含每位玩家的索引
    word_indices = range(len(words))    # 包含每个单词的索引
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    # END PROBLEM 10


def check_words_and_times(words_and_times):
    """检查 words_and_times 是否为 {'words': words, 'times': times} 形式的字典，且 times 的每个元素都是与 words 等长的数值列表。
    """
    assert 'words' in words_and_times and 'times' in words_and_times and len(words_and_times) == 2
    words, times = words_and_times['words'], words_and_times['times']
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all([isinstance(i, (int, float)) for t in times for i in t]), "times lists should contain numbers"
    assert all([len(t) == len(words) for t in times]), "There should be one word per time."


def get_time(times, player_num, word_index):
    """给定 time_per_word 返回的时长列表的列表，返回玩家 player_num 输入索引 word_index 处单词所用的时间。"""
    num_players = len(times)
    num_words = len(times[0])
    assert word_index < len(times[0]), f"word_index {word_index} outside of 0 to {num_words-1}"
    assert player_num < len(times), f"player_num {player_num} outside of 0 to {num_players-1}"
    return times[player_num][word_index]


enable_multiplayer = False  # 准备好比赛时，改为 True。

##########################
# 命令行界面 #
##########################


def run_typing_test(topics):
    """在命令行中测量打字速度和准确率。"""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    random.shuffle(paragraphs)
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(typed, elapsed))
        print("Accuracy:        ", accuracy(typed, source))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """读取命令行参数并调用相应函数。"""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)