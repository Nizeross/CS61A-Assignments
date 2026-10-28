test = {
  'name': 'Problem EC 1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # 测试状态参数
          >>> slow = SlowThrower()
          >>> SlowThrower.food_cost
          50ae32be3e31df6c59633df7fdfb3a72
          # locked
          >>> slow.health
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试减速效果
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(slow)
          >>> gamestate.places["tunnel_0_5"].add_insect(bee)
          >>> slow.action(gamestate) # slow 向蜜蜂投掷糖浆
          >>> gamestate.time = 1
          >>> bee.action(gamestate) # 当 gamestate.time 为奇数时，slow 使蜜蜂减速；蜜蜂不应执行任何行动（移动或蜇刺）
          >>> bee.place.name
          46f9851313dc368f747e69f1670450da
          # locked
          >>> gamestate.time += 1
          >>> bee.action(gamestate) # 当 gamestate.time 为偶数时，蜜蜂不受影响，应正常行动
          >>> bee.place.name
          040b6ad98a7360eba8d493c250a9b82e
          # locked
          >>> for _ in range(5):
          ...    gamestate.time += 1
          ...    bee.action(gamestate)
          >>> bee.place.name # 提示：减速效果在 5 回合后消失。注意 for 循环开始之前，蜜蜂已经受到影响多少回合。
          7f44338412808161209e944b1ee0f78c
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试减速效果
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(slow)
          >>> gamestate.places["tunnel_0_5"].add_insect(bee)
          >>> slow.action(gamestate) # slow 向蜜蜂投掷糖浆
          >>> gamestate.time = 1
          >>> bee.action(gamestate) # 当 gamestate.time 为奇数时，slow 使蜜蜂减速；蜜蜂不应执行任何行动（移动或蜇刺）
          >>> bee.place.name
          46f9851313dc368f747e69f1670450da
          # locked
          >>> gamestate.time += 1
          >>> bee.action(gamestate) # 当 gamestate.time 为偶数时，蜜蜂不受影响，应正常行动
          >>> bee.place.name
          040b6ad98a7360eba8d493c250a9b82e
          # locked
          >>> slow.action(gamestate) # slow 再次投掷糖浆，减速效果将再持续 5 回合
          >>> for _ in range(5):
          ...    gamestate.time += 1
          ...    bee.action(gamestate)
          >>> bee.place.name
          ba5c35f55ba3229d1eb021382d9d19c5
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 Bee.action 未被修改
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(slow)
          >>> gamestate.places["tunnel_0_5"].add_insect(bee)
          >>> slow.action(gamestate)
          >>> gamestate.time = 1
          >>> Bee.action(bee, gamestate) # 使用原始 Bee.action
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time += 1
          >>> Bee.action(bee, gamestate) # 使用原始 Bee.action
          >>> bee.place.name
          'tunnel_0_3'
          >>> for _ in range(3):
          ...    gamestate.time += 1
          ...    bee.action(gamestate) # 使用原先新建的减速行动
          >>> bee.place.name
          'tunnel_0_2'
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试减速效果结束后 Bee 正常移动
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(slow)
          >>> gamestate.places["tunnel_0_8"].add_insect(bee)
          >>> slow.action(gamestate) # slow 向蜜蜂投掷糖浆
          >>> gamestate.time = 0
          >>> bee.action(gamestate) # 偶数时刻，蜜蜂应移动
          >>> bee.place.name
          'tunnel_0_7'
          >>> gamestate.time = 1
          >>> bee.action(gamestate) # 奇数时刻，蜜蜂不应移动
          >>> bee.place.name
          'tunnel_0_7'
          >>> gamestate.time = 2
          >>> bee.action(gamestate) # 偶数时刻，蜜蜂应移动
          >>> bee.place.name
          'tunnel_0_6'
          >>> gamestate.time = 3
          >>> bee.action(gamestate) # 奇数时刻，蜜蜂不应移动
          >>> bee.place.name
          'tunnel_0_6'
          >>> gamestate.time = 4
          >>> bee.action(gamestate) # 偶数时刻，蜜蜂应移动
          >>> bee.place.name
          'tunnel_0_5'
          >>> gamestate.time = 5
          >>> bee.action(gamestate) # 减速结束，蜜蜂应正常移动
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time = 6
          >>> bee.action(gamestate) # 减速结束，蜜蜂应正常移动
          >>> bee.place.name
          'tunnel_0_3'
          >>> gamestate.time = 7
          >>> bee.action(gamestate) # 减速结束，蜜蜂应正常移动
          >>> bee.place.name
          'tunnel_0_2'
          >>> gamestate.time = 8
          >>> bee.action(gamestate) # 减速结束，蜜蜂应正常移动
          >>> bee.place.name
          'tunnel_0_1'
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> beehive, layout = Hive(AssaultPlan()), dry_layout
      >>> dimensions = (1, 9)
      >>> gamestate = GameState(beehive, ant_types(), layout, dimensions)
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
