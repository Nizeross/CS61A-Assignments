
from abc import ABC, abstractmethod
from math import pi


class Canvas(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._turtle = None

    @property
    def turtle(self):
        return self._turtle

    @turtle.setter
    def turtle(self, turtle):
        self._turtle = turtle
        self.refreshed_turtle(turtle)

    @abstractmethod
    def draw_rectangular_line(self, start, end, color, width):
        """
        使用 COLOR 从 START 到 END 绘制宽度为 1 的线段
        """
        pass

    def draw_line(self, start, end, color, width):
        if width > 1:
            self.draw_circle(start, width / 2, color, width, True, 0, 2 * pi)
        self.draw_rectangular_line(start, end, color, width)
        if width > 1:
            self.draw_circle(end, width / 2, color, width, True, 0, 2 * pi)

    @abstractmethod
    def draw_circle(self, center, radius, color, width, is_filled, start, end):
        """
        绘制宽度为 1 的圆，圆心为 CENTER，半径为 RADIUS，颜色为 COLOR。仅绘制从 START 到 END 的角度范围，沿逆时针方向绘制。RADIUS 必须非负。

        如果 IS_FILLED 为真，则填充圆。
        """
        pass

    @abstractmethod
    def fill_path(self, path, color):
        """
        使用填充色 COLOR 填充由 PATH 中的移动构成的多边形。
        """
        pass

    @abstractmethod
    def axis_aligned_rectangle(self, bottom_left, width, height, color):
        """
        使用 COLOR 填充矩形，其左下角为 BOTTOM_LEFT，尺寸为 (WIDTH, HEIGHT)
        """
        pass

    @abstractmethod
    def set_bgcolor(self, color):
        """
        使用给定 COLOR 填充整个背景
        """
        pass

    @abstractmethod
    def clear(self):
        """
        清除前景中的所有内容
        """
        pass

    @abstractmethod
    def refreshed_turtle(self, drawn_turtle):
        """
        将海龟更新为给定的 DrawnTurtle 对象；如果传入 None，则移除海龟
        """
        pass

    @abstractmethod
    def set_speed(self, speed):
        """
        设置动画速度；若实现此功能，其行为应与内置 turtle 模块一致。
        """
        pass

    @abstractmethod
    def exit_on_click(self):
        """
        阻塞等待点击，点击后关闭图形界面。对于非图形界面应用，此操作无效果；图形界面应用应重写此行为。
        """
        pass
