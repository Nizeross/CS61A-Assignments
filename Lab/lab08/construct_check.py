from ast import parse, NodeVisitor, Name

# 仅用于面向学生的错误消息
_NAMES = {
    'Add': '+',
    'And': 'and',
    'Assert': 'assert',
    'Assign': '=',
    'AnnAssign': '=',
    'AugAssign': 'op=',
    'BitAnd': '&',
    'BitOr': '|',
    'BitXor': '^',
    'Break': 'break',
    'Recursion': 'recursive call',
    'ClassDef': 'class',
    'Continue': 'continue',
    'Del': 'del',
    'Delete': 'delete',
    'Dict': '{...}',
    'DictComp': '{...}',
    'Div': '/',
    'Ellipsis': '...',
    'Eq': '==',
    'ExceptHandler': 'except',
    'ExtSlice': '[::]',
    'FloorDiv': '//',
    'For': 'for',
    'FunctionDef': 'def',
    'Filter': 'filter',
    'GeneratorExp': '(... for ...)',
    'Global': 'global',
    'Gt': '>',
    'GtE': '>=',
    'If': 'if',
    'IfExp': '...if...else...',
    'Import': 'import',
    'ImportFrom': 'from ... import ...',
    'In': 'in',
    'Index': '...[...]',
    'Invert': '~',
    'Is': 'is',
    'IsNot': 'is not ',
    'LShift': '<<',
    'Lambda': 'lambda',
    'List': '[...]',
    'ListComp': '[...for...]',
    'Lt': '<',
    'LtE': '<=',
    'Mod': '%',
    'Mult': '*',
    'NamedExpr': ':=',
    'Nonlocal': 'nonlocal',
    'Not': 'not',
    'NotEq': '!=',
    'NotIn': 'not in',
    'Or': 'or',
    'Pass': 'pass',
    'Pow': '**',
    'RShift': '>>',
    'Raise': 'raise',
    'Return': 'return',
    'Set': '{ ... } (set)',
    'SetComp': '{ ... for ... } (set)',
    'Slice': '[ : ]',
    'Starred': '',
    'Str': 'str',
    'Sub': '-',
    'Subscript': '[]',
    'Try': 'try',
    'Tuple': '(... , ... )',
    'UAdd': '+',
    'USub': '-',
    'While': 'while',
    'With': 'with',
    'Yield': 'yield',
    'YieldFrom': 'yield from',
}

def check(source_file, checked_funcs, disallow, source=None):
    """检查 SOURCE 中由 CHECKED_FUNCS 指定的函数，确保不含类型名位于 DISALLOW 中的 AST 节点（DISALLOW 支持 in 运算）。SOURCE 默认为 SOURCE_FILE 文件的内容。CHECKED_FUNCS 可以是表示单个函数名的字符串，也可以是其他支持 in 运算的对象；包含 __main__ 时表示检查整个模块。打印每个违规节点的报告，仅在未发现违规节点时返回 True。AST 类型名见 ast.__dir__()。特殊名称 'Recursion' 用于检查显式递归调用，即 NAME(...) 形式中 NAME 是外层 def 定义的名称。"""
    return ExclusionChecker(disallow).check(source_file, checked_funcs, source)

class ExclusionChecker(NodeVisitor):
    """用于检查程序指定部分是否使用了禁用语法结构的 AST 访问器。ExclusionChecker(EXC) 检查类型名位于序列或集合 EXC 中的 AST 节点是否存在。其 check 方法遍历源文件中的指定函数，检查是否使用了这些节点类型。"""

    def __init__(self, disallow=()):
        """DISALLOW 是初始默认的禁用节点类型名称列表。"""
        self._disallow = set(disallow)
        self._checking = False
        self._errs = 0

    def generic_visit(self, node):
        if self._checking and type(node).__name__ in self._disallow:
            self._report(node)
        super().generic_visit(node)

    def visit_Module(self, node):
        if "__main__" in self._checked_funcs:
            self._checking = True
            self._checked_name = self._source_file
        super().generic_visit(node)

    def visit_Call(self, node):
        if 'Recursion' in self._disallow and \
           type(node.func) is Name and \
           node.func.id in self._func_nest:
            self._report(node, "should not be recursive")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self._func_nest.append(node.name)
        if self._checking:
            self.generic_visit(node)
        elif node.name in self._checked_funcs:
            self._checked_name = "Function " + node.name
            checking0 = self._checking
            self._checking = True
            super().generic_visit(node)
            self._checking = checking0
        self._func_nest.pop()

    def _report(self, node, msg=None):
        node_name = _NAMES.get(type(node).__name__, type(node).__name__)
        if msg is None:
            msg = "should not contain '{}'".format(node_name)
        print("{} {}".format(self._checked_name, msg))
        self._errs += 1

    def errors(self):
        """返回最近一次调用 check 时发现的禁用语法结构数量。"""
        return self._errs

    def check(self, source_file, checked_funcs, disallow=None, source=None):
        """检查 SOURCE 中由 CHECKED_FUNCS 指定的函数，确保不含类型名位于 DISALLOW 中的 AST 节点（DISALLOW 支持成员包含测试）。SOURCE 默认为 SOURCE_FILE 文件的内容。DISALLOW 默认为构造函数收到的参数；若本次提供该参数，也会更新默认值。CHECKED_FUNCS 可以是表示单个函数名的字符串，也可以是其他支持 in 运算的对象；包含 __main__ 时表示检查整个模块。打印每个违规节点的报告，仅在未发现违规节点时返回 True。AST 类型名见 ast.__dir__()。特殊名称 'Recursion' 用于检查显式递归调用，即 NAME(...) 形式中 NAME 是外层 def 定义的名称。"""

        self._checking = False
        self._source_file = source_file
        self._func_nest = []
        if type(checked_funcs) is str:
            self._checked_funcs = { checked_funcs }
        else:
            self._checked_funcs = set(checked_funcs)
        if disallow is not None:
            self._disallow = set(disallow)
        if source is None:
            with open(source_file, 'r', errors='ignore') as inp:
                source = inp.read()
        p = parse(source, source_file)
        self._errs = 0

        self.visit(p)
        return self._errs == 0