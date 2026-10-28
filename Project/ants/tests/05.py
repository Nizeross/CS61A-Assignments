test = {
  'name': 'Problem 5',
  'points': 3,
  'suites': [
    {
      'cases': [
        {
          'answer': '9b8f7869c0cf94ceb6a862dc352b4df1',
          'choices': [
            'By accessing the place instance attribute, which is a Place object',
            r"""
            By accessing the place instance attribute, which is the name of
            some Place object
            """,
            'By calling the Place constructor, passing in the FireAnt instance',
            'By calling the FireAnt constructor'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'How can you obtain the current place of a FireAnt?'
        },
        {
          'answer': '81e2e777eb97c4cb836bdcb2fbb428d6',
          'choices': [
            r"""
            By accessing the bees instance attribute, which is a list of Bee
            objects
            """,
            r"""
            By accessing the bees instance attribute, which is a dictionary of
            Bee objects
            """,
            'By calling the add_insect method on the place instance',
            'By calling the Bee constructor, passing in the place instance'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'How can you obtain all of the Bees currently in a given place?'
        },
        {
          'answer': 'c95a4e74584be420b1318afb809bb642',
          'choices': [
            r"""
            Yes, but you should iterate over a copy of the list to avoid skipping
            elements
            """,
            'Yes, you can mutate a list while iterating over it with no problems',
            r"""
            No, Python doesn't allow list mutation on a list that is being
            iterated through
            """
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'Can you iterate over a list while mutating it?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # 测试 FireAnt 的参数
          >>> fire = FireAnt()
          >>> FireAnt.food_cost
          62674984f877ec783f37e8b8b9c264d0
          # locked
          >>> fire.health
          81a7d27d1a4a958871bb97b545b871db
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 抽象测试
          >>> original = Ant.__init__
          >>> Ant.__init__ = lambda self, health: print("init") #如果报错，说明没有正确调用父类构造函数。
          >>> fire = FireAnt()
          init
          >>> Ant.__init__ = original
          >>> fire = FireAnt()
          >>> original = Ant.reduce_health
          >>> Ant.reduce_health = lambda self, amount: print("reduced") #如果报错，说明没有正确调用继承的方法
          >>> place = gamestate.places['tunnel_0_4']
          >>> place.add_insect(fire)
          >>> fire.reduce_health(1)
          reduced
          >>> Ant.reduce_health = original
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试火蚁会伤害所在地点的所有蜜蜂
          >>> place = gamestate.places['tunnel_0_4']
          >>> fire = FireAnt(health=1)
          >>> place.add_insect(fire)        # 添加一只生命值为 1 的 FireAnt
          >>> place.add_insect(Bee(3))      # 添加一只生命值为 3 的 Bee
          >>> place.add_insect(Bee(5))      # 添加一只生命值为 5 的 Bee
          >>> len(place.bees)               # 共有多少只蜜蜂？
          20d533d3e06345c8bd7072212867f2d1
          # locked
          >>> place.bees[0].action(gamestate)  # 第一只 Bee 攻击 FireAnt
          >>> fire.health
          73b94a1326ae2e803c3421016112207b
          # locked
          >>> fire.place is None
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> len(place.bees)               # 还剩多少只蜜蜂？
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> place.bees[0].health           # 剩余蜜蜂的生命值是多少？
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> place = gamestate.places['tunnel_0_4']
          >>> ant = FireAnt(health=1)           # 创建一只生命值为 1 的 FireAnt
          >>> place.add_insect(ant)      # 将 FireAnt 添加到地点
          >>> ant.place is place
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> place.remove_insect(ant)   # 从地点移除 FireAnt
          >>> ant.place is place         # 蚂蚁的 place 是否仍指向该地点？
          03456a09f22295a39ca84d133a26f63d
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试火蚁未死亡时的火焰伤害
          >>> place = gamestate.places['tunnel_0_4']
          >>> bee = Bee(5)
          >>> ant = FireAnt(health=100)
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> bee.action(gamestate) # 攻击 FireAnt
          >>> ant.health
          99
          >>> bee.health
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试没有写死数值 3
          >>> place = gamestate.places['tunnel_0_4']
          >>> bee = Bee(100)
          >>> ant = FireAnt(health=1)
          >>> ant.damage = 49
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> bee.action(gamestate) # 攻击 FireAnt
          >>> ant.health
          0
          >>> bee.health
          50
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试火蚁死亡时的火焰伤害
          >>> place = gamestate.places['tunnel_0_4']
          >>> bee = Bee(5)
          >>> ant = FireAnt(health=1)
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> bee.action(gamestate) # 攻击 FireAnt
          >>> ant.health
          0
          >>> bee.health
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试火蚁会伤害所在地点的所有蜜蜂
          >>> place = gamestate.places['tunnel_0_4']
          >>> place.add_insect(FireAnt(1))
          >>> for i in range(100):          # 添加 100 只生命值为 3 的蜜蜂
          ...     place.add_insect(Bee(3))
          >>> place.bees[0].action(gamestate)  # 第一只 Bee 攻击 FireAnt
          >>> len(place.bees)               # 还剩多少只蜜蜂？
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试火焰伤害使用实例属性
          >>> place = gamestate.places['tunnel_0_4']
          >>> bee = Bee(900)
          >>> buffAnt = FireAnt(1)
          >>> buffAnt.damage = 500   # 感受火焰吧！
          >>> place.add_insect(bee)
          >>> place.add_insect(buffAnt)
          >>> bee.action(gamestate) # 攻击 FireAnt
          >>> bee.health  # damage 是实例属性吗？
          399
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # FireAnt 的综合测试
          >>> place = gamestate.places['tunnel_0_4']
          >>> bee = Bee(10)
          >>> ant = FireAnt(1)
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> bee.action(gamestate)    # 攻击 FireAnt
          >>> bee.health
          6
          >>> ant.health
          0
          >>> place.ant is None     # FireAnt 应不再占据该地点
          True
          >>> bee.action(gamestate)
          >>> bee.health             # Bee 不应再次受到伤害
          6
          >>> bee.place.name        # Bee 不应被阻挡
          'tunnel_0_3'
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # FireAnt 的综合测试
          >>> place = gamestate.places['tunnel_0_4']
          >>> bee = Bee(10)
          >>> ant = FireAnt()
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> ant.reduce_health(0.1) # 戳一下 FireAnt
          >>> bee.health             # Bee 应只受到少量伤害
          9.9
          >>> ant.health
          2.9
          >>> place.ant is ant      # FireAnt 应仍在该地点
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试是否正确调用生命值归零时的回调函数
          >>> original_zero_health_callback = Insect.zero_health_callback
          >>> Insect.zero_health_callback = lambda x: print("insect died")
          >>> place = gamestate.places["tunnel_0_0"]
          >>> bee = Bee(3)
          >>> ant = FireAnt()
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> bee.action(gamestate)
          >>> bee.action(gamestate)
          >>> bee.action(gamestate) # 如果此测试失败，可能是没有正确调用 Ant.reduce_health 或 Insect.reduce_health
          insect died
          insect died
          >>> Insect.zero_health_callback = original_zero_health_callback
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
      >>> #
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> from ants import *
          >>> FireAnt.implemented
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
