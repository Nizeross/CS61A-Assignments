test = {
  'name': 'Problem 12',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'answer': '7f1e876193ad01466bb1f843c9a17b72',
          'choices': [
            r"""
            Attacks the nearest bee and doubles the damage of all the ants
            behind her (that haven't already been doubled)
            """,
            r"""
            Doubles the damage of all the ants behind her (that haven't
            already been doubled)
            """,
            r"""
            Doubles the damage of all the ants in front of her (that haven't
            already been doubled)
            """,
            r"""
            Doubles the damage of all the ants in the colony (that haven't
            already been doubled)
            """
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What does a QueenAnt do each turn?'
        },
        {
          'answer': '5513089cd61eeda577f95f887b408517',
          'choices': [
            'If a Bee reaches the end of a tunnel or a QueenAnt dies',
            'If there are no ants left in the colony',
            'If a second QueenAnt is placed in the colony',
            'If a Bee attacks a QueenAnt'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'Under what circumstances do Ants lose the game?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # 测试 QueenAnt 的参数
          >>> QueenAnt.food_cost
          7cd035adf49fc93a635b4e8bb2e28bd4
          # locked
          >>> queen = QueenAnt()
          >>> queen.health
          d89cf7c79d5a479b0f636734143ed5e6
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
      >>> beehive = Hive(AssaultPlan())
      >>> dimensions = (2, 9)
      >>> gamestate = GameState(beehive, ant_types(), dry_layout, dimensions, food=100)
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # 放置 QueenAnt
          >>> queen = ants.QueenAnt()
          >>> front_ant, back_ant = ants.ThrowerAnt(), ants.ThrowerAnt()
          >>> tunnel = [gamestate.places['tunnel_0_{0}'.format(i)]
          ...         for i in range(9)]
          >>> tunnel[1].add_insect(back_ant)
          >>> tunnel[7].add_insect(front_ant)
          >>> tunnel[4].ant is None
          True
          >>> back_ant.damage           # 此时蚂蚁的伤害尚不应翻倍
          1
          >>> front_ant.damage
          1
          >>> tunnel[4].add_insect(queen)
          >>> queen.action(gamestate)
          >>> back_ant.damage           # 蚁后身后的蚂蚁应具有双倍伤害
          2
          >>> front_ant.damage
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试伤害倍增效果
          >>> queen_tunnel, side_tunnel = [[gamestate.places['tunnel_{0}_{1}'.format(i, j)]
          ...         for j in range(9)] for i in range(2)]
          >>> # 布局
          >>> # queen_tunnel：[后方、保镖/被保护者、蚁后、前方、蜜蜂]
          >>> # side_tunnel：[侧方、空、空、空、侧方蜜蜂]
          >>> queen = ants.QueenAnt()
          >>> back = ants.ThrowerAnt()
          >>> front = ants.ThrowerAnt()
          >>> guard = ants.BodyguardAnt()
          >>> guarded = ants.ThrowerAnt()
          >>> side = ants.ThrowerAnt()
          >>> bee = ants.Bee(10)
          >>> side_bee = ants.Bee(10)
          >>> queen_tunnel[0].add_insect(back)
          >>> queen_tunnel[1].add_insect(guard)
          >>> queen_tunnel[1].add_insect(guarded)
          >>> queen_tunnel[2].add_insect(queen)
          >>> queen_tunnel[3].add_insect(front)
          >>> side_tunnel[0].add_insect(side)
          >>> queen_tunnel[4].add_insect(bee)
          >>> side_tunnel[4].add_insect(side_bee)
          >>> queen.action(gamestate)
          >>> bee.health
          9
          >>> back.action(gamestate)
          >>> bee.health
          7
          >>> front.action(gamestate)
          >>> bee.health
          6
          >>> guard.action(gamestate)
          >>> bee.health # 如果结果为 5，你可能忘了将保镖内部蚂蚁的伤害翻倍
          4
          >>> side.action(gamestate)
          >>> side_bee.health
          9
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> import ants, importlib
      >>> importlib.reload(ants)
      >>> beehive = ants.Hive(ants.AssaultPlan())
      >>> dimensions = (2, 9)
      >>> gamestate = ants.GameState(beehive, ants.ant_types(),
      ...                            ants.dry_layout, dimensions, food=20)
      >>> ants.ants_lose = lambda: None
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # 测试游戏结束
          >>> queen = ants.QueenAnt()
          >>> tunnel = [gamestate.places['tunnel_0_{0}'.format(i)]
          ...           for i in range(9)]
          >>> tunnel[4].add_insect(queen)
          >>> bee = ants.Bee(3)
          >>> tunnel[6].add_insect(bee)     # 蜜蜂与蚁后位于不同地点
          >>> bee.action(gamestate)         # 游戏不应结束
          >>> bee.move_to(tunnel[4])        # 蜜蜂移动到蚁后所在地点
          >>> bee.action(gamestate)         # 游戏应结束
          AntsLoseException
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试没有可增强的蚂蚁时蚁后不会报错
          >>> queen = ants.QueenAnt()
          >>> gamestate.places['tunnel_0_2'].add_insect(queen)
          >>> queen.action(gamestate)
          >>> # 攻击蜜蜂
          >>> bee = ants.Bee(3)
          >>> gamestate.places['tunnel_0_4'].add_insect(bee)
          >>> queen.action(gamestate)
          >>> bee.health # 蚁后仍应击中蜜蜂
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试 QueenAnt 的 action 方法
          >>> queen = ants.QueenAnt()
          >>> bee = ants.Bee(10)
          >>> ant = ants.ThrowerAnt()
          >>> gamestate.places['tunnel_0_0'].add_insect(ant)
          >>> gamestate.places['tunnel_0_1'].add_insect(queen)
          >>> gamestate.places['tunnel_0_4'].add_insect(bee)
          >>> queen.action(gamestate)
          >>> bee.health   # 蚁后应对蜜蜂造成伤害
          9
          >>> ant.damage  # 蚁后应将伤害翻倍
          2
          >>> ant.action(gamestate)
          >>> bee.health   # 若失败，则 ThrowerAnt 的伤害不正确
          7
          >>> queen.health   # 蚁后万岁
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 全面测试伤害翻倍
          >>> queen_tunnel, side_tunnel = [[gamestate.places['tunnel_{0}_{1}'.format(i, j)]
          ...         for j in range(9)] for i in range(2)]
          >>> queen = ants.QueenAnt()
          >>> queen_tunnel[7].add_insect(queen)
          >>> # 第 0 回合
          >>> thrower = ants.ThrowerAnt()
          >>> fire = ants.FireAnt()
          >>> side = ants.ThrowerAnt()
          >>> front = ants.ThrowerAnt()
          >>> queen_tunnel[0].add_insect(thrower)
          >>> queen_tunnel[1].add_insect(fire)
          >>> queen_tunnel[8].add_insect(front)
          >>> side_tunnel[0].add_insect(side)
          >>> # 当前布局
          >>> # [thrower, fire, , , , , , queen, front]
          >>> # [side   ,     , , , , , ,      ,      ]
          >>> thrower.damage, fire.damage = 101, 102
          >>> front.damage, side.damage = 104, 105
          >>> queen.action(gamestate)
          >>> (thrower.damage, fire.damage)
          (202, 204)
          >>> (front.damage, side.damage)
          (104, 105)
          >>> # 第 1 回合
          >>> tank = ants.TankAnt()
          >>> guard = ants.BodyguardAnt()
          >>> queen_tank = ants.TankAnt()
          >>> queen_tunnel[6].add_insect(tank)          # 没有保护任何蚂蚁
          >>> queen_tunnel[1].add_insect(guard)         # 保护 FireAnt
          >>> queen_tunnel[7].add_insect(queen_tank)    # 保护 QueenAnt
          >>> # 当前布局
          >>> # [thrower, guard/fire, , , , , tank, queen_tank/queen, front]
          >>> # [side   ,           , , , , ,     ,                 ,      ]
          >>> tank.damage, guard.damage, queen_tank.damage = 1001, 1002, 1003
          >>> queen.action(gamestate)
          >>> # 保持不变
          >>> (thrower.damage, fire.damage)
          (202, 204)
          >>> (front.damage, side.damage)
          (104, 105)
          >>> (tank.damage, guard.damage)
          (2002, 2004)
          >>> queen_tank.damage
          1003
          >>> # 第 2 回合
          >>> thrower1 = ants.ThrowerAnt()
          >>> thrower2 = ants.ThrowerAnt()
          >>> queen_tunnel[6].add_insect(thrower1)      # 将 thrower1 放入 TankAnt
          >>> queen_tunnel[5].add_insect(thrower2)
          >>> # 当前布局
          >>> # [thrower, guard/fire, , , , thrower2, tank/thrower1, queen_tank/queen, front]
          >>> # [side   ,           , , , ,         ,              ,                 ,      ]
          >>> thrower1.damage, thrower2.damage = 10001, 10002
          >>> queen.action(gamestate)
          >>> (thrower.damage, fire.damage)
          (202, 204)
          >>> (front.damage, side.damage)
          (104, 105)
          >>> (tank.damage, guard.damage)
          (2002, 2004)
          >>> queen_tank.damage
          1003
          >>> (thrower1.damage, thrower2.damage)
          (20002, 20004)
          >>> # 第 3 回合
          >>> tank.reduce_health(tank.health)             # 让 thrower1 失去容器保护
          >>> queen.action(gamestate)
          >>> (thrower.damage, fire.damage)
          (202, 204)
          >>> (front.damage, side.damage)
          (104, 105)
          >>> guard.damage
          2004
          >>> queen_tank.damage
          1003
          >>> (thrower1.damage, thrower2.damage)
          (20002, 20004)
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 添加或移除带有容器的 QueenAnt
          >>> place = gamestate.places['tunnel_0_3']
          >>> queen = ants.QueenAnt()
          >>> container = ants.TankAnt()
          >>> place.add_insect(container)
          >>> place.ant is container
          True
          >>> container.place is place
          True
          >>> container.ant_contained is None
          True
          >>> place.add_insect(queen)
          >>> container.ant_contained is queen
          True
          >>> queen.place is place
          True
          >>> queen.action(gamestate) # 不应报错
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 测试是否正确调用 zero_health_callback
          >>> original_zero_health_callback = ants.Insect.zero_health_callback
          >>> ants.Insect.zero_health_callback = lambda x: print("insect died")
          >>> real = ants.QueenAnt()
          >>> gamestate.places['tunnel_0_2'].add_insect(real)
          >>> ants.Insect.zero_health_callback = original_zero_health_callback
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> from ants import *
          >>> QueenAnt.implemented
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> import ants, importlib
      >>> importlib.reload(ants)
      >>> beehive = ants.Hive(ants.AssaultPlan())
      >>> dimensions = (2, 9)
      >>> gamestate = ants.GameState(beehive, ants.ant_types(),
      ...                            ants.dry_layout, dimensions, food=20)
      >>> #
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
