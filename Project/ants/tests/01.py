test = {
  'name': 'Problem 1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'answer': 'b11e19127a1cf83e285f83984cae6d4f',
          'choices': [
            r"""
            Placing an ant into the colony will decrease the colony's total
            available food by that ant's food_cost
            """,
            r"""
            Each turn, each Ant in the colony eats food_cost food from the
            colony's total available food
            """,
            r"""
            Each turn, each Ant in the colony adds food_cost food to the
            colony's total available food
            """
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What is the purpose of the food_cost attribute?'
        },
        {
          'answer': '2d3f4f6f9e9a083f23302e78084d5448',
          'choices': [
            'class, all Ants of the same subclass cost the same to place',
            'class, all Ants cost the same to place no matter what type of Ant it is',
            'instance, the food_cost of an Ant depends on the location it is placed',
            'instance, the food_cost of an Ant is randomized upon initialization'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What type of attribute is food_cost?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> Ant.food_cost
          73b94a1326ae2e803c3421016112207b
          # locked
          >>> HarvesterAnt.food_cost
          20d533d3e06345c8bd7072212867f2d1
          # locked
          >>> ThrowerAnt.food_cost
          81a7d27d1a4a958871bb97b545b871db
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 HarvesterAnt 的行动
          >>> # 创建单行、包含 9 个地块的蚁群测试布局
          >>> beehive = Hive(make_test_assault_plan())
          >>> gamestate = GameState(beehive, ant_types(), dry_layout, (1, 9))
          >>> #
          >>> gamestate.food = 4
          >>> harvester = HarvesterAnt()
          >>> # 注意：初始化 Ant 不消耗食物，
          >>> # 只有将 Ant 部署到游戏地图中才消耗食物。
          >>> # 在此测试中，蚂蚁即使没有
          >>> # 部署到游戏地图中，也能行动。
          >>> #
          >>> gamestate.food
          c9452203eb0b0f0bd2454586a6c2fc5c
          # locked
          >>> harvester.action(gamestate) # 执行 harvester 的 action 方法，表示这只蚂蚁行动一回合。
          >>> gamestate.food
          62674984f877ec783f37e8b8b9c264d0
          # locked
          >>> harvester.action(gamestate) # 再次执行 harvester 的行动。
          >>> gamestate.food
          50ae32be3e31df6c59633df7fdfb3a72
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> from ants import *
          >>> HarvesterAnt.implemented
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants import *
      >>> from ants_plans import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
