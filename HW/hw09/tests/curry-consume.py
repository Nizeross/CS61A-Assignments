test = {
  'name': 'curry-consume',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (define three-curry (curry-cook '(x y z) '(+ x (* y z))))
          three-curry
          scm> three-curry
          (lambda (x) (lambda (y) (lambda (z) (+ x (* y z)))))
          scm> (define three-curry-fn (eval three-curry)) ; three-curry-fn 是从该程序推导出的 lambda 函数
          three-curry-fn
          scm> (define eat-two (curry-consume three-curry-fn '(1 2))) ; 只传入两个参数，应返回一个单参数 lambda 函数！
          eat-two
          scm> eat-two
          (lambda (z) (+ x (* y z)))
          scm> (eat-two 3) ; 传入最后一个参数；1 + (2 * 3)
          7
          scm> (curry-consume three-curry-fn '(1 2 3)) ; 一次传入全部三个参数！
          7
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      scm> (load-all ".")
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
