test = {
  'name': 'Problem EC 3',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'answer': 'd867280d511300bf4fa42dae8866a575',
          'choices': [
            r"""
            All Ant types have a blocks_path attribute that is inherited from
            the Ant superclass
            """,
            'Only the NinjaAnt has a blocks_path attribute',
            'None of the Ant subclasses have a blocks_path attribute',
            'All Ant types except for NinjaAnt have a blocks_path attribute'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'Which Ant types have a blocks_path attribute?'
        },
        {
          'answer': '0a74e2e9020b74e8968cc9a0ed1ef38d',
          'choices': [
            'blocks_path is True for every Ant subclass except NinjaAnt',
            'blocks_path is False for every Ant subclass except NinjaAnt',
            'blocks_path is True for all Ants',
            'blocks_path is False for all Ants'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What is the value of blocks_path for each Ant subclass?'
        },
        {
          'answer': 'ad3ed5994969f15b71d99c706bb59339',
          'choices': [
            "When there is an Ant in the Bee's place",
            r"""
            When there is an Ant whose blocks_path attribute is True in the
            Bee's place
            """,
            "When there is not an NinjaAnt in the Bee's place",
            "When there are no Ants in the Bee's place"
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'When is the path of a Bee blocked?'
        },
        {
          'answer': '94f9395e9fd1d730fd15d335ecdaedd2',
          'choices': [
            "Reduces the Bee's health by the NinjaAnt's damage attribute",
            "Reduces the Bee's health to 0",
            "Nothing, the NinjaAnt doesn't damage Bees",
            "Blocks the Bee's path"
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What does a NinjaAnt do to each Bee that flies in its place?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # 测试 NinjaAnt 的参数
          >>> ninja = NinjaAnt()
          >>> ninja.health
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> NinjaAnt.food_cost
          62674984f877ec783f37e8b8b9c264d0
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 blocks_path
          >>> NinjaAnt.blocks_path
          03456a09f22295a39ca84d133a26f63d
          # locked
          >>> HungryAnt.blocks_path
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> FireAnt.blocks_path
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 NinjaAnt 不阻挡蜜蜂
          >>> p0 = gamestate.places["tunnel_0_0"]
          >>> p1 = gamestate.places["tunnel_0_1"]  # p0 是 p1 的出口
          >>> bee = Bee(2)
          >>> ninja = NinjaAnt()
          >>> thrower = ThrowerAnt()
          >>> p0.add_insect(thrower)            # 向 p0 添加 ThrowerAnt
          >>> p1.add_insect(bee)
          >>> p1.add_insect(ninja)              # 向 p1 添加 Bee 和 NinjaAnt
          >>> bee.action(gamestate)
          >>> bee.place is ninja.place          # NinjaAnt 是否阻挡了 Bee 的移动？
          03456a09f22295a39ca84d133a26f63d
          # locked
          >>> bee.place is p0
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> ninja.health
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> bee.action(gamestate)
          >>> bee.place is p0                   # ThrowerAnt 是否阻挡了 Bee 的移动？
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试不阻路的蚂蚁确实不会阻挡蜜蜂
          >>> p0 = gamestate.places["tunnel_0_0"]
          >>> p1 = gamestate.places["tunnel_0_1"]  # p0 是 p1 的出口
          >>> bee = Bee(2)
          >>> ninja_fire = FireAnt(1)
          >>> ninja_fire.blocks_path = False
          >>> thrower = ThrowerAnt()
          >>> p0.add_insect(thrower)            # 向 p0 添加 ThrowerAnt
          >>> p1.add_insect(bee)
          >>> p1.add_insect(ninja_fire)              # 向 p1 添加 Bee 和 NinjaAnt
          >>> bee.action(gamestate)
          >>> bee.place is ninja_fire.place          # 具有忍者特性的 FireAnt 是否阻挡了 Bee 的移动？
          03456a09f22295a39ca84d133a26f63d
          # locked
          >>> bee.place is p0
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> ninja_fire.health
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> bee.action(gamestate)
          >>> bee.place is p0                   # ThrowerAnt 是否阻挡了 Bee 的移动？
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 NinjaAnt 攻击所在地点的所有蜜蜂
          >>> test_place = gamestate.places["tunnel_0_0"]
          >>> for _ in range(3):
          ...     test_place.add_insect(Bee(2))
          >>> ninja = NinjaAnt()
          >>> test_place.add_insect(ninja)
          >>> ninja.action(gamestate)   # 应攻击该地点的所有蜜蜂
          >>> [bee.health for bee in test_place.bees]
          [1, 1, 1]
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 NinjaAnt 没有写死伤害值
          >>> test_place = gamestate.places["tunnel_0_0"]
          >>> for _ in range(3):
          ...     test_place.add_insect(Bee(100))
          >>> ninja = NinjaAnt()
          >>> ninja.damage = 50
          >>> test_place.add_insect(ninja)
          >>> ninja.action(gamestate)   # 应攻击该地点的所有蜜蜂
          >>> [bee.health for bee in test_place.bees]
          [50, 50, 50]
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试即使有蜜蜂死亡，NinjaAnt 仍会攻击所有蜜蜂
          >>> test_place = gamestate.places["tunnel_0_0"]
          >>> for _ in range(3):
          ...     test_place.add_insect(Bee(1))
          >>> ninja = NinjaAnt()
          >>> test_place.add_insect(ninja)
          >>> ninja.action(gamestate)   # 应攻击该地点的所有蜜蜂
          >>> len(test_place.bees)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试是否从实例上查找 damage
          >>> place = gamestate.places["tunnel_0_0"]
          >>> bee = Bee(900)
          >>> place.add_insect(bee)
          >>> buffNinja = NinjaAnt()
          >>> buffNinja.damage = 500  # 磨快刀剑
          >>> place.add_insect(buffNinja)
          >>> buffNinja.action(gamestate)
          >>> bee.health
          400
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 NinjaAnt 独处时不会报错
          >>> ninja = NinjaAnt()
          >>> gamestate.places["tunnel_0_0"].add_insect(ninja)
          >>> ninja.action(gamestate)
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 Bee 独处时不会报错
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_1"].add_insect(bee)
          >>> bee.action(gamestate)
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
          >>> NinjaAnt.implemented
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
