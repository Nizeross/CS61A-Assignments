test = {
  'name': 'Problem 8',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'answer': 'c1637d7df9f040dc0b1cd3b7d43616a9',
          'choices': [
            'No, I will go do them right now',
            'Yes!'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'Did you complete all the unlocking tests for each subpart?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # 抽象测试
          >>> original = ContainerAnt.__init__
          >>> ContainerAnt.__init__ = lambda self, health: print("init") #如果报错，说明没有正确调用父类构造函数。
          >>> bodyguard = BodyguardAnt()
          init
          >>> ContainerAnt.__init__ = original
          >>> bodyguard = BodyguardAnt()
          >>> hasattr(bodyguard, 'ant_contained')
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
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> bodyguard = BodyguardAnt()
          >>> bodyguard.action(gamestate) # 没有被容纳的蚂蚁时，执行行动不应报错
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试保镖是否执行投掷蚁的行动
          >>> bodyguard = BodyguardAnt()
          >>> thrower = ThrowerAnt()
          >>> bee = Bee(2)
          >>> # 先放置保镖，再放置投掷蚁
          >>> gamestate.places["tunnel_0_0"].add_insect(bodyguard)
          >>> gamestate.places["tunnel_0_0"].add_insect(thrower)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee)
          >>> bodyguard.action(gamestate)
          >>> bee.health
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试保镖是否执行投掷蚁的行动
          >>> bodyguard = BodyguardAnt()
          >>> thrower = ThrowerAnt()
          >>> bee = Bee(2)
          >>> # 先放置投掷蚁，再放置保镖
          >>> gamestate.places["tunnel_0_0"].add_insect(thrower)
          >>> gamestate.places["tunnel_0_0"].add_insect(bodyguard)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee)
          >>> bodyguard.action(gamestate)
          >>> bee.health
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试移除保镖时不会移除被容纳的蚂蚁
          >>> place = gamestate.places['tunnel_0_0']
          >>> bodyguard = BodyguardAnt()
          >>> test_ant = Ant(1)
          >>> # 先添加保镖
          >>> place.add_insect(bodyguard)
          >>> place.add_insect(test_ant)
          >>> gamestate.remove_ant('tunnel_0_0')
          >>> place.ant is test_ant
          True
          >>> bodyguard.place is None
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试移除保镖时不会移除被容纳的蚂蚁
          >>> place = gamestate.places['tunnel_0_0']
          >>> bodyguard = BodyguardAnt()
          >>> test_ant = Ant(1)
          >>> # 先添加蚂蚁
          >>> place.add_insect(test_ant)
          >>> place.add_insect(bodyguard)
          >>> gamestate.remove_ant('tunnel_0_0')
          >>> place.ant is test_ant
          True
          >>> bodyguard.place is None
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试受到保镖保护的蚂蚁仍保留实例属性
          >>> test_ant = Ant()
          >>> def new_action(gamestate):
          ...     test_ant.health += 9000
          >>> test_ant.action = new_action
          >>> place = gamestate.places['tunnel_0_0']
          >>> bodyguard = BodyguardAnt()
          >>> place.add_insect(test_ant)
          >>> place.add_insect(bodyguard)
          >>> place.ant.action(gamestate)
          >>> place.ant.ant_contained.health
          9001
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试一个 BodyguardAnt 不能容纳另外两只蚂蚁
          >>> bodyguard = BodyguardAnt()
          >>> first_ant = ThrowerAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(bodyguard)
          >>> place.add_insect(first_ant)
          >>> second_ant = ThrowerAnt()
          >>> place.add_insect(second_ant)
          Traceback (most recent call last):
          ...
          AssertionError: Too many ants in tunnel_0_0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 BodyguardAnt 不能容纳另一个 BodyguardAnt
          >>> bodyguard1 = BodyguardAnt()
          >>> bodyguard2 = BodyguardAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(bodyguard1)
          >>> place.add_insect(bodyguard2)
          Traceback (most recent call last):
          ...
          AssertionError: Too many ants in tunnel_0_0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 BodyguardAnt 承受全部伤害
          >>> thrower = ThrowerAnt()
          >>> bodyguard = BodyguardAnt()
          >>> bee = Bee(1)
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(thrower)
          >>> place.add_insect(bodyguard)
          >>> place.add_insect(bee)
          >>> bodyguard.health
          2
          >>> bee.action(gamestate)
          >>> (bodyguard.health, thrower.health)
          (1, 1)
          >>> bee.action(gamestate)
          >>> (bodyguard.health, thrower.health)
          (0, 1)
          >>> bodyguard.place is None
          True
          >>> place.ant is thrower
          True
          >>> bee.action(gamestate)
          >>> thrower.health
          0
          >>> place.ant is None
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试是否正确调用死亡回调函数
          >>> original_zero_health_callback = Insect.zero_health_callback
          >>> Insect.zero_health_callback = lambda x: print("insect died")
          >>> place = gamestate.places["tunnel_0_0"]
          >>> bee = Bee(3)
          >>> bodyguard = BodyguardAnt()
          >>> ant = ThrowerAnt()
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> place.add_insect(bodyguard)
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
      >>> from ants import *
      >>> beehive, layout = Hive(AssaultPlan()), dry_layout
      >>> gamestate = GameState(beehive, ant_types(), layout, (1, 9))
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
          >>> BodyguardAnt.implemented
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
