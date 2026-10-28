test = {
  'name': 'Problem 7',
  'points': 3,
  'suites': [
    {
      'cases': [
        {
          'answer': '9bdaf9d21c5bc25bc5b465def43443fc',
          'choices': [
            r"""
            instance, each HungryAnt instance chews independently of other
            HungryAnt instances
            """,
            'instance, all HungryAnt instances in the game chew simultaneously',
            r"""
            class, each HungryAnt instance chews independently of other
            HungryAnt instances
            """,
            'class, all HungryAnt instances in the game chew simultaneously'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'Should cooldown be an instance or class attribute? Why?'
        },
        {
          'answer': 'de71be3fec0cba010db49e459529fa5e',
          'choices': [
            'When it is not chewing, i.e. when its cooldown attribute is 0',
            'When it is chewing, i.e. when its cooldown attribute is at least 1',
            'Each turn',
            'Whenever a Bee is in its place'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'When is a HungryAnt able to eat a Bee?'
        },
        {
          'answer': '30589d40710d13dfd27efd5cdd28c0f0',
          'choices': [
            'A random Bee in the same place as itself',
            'The closest Bee in front of it',
            'The closest Bee behind it',
            'The closest Bee in either direction'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'When a HungryAnt is able to eat, which Bee does it eat?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # 测试 HungryAnt 的参数
          >>> hungry = HungryAnt()
          >>> HungryAnt.food_cost
          c9452203eb0b0f0bd2454586a6c2fc5c
          # locked
          >>> hungry.health
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> hungry.chew_cooldown
          81a7d27d1a4a958871bb97b545b871db
          # locked
          >>> hungry.cooldown
          73b94a1326ae2e803c3421016112207b
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
          >>> Ant.__init__ = lambda self, health: print("init")  # 如果报错，说明没有正确调用父类构造函数。
          >>> hungry = HungryAnt()
          init
          >>> Ant.__init__ = original
          >>> hungry = HungryAnt()
          >>> # 类属性与实例属性
          >>> hasattr(HungryAnt, 'cooldown')  # cooldown 应为实例属性
          False
          >>> hungry.cooldown  # HungryAnt 已准备好吃蜜蜂
          0
          >>> HungryAnt.chew_cooldown
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 HungryAnt 吞食并消化蜜蜂
          >>> hungry = HungryAnt()
          >>> bee1 = Bee(1000)              # 一只生命值为 1000 的蜜蜂
          >>> place = gamestate.places["tunnel_0_0"]
          >>> place.add_insect(hungry)
          >>> place.add_insect(bee1)         # 将蜜蜂添加到 HungryAnt 所在地点
          >>> hungry.action(gamestate)
          >>> bee1.health
          0
          >>> bee2 = Bee(1)                 # 一只生命值为 1 的蜜蜂
          >>> place.add_insect(bee2)
          >>> for _ in range(3):
          ...     hungry.action(gamestate)     # 正在消化，不进食
          >>> bee2.health
          1
          >>> hungry.action(gamestate)
          >>> bee2.health
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 HungryAnt 吞食后消化指定时长
          >>> hungry = HungryAnt()
          >>> bee1 = Bee(1000)              # 一只生命值为 1000 的蜜蜂
          >>> place = gamestate.places["tunnel_0_0"]
          >>> place.add_insect(hungry)
          >>> place.add_insect(bee1)         # 将蜜蜂添加到 HungryAnt 所在地点
          >>> hungry.action(gamestate)
          >>> bee1.health
          0
          >>> bee2 = Bee(1)                 # 一只生命值为 1 的蜜蜂
          >>> place.add_insect(bee2)
          >>> for _ in range(2):
          ...     hungry.action(gamestate)     # 正在消化，不进食，此时不应结束消化！
          >>> bee2.health
          1
          >>> hungry.action(gamestate)
          >>> bee2.health
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 HungryAnt 吞食并消化蜜蜂
          >>> hungry = HungryAnt()
          >>> super_bee, wimpy_bee = Bee(1000), Bee(1)
          >>> place = gamestate.places["tunnel_0_0"]
          >>> place.add_insect(hungry)
          >>> place.add_insect(super_bee)
          >>> hungry.action(gamestate)         # super_bee 也不是 HungryAnt 的对手！
          >>> super_bee.health
          73b94a1326ae2e803c3421016112207b
          # locked
          >>> place.add_insect(wimpy_bee)
          >>> for _ in range(3):
          ...     hungry.action(gamestate)     # 正在咀嚼，不进食
          >>> wimpy_bee.health
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> hungry.action(gamestate)         # 再次开始进食！
          >>> wimpy_bee.health
          73b94a1326ae2e803c3421016112207b
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 HungryAnt 只在消化时等待
          >>> hungry = HungryAnt()
          >>> place = gamestate.places["tunnel_0_0"]
          >>> place.add_insect(hungry)
          >>> # 等待几回合后再添加蜜蜂
          >>> for _ in range(5):
          ...     hungry.action(gamestate)  # 此时不应处于消化状态
          >>> bee = Bee(3)
          >>> place.add_insect(bee)
          >>> hungry.action(gamestate)  # 开饭了！
          >>> bee.health
          0
          >>> bee = Bee(3)
          >>> place.add_insect(bee)
          >>> for _ in range(3):
          ...     hungry.action(gamestate)     # 应处于消化状态
          >>> bee.health
          3
          >>> hungry.action(gamestate)
          >>> bee.health
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试从实例上查找 HungryAnt 的消化时长
          >>> very_hungry = HungryAnt()  # 添加一只非常饥饿的蚂蚁
          >>> HungryAnt.chew_cooldown = 0
          >>> place = gamestate.places["tunnel_0_0"]
          >>> place.add_insect(very_hungry)
          >>> for _ in range(100):
          ...     place.add_insect(Bee(3))
          >>> for _ in range(100):
          ...     very_hungry.action(gamestate)   # 吃掉所有蜜蜂！
          >>> len(place.bees)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 HungryAnt 在消化时死亡
          >>> hungry = HungryAnt()
          >>> place = gamestate.places["tunnel_0_0"]
          >>> place.add_insect(hungry)
          >>> place.add_insect(Bee(3))
          >>> hungry.action(gamestate)
          >>> len(place.bees)
          0
          >>> bee = Bee(3)
          >>> place.add_insect(bee)
          >>> bee.action(gamestate) # 蜜蜂杀死正在消化的蚂蚁
          >>> place.ant is None
          True
          >>> len(place.bees)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 HungryAnt 不能吃掉其他地点的蜜蜂
          >>> hungry = HungryAnt()
          >>> gamestate.places["tunnel_0_0"].add_insect(hungry)
          >>> gamestate.places["tunnel_0_1"].add_insect(Bee(3))
          >>> hungry.action(gamestate)
          >>> len(gamestate.places["tunnel_0_1"].bees)
          1
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
          >>> ant = HungryAnt()
          >>> bee = Bee(1000)              # 一只生命值为 1000 的蜜蜂
          >>> place = gamestate.places["tunnel_0_0"]
          >>> place.add_insect(bee)
          >>> place.add_insect(ant)
          >>> ant.action(gamestate) # 如果此测试失败，可能是没有正确调用 Ant.reduce_health 或 Insect.reduce_health
          insect died
          >>> Insect.zero_health_callback = original_zero_health_callback
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 HungryAnt 吞食时会移除蜜蜂。
          >>> hungry = HungryAnt()
          >>> place = gamestate.places["tunnel_0_0"]
          >>> place.add_insect(hungry)
          >>> place.add_insect(Bee(3))
          >>> place.add_insect(Bee(3))
          >>> hungry.action(gamestate)
          >>> len(place.bees)
          1
          >>> bee = Bee(3)
          >>> place.add_insect(bee)
          >>> bee.action(gamestate) # 蜜蜂杀死正在消化的蚂蚁
          >>> place.ant is None
          True
          >>> len(place.bees)
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 HungryAnt 在所在地点随机选择一只蜜蜂，并将其生命值降为 0。
          >>> hungry = HungryAnt()
          >>> HungryAnt.chew_cooldown = 0
          >>> place = gamestate.places["tunnel_0_0"]
          >>> place.add_insect(hungry)
          >>> first_bee_chosen_count = 0
          >>> for _ in range(1000):
          ...     place.add_insect(Bee(1)) # 向地点添加一只生命值为 1 的蜜蜂
          ...     place.add_insect(Bee(2)) # 向地点添加第二只蜜蜂，其生命值为 2
          ...     hungry.action(gamestate) # 随机吃掉其中一只蜜蜂
          ...     assert len(place.bees) == 1, "A bee was not eaten! Make sure you are reducing the bee's health by the correct amount."
          ...     if place.bees[0].health == 2:
          ...             first_bee_chosen_count += 1
          ...     place.remove_insect(place.bees[0])
          >>> first_bee_chosen_count < 1000 # 若随机选择蜜蜂，则 HungryAnt 吃掉第一只蜜蜂的次数应以很高概率少于 1000
          True
          >>> first_bee_chosen_count > 0 # 若随机选择蜜蜂，则 HungryAnt 应以很高概率至少吃掉第一只蜜蜂一次
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
          >>> HungryAnt.implemented
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
