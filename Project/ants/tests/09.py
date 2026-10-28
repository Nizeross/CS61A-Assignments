test = {
  'name': 'Problem 9',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'answer': 'df9239b5516819d074706715cb1822fe',
          'choices': [
            'A TankAnt does damage to all Bees in its place each turn',
            'A TankAnt has greater health than a BodyguardAnt',
            'A TankAnt can contain multiple ants',
            'A TankAnt increases the damage of the ant it contains'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': r"""
          Besides costing more to place, what is the only difference between a
          TankAnt and a BodyguardAnt?
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
          >>> # 测试 TankAnt 的参数
          >>> TankAnt.food_cost
          50ae32be3e31df6c59633df7fdfb3a72
          # locked
          >>> TankAnt.damage
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> tank = TankAnt()
          >>> tank.health
          20d533d3e06345c8bd7072212867f2d1
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 TankAnt 的行动
          >>> tank = TankAnt()
          >>> place = gamestate.places['tunnel_0_1']
          >>> other_place = gamestate.places['tunnel_0_2']
          >>> place.add_insect(tank)
          >>> for _ in range(3):
          ...     place.add_insect(Bee(3))
          >>> other_place.add_insect(Bee(3))
          >>> tank.action(gamestate)
          >>> [bee.health for bee in place.bees]
          [2, 2, 2]
          >>> [bee.health for bee in other_place.bees]
          [3]
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 TankAnt 的容器方法
          >>> tank = TankAnt()
          >>> thrower = ThrowerAnt()
          >>> place = gamestate.places['tunnel_0_1']
          >>> place.add_insect(thrower)
          >>> place.add_insect(tank)
          >>> place.ant is tank
          True
          >>> bee = Bee(3)
          >>> place.add_insect(bee)
          >>> tank.action(gamestate)   # 两只蚂蚁都攻击蜜蜂
          >>> bee.health
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from ants_plans import *
      >>> from ants import *
      >>> beehive, layout = Hive(make_test_assault_plan()), dry_layout
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
          >>> # 测试 TankAnt 的行动
          >>> tank = TankAnt()
          >>> place = gamestate.places['tunnel_0_1']
          >>> place.add_insect(tank)
          >>> for _ in range(3):  # 添加三只各有 1 点生命值的蜜蜂
          ...     place.add_insect(Bee(1))
          >>> tank.action(gamestate)
          >>> len(place.bees)  # 蜜蜂因 TankAnt 的伤害而被从地点移除
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 TankAnt.damage
          >>> tank = TankAnt()
          >>> tank.damage = 100
          >>> place = gamestate.places['tunnel_0_1']
          >>> place.add_insect(tank)
          >>> for _ in range(3):
          ...     place.add_insect(Bee(100))
          >>> tank.action(gamestate)
          >>> len(place.bees)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 放置蚂蚁
          >>> tank = TankAnt()
          >>> harvester = HarvesterAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> # 先添加 tank，再添加 harvester
          >>> place.add_insect(tank)
          >>> place.add_insect(harvester)
          >>> gamestate.food = 0
          >>> tank.action(gamestate)
          >>> gamestate.food
          1
          >>> try:
          ...   place.add_insect(TankAnt())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.ant is tank
          True
          >>> tank.ant_contained is harvester
          True
          >>> try:
          ...   place.add_insect(HarvesterAnt())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.ant is tank
          True
          >>> tank.ant_contained is harvester
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 放置蚂蚁
          >>> tank = TankAnt()
          >>> harvester = HarvesterAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> # 先添加 harvester，再添加 tank
          >>> place.add_insect(harvester)
          >>> place.add_insect(tank)
          >>> gamestate.food = 0
          >>> tank.action(gamestate)
          >>> gamestate.food
          1
          >>> try:
          ...   place.add_insect(TankAnt())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.ant is tank
          True
          >>> tank.ant_contained is harvester
          True
          >>> try:
          ...   place.add_insect(HarvesterAnt())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.ant is tank
          True
          >>> tank.ant_contained is harvester
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 移除蚂蚁
          >>> tank = TankAnt()
          >>> test_ant = Ant()
          >>> place = Place('Test')
          >>> place.add_insect(tank)
          >>> place.add_insect(test_ant)
          >>> place.remove_insect(test_ant)
          >>> tank.ant_contained is None
          True
          >>> test_ant.place is None
          True
          >>> place.remove_insect(tank)
          >>> place.ant is None
          True
          >>> tank.place is None
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> tank = TankAnt()
          >>> place = Place('Test')
          >>> place.add_insect(tank)
          >>> tank.action(gamestate) # 没有 ant_contained 时，执行行动不应报错
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
          >>> tank = TankAnt()
          >>> ant = ThrowerAnt()
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> place.add_insect(tank)
          >>> bee.action(gamestate)
          >>> bee.action(gamestate)
          insect died
          >>> bee.action(gamestate) # 如果此测试失败，可能是没有正确调用 Ant.reduce_health 或 Insect.reduce_health
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
      >>> from ants_plans import *
      >>> from ants import *
      >>> beehive, layout = Hive(make_test_assault_plan()), dry_layout
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
          >>> TankAnt.implemented
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> from ants import *
          >>> # 抽象测试
          >>> original = Ant.__init__
          >>> Ant.__init__ = lambda self, health: print("init") #如果报错，说明没有正确调用父类构造函数。
          >>> tank = TankAnt()
          init
          >>> Ant.__init__ = original
          >>> tank = TankAnt()
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
