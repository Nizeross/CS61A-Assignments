test = {
  'name': 'Problem 7',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (lambda (x y) (+ x y)) ;; lambda 过程的显示形式与其书写形式完全一致
          1456de84c3edf333b6f7aee0c0624b20
          # locked
          scm> (lambda (x)) ; 如果你认为会报错，输入 SchemeError
          ec908af60f03727428c7ee3f22ec3cd8
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (lambda (x) (+ x) (+ x x))
          (lambda (x) (+ x) (+ x x))
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          scm> (lambda () 2)
          (lambda () 2)
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'scheme'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> env = create_global_frame()
          >>> lambda_line = read_line("(lambda (a b c) (+ a b c))")
          >>> lambda_proc = do_lambda_form(lambda_line.rest, env)
          >>> lambda_proc.formals # 答案中的字符串请用单引号 ' 包围
          d106bb7be6b014a9d16d74410be4a8a5
          # locked
          # choice: Pair('a', Pair('b', Pair('c', nil)))
          # choice: Pair('+', Pair('a', Pair('b', Pair('c', nil))))
          # choice: Pair(Pair('a', Pair('b', Pair('c', nil))))
          >>> lambda_proc.body # 过程体是表达式组成的 Scheme 列表！确保答案是正确嵌套的 Pair。
          0ef147cfe5caf670e985d95d923f4b06
          # locked
          # choice: Pair(Pair('+', Pair('a', Pair('b', Pair('c', nil)))), nil)
          # choice: Pair('+', Pair('a', Pair('b', Pair('c', nil))))
          # choice: Pair('+', 'a', 'b', 'c')
          # choice: Pair('a', Pair('b', Pair('c')))
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> env = create_global_frame()
          >>> lambda_line = read_line("(lambda (x y) x)")
          >>> lambda_proc = do_lambda_form(lambda_line.rest, env)
          >>> isinstance(lambda_proc, LambdaProcedure)
          True
          >>> lambda_proc.env is env
          True
          >>> lambda_proc
          LambdaProcedure(Pair('x', Pair('y', nil)), Pair('x', nil), <Global Frame>)
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from scheme_reader import *
      >>> from scheme import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
