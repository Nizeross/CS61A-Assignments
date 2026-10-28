"""打字图形界面的 Web 服务器。"""
import base64
import os
import random
import string

import cats
from gui_files.common_server import Server, route, sendto, start
from multiplayer import multiplayer

PORT = 31415
DEFAULT_SERVER = "https://cats.cs61a.org"
GUI_FOLDER = "gui_files/"
PARAGRAPH_PATH = "./data/sample_paragraphs.txt"
WORDS_LIST = cats.lines_from_file("data/words.txt")
WORDS_SET = set(WORDS_LIST)
LETTER_SETS = [(w, set(w)) for w in WORDS_LIST]
SIMILARITY_LIMIT = 2


@route
def request_paragraph(topics=None):
    """返回一个随机段落。"""
    paragraphs = cats.lines_from_file(PARAGRAPH_PATH)
    random.shuffle(paragraphs)
    select = cats.about(topics) if topics else lambda x: True
    return cats.pick(paragraphs, select, 0)


@route
def analyze(prompted_text, typed_text, start_time, end_time):
    """返回 [wpm, accuracy]（速度和准确率）。"""
    return {
        "wpm": cats.wpm(typed_text, end_time - start_time),
        "accuracy": cats.accuracy(typed_text, prompted_text),
    }


def similar(w, v, n):
    """判断 W 与 V 的交集是否至少同时包含 |W|-N 个和 |V|-N 个元素。"""
    intersect = len(w.intersection(v))
    return intersect >= len(w) - n and intersect >= len(v) - n


@route
def autocorrect(word=""):
    """使用当前可用的最佳评分函数调用 autocorrect。"""
    raw_word = word
    word = cats.lower(cats.remove_punctuation(raw_word))
    if word in WORDS_SET or word == "":
        return raw_word

    # 使用启发式方法选择待评分的候选单词。
    letters = set(word)
    candidates = [w for w, s in LETTER_SETS if similar(s, letters, SIMILARITY_LIMIT)]

    # 尝试不同的差异函数，直到找到一个不会抛出异常的函数。
    for fn in [cats.final_diff, cats.minimum_mewtations, cats.furry_fixes]:
        try:
            guess = cats.autocorrect(word, candidates, fn, SIMILARITY_LIMIT)
            return reformat(guess, raw_word)
        except BaseException:
            pass

    return raw_word


def reformat(word, raw_word):
    """调整 WORD 的大小写和标点格式，使其与 RAW_WORD 一致。"""
    # 处理大小写
    if raw_word != "" and raw_word[0].isupper():
        word = word.capitalize()

    # 找到原始单词的边界
    first = 0
    while first < len(raw_word) and raw_word[first] in string.punctuation:
        first += 1
    last = len(raw_word) - 1
    while last > first and raw_word[last] in string.punctuation:
        last -= 1

    # 给单词加回两侧的标点符号
    if raw_word != word:
        word = raw_word[:first] + word
        word = word + raw_word[last + 1 :]

    return word


###############
# 多人模式 #
###############


@route
def request_id():
    if not cats.enable_multiplayer:
        return
    return Server.provide_id()


@route
def report_progress(id, typed, prompt):
    """向多人服务器报告进度，并返回该进度。"""
    typed = typed.split()  # 由单词字符串组成的列表
    prompt = prompt.split()  # 由单词字符串组成的列表

    return cats.report_progress(typed, prompt, id, sendto(Server.set_progress))


@route
def fastest_words(prompt, targets):
    """返回描述本场比赛的 word_speed 值列表。"""
    words = prompt.split()
    progress = Server.request_all_progress(targets=targets)
    start_times = [p[0][1] for p in progress]
    times_per_player = [[p[1] - s for p in ps] for s, ps in zip(start_times, progress)]
    match = cats.time_per_word(words, times_per_player)
    return cats.fastest_words(match)


multiplayer.create_multiplayer_server()

###############
# 网站图标 #
###############


@route
@route("favicon.ico")
def favicon():
    favicon_folder = "favicons"
    favicons = os.listdir(favicon_folder)
    path = os.path.join(favicon_folder, random.choice(favicons))
    with open(path, "rb") as f:
        data = f.read()
    image_b64 = base64.b64encode(data).decode("utf-8")
    return "data:image/png;base64," + image_b64


if __name__ == "__main__" or os.environ.get("ENV") == "prod":
    app = start(PORT, DEFAULT_SERVER, GUI_FOLDER, multiplayer.db_init)