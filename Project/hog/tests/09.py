test = {
  'name': 'Question 9',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'answer': '98acc434a18370bb040345206aea9e70',
          'choices': [
            'The lowest num_rolls',
            'The highest num_rolls',
            'A random num_rolls'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': r"""
          If multiple num_rolls are tied for the highest scoring
          average, which should you return?
          """
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> dice = make_test_dice(3)   # dice 始终返回 3
          >>> max_scoring_num_rolls(dice, times_called=1000)
          70e71b420a966665c548a3bb2cb30d7d
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> dice = make_test_dice(1, 2, 2, 2, 2, 2, 2, 2)
          >>> max_scoring_num_rolls(dice, times_called=1000)
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> dice = make_test_dice(*([2] * 55 + [1, 2] * 500)) # 检查是否没有进行多余的掷骰调用
          >>> max_scoring_num_rolls(dice, times_called=1) # dice 前 55 次返回 2，随后一次返回 1，再连续 1000 次返回 2
          10
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from hog import *
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> dice = make_test_dice(2)     # dice 始终返回 2
          >>> max_scoring_num_rolls(dice, times_called=1000)
          70e71b420a966665c548a3bb2cb30d7d
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> dice = make_test_dice(1)     # dice 始终返回 1
          >>> max_scoring_num_rolls(dice, times_called=1000)
          43d176e102c8d95338faf8791aa509b3
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> dice = make_test_dice(1, 2)  # dice 交替返回 1 和 2
          >>> max_scoring_num_rolls(dice, times_called=1000)
          43d176e102c8d95338faf8791aa509b3
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 100 个 2，然后是 100 个 1（不必担心这里如何实现）
          >>> dice = make_test_dice(*([2] * 100 + [1] * 100))
          >>> max_scoring_num_rolls(dice, times_called=1)
          10
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> dice = make_test_dice(1, 2, 3, 4, 5)  # dice 循环返回 1 到 5
          >>> max_scoring_num_rolls(dice, times_called=1000)
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> dice = make_test_dice(6, 5, 4, 3, 2, 1)  # dice 循环返回 1 到 6
          >>> max_scoring_num_rolls(dice, times_called=1) # 确保使用了 times_called
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from hog import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
