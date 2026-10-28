"""scheme_tokens 模块提供 tokenize_line 和 tokenize_lines 函数，用于将字符串（或生成字符串的迭代器）转换为词法单元列表（或生成此类列表的迭代器）。词法单元可以是：

  * 数字（用 int 或 float 表示）
    * 布尔值（用 bool 表示）
    * 符号（用字符串表示）
    * 分隔符，包括括号、点和单引号

此文件也包含课程中尚未涉及的 Scheme 特性，例如 Scheme 字符串。
"""

from ucb import main
import sys

_NUMERAL_STARTS = set("0123456789") | set('+-.')
_SYMBOL_CHARS = (set('!$%&*/:<=>?@^_~') | set("abcdefghijklmnopqrstuvwxyz") |
                 set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") | _NUMERAL_STARTS)
_STRING_DELIMS = set('"')
_WHITESPACE = set(' \t\n\r')
_SINGLE_CHAR_TOKENS = set("()[]'`")
_TOKEN_END = _WHITESPACE | _SINGLE_CHAR_TOKENS | _STRING_DELIMS | {',', ',@'}
DELIMITERS = _SINGLE_CHAR_TOKENS | {'.', ',', ',@'}
_MAX_TOKEN_LENGTH = 50


def chain(*iters):
    for iter in iters:
        yield from iter


def valid_symbol(s):
    """返回 s 是否为结构正确的符号。"""
    if len(s) == 0:
        return False
    for c in s:
        if c not in _SYMBOL_CHARS:
            return False
    return True

def next_candidate_token(line, k):
    """返回元组 (tok, k')：tok 是 line 中从位置 k 或其后开始的、可能构成词法单元的下一个子串（假设它能通过合法性检查），k' 是该词法单元之后的位置。没有更多词法单元时返回 (None, len(line))。"""
    while k < len(line):
        c = line[k]
        if c == ';':
            return None, len(line)
        elif c in _WHITESPACE:
            k += 1
        elif c in _SINGLE_CHAR_TOKENS:
            if c == ']': c = ')'
            if c == '[': c = '('
            return c, k+1
        elif c == '#':  # 布尔值 #t 和 #f
            return line[k:k+2], min(k+2, len(line))
        elif c == ',': # 取消引用；检查是否带有 @
            if k+1 < len(line) and line[k+1] == '@':
                return ',@', k+2
            return c, k+1
        elif c in _STRING_DELIMS:
            if k+1 < len(line) and line[k+1] == c: # Scheme 中没有三引号
                return c+c, k+2
            s = ""
            k += 1
            while k < len(line):
                c = line[k]
                if c == "\"":
                    check_token_length_warning(s, len(s) + 2)
                    return "\"" + s + "\"", k+1
                elif c == "\\":
                    if k + 1 == len(line):
                        raise SyntaxError("String ended abruptly")
                    next = line[k + 1]
                    if next == "n":
                        s += "\n"
                    else:
                        s += next
                    k += 2
                else:
                    s += c
                    k += 1
            raise SyntaxError("String ended abruptly")
        else:
            j = k
            while j < len(line) and line[j] not in _TOKEN_END:
                j += 1
            check_token_length_warning(line[k:j], min(j, len(line)) - k)
            return line[k:j], min(j, len(line))
    return None, len(line)

def tokenize_line(line):
    """返回 line 中的 Scheme 词法单元列表，不包含注释和空白。"""
    result = []
    text, i = next_candidate_token(line, 0)
    while text is not None:
        if text in DELIMITERS:
            result.append(text)
        elif text == '#t' or text.lower() == 'true':
            result.append(True)
        elif text == '#f' or text.lower() == 'false':
            result.append(False)
        elif text == 'nil':
            result.append(text)
        elif text[0] in _SYMBOL_CHARS:
            number = False
            if text[0] in _NUMERAL_STARTS:
                try:
                    result.append(int(text))
                    number = True
                except ValueError:
                    try:
                        result.append(float(text))
                        number = True
                    except ValueError:
                        pass
            if not number:
                if valid_symbol(text):
                    result.append(text.lower())
                else:
                    raise ValueError("invalid numeral or symbol: {0}".format(text))
        elif text[0] in _STRING_DELIMS:
            result.append(text)
        else:
            error_message = [
                "warning: invalid token: {0}".format(text),
                " " * 4       + line,
                " " * (i + 4) + "^"
            ]
            raise ValueError("\n".join(error_message))
        text, i = next_candidate_token(line, i)
    return result

def check_token_length_warning(token, length):
    if length > _MAX_TOKEN_LENGTH:
        import warnings
        warnings.warn("Token {} has exceeded the maximum token length {}".format(token, _MAX_TOKEN_LENGTH, length))

def tokenize_lines(inp):
    """返回一个迭代器：对可迭代输入序列 inp 中的每一行，生成一个词法单元列表。"""
    return (tokenize_line(line) for line in inp)

def count_tokens(inp):
    """统计 inp 中非分隔符词法单元的数量。"""
    return len(list(chain(*tokenize_lines(inp))))

@main
def run(*args):
    import argparse
    parser = argparse.ArgumentParser(description='Count Scheme tokens.')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='input file to be counted')
    args = parser.parse_args()
    print('counted', count_tokens(args.file), 'tokens')