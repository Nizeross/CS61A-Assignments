test = {
  'name': 'Problem EC 2',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # 测试状态参数
          >>> slow = SlowThrower()
          >>> scary = ScaryThrower()
          >>> SlowThrower.food_cost
          50ae32be3e31df6c59633df7fdfb3a72
          # locked
          >>> ScaryThrower.food_cost
          50ae32be3e31df6c59633df7fdfb3a72
          # locked
          >>> slow.health
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> scary.health
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
          >>> slow.action(gamestate)
          >>> gamestate.time = 1
          >>> bee.action(gamestate)
          >>> bee.place.name
          46f9851313dc368f747e69f1670450da
          # locked
          >>> gamestate.time += 1
          >>> bee.action(gamestate)
          >>> bee.place.name
          040b6ad98a7360eba8d493c250a9b82e
          # locked
          >>> for _ in range(3):
          ...    gamestate.time += 1
          ...    bee.action(gamestate)
          >>> bee.place.name
          8344c19df8015306b462119efc8419cb
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试恐吓效果
          >>> scary = ScaryThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scary)
          >>> gamestate.places["tunnel_0_4"].add_insect(bee)
          >>> scary.action(gamestate)
          >>> bee.action(gamestate)
          >>> bee.place.name # ScaryThrower 应使恐吓持续两回合（第一回合）
          46f9851313dc368f747e69f1670450da
          # locked
          >>> bee.action(gamestate)
          >>> bee.place.name # ScaryThrower 应使恐吓持续两回合（第二回合）
          32a5320f2c5021a9b66582af8b364dc7
          # locked
          >>> bee.action(gamestate)
          >>> bee.place.name # ScaryThrower 的效果已消失
          46f9851313dc368f747e69f1670450da
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # Scary 蜜蜂蜇刺一只蚂蚁
          >>> scary = ScaryThrower()
          >>> harvester = HarvesterAnt()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scary)
          >>> gamestate.places["tunnel_0_4"].add_insect(bee)
          >>> gamestate.places["tunnel_0_5"].add_insect(harvester)
          >>> scary.action(gamestate)
          >>> bee.action(gamestate)
          >>> bee.place.name # ScaryThrower 应使恐吓持续两回合
          46f9851313dc368f747e69f1670450da
          # locked
          >>> harvester.health
          d89cf7c79d5a479b0f636734143ed5e6
          # locked
          >>> bee.action(gamestate)
          >>> harvester.health
          73b94a1326ae2e803c3421016112207b
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试状态效果是否可以叠加
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> slow_place = gamestate.places["tunnel_0_0"]
          >>> bee_place = gamestate.places["tunnel_0_8"]
          >>> slow_place.add_insect(slow)
          >>> bee_place.add_insect(bee)
          >>> slow.action(gamestate)    # 对蜜蜂施加两次减速
          >>> slow.action(gamestate)
          >>> gamestate.time = 1
          >>> bee.action(gamestate) # 不行动。减速效果剩余 5 回合。
          >>> bee.place.name
          'tunnel_0_8'
          >>> gamestate.time = 2
          >>> bee.action(gamestate) # 向前移动。减速效果剩余 4 回合。
          >>> bee.place.name
          'tunnel_0_7'
          >>> gamestate.time = 3
          >>> bee.action(gamestate) # 不行动。减速效果剩余 3 回合。
          >>> bee.place.name
          'tunnel_0_7'
          >>> gamestate.time = 4
          >>> bee.action(gamestate) # 向前移动。减速效果剩余 2 回合。
          >>> bee.place.name
          'tunnel_0_6'
          >>> gamestate.time = 5
          >>> bee.action(gamestate) # 不行动。减速效果剩余 1 回合。
          >>> bee.place.name
          'tunnel_0_6'
          >>> gamestate.time = 6      # 向前移动。减速状态现已消失
          >>> bee.action(gamestate)
          >>> bee.place.name
          'tunnel_0_5'
          >>> gamestate.time = 7      # 减速状态已消失
          >>> bee.action(gamestate)
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time = 8      # 减速状态已消失
          >>> bee.action(gamestate)
          >>> bee.place.name
          'tunnel_0_3'
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试多只被恐吓的蜜蜂
          >>> scare1 = ScaryThrower()
          >>> scare2 = ScaryThrower()
          >>> bee1 = Bee(3)
          >>> bee2 = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scare1)
          >>> gamestate.places["tunnel_0_1"].add_insect(bee1)
          >>> gamestate.places["tunnel_0_4"].add_insect(scare2)
          >>> gamestate.places["tunnel_0_5"].add_insect(bee2)
          >>> scare1.action(gamestate)
          >>> scare2.action(gamestate)
          >>> bee1.action(gamestate)
          >>> bee2.action(gamestate)
          >>> bee1.place.name
          'tunnel_0_2'
          >>> bee2.place.name
          'tunnel_0_6'
          >>> bee1.action(gamestate)
          >>> bee2.action(gamestate)
          >>> bee1.place.name
          'tunnel_0_3'
          >>> bee2.place.name
          'tunnel_0_7'
          >>> bee1.action(gamestate)
          >>> bee2.action(gamestate)
          >>> bee1.place.name
          'tunnel_0_2'
          >>> bee2.place.name
          'tunnel_0_6'
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> scare = ScaryThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scare)
          >>> gamestate.places["tunnel_0_1"].add_insect(bee)
          >>> scare.action(gamestate)
          >>> bee.action(gamestate)
          >>> bee.place.name
          'tunnel_0_2'
          >>> bee.action(gamestate)
          >>> bee.place.name
          'tunnel_0_3'
          >>> #
          >>> # 同一只蜜蜂不应被恐吓多次
          >>> scare.action(gamestate)
          >>> bee.action(gamestate)
          >>> bee.place.name
          'tunnel_0_2'
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试持续多回合的状态叠加
          >>> scary = ScaryThrower()
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scary)
          >>> gamestate.places["tunnel_0_1"].add_insect(slow)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee)
          >>> scary.action(gamestate) # 恐吓蜜蜂一次
          >>> gamestate.time = 0
          >>> bee.action(gamestate) # 受到恐吓
          >>> bee.place.name
          'tunnel_0_4'
          >>> for _ in range(3): # 对蜜蜂施加三次减速，总共持续 5 回合
          ...    slow.action(gamestate)
          >>> gamestate.time = 1
          >>> bee.action(gamestate) # 受到恐吓，同时还有 5 回合减速，因此暂时不后退
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time = 2
          >>> bee.action(gamestate) # 此后不再受到恐吓，但仍有 4 回合减速
          >>> bee.place.name #  这是偶数回合，因此蜜蜂可以因恐吓而后退
          'tunnel_0_5'
          >>> gamestate.time = 3
          >>> bee.action(gamestate) # 减速还剩 3 回合
          >>> bee.place.name
          'tunnel_0_5'
          >>> gamestate.time = 4
          >>> bee.action(gamestate) # 减速还剩 2 回合
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time = 5
          >>> bee.action(gamestate) # 减速还剩 1 回合
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time = 6
          >>> bee.action(gamestate) # 不再减速
          >>> bee.place.name
          'tunnel_0_3'
          >>> gamestate.time = 7
          >>> bee.action(gamestate) # 不再减速
          >>> bee.place.name
          'tunnel_0_2'
          >>> gamestate.time = 8
          >>> bee.action(gamestate) # 不再减速
          >>> bee.place.name
          'tunnel_0_1'
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> scary = ScaryThrower()
          >>> slow = SlowThrower()
          >>> bee = Bee(3)
          >>> gamestate.places["tunnel_0_0"].add_insect(scary)
          >>> gamestate.places["tunnel_0_1"].add_insect(slow)
          >>> gamestate.places["tunnel_0_3"].add_insect(bee)
          >>> slow.action(gamestate) # 使蜜蜂减速
          >>> scary.action(gamestate) # 恐吓蜜蜂
          >>> bee.place.name
          'tunnel_0_3'
          >>> gamestate.time = 0
          >>> bee.action(gamestate) # 同时受到恐吓和减速；游戏时间为偶数，因此可以后退
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time = 1
          >>> bee.action(gamestate) # 同时受到恐吓和减速；游戏时间为奇数，因此不能后退
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time = 2
          >>> bee.action(gamestate) # 同时受到恐吓和减速；游戏时间为偶数，因此可以后退，此后不再受到恐吓
          >>> bee.place.name
          'tunnel_0_5'
          >>> gamestate.time = 3
          >>> bee.action(gamestate) # 减速中，游戏时间为奇数，不能前进
          >>> bee.place.name
          'tunnel_0_5'
          >>> gamestate.time = 4
          >>> bee.action(gamestate) # 减速中，游戏时间为偶数，可以前进
          >>> bee.place.name
          'tunnel_0_4'
          >>> gamestate.time = 3
          >>> bee.action(gamestate) # 既不受恐吓，也不减速
          >>> bee.place.name
          'tunnel_0_3'
          >>> gamestate.time = 2
          >>> bee.action(gamestate) # 既不受恐吓，也不减速
          >>> bee.place.name
          'tunnel_0_2'
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> ScaryThrower.implemented
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          >>> SlowThrower.implemented
          c7a88a0ffd3aef026b98eef6e7557da3
          # locked
          """,
          'hidden': False,
          'locked': True,
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
