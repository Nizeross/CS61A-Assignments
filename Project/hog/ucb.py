"""UCB 模块包含 UC Berkeley 61A 项目专用的函数。"""

import code
import functools
import inspect
import re
import signal
import sys


def main(fn):
    """使用命令行参数调用 fn。用作装饰器。

    main 装饰器用于标记程序入口函数。例如，

    @main
    def my_run_function():
        # function body

    使用此装饰器代替通常的 __name__ == "__main__" 判断。
    """
    if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
        args = sys.argv[1:] # 从命令行中去掉脚本名称
        fn(*args) # 调用主函数
    return fn

_PREFIX = ''
def trace(fn):
    """一个装饰器：每次调用函数时，打印函数名、参数和返回值。例如，

    @trace
    def compute_something(x, y):
        # function body
    """
    @functools.wraps(fn)
    def wrapped(*args, **kwds):
        global _PREFIX
        reprs = [repr(e) for e in args]
        reprs += [repr(k) + '=' + repr(v) for k, v in kwds.items()]
        log('{0}({1})'.format(fn.__name__, ', '.join(reprs)) + ':')
        _PREFIX += '    '
        try:
            result = fn(*args, **kwds)
            _PREFIX = _PREFIX[:-4]
        except Exception as e:
            log(fn.__name__ + ' exited via exception')
            _PREFIX = _PREFIX[:-4]
            raise
        # 在这里打印返回值。
        log('{0}({1}) -> {2}'.format(fn.__name__, ', '.join(reprs), result))
        return result
    return wrapped


def log(message):
    """打印一条带缩进的消息（与 trace 配合使用）。"""
    print(_PREFIX + re.sub('\n', '\n' + _PREFIX, str(message)))


def log_current_line():
    """打印当前代码行的信息。"""
    frame = inspect.stack()[1]
    log('Current line: File "{f[1]}", line {f[2]}, in {f[3]}'.format(f=frame))


def interact(msg=None):
    """在当前环境中启动交互式解释器会话。

    Unix：按 <Control>-D 退出交互会话并恢复正常执行。Windows：按 <Control>-Z 后再按 <Enter> 退出交互会话并恢复正常执行。
    """
    # 在当前命名空间中对命令求值
    frame = inspect.currentframe().f_back
    namespace = frame.f_globals.copy()
    namespace.update(frame.f_locals)

    # 遇到中断时退出
    def handler(signum, frame):
        print()
        exit(0)
    signal.signal(signal.SIGINT, handler)

    if not msg:
        _, filename, line, _, _, _ = inspect.stack()[1]
        msg = 'Interacting at File "{0}", line {1} \n'.format(filename, line)
        msg += '    Unix:    <Control>-D continues the program; \n'
        msg += '    Windows: <Control>-Z <Enter> continues the program; \n'
        msg += '    exit() or <Control>-C exits the program'

    code.interact(msg, None, namespace)