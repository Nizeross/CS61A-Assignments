"""CS 61A 出品：蚂蚁大战蜜蜂。"""

import random
from ucb import main, interact, trace
from collections import OrderedDict

################
# 核心类 #
################


class Place:
    """Place 容纳昆虫，并有一个通向另一个 Place 的出口。"""
    is_hive = False

    def __init__(self, name, exit=None):
        """用给定的 NAME 和 EXIT 创建 Place。

        name：字符串，此地点的名称。
        exit：从此地点离开时到达的 Place（可以为 None）。
        """
        self.name = name
        self.exit = exit
        self.bees = []        # 蜜蜂列表
        self.ant = None       # 一只蚂蚁
        self.entrance = None  # 一个地点
        # 第一阶段：为出口添加入口
        # BEGIN Problem 2
        "*** YOUR CODE HERE ***"
        # END Problem 2

    def add_insect(self, insect):
        """让昆虫将自身添加到此地点。提供此方法是为了允许子类重写。
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """让昆虫将自身从此地点移除。提供此方法是为了允许子类重写。
        """
        insect.remove_from(self)

    def __str__(self):
        return self.name


class Insect:
    """Insect 是 Ant 和 Bee 的基类，具有生命值 health 和所在地点 Place。"""

    next_id = 0  # 每只昆虫都有唯一的编号
    damage = 0
    # 在此添加类属性

    def __init__(self, health, place=None):
        """用给定的生命值和起始地点 PLACE 创建 Insect。"""
        self.health = health
        self.place = place

        # 为每只昆虫分配唯一的 ID
        self.id = Insect.next_id
        Insect.next_id += 1

    def reduce_health(self, amount):
        """将生命值减少 AMOUNT；如果生命值耗尽，则将昆虫从所在地点移除。

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= amount
        if self.health <= 0:
            self.zero_health_callback()
            self.place.remove_insect(self)

    def action(self, gamestate):
        """每回合执行的行动。"""

    def zero_health_callback(self):
        """生命值降至 0 或以下时调用。"""

    def add_to(self, place):
        self.place = place

    def remove_from(self, place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """Ant 占据一个地点，并为蚁群工作。"""

    implemented = False  # 只能实例化已实现的 Ant 类
    food_cost = 0
    is_container = False
    # 在此添加类属性

    def __init__(self, health=1):
        super().__init__(health)

    def can_contain(self, other):
        return False

    def store_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place):
        if place.ant is None:
            place.ant = self
        else:
            # BEGIN Problem 8b
            assert place.ant is None, 'Too many ants in {0}'.format(place)
            # END Problem 8b
        Insect.add_to(self, place)

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def double(self):
        """如果这只蚂蚁的伤害尚未翻倍，则将其伤害翻倍。"""
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        # END Problem 12


class HarvesterAnt(Ant):
    """HarvesterAnt 每回合为蚁群额外生产 1 单位食物。"""

    name = 'Harvester'
    implemented = True
    # 在此重写类属性

    def action(self, gamestate):
        """为蚁群额外生产 1 单位食物。

        gamestate：GameState 对象，用于访问游戏状态信息。
        """
        # BEGIN Problem 1
        "*** YOUR CODE HERE ***"
        # END Problem 1


class ThrowerAnt(Ant):
    """ThrowerAnt 每回合向射程内最近的 Bee 投掷一片树叶。"""

    name = 'Thrower'
    implemented = True
    damage = 1
    # 在此添加或重写类属性

    def nearest_bee(self):
        """沿入口方向查找与 ThrowerAnt 所在地点相连的地点，返回其中最近的 Bee，蜂巢除外。

        如果没有这样的蜜蜂，或射程内没有蜜蜂，此方法返回 None。
        """
        # BEGIN Problem 3 and 4
        return random_bee(self.place.bees) # 替换此行
        # END Problem 3 and 4

    def throw_at(self, target):
        """向目标 Bee 投掷一片树叶，降低其生命值。"""
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate):
        """向射程内最近的 Bee 投掷一片树叶。"""
        self.throw_at(self.nearest_bee())


def random_bee(bees):
    """从蜜蜂列表中随机返回一只蜜蜂；如果 bees 为空，返回 None。"""
    assert isinstance(bees, list), \
        "random_bee's argument should be a list but was a %s" % type(bees).__name__
    if bees:
        return random.choice(bees)

##############
# 扩展功能 #
##############


class ShortThrower(ThrowerAnt):
    """只向距离不超过 3 个地点的蜜蜂投掷树叶的 ThrowerAnt。"""

    name = 'Short'
    food_cost = 2
    # 在此重写类属性
    # BEGIN Problem 4
    implemented = False   # 改为 True 后即可在图形界面中查看
    # END Problem 4


class LongThrower(ThrowerAnt):
    """只向距离至少为 5 个地点的蜜蜂投掷树叶的 ThrowerAnt。"""

    name = 'Long'
    food_cost = 2
    # 在此重写类属性
    # BEGIN Problem 4
    implemented = False   # 改为 True 后即可在图形界面中查看
    # END Problem 4


class FireAnt(Ant):
    """FireAnt 死亡时，会灼伤其所在地点的所有蜜蜂。"""

    name = 'Fire'
    damage = 3
    food_cost = 5
    # 在此重写类属性
    # BEGIN Problem 5
    implemented = False   # 改为 True 后即可在图形界面中查看
    # END Problem 5

    def __init__(self, health=3):
        """创建生命值为 HEALTH 的 Ant。"""
        super().__init__(health)

    def reduce_health(self, amount):
        """将生命值减少 AMOUNT；如果生命值耗尽，则将 FireAnt 从所在地点移除。

        务必降低当前地点中每只蜜蜂的生命值，并在火蚁死亡时施加额外伤害。
        """
        # BEGIN Problem 5
        "*** YOUR CODE HERE ***"
        # END Problem 5

# BEGIN Problem 6
# WallAnt 类
# END Problem 6

# BEGIN Problem 7
# HungryAnt 类
# END Problem 7


class ContainerAnt(Ant):
    """
    ContainerAnt 可以通过容纳其他蚂蚁，与它们共享一个地点。
    """
    is_container = True

    def __init__(self, health):
        super().__init__(health)
        self.ant_contained = None

    def can_contain(self, other):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        # END Problem 8a

    def store_ant(self, ant):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        # END Problem 8a

    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        # 对容器蚂蚁进行特殊处理
        if place.ant is self:
            # 容器已被移除，其中的蚂蚁应继续留在游戏中
            place.ant = place.ant.ant_contained
            Insect.remove_from(self, place)
        else:
            # 默认使用正常行为
            Ant.remove_from(self, place)

    def action(self, gamestate):
        # BEGIN Problem 8a
        "*** YOUR CODE HERE ***"
        # END Problem 8a


class BodyguardAnt(ContainerAnt):
    """BodyguardAnt 为其他蚂蚁提供保护。"""

    name = 'Bodyguard'
    food_cost = 4
    # 在此重写类属性
    # BEGIN Problem 8c
    implemented = False   # 改为 True 后即可在图形界面中查看
    # END Problem 8c

# BEGIN Problem 9
# TankAnt 类
# END Problem 9


class Water(Place):
    """Water 是仅允许防水昆虫存活的地点。"""

    def add_insect(self, insect):
        """将 Insect 添加到此地点。如果该昆虫不防水，则将其生命值降至 0。"""
        # BEGIN Problem 10
        "*** YOUR CODE HERE ***"
        # END Problem 10

# BEGIN Problem 11
# ScubaThrower 类
# END Problem 11


class QueenAnt(ThrowerAnt):
    """QueenAnt 提升她身后所有蚂蚁的伤害。"""

    name = 'Queen'
    food_cost = 7
    # 在此重写类属性
    # BEGIN Problem 12
    implemented = False   # 改为 True 后即可在图形界面中查看
    # END Problem 12

    def action(self, gamestate):
        """蚁后投掷一片树叶，同时将其隧道中蚂蚁的伤害翻倍。
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        # END Problem 12

    def reduce_health(self, amount):
        """将生命值减少 AMOUNT；如果 QueenAnt 的生命值耗尽，则发出游戏结束信号。
        """
        # BEGIN Problem 12
        "*** YOUR CODE HERE ***"
        # END Problem 12


################
# 额外挑战 #
################

class SlowThrower(ThrowerAnt):
    """使蜜蜂减速的 ThrowerAnt。"""

    name = 'Slow'
    food_cost = 6
    # BEGIN Problem EC 1
    implemented = False   # 改为 True 后即可在图形界面中查看
    # END Problem EC 1

    def throw_at(self, target):
        # BEGIN Problem EC 1
        "*** YOUR CODE HERE ***"
        # END Problem EC 1


class ScaryThrower(ThrowerAnt):
    """恐吓蜜蜂，使其后退而不是前进的 ThrowerAnt。"""

    name = 'Scary'
    food_cost = 6
    # BEGIN Problem EC 2
    implemented = False   # 改为 True 后即可在图形界面中查看
    # END Problem EC 2

    def throw_at(self, target):
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # END Problem EC 2


class NinjaAnt(Ant):
    """NinjaAnt 不阻挡道路，并对所在地点的所有蜜蜂造成伤害。"""

    name = 'Ninja'
    damage = 1
    food_cost = 5
    # 在此重写类属性
    # BEGIN Problem EC 3
    implemented = False   # 改为 True 后即可在图形界面中查看
    # END Problem EC 3

    def action(self, gamestate):
        # BEGIN Problem EC 3
        "*** YOUR CODE HERE ***"
        # END Problem EC 3


class LaserAnt(ThrowerAnt):
    """对其路径上的所有昆虫造成伤害的 ThrowerAnt。"""

    name = 'Laser'
    food_cost = 10
    # 在此重写类属性
    # BEGIN Problem EC 4
    implemented = False   # 改为 True 后即可在图形界面中查看
    # END Problem EC 4

    def __init__(self, health=1):
        super().__init__(health)
        self.insects_shot = 0

    def insects_in_front(self):
        # BEGIN Problem EC 4
        return {}
        # END Problem EC 4

    def calculate_damage(self, distance):
        # BEGIN Problem EC 4
        return 0
        # END Problem EC 4

    def action(self, gamestate):
        insects_and_distances = self.insects_in_front()
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1


########
# 蜜蜂 #
########

class Bee(Insect):
    """Bee 沿出口在各个地点之间移动，并蜇刺蚂蚁。"""

    name = 'Bee'
    damage = 1
    is_waterproof = True


    def sting(self, ant):
        """攻击 ANT，使其生命值减少 1。"""
        ant.reduce_health(self.damage)

    def move_to(self, place):
        """将蜜蜂从当前地点移动到新的 PLACE。"""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """如果此蜜蜂无法前进到下一个地点，返回 True。"""
        # 对 NinjaAnt 进行特殊处理
        # BEGIN Problem EC 3
        return self.place.ant is not None
        # END Problem EC 3

    def action(self, gamestate):
        """蜜蜂行动时，如果出口被蚂蚁挡住，则蜇刺该蚂蚁；否则移动到当前地点的出口。

        gamestate：GameState 对象，用于访问游戏状态信息。
        """
        destination = self.place.exit


        if self.blocked():
            self.sting(self.place.ant)
        elif self.health > 0 and destination is not None:
            self.move_to(destination)

    def add_to(self, place):
        place.bees.append(self)
        super().add_to( place)

    def remove_from(self, place):
        place.bees.remove(self)
        super().remove_from(place)

    def scare(self, length):
        """
        如果这只蜜蜂之前未被恐吓过，则使其尝试后退 LENGTH 次。
        """
        # BEGIN Problem EC 2
        "*** YOUR CODE HERE ***"
        # END Problem EC 2


class Wasp(Bee):
    """伤害更高的 Bee 类。"""
    name = 'Wasp'
    damage = 2


class Boss(Wasp):
    """蜜蜂首领。每次攻击对首领造成的伤害都有上限。
    """
    name = 'Boss'
    damage_cap = 8

    def reduce_health(self, amount):
        super().reduce_health(min(amount, self.damage_cap))


class Hive(Place):
    """蜜蜂发起进攻的地点。

    assault_plan：AssaultPlan 对象，指定蜜蜂何时、从何处进入蚁群。
    """
    is_hive = True

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees():
            self.add_insect(bee)
        # 对于 Hive，以下属性始终为 None
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, gamestate):
        exits = [p for p in gamestate.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(gamestate.time, []):
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)

###################
# 游戏组件 #
###################

class GameState:
    """管理全局游戏状态并模拟时间推进的蚁群。

    属性：
    time：已过去的时间。
    food：蚁群可用的食物总量。
    places：蚁群中所有地点的列表（包括 Hive）。
    bee_entrances：蜜蜂可以进入的地点列表。
    """

    def __init__(self, beehive, ant_types, create_places, dimensions, food=2):
        """创建用于模拟游戏的 GameState。

        参数：
        beehive：装有蜜蜂的 Hive。
        ant_types：蚂蚁类的列表。
        create_places：创建地点集合的函数。
        dimensions：包含游戏地图尺寸的一对数值。
        """
        self.time = 0
        self.food = food
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(beehive, create_places)

    def configure(self, beehive, create_places):
        """配置蚁群中的地点。"""
        self.base = AntHomeBase('Ant Home Base')
        self.places = OrderedDict()
        self.bee_entrances = []

        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)
        register_place(self.beehive, False)
        create_places(self.base, register_place,
                      self.dimensions[0], self.dimensions[1])

    def ants_take_actions(self): # 让蚂蚁执行行动
        for ant in self.ants:
            if ant.health > 0:
                ant.action(self)

    def bees_take_actions(self, num_bees): # 让蜜蜂执行行动
        for bee in self.active_bees[:]:
            if bee.health > 0:
                bee.action(self)
            if bee.health <= 0:
                num_bees -= 1
                self.active_bees.remove(bee)
        if num_bees == 0: # 检查玩家是否获胜
            raise AntsWinException()
        return num_bees

    def simulate(self):
        """模拟对蚁群的进攻。图形界面调用此方法来运行游戏。"""
        num_bees = len(self.bees)
        try:
            while True:
                self.beehive.strategy(self) # 蜜蜂从蜂巢入侵
                yield None # yield 之后，玩家有时间放置蚂蚁
                self.ants_take_actions()
                self.time += 1
                yield None # yield 之后，等待投掷树叶动画播放完毕，再让蜜蜂行动
                num_bees = self.bees_take_actions(num_bees)
        except AntsWinException:
            print('All bees are vanquished. You win!')
            yield True
        except AntsLoseException:
            print('The bees reached homebase or the queen ant queen has perished. Please try again :(')
            yield False

    def deploy_ant(self, place_name, ant_type_name):
        """如果有足够食物，则放置一只蚂蚁。

        当前策略调用此方法来部署蚂蚁。
        """
        ant_type = self.ant_types[ant_type_name]
        if ant_type.food_cost > self.food:
            print('Not enough food remains to place ' + ant_type.__name__)
        else:
            ant = ant_type()
            self.places[place_name].add_insect(ant)
            self.food -= ant.food_cost
            return ant

    def remove_ant(self, place_name):
        """从游戏中移除一只 Ant。"""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


class AntHomeBase(Place):
    """位于隧道末端的 AntHomeBase，蚁后通常居住于此。"""

    def add_insect(self, insect):
        """将一只 Insect 添加到此 Place。

        不能真正将蚂蚁添加到 AntHomeBase。但如果蜜蜂尝试进入 AntHomeBase，则抛出 AntsLoseException，表示游戏结束。
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'
        raise AntsLoseException()


def ants_win():
    """发出蚂蚁获胜的信号。"""
    raise AntsWinException()


def ants_lose():
    """发出蚂蚁失败的信号。"""
    raise AntsLoseException()


def ant_types():
    """返回所有已实现的 Ant 类组成的列表。"""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]


def bee_types():
    """返回所有已实现的 Bee 类组成的列表。"""
    all_bee_types = []
    new_types = [Bee]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_bee_types.extend(new_types)
    return all_bee_types


class GameOverException(Exception):
    """游戏结束异常的基类。"""
    pass


class AntsWinException(GameOverException):
    """表示蚂蚁获胜的异常。"""
    pass


class AntsLoseException(GameOverException):
    """表示蚂蚁失败的异常。"""
    pass


###########
# 地图布局 #
###########


def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """注册包含水域与陆地的混合地点布局。"""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(queen, register_place, tunnels=3, length=9):
    """注册陆地隧道。"""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# 进攻计划 #
#################

class AssaultPlan(dict):
    """蜜蜂进攻蚁群的计划。进攻按定时波次进行。

    AssaultPlan 是从时间（int）到进攻波次（Bee 列表）的字典。

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_health, time, count):
        """在 time 时刻添加一波进攻，包含 count 只具有指定生命值的蜜蜂。"""
        bees = [bee_type(bee_health) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    def all_bees(self):
        """将所有蜜蜂放入蜂巢，并返回蜜蜂列表。"""
        return [bee for wave in self.values() for bee in wave]