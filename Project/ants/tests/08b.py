test = {
  'name': 'Problem 8b',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'answer': '7a81f10493cb9dd2a778afa061e3edd5',
          'choices': [
            r"""
            When exactly one of the Ant instances is a container and the
            container ant does not already contain another ant
            """,
            'When exactly one of the Ant instances is a container',
            'When both Ant instances are containers',
            'There can never be two Ant instances in the same place'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'When can a second Ant be added to a place that already contains an Ant?'
        },
        {
          'answer': '9ee6782d61a987d40e66726eb2354093',
          'choices': [
            'The Container Ant',
            'The Ant being contained',
            'A list containing both Ants',
            'Whichever Ant was placed there first'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': r"""
          If two Ants occupy the same Place, what is stored in that place's ant
          instance attribute?
          """
        },
        {
          'answer': 'c9e4559526ed96dcae3a8a67e48f2539',
          'choices': [
            'The Ant instance that is in the same place as itself',
            'The Ant instance in the place closest to its own place',
            'A random Ant instance in the gamestate',
            'All the Ant instances in the gamestate'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'Which Ant does a ContainerAnt guard?'
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # 先添加容器蚂蚁，再添加另一只蚂蚁
          >>> container = ContainerAnt(1)
          >>> other_ant = ThrowerAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(container)  # 先将 ContainerAnt 放入地点
          >>> place.add_insect(other_ant)
          >>> place.ant is other_ant
          False
          >>> place.ant is container
          True
          >>> container.ant_contained is other_ant
          True
          >>> container.place is place
          True
          >>> other_ant.place is container.place  # ThrowerAnt 的 place 属性应与 ContainerAnt 相同
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 任意容器蚂蚁都可以在另一只蚂蚁之后添加
          >>> container = ContainerAnt(1)
          >>> other_ant = ThrowerAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(other_ant)  # 先将其他蚂蚁放入地点
          >>> place.ant is other_ant
          True
          >>> place.add_insect(container)
          >>> place.ant is container
          True
          >>> container.ant_contained is other_ant
          True
          >>> container.place is place
          True
          >>> other_ant.place is container.place  # ThrowerAnt 的 place 属性应与 ContainerAnt 相同
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # 一个容器中只能添加一只蚂蚁
          >>> container = ContainerAnt(1)
          >>> a = ThrowerAnt()
          >>> b = ThrowerAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(container)
          >>> place.add_insect(a)
          >>> place.add_insect(b)
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
          >>> # 组合测试添加和移除操作
          >>> container = ContainerAnt(1)
          >>> a = ThrowerAnt()
          >>> b = ThrowerAnt()
          >>> place = gamestate.places['tunnel_0_0']
          >>> place.add_insect(a)
          >>> place.add_insect(container)
          >>> container.remove_from(place)
          >>> place.ant is a
          True
          >>> container = ContainerAnt(1)
          >>> place.add_insect(container)
          >>> a.remove_from(place)
          >>> place.add_insect(b)
          >>> place.ant is container
          True
          >>> b.place is place
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
      >>> gamestate = GameState(beehive, ant_types(), layout, (1, 9))
      >>> #
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
