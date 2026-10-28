#!/usr/bin/env python

# Licensed under the MIT license

# 使用 Python 内置适配器的简易 SQLite 命令行工具。

import codecs
import io
import os
import sys
import sqlite3
import time
import warnings

try: FileNotFoundError
except NameError: FileNotFoundError = OSError

if str != bytes: buffer = bytes
if str != bytes: unicode = str

try: import msvcrt
except ImportError: msvcrt = None

CP_UTF8 = 65001
pythonapi = None
if msvcrt:
	import ctypes
	(BOOL, DWORD, HANDLE, UINT) = (ctypes.c_long, ctypes.c_ulong, ctypes.c_void_p, ctypes.c_uint)
	GetConsoleCP = ctypes.WINFUNCTYPE(UINT)(('GetConsoleCP', ctypes.windll.kernel32))
	SetConsoleCP = ctypes.WINFUNCTYPE(BOOL, UINT)(('SetConsoleCP', ctypes.windll.kernel32))
	GetConsoleOutputCP = ctypes.WINFUNCTYPE(UINT)(('GetConsoleOutputCP', ctypes.windll.kernel32))
	SetConsoleOutputCP = ctypes.WINFUNCTYPE(BOOL, UINT)(('SetConsoleOutputCP', ctypes.windll.kernel32))
	GetConsoleMode = ctypes.WINFUNCTYPE(BOOL, HANDLE, ctypes.POINTER(DWORD), use_last_error=True)(('GetConsoleMode', ctypes.windll.kernel32))
	GetNumberOfConsoleInputEvents = ctypes.WINFUNCTYPE(BOOL, HANDLE, ctypes.POINTER(DWORD), use_last_error=True)(('GetNumberOfConsoleInputEvents', ctypes.windll.kernel32))
	ReadConsoleW = ctypes.WINFUNCTYPE(BOOL, HANDLE, ctypes.c_void_p, DWORD, ctypes.POINTER(DWORD), ctypes.c_void_p, use_last_error=True)(('ReadConsoleW', ctypes.windll.kernel32))
	WriteConsoleW = ctypes.WINFUNCTYPE(BOOL, HANDLE, ctypes.c_void_p, DWORD, ctypes.POINTER(DWORD), ctypes.c_void_p, use_last_error=True)(('WriteConsoleW', ctypes.windll.kernel32))
	class Py_buffer(ctypes.Structure): _fields_ = [('buf', ctypes.c_void_p), ('obj', ctypes.py_object), ('len', ctypes.c_ssize_t), ('itemsize', ctypes.c_ssize_t), ('readonly', ctypes.c_int), ('ndim', ctypes.c_int), ('format', ctypes.c_char_p), ('shape', ctypes.POINTER(ctypes.c_ssize_t)), ('strides', ctypes.POINTER(ctypes.c_ssize_t)), ('suboffsets', ctypes.POINTER(ctypes.c_ssize_t))] + ([('smalltable', ctypes.c_ssize_t * 2)] if sys.version_info[0] <= 2 else []) + [('internal', ctypes.c_void_p)]
	try: from ctypes import pythonapi
	except ImportError: pass
if pythonapi:
	def getbuffer(b, writable):
		arr = Py_buffer()
		pythonapi.PyObject_GetBuffer(ctypes.py_object(b), ctypes.byref(arr), ctypes.c_int(writable))
		try: buf = (ctypes.c_ubyte * arr.len).from_address(arr.buf)
		finally: pythonapi.PyBuffer_Release(ctypes.byref(arr))
		return buf

ENCODING = 'utf-8'

if sys.version_info[0] < 3:
	class NotASurrogateError(Exception): pass
	def surrogateescape_handler(exc):
		# 来源：https://github.com/PythonCharmers/python-future/blob/aef57391c0cd58bf840dff5e2bc2c8c0f5b0a1b4/src/future/utils/surrogateescape.py
		mystring = exc.object[exc.start:exc.end]
		try:
			if isinstance(exc, UnicodeDecodeError):
				decoded = []
				for ch in mystring:
					if isinstance(ch, int):
						code = ch
					else:
						code = ord(ch)
					if 0x80 <= code <= 0xFF:
						decoded.append(unichr(0xDC00 + code))
					elif code <= 0x7F:
						decoded.append(unichr(code))
					else:
						raise NotASurrogateError()
				decoded = str().join(decoded)
			elif isinstance(exc, UnicodeEncodeError):
				decoded = []
				for ch in mystring:
					code = ord(ch)
					if not 0xD800 <= code <= 0xDCFF:
						raise NotASurrogateError()
					if 0xDC00 <= code <= 0xDC7F:
						decoded.append(unichr(code - 0xDC00))
					elif code <= 0xDCFF:
						decoded.append(unichr(code - 0xDC00))
					else:
						raise NotASurrogateError()
				decoded = str().join(decoded)
			else:
				raise exc
		except NotASurrogateError:
			raise exc
		return (decoded, exc.end)
	codecs.register_error('surrogateescape', surrogateescape_handler)

def exception_encode(ex, codec):
	if str == bytes:
		reduced = ex.__reduce__()
		ex = reduced[0](*tuple(map(lambda arg: codec.decode(arg)[0] if isinstance(arg, bytes) else arg, reduced[1])))
	return ex

def sql_commands(read_line):
	delims = ['"', "'", ';', '--']
	counter = 0
	in_string = None
	j = i = 0
	prev_line = None
	line = None
	concat = []
	while True:
		if line is None:
			while True:  # 处理预处理指令
				counter += 1
				not_in_the_middle_of_any_input = not in_string and i == j and all(map(lambda chunk_: len(chunk_) == 0, concat))
				line = read_line(counter - 1, not_in_the_middle_of_any_input, prev_line)
				empty_string = line[:0] if line is not None else line
				prev_line = line
				if not line:
					break
				if not_in_the_middle_of_any_input and line.startswith("."):
					yield line
					line = None
				else:
					break
			if not line:
				break
			j = i = 0
		if j < len(line):
			(j, delim) = min(map(lambda pair: pair if pair[0] >= 0 else (len(line), pair[1]), map(lambda d: (line.find(d, j), d), in_string or delims if in_string != '--' else "\n")))
			if i < j: concat.append(line[i:j]); i = j
			if not in_string:
				if j < len(line):
					j += len(delim)
					if delim == ';':
						i = j
						concat.append(line[j : j + len(delim)])    # 确保分隔符与字符串的类型相同（隐式转换可能使二者类型不同）
						# 跳过后续空格，直到遇到换行符
						while j < len(line):
							delim = line[j:j+1]
							if not delim.isspace(): break
							j += 1
							if delim == "\n": break
						if i < j: concat.append(line[i:j]); i = j
						yield empty_string.join(concat)
						del concat[:]
					else:
						in_string = delim
			else:
				if j < len(line):
					ch = line[j:j+1]
					assert ch == in_string or in_string == '--'
					j += 1
					i = j
					concat.append(ch)
					in_string = None
		else:
			if i < j: concat.append(line[i:j]); i = j
			line = None

class WindowsConsoleIOMixin(object):
	# 从 Windows 8 开始，Windows 上 ReadFile() 对 Ctrl+C 的处理存在问题。相关背景资料如下：
	#   https://stackoverflow.com/a/43260436
	#   https://github.com/microsoft/terminal/issues/334
	# 我们尽可能使用 ReadConsole，因此不受影响，但了解这些信息仍有帮助。
	def __init__(self, fd):
		assert isatty(fd), "file descriptor must refer to a console (note that on Windows, NUL satisfies isatty(), but is not a console)"
		self.fd = fd
		self.handle = msvcrt.get_osfhandle(fd)
	def fileno(self): return self.fd
	def isatty(self): return isatty(self.fd)
	def seekable(self): return False
	def readable(self): return GetNumberOfConsoleInputEvents(self.handle, ctypes.byref(DWORD(0))) != 0
	def writable(self): n = DWORD(0); return WriteConsoleW(self.handle, ctypes.c_void_p(), n, ctypes.byref(n), ctypes.c_void_p()) != 0
	def readwcharsinto(self, buf, n):
		nr = DWORD(n)
		old_error = ctypes.get_last_error()
		ctypes.set_last_error(0)
		success = ReadConsoleW(self.handle, buf, nr, ctypes.byref(nr), ctypes.c_void_p())
		error = ctypes.get_last_error()
		ctypes.set_last_error(old_error)
		if not success: raise ctypes.WinError(error)
		ERROR_OPERATION_ABORTED = 995
		if nr.value == 0 and error == ERROR_OPERATION_ABORTED:
			# 这似乎会触发挂起的 KeyboardInterrupt？
			time.sleep(1.0 / (1 << 64))
			raise KeyboardInterrupt()  # 如果 Python 没有抛出该异常，我们可以主动抛出
		return nr.value
	def writewchars(self, buf, n):
		nw = DWORD(n)
		if not WriteConsoleW(self.handle, buf, nw, ctypes.byref(nw), ctypes.c_void_p()):
			raise ctypes.WinError()
		return nw.value

class WindowsConsoleRawIO(WindowsConsoleIOMixin, io.RawIOBase):
	def readinto(self, b):
		wordsize = ctypes.sizeof(ctypes.c_wchar)
		return self.readwcharsinto(getbuffer(b, True), len(b) // wordsize) * wordsize
	def write(self, b):
		wordsize = ctypes.sizeof(ctypes.c_wchar)
		return self.writewchars(getbuffer(b, False), len(b) // wordsize) * wordsize

class WindowsConsoleTextIO(WindowsConsoleIOMixin, io.TextIOBase):
	buf = None
	buffered = unicode()
	translate = True
	def getbuf(self, ncodeunits):
		buf = self.buf
		if buf is None or len(buf) < ncodeunits:
			self.buf = buf = ctypes.create_unicode_buffer(ncodeunits)
		return buf
	@staticmethod  # 不要让子类重写此方法；可以重写调用它的方法
	def do_read(self, nchars, translate_newlines):
		prenewline = os.linesep[:-1]
		newline = os.linesep[-1:]
		empty = os.linesep[:0]
		if nchars is None or nchars < -1: nchars = -1
		ncodeunits = nchars if nchars >= 0 else io.DEFAULT_BUFFER_SIZE  # 单位不匹配，但不影响，因为这里会循环处理
		buf = None
		istart = 0
		while True:
			iend = self.buffered.find(newline, istart, min(istart + nchars, len(self.buffered)) if nchars >= 0 else None) if newline is not None else nchars
			if iend >= 0: iend += len(newline) if newline is not None else 0
			if 0 <= iend <= len(self.buffered):
				break
			if buf is None: buf = self.getbuf(ncodeunits)
			istart = len(self.buffered)
			chunk = buf[:self.readwcharsinto(buf, ncodeunits)]
			if translate_newlines: chunk = chunk.replace(prenewline, empty)
			if chunk.startswith('\x1A'):  # 在 Windows 上，行首输入文件结束符（Ctrl+Z）会丢弃缓冲区剩余的全部内容
				iend = istart
				break
			# Windows 上 Python 2 和 Python 3 的行为不同：Python 2 的 sys.stdin.readline() 在字符串中间遇到 EOF 时只会删除下一个字符！这里不模拟这种行为。
			self.buffered += chunk  # 这里依赖 Python 的拼接优化，不自行实现；这样每次迭代时 self.buffered 都保持有效，便于处理异常
		result = self.buffered[:iend]
		self.buffered = self.buffered[iend:]
		return result
	def read(self, nchars=-1): return WindowsConsoleTextIO.do_read(self, nchars, None, self.translate)
	def readline(self, nchars=-1): return WindowsConsoleTextIO.do_read(self, nchars, self.translate)
	def write(self, text): buf = ctypes.create_unicode_buffer(text); return self.writewchars(buf, max(len(buf) - 1, 0))

def wrap_windows_console_io(stream, is_output):
	fd = None
	if stream is not None and sys.version_info[0] < 3 and msvcrt and (is_output or pythonapi) and isatty(stream):
		try: fd = stream.fileno()
		except io.UnsupportedOperation: pass
	result = stream
	if fd is not None:
		f = GetConsoleOutputCP if is_output else GetConsoleCP
		if not f or f() != CP_UTF8:
			try:
				if True or is_output:
					result = WindowsConsoleTextIO(fd)
				else:
					result = io.TextIOWrapper((io.BufferedWriter if is_output else io.BufferedReader)(WindowsConsoleRawIO(fd)), 'utf-16-le', 'strict', line_buffering=True)
			except IOError: pass
	return result

class NonOwningTextIOWrapper(io.TextIOWrapper):
	def __init__(self, base_textiowrapper, **kwargs):
		assert isinstance(base_textiowrapper, io.TextIOWrapper)
		self.base = base_textiowrapper  # 必须保留此对象的引用，以免它被关闭
		super(NonOwningTextIOWrapper, self).__init__(base_textiowrapper.buffer, **kwargs)
	def close(self):
		super(NonOwningTextIOWrapper, self).flush()

def wrap_unicode_stdio(stream, is_writer, encoding):  # 在此函数返回的流被释放之前，绝不能直接使用底层流
	if isinstance(stream, io.TextIOWrapper):
		stream.flush()  # 重新包装之前，确保缓冲区中没有残留数据
		none = object()
		kwargs = {}
		for key in ['encoding', 'errors', 'newline', 'line_buffering', 'write_through']:
			value = getattr(stream, 'newlines' if key == 'newline' else key, none)
			if value is not none:
				kwargs[key] = value
		kwargs['encoding'] = encoding
		result = NonOwningTextIOWrapper(stream, **kwargs)
	elif 'PYTHONIOENCODING' not in os.environ and str == bytes and stream in (sys.stdin, sys.stdout, sys.stderr):
		result = (codecs.getwriter if is_writer else codecs.getreader)(encoding)(stream)
	else:
		result = stream
	return result

class StringEscapeParser(object):
	def __init__(self):
		import re
		self.pattern = re.compile("\"((?:[^\"\\n]+|\\\\.)*)(?:\"|$)|\'([^\'\\n]*)(?:\'|$)|(\\S+)")
		self.escape_pattern = re.compile("\\\\(.)", re.DOTALL)
	@staticmethod
	def escape_replacement(m):
		text = m.group(1)
		if text == "\\": text = "\\"
		elif text == "/": text = "\n"
		elif text == "n": text = "\n"
		elif text == "r": text = "\r"
		elif text == "t": text = "\t"
		elif text == "v": text = "\v"
		elif text == "f": text = "\f"
		elif text == "a": text = "\a"
		elif text == "b": text = "\b"
		return text
	def __call__(self, s):
		escape_pattern = self.escape_pattern
		escape_replacement = self.escape_replacement
		result = []
		for match in self.pattern.finditer(s):
			[m1, m2, m3] = match.groups()
			if m1 is not None: result.append(escape_pattern.sub(escape_replacement, m1))
			if m2 is not None: result.append(m2)
			if m3 is not None: result.append(escape_pattern.sub(escape_replacement, m3))
		return result

class Database(object):
	def __init__(self, name, *args, **kwargs):
		self.connection = sqlite3.connect(name, *args, **kwargs)
		self.cursor = self.connection.cursor()
		self.name = name  # 仅在创建游标之后才给 name 赋值

def isatty(file_or_fd):
	result = True
	method = getattr(file_or_fd, 'isatty', None) if not isinstance(file_or_fd, int) else None  # 此检查仅用于优化
	if method is not None:
		try: tty = method()
		except io.UnsupportedOperation: tty = None
		result = result and tty is not None and tty
	method = getattr(file_or_fd, 'fileno', None) if not isinstance(file_or_fd, int) else None  # 此检查仅用于优化
	if method is not None:
		try: fd = method()
		except io.UnsupportedOperation: fd = None
		result = result and fd is not None and os.isatty(fd) and (not msvcrt or GetConsoleMode(msvcrt.get_osfhandle(fd), ctypes.byref(DWORD(0))) != 0)
	return result

def can_call_input_for_stdio(stream):
	return stream == sys.stdin and sys.version_info[0] >= 3

class StdIOProxy(object):
	# 以后可能有用：codecs.StreamRecoder(bytesIO, codec.decode, codec.encode, codec.streamwriter, codec.streamreader, errors='surrogateescape')
	def __init__(self, stdin, stdout, stderr, codec, allow_set_code_page):
		self.codec = codec
		streams = (stdin, stdout, stderr)
		for stream in streams:
			assert isinstance(stream, io.IOBase) or sys.version_info[0] < 3 and isinstance(stream, file) or hasattr(stream, 'mode'), "unable to determine stream type"
			assert not isinstance(stream, io.RawIOBase), "RAW I/O APIs are different and not supported"
		self.streaminfos = tuple(map(lambda stream:
			(
				stream,
				isinstance(stream, io.BufferedIOBase) or isinstance(stream, io.RawIOBase) or not isinstance(stream, io.TextIOBase) and 'b' in stream.mode,
				isinstance(stream, io.TextIOBase) or not (isinstance(stream, io.BufferedIOBase) or isinstance(stream, io.RawIOBase)) and 'b' not in stream.mode,
				allow_set_code_page
			),
			streams))
	@property
	def stdin(self): return self.streaminfos[0][0]
	@property
	def stdout(self): return self.streaminfos[1][0]
	@property
	def stderr(self): return self.streaminfos[2][0]
	def _coerce(self, streaminfo, codec, arg):
		stream = streaminfo[0]
		can_binary = streaminfo[1]
		can_text = streaminfo[2]
		if not isinstance(arg, bytes) and not isinstance(arg, buffer) and not isinstance(arg, unicode):
			arg = unicode(arg)
		if isinstance(arg, bytes) or isinstance(arg, buffer):
			if not can_binary:
				arg = codec.decode(arg, 'surrogateescape')[0]
		elif isinstance(arg, unicode):
			if not can_text:
				arg = codec.encode(unicode(arg), 'strict')[0]
		return arg
	@staticmethod
	def _do_readline(stream, allow_set_code_page, *args):
		new_code_page = CP_UTF8
		old_code_page = GetConsoleCP() if msvcrt and GetConsoleCP and isatty(stream) else None
		if old_code_page == new_code_page: old_code_page = None  # 如果代码页已经正确，就不要更改
		if old_code_page is not None:
			if not SetConsoleCP(new_code_page):
				old_code_page = None
		try:
			result = stream.readline(*args)
		finally:
			if old_code_page is not None:
				SetConsoleCP(old_code_page)
		return result
	@staticmethod
	def _do_write(stream, allow_set_code_page, *args):
		new_code_page = CP_UTF8
		old_code_page = GetConsoleOutputCP() if msvcrt and GetConsoleOutputCP and isatty(stream) else None
		if old_code_page == new_code_page: old_code_page = None  # 如果代码页已经正确，就不要更改
		if old_code_page is not None:
			if not SetConsoleOutputCP(new_code_page):
				old_code_page = None
		try:
			result = stream.write(*args)
		finally:
			if old_code_page is not None:
				SetConsoleCP(old_code_page)
		return result
	def _readln(self, streaminfo, codec, prompt):
		stream = streaminfo[0]
		can_binary = streaminfo[1]
		allow_set_code_page = streaminfo[3]
		if can_call_input_for_stdio(stream) and not can_binary:  # input() 无法处理二进制数据
			result = self._coerce(streaminfo, codec, "")
			try:
				result = input(*((self._coerce(streaminfo, codec, prompt),) if prompt is not None else ()))
				result += self._coerce(streaminfo, codec, "\n")
			except EOFError: pass
		else:
			self.output(*((prompt,) if prompt is not None else ()))
			self.error()
			result = StdIOProxy._do_readline(stream, allow_set_code_page)
		return result
	def _writeln(self, streaminfo, codec, *args, **kwargs):
		stream = streaminfo[0]
		allow_set_code_page = streaminfo[3]
		flush = kwargs.pop('flush', True)
		kwargs.setdefault('end', '\n')
		kwargs.setdefault('sep', ' ')
		end = kwargs.get('end')
		sep = kwargs.get('sep')
		first = True
		for arg in args:
			if first: first = False
			elif sep is not None:
				StdIOProxy._do_write(stream, allow_set_code_page, self._coerce(streaminfo, codec, sep))
			StdIOProxy._do_write(stream, allow_set_code_page, self._coerce(streaminfo, codec, arg))
		if end is not None:
			StdIOProxy._do_write(stream, allow_set_code_page, self._coerce(streaminfo, codec, end))
		if flush: stream.flush()
	def inputln(self, prompt=None): return self._readln(self.streaminfos[0], self.codec, prompt)
	def output(self, *args, **kwargs): kwargs.setdefault('end', None); return self._writeln(self.streaminfos[1], self.codec, *args, **kwargs)
	def outputln(self, *args, **kwargs): return self._writeln(self.streaminfos[1], self.codec, *args, **kwargs)
	def error(self, *args, **kwargs): kwargs.setdefault('end', None); return self._writeln(self.streaminfos[2], self.codec, *args, **kwargs)
	def errorln(self, *args, **kwargs): return self._writeln(self.streaminfos[2], self.codec, *args, **kwargs)

class bytes_comparable_with_unicode(bytes):  # 为兼容 Python 2/3，在安全的情况下允许字符串与字节串之间进行隐式转换。（用于已知安全的字面量等字符串。）
	codec = codecs.lookup('ascii')  # 必须使用安全的编码
	@classmethod
	def coerce(cls, other, for_output=False):
		return cls.codec.encode(other)[0] if not isinstance(other, bytes) else bytes_comparable_with_unicode(other) if for_output else other
	@classmethod
	def translate_if_bytes(cls, value):
		if value is not None and isinstance(value, bytes): value = cls(value)
		return value
	def __hash__(self): return super(bytes_comparable_with_unicode, self).__hash__()  # 避免警告
	def __eq__(self, other): return super(bytes_comparable_with_unicode, self).__eq__(self.coerce(other))
	def __ne__(self, other): return super(bytes_comparable_with_unicode, self).__ne__(self.coerce(other))
	def __lt__(self, other): return super(bytes_comparable_with_unicode, self).__lt__(self.coerce(other))
	def __gt__(self, other): return super(bytes_comparable_with_unicode, self).__gt__(self.coerce(other))
	def __le__(self, other): return super(bytes_comparable_with_unicode, self).__le__(self.coerce(other))
	def __ge__(self, other): return super(bytes_comparable_with_unicode, self).__ge__(self.coerce(other))
	def __getitem__(self, index): return self.coerce(super(bytes_comparable_with_unicode, self).__getitem__(index), True)
	def __add__(self, other): return self.coerce(super(bytes_comparable_with_unicode, self).__add__(self.coerce(other)), True)
	def __iadd__(self, other): return self.coerce(super(bytes_comparable_with_unicode, self).__iadd__(self.coerce(other)), True)
	def __radd__(self, other): return self.coerce(self.coerce(other).__add__(self), True)
	def find(self, other, *args): return super(bytes_comparable_with_unicode, self).find(self.coerce(other), *args)
	def join(self, others): return self.coerce(super(bytes_comparable_with_unicode, self).join(map(self.coerce, others)), True)
	def startswith(self, other): return super(bytes_comparable_with_unicode, self).startswith(self.coerce(other))
	def __str__(self): return self.codec.decode(self)[0]
	if str == bytes:
		__unicode__ = __str__
		def __str__(self): raise NotImplementedError()

def wrap_bytes_comparable_with_unicode_readline(readline):
	def callback(*args):
		line = readline(*args)
		line = bytes_comparable_with_unicode.translate_if_bytes(line)
		return line
	return callback

def main(program, *args, **kwargs):  # **kwargs = dict(stdin=file, stdout=file, stderr=file)；供导入此模块的调用方使用
	import argparse  # 导入较慢（需要编译正则表达式等），因此在需要时才导入
	argparser = argparse.ArgumentParser(
		prog=os.path.basename(program),
		usage=None,
		description=None,
		epilog=None,
		parents=[],
		formatter_class=argparse.RawTextHelpFormatter)
	argparser.add_argument('-version', '--version', action='store_true', help="show SQLite version")
	argparser.add_argument('-batch', '--batch', action='store_true', help="force batch I/O")
	argparser.add_argument('-init', '--init', metavar="FILE", help="read/process named file")
	argparser.add_argument('filename', nargs='?', metavar="FILENAME", help="is the name of an SQLite database.\nA new database is created if the file does not previously exist.")
	argparser.add_argument('sql', nargs='*', metavar="SQL", help="SQL commnds to execute after opening database")
	argparser.add_argument('--readline', action='store', metavar="(true|false)", default="true", choices=("true", "false"), help="whether to import readline if available (default: %(default)s)")
	argparser.add_argument('--self-test', action='store_true', help="perform a basic self-test")
	argparser.add_argument('--cross-test', action='store_true', help="perform a basic test against the official executable")
	argparser.add_argument('--unicode-stdio', action='store', metavar="(true|false)", default="true", choices=("true", "false"), help="whether to enable Unicode wrapper for standard I/O (default: %(default)s)")
	argparser.add_argument('--console', action='store', metavar="(true|false)", default="true", choices=("true", "false"), help="whether to auto-detect and use console window APIs (default: %(default)s)")
	argparser.add_argument('--encoding', default=ENCODING, help="the default encoding to use (default: %(default)s)")
	(stdin, stdout, stderr) = (kwargs.pop('stdin', sys.stdin), kwargs.pop('stdout', sys.stdout), kwargs.pop('stderr', sys.stderr))
	parsed_args = argparser.parse_args(args)
	codec = codecs.lookup(parsed_args.encoding or argparser.get_default('encoding'))
	if parsed_args.self_test: self_test(codec)
	if parsed_args.cross_test: cross_test("sqlite3", codec)
	parse_escaped_strings = StringEscapeParser()
	if parsed_args.unicode_stdio == "true":
		stdin = wrap_unicode_stdio(stdin, False, codec.name)
		stdout = wrap_unicode_stdio(stdout, True, codec.name)
		stderr = wrap_unicode_stdio(stderr, True, codec.name)
	if parsed_args.console == "true":
		stdin = wrap_windows_console_io(stdin, False)
		stdout = wrap_windows_console_io(stdout, True)
		stderr = wrap_windows_console_io(stderr, True)
	allow_set_code_page = sys.version_info[0] < 3 and False  # 仅当 Python 2 使用默认输入输出函数，而没有直接调用 ReadConsole()/WriteConsole() 时才需要这样处理
	stdio = StdIOProxy(stdin, stdout, stderr, codec, allow_set_code_page)
	db = None
	no_args = len(args) == 0
	init_sql = parsed_args.sql
	is_nonpipe_input = stdin.isatty()  # 这与 TTY 不同！（区别在于 NUL 和 /dev/null）
	init_show_prompt = not parsed_args.batch and is_nonpipe_input
	if not parsed_args.batch and isatty(stdin) and (parsed_args.readline == "true" or __name__ == '__main__') and parsed_args.readline != "false":
		try:
			with warnings.catch_warnings():
				warnings.filterwarnings('ignore', category=DeprecationWarning)
				import readline
		except ImportError: pass
	if parsed_args and parsed_args.version:
		stdio.outputln(sqlite3.sqlite_version);
	else:
		filename = parsed_args.filename
		if filename is None: filename = ":memory:"
		db = Database(filename, isolation_level=None)
	def exec_script(db, filename, ignore_io_errors):
		try:
			with io.open(filename, 'r', encoding=codec.name) as f:  # 假定 .sql 文件是文本；其中的二进制数据应采用 X'' 编码，而不是直接嵌入
				for command in sql_commands(wrap_bytes_comparable_with_unicode_readline(lambda *args: (lambda s: (s) or None)(f.readline()))):
					result = exec_command(db, command, False and ignore_io_errors)
					if result is not None:
						return result
		except IOError as ex:
			stdio.errorln(ex)
			if not ignore_io_errors: return ex.errno
	def raise_invalid_command_error(command):
		if isinstance(command, bytes): command = codec.decode(command)[0]
		if command.startswith("."): command = command[1:]
		raise RuntimeError("Error: unknown command or invalid arguments:  \"%s\". Enter \".help\" for help" % (command.rstrip().replace("\\", "\\\\").replace("\"", "\\\""),))
	def exec_command(db, command, ignore_io_errors):
		results = None
		query = None
		query_parameters = {}
		try:
			if command.startswith("."):
				args = list(parse_escaped_strings(command))
				if args[0] in (".quit", ".exit"):
					return 0
				elif args[0] == ".help":
					stdio.error("""
.cd DIRECTORY          Change the working directory to DIRECTORY
.dump                  Dump the database in an SQL text format
.exit                  Exit this program
.help                  Show this message
.open FILE             Close existing database and reopen FILE
.print STRING...       Print literal STRING
.quit                  Exit this program
.read FILENAME         Execute SQL in FILENAME
.schema ?PATTERN?      Show the CREATE statements matching PATTERN
.show                  Show the current values for various settings
.tables ?TABLE?        List names of tables
""".lstrip())
				elif args[0] == ".cd":
					if len(args) != 2: raise_invalid_command_error(command)
					os.chdir(args[1])
				elif args[0] == ".dump":
					if len(args) != 1: raise_invalid_command_error(command)
					foreign_keys = db.cursor.execute("PRAGMA foreign_keys;").fetchone()[0]
					if foreign_keys in (0, "0", "off", "OFF"):
						stdio.outputln("PRAGMA foreign_keys=OFF;", flush=False)
					for line in db.connection.iterdump():
						stdio.outputln(line, flush=False)
					stdio.output()
				elif args[0] == ".open":
					if len(args) <= 1: raise_invalid_command_error(command)
					filename = args[-1]
					for option in args[+1:-1]:
						raise ValueError("option %s not supported" % (repr(option),))
					try: db.__init__(filename)
					except sqlite3.OperationalError as ex:
						ex.args = ex.args[:0] + ("Error: unable to open database \"%s\": %s" % (filename, ex.args[0]),) + ex.args[1:]
						raise
				elif args[0] == ".print":
					stdio.outputln(*args[1:])
				elif args[0] == ".read":
					if len(args) != 2: raise_invalid_command_error(command)
					exec_script(db, args[1], ignore_io_errors)
				elif args[0] == ".schema":
					if len(args) > 2: raise_invalid_command_error(command)
					pattern = args[1] if len(args) > 1 else None
					query_parameters['type'] = 'table'
					if pattern is not None:
						query_parameters['pattern'] = pattern
					query = "SELECT sql || ';' FROM sqlite_master WHERE type = :type" + (" AND name LIKE :pattern" if pattern is not None else "") + ";"
				elif args[0] == ".show":
					if len(args) > 2: raise_invalid_command_error(command)
					stdio.errorln("    filename:", db.name)
				elif args[0] == ".tables":
					if len(args) > 2: raise_invalid_command_error(command)
					pattern = args[1] if len(args) > 1 else None
					query_parameters['type'] = 'table'
					if pattern is not None:
						query_parameters['pattern'] = pattern
					query = "SELECT name FROM sqlite_master WHERE type = :type" + (" AND name LIKE :pattern" if pattern is not None else "") + ";"
				else:
					raise_invalid_command_error(args[0])
			else:
				query = command
			if query is not None:
				results = db.cursor.execute(query if isinstance(query, unicode) else codec.decode(query, 'surrogatereplace')[0], query_parameters)
		except (RuntimeError, OSError, FileNotFoundError, sqlite3.OperationalError) as ex:
			stdio.errorln(exception_encode(ex, codec))
		if results is not None:
			for row in results:
				stdio.outputln(*tuple(map(lambda item: item if item is not None else "", row)), sep="|", flush=False)
			stdio.output()
	if db:
		if parsed_args and parsed_args.init:
			if is_nonpipe_input: stdio.errorln("-- Loading resources from", parsed_args.init)
			exec_script(db, parsed_args.init, False)
		def read_stdin(index, not_in_the_middle_of_any_input, prev_line):
			show_prompt = init_show_prompt
			to_write = []
			if index < len(init_sql):
				line = init_sql[index]
				if not line.startswith(".") and not line.rstrip().endswith(";"):
					line += ";"
			elif index == len(init_sql) and len(init_sql) > 0:
				line = None
			else:
				if show_prompt:
					if not_in_the_middle_of_any_input:
						show_prompt = False
						if index == 0:
							to_write.append("SQLite version %s (adapter version %s)\nEnter \".help\" for usage hints.\n" % (sqlite3.sqlite_version, sqlite3.version))
							if no_args:
								to_write.append("Connected to a transient in-memory database.\nUse \".open FILENAME\" to reopen on a persistent database.\n")
					if index > 0 and not prev_line:
						to_write.append("\n")
					to_write.append("%7s " % ("sqlite%s>" % ("",) if not_in_the_middle_of_any_input else "...>",))
				try:
					line = stdio.inputln("".join(to_write))
				except KeyboardInterrupt:
					line = ""
					raise  # 暂时不处理这种情况
			return line
		for command in sql_commands(wrap_bytes_comparable_with_unicode_readline(read_stdin)):
			result = exec_command(db, command, True)
			if result is not None:
				return result
		if init_show_prompt and len(init_sql) == 0:
			stdio.outputln()

def call_program(cmdline, input_text):
	import subprocess
	return subprocess.Popen(cmdline, bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=False).communicate(input_text)

def test_query():
	hexcodec = codecs.lookup('hex_codec')
	ascii = 'ascii'
	data1 = b"\xD8\xA2"
	data2 = b"\x01\x02\xFF\x01\xFF\xFE\xFD"
	values = [data1, data2]
	query_bytes = b'SELECT %s;' % (b", ".join(map(lambda b: b"X'%s'" % (hexcodec.encode(b)[0].upper(),), values)),)
	expected_bytes = b"%s\n" % (b"|".join(values),)
	return query_bytes, expected_bytes

def cross_test(sqlite_cmdline, codec):
	(query_bytes, expected_bytes) = test_query()
	(official_output, official_error) = call_program(sqlite_cmdline, query_bytes)
	# 这里不能使用 os.linesep，因为二进制程序可能属于不同平台（Win32/MinGW、MSYS/Cygwin 或 WSL 等）
	official_output = official_output.replace(b"\r\n", b"\n")
	official_error = official_error.replace(b"\r\n", b"\n")
	if official_output != expected_bytes:
		raise sqlite3.ProgrammingError("expected bytes are wrong: official %s != expected %s" % (repr(official_output), repr(expected_bytes)))
	if official_error:
		raise sqlite3.ProgrammingError("did not expect errors from official binary")

def self_test(codec):
	(query_bytes, expected_bytes) = test_query()
	if not (lambda stdin, stdout, stderr: not main(sys.argv[0], stdin=stdin, stdout=stdout, stderr=stderr) and stdout.getvalue() == expected_bytes)(io.BytesIO(query_bytes), io.BytesIO(), io.BytesIO()):
		raise sqlite3.ProgrammingError("byte I/O is broken")
	if not (lambda stdin, stdout, stderr: not main(sys.argv[0], stdin=stdin, stdout=stdout, stderr=stderr) and stdout.getvalue() == codec.decode(expected_bytes, 'surrogateescape'))(io.StringIO(query_bytes.decode(ascii)), io.StringIO(), io.StringIO()):
		raise sqlite3.ProgrammingError("string I/O is broken")

if __name__ == '__main__':
	import sys
	exit_code = main(*sys.argv)
	if exit_code not in (None, 0): raise SystemExit(exit_code)
