test = {
  'name': 'Higher Order Functions',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # 如果 Python 显示 <function...>，输入 Function；如果报错，输入 Error；如果没有显示内容，输入 Nothing
          >>> def cake():
          ...    print('beets')
          ...    def pie():
          ...        print('sweets')
          ...        return 'cake'
          ...    return pie
          >>> chocolate = cake()
          0127137631d037670fa6a894e2d548ee
          # locked
          >>> chocolate
          4f02258d689b15b516174b381ad2aef8
          # locked
          >>> chocolate()
          28f5a700252060ec3bbc4bf4ca744c56
          7fccab88a7c3c0cbffe0142e723d1984
          # locked
          >>> more_chocolate, more_cake = chocolate(), cake
          28f5a700252060ec3bbc4bf4ca744c56
          # locked
          >>> more_chocolate
          7fccab88a7c3c0cbffe0142e723d1984
          # locked
          >>> # 提醒：cake、more_cake 和 chocolate 已在上面的代码中定义或赋值！
          >>> # 可以对照作业网站上的定义，减少来回滚动查找！
          >>> def snake(x, y):
          ...    if cake == more_cake:
          ...        return chocolate
          ...    else:
          ...        return x + y
          >>> snake(10, 20)
          4f02258d689b15b516174b381ad2aef8
          # locked
          >>> snake(10, 20)()
          28f5a700252060ec3bbc4bf4ca744c56
          7fccab88a7c3c0cbffe0142e723d1984
          # locked
          >>> cake = 'cake'
          >>> snake(10, 20)
          c06666e98ec36af7add28e636f1488ee
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        }
      ],
      'scored': False,
      'type': 'wwpp'
    }
  ]
}
