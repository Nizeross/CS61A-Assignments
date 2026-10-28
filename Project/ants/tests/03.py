test = {
  'name': 'Problem 3',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'answer': 'e3b9ee99ac396e56608b45e886edbec1',
          'choices': [
            r"""
            The ThrowerAnt finds the nearest place including and in front of its
            own place that has Bees and throws at a random Bee in that place
            """,
            r"""
            The ThrowerAnt finds the nearest place behind its own place
            that has Bees and throws at a random Bee in that place
            """,
            r"""
            The ThrowerAnt finds the nearest place in either direction that has
            Bees and throws at a random Bee in that place
            """,
            'The ThrowerAnt throws at a random Bee in its own Place'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What Bee should a ThrowerAnt throw at?'
        },
        {
          'answer': '9bd9c23a391f841e8d9e4147c56659a7',
          'choices': [
            "The place's entrance instance attribute",
            "The place's exit instance attribute",
            'Increment the place by 1',
            'Decrement the place by 1'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'How do you get the Place object in front of another Place object?'
        },
        {
          'answer': '2ca313dd416803bfaecbcf4a2d1851c1',
          'choices': [
            'The Hive',
            'None',
            'An empty Place'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What is the entrance of the first Place in a tunnel (i.e. where do the bees enter from)?'
        },
        {
          'answer': '7e8d1faa22ac0ad46c7db356d171f71c',
          'choices': [
            'by using the is_hive attribute of the place instance',
            'by checking the bees attribute of the place instance',
            'by checking the ant attribute of the place instance'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'How can you determine if a given Place is the Hive?'
        },
        {
          'answer': '044ef3c0c6fd739b6260fe6f6cae71dd',
          'choices': [
            'None',
            'A random Bee in the Hive',
            'The closest Bee behind the ThrowerAnt'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What should nearest_bee return if there is no Bee in front of the ThrowerAnt in the tunnel?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # 测试 nearest_bee
          >>> near_bee = Bee(2) # 一只生命值为 2 的蜜蜂
          >>> far_bee = Bee(3)  # 一只生命值为 3 的蜜蜂
          >>> hive_bee = Bee(4) # 一只生命值为 4 的蜜蜂
          >>> hive_place = gamestate.beehive
          >>> hive_place.is_hive # 检查此地点是否为 Hive
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> hive_place.add_insect(hive_bee)
          >>> thrower.nearest_bee() is hive_bee # 蜂巢中的蜜蜂永远不能被攻击
          03456a09f22295a39ca84d133a26f63d
          # locked
          >>> near_place = gamestate.places['tunnel_0_3']
          >>> far_place = gamestate.places['tunnel_0_6']
          >>> near_place.is_hive # 检查此地点是否为 Hive
          03456a09f22295a39ca84d133a26f63d
          # locked
          >>> near_place.add_insect(near_bee)
          >>> far_place.add_insect(far_bee)
          >>> nearest_bee = thrower.nearest_bee()
          >>> thrower.place is ant_place    # 不要修改 self.place！
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> nearest_bee is far_bee
          03456a09f22295a39ca84d133a26f63d
          # locked
          >>> nearest_bee is near_bee
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> nearest_bee.health
          20d533d3e06345c8bd7072212867f2d1
          # locked
          >>> thrower.action(gamestate)    # 攻击！ThrowerAnt 造成 1 点伤害
          >>> near_bee.health
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> far_bee.health
          81a7d27d1a4a958871bb97b545b871db
          # locked
          >>> thrower.place is ant_place    # 不要修改 self.place！
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试最近的蜜蜂不在蜂巢中
          >>> beehive = gamestate.beehive
          >>> bee = Bee(2)
          >>> beehive.add_insect(bee)      # 向蜂巢添加一只蜜蜂
          >>> thrower.nearest_bee() is bee
          False
          >>> thrower.action(gamestate)    # 尝试攻击
          >>> bee.health                 # 蜜蜂的生命值不应改变
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 ThrowerAnt 攻击同一地块上的蜜蜂
          >>> near_bee = Bee(2)
          >>> ant_place.add_insect(near_bee)
          >>> thrower.nearest_bee() is near_bee
          True
          >>> thrower.action(gamestate)   # 攻击！
          >>> near_bee.health           # 应造成 1 点伤害
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 ThrowerAnt 攻击隧道末端的蜜蜂
          >>> near_bee = Bee(2)
          >>> gamestate.places["tunnel_0_8"].add_insect(near_bee)
          >>> thrower.nearest_bee() is near_bee
          True
          >>> thrower.action(gamestate)   # 攻击！
          >>> near_bee.health           # 应造成 1 点伤害
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 ThrowerAnt 攻击距离为 4 个地点的蜜蜂
          >>> near_bee = Bee(2)
          >>> gamestate.places["tunnel_0_4"].add_insect(near_bee)
          >>> thrower.nearest_bee() is near_bee
          True
          >>> thrower.action(gamestate)   # 攻击！
          >>> near_bee.health           # 应造成 1 点伤害
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 ThrowerAnt 随机选择目标
          >>> bee1 = Bee(1001)
          >>> bee2 = Bee(1001)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee1)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee2)
          >>> # 投掷 1000 次。第一只蜜蜂应受到约 1000*1/2 = 500 点伤害，
          >>> # 剩余生命值约为 501。
          >>> for _ in range(1000):
          ...     thrower.action(gamestate)
          >>> # 测试 bee1 受到的伤害是否处于 6 个标准差（约 95 点伤害）的范围内
          >>> # 若均匀随机选择蜜蜂，这一条件成立的概率为 99.9999998%。
          >>> def dmg_within_tolerance():
          ...     return abs(bee1.health-501) < 95
          >>> dmg_within_tolerance()
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> from ants import *
          >>> ThrowerAnt.implemented
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
      >>> thrower = ThrowerAnt()
      >>> ant_place = gamestate.places["tunnel_0_0"]
      >>> ant_place.add_insect(thrower)
      >>> #
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
