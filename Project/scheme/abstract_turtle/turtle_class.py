from functools import wraps
from math import pi, sin, cos, copysign

from .model import Color, Position, DrawnTurtle, Mode, LineTo, Arc
from .canvas import Canvas

def turtle_method(func):
    """
    将给定方法标记为需要放入全局命名空间的方法。
    """
    func.is_turtle_method = True
    return func


def make_formode():
    handlers = {}

    def formode(mode):
        def decorator(func):
            @wraps(func)
            def error(self, *args, **kwargs):
                raise RuntimeError(
                    "Handler not available for mode: {}".format(self._BaseTurtle__mode)
                )

            prev = handlers.get(func.__name__, error)

            @wraps(func)
            def handler(self, *args, **kwargs):
                if self._BaseTurtle__mode == mode:
                    return func(self, *args, **kwargs)
                else:
                    return prev(self, *args, **kwargs)

            handlers[func.__name__] = handler

            return handler

        return decorator

    return formode


formode = make_formode()


class BaseTurtle:
    """
    管理所有基本的海龟功能。其他海龟方法都可以通过这些功能表达。
    """
    def __init__(self, canvas):
        if not isinstance(canvas, Canvas):
            raise RuntimeError("Expected the argument to Turtle to be of type {} but was {} of type {}".format(
                Canvas.__name__,
                canvas,
                type(canvas).__name__
            ))
        self.__canvas = canvas
        self.__x = 0
        self.__y = 0
        self.__line_width = 1
        self.__theta = 0
        self.__pen_color = Color(0, 0, 0)
        self.__fill_color = Color(0, 0, 0)
        self.__pen_down = True
        self.__degrees = 360
        self.__path = None
        self.__turtle_is_shown = True
        self.__turtle_stretch_wid = 1
        self.__turtle_stretch_len = 1
        self.__pixel_size = 1
        self.__mode = Mode.STANDARD
        self.__speed = 3 # 普通 turtle 模块的默认值

        self.__update_turtle()

    @turtle_method
    def goto(self, x, y):
        """
        移动到给定位置 (X, Y)。
        """
        if self.__pen_down:
            self.__canvas.draw_line(self.__current_pos, Position(x, y), self.__pen_color, self.__line_width)
        self.__x = x
        self.__y = y
        if self.filling():
            self.__path.append(LineTo(self.__current_pos))
        self.__update_turtle()
    setpos = setposition = goto

    @turtle_method
    def forward(self, amount):
        """
        向前移动给定距离。
        """
        self.goto(self.xcor() + amount * cos(self.__theta), self.ycor() + amount * sin(self.__theta))
    fd = forward

    @turtle_method
    def setheading(self, heading):
        """
        将朝向设置为给定角度值，单位为度
        """
        self.__theta = self.__to_real_angle(heading)
        self.__update_turtle()
    seth = setheading

    @turtle_method
    def circle(self, radius, extent=None):
        """
        从给定点开始，按 RADIUS 和 EXTENT 画圆。若指定 EXTENT，则只画圆的前 EXTENT 度。RADIUS 为正时逆时针绘制，否则顺时针绘制。
        """
        if extent is None:
            extent = self.__degrees

        extent = extent / self.__degrees * (2 * pi)

        center = Position(
            self.__current_pos.x - radius * sin(self.__theta),
            self.__current_pos.y + radius * cos(self.__theta),
        )
        angle_change = copysign(1, radius) * extent
        start_angle = self.__theta - pi / 2 * copysign(1, radius)
        end_angle = start_angle + angle_change

        if self.filling():
            self.__path.append(Arc(center, abs(radius), start_angle, end_angle))

        if self.__pen_down:
            if radius * extent < 0:
                start_angle, end_angle = end_angle, start_angle
            self.__canvas.draw_circle(center, abs(radius), self.__pen_color, self.__line_width, False, start_angle,
                                      end_angle)

        final_pos = Position(
            center.x + radius * sin(self.__theta + angle_change),
            center.y - radius * cos(self.__theta + angle_change),
        )
        self.__theta += angle_change
        self.__x, self.__y = final_pos.x, final_pos.y
        self.__update_turtle()

    @turtle_method
    def dot(self, size=None):
        """
        在当前位置画点。若未指定 size，则设为 (pensize + 4, pensize * 2)
        """
        if size is None:
            size = max(self.__line_width + 4, self.__line_width * 2)
        if self.__pen_down:
            self.__canvas.draw_circle(self.__current_pos, size, self.__pen_color, self.__line_width, True, 0, 2 * pi)

    @turtle_method
    def pixel(self, x, y, *color):
        """
        在 (x * pixel_size, y * pixel_size) 处，用给定颜色填充边长为 pixel_size 的正方形。
        """
        d = self.__pixel_size
        self.__canvas.axis_aligned_rectangle(
            Position(x * d, y * d),
            d, d,
            self.__convert_color(*color)
        )

    @turtle_method
    def pixel_size(self, pixel_size):
        if not isinstance(pixel_size, int) or pixel_size <= 0:
            raise ValueError("Expected a positive integer for pixel_size but got {}".format(pixel_size))
        self.__pixel_size = pixel_size

    @turtle_method
    def canvas_width(self):
        """
        返回当前屏幕尺寸，单位为像素
        """
        return self.__canvas.width // self.__pixel_size

    @turtle_method
    def canvas_height(self):
        """
        返回当前屏幕尺寸，单位为像素
        """
        return self.__canvas.height // self.__pixel_size

    @turtle_method
    def xcor(self):
        """
        获取当前 x 坐标
        """
        return self.__x

    @turtle_method
    def ycor(self):
        """
        获取当前 y 坐标
        """
        return self.__y

    @turtle_method
    def heading(self):
        """
        获取当前朝向
        """
        return self.__from_real_angle(self.__theta)

    @turtle_method
    def degrees(self, amount=360):
        """
        设置一整圈所对应的角度单位数
        """
        self.__degrees = amount

    @turtle_method
    def pendown(self):
        """
        移动时绘图
        """
        self.__pen_down = True
    pd = down = pendown

    @turtle_method
    def penup(self):
        """
        移动时不绘图
        """
        self.__pen_down = False
    pu = up = penup

    @turtle_method
    def pensize(self, width=None):
        """
        设置或获取画笔粗细。WIDTH 为 None 时获取，否则设置。
        """
        if width is None:
            return self.__line_width
        self.__line_width = width
    width = pensize

    @turtle_method
    def isdown(self):
        """
        返回画笔是否落下
        """
        return self.__pen_down

    @turtle_method
    def pencolor(self, *color):
        """
        将画笔颜色设为 COLOR
        """
        self.__pen_color = self.__convert_color(*color)

    @turtle_method
    def fillcolor(self, *color):
        """
        将填充颜色设为 COLOR
        """
        self.__fill_color = self.__convert_color(*color)

    @turtle_method
    def filling(self):
        """
        返回画布是否处于填充状态。
        """
        return self.__path is not None

    @turtle_method
    def begin_fill(self):
        """
        开始定义待填充的多边形
        """
        self.__path = [LineTo(self.__current_pos)]

    @turtle_method
    def end_fill(self):
        """
        结束定义待填充的多边形，并进行填充。
        """
        if self.__path is None:
            return
        self.__canvas.fill_path(self.__path, self.__fill_color)
        self.__path = None

    @turtle_method
    def clear(self):
        """
        清空画布，但不移动海龟。
        """
        self.__canvas.clear()

    @turtle_method
    def bgcolor(self, *color):
        self.__canvas.set_bgcolor(self.__convert_color(*color))

    def __update_turtle(self):
        if self.__turtle_is_shown:
            self.__canvas.turtle = DrawnTurtle(self.__current_pos, self.__theta % (2 * pi), self.__turtle_stretch_wid, self.__turtle_stretch_len)
        else:
            self.__canvas.turtle = None

    @turtle_method
    def hideturtle(self):
        """
        在画布上隐藏海龟。
        """
        self.__turtle_is_shown = False
        self.__update_turtle()
    ht = hideturtle

    @turtle_method
    def showturtle(self):
        """
        在画布上显示海龟
        """
        self.__turtle_is_shown = True
        self.__update_turtle()
    st = showturtle

    @turtle_method
    def isvisible(self):
        """
        返回海龟是否可见
        """
        return self.__turtle_is_shown

    @turtle_method
    def shapesize(self, stretch_wid=None, stretch_len=None):
        self.__turtle_stretch_wid = stretch_wid
        self.__turtle_stretch_len = stretch_len
        self.__update_turtle()
    turtlesize = shapesize

    @turtle_method
    def mode(self, mode=None):
        if mode is None:
            return self.__mode.value
        elif mode == "standard":
            self.__mode = Mode.STANDARD
        elif mode == "logo":
            self.__mode = Mode.LOGO
        elif mode == "world":
            raise RuntimeError("Custom world coordinates not supported.")
        else:
            raise RuntimeError("Unknown mode: {}".format(mode))
        self.goto(0, 0)
        self.setheading(0)
        self.clear()

    @turtle_method
    def speed(self, speed=None):
        if speed is None:
            return self.__speed
        self.__speed = speed
        self.__canvas.set_speed(speed)

    @turtle_method
    def exitonclick(self):
        return self.__canvas.exit_on_click()

    @property
    def __current_pos(self):
        return Position(self.__x, self.__y)

    @formode(Mode.STANDARD)
    def __to_real_angle(self, amount):
        return (amount / self.__degrees) * (2 * pi)

    @formode(Mode.STANDARD)
    def __from_real_angle(self, angle):
        return (angle / (2 * pi)) * self.__degrees % self.__degrees

    @formode(Mode.LOGO)
    def __to_real_angle(self, amount):
        return (1 / 4 - amount / self.__degrees) * (2 * pi)

    @formode(Mode.LOGO)
    def __from_real_angle(self, angle):
        return (1 / 4 - angle / (2 * pi)) * self.__degrees % self.__degrees

    @staticmethod
    def __convert_color(*color):
        return Color.of(*color)


class Turtle(BaseTurtle):
    """
    此类只能使用 BaseTurtle 类的公开方法。
    """

    @turtle_method
    def backward(self, amount):
        """
        向后移动给定距离。
        """
        self.forward(-amount)
    bk = back = backward

    @formode(Mode.STANDARD)
    def right(self, amount):
        self.setheading(self.heading() - amount)

    @turtle_method
    @formode(Mode.LOGO)
    def right(self, amount):
        """
        向右旋转给定角度。
        """
        self.setheading(self.heading() + amount)

    rt = right

    @turtle_method
    def left(self, amount):
        """
        向左旋转给定角度。
        """
        self.right(-amount)
    lt = left

    @turtle_method
    def setx(self, x):
        """
        移动至 x 坐标为 X 的位置
        """
        self.goto(x, self.xcor())

    @turtle_method
    def sety(self, y):
        """
        移动至 y 坐标为 Y 的位置
        """
        self.goto(self.xcor(), y)

    @turtle_method
    def home(self):
        """
        移动至 (0, 0)，并将朝向设置为 0
        """
        self.goto(0, 0)
        self.setheading(0)

    @turtle_method
    def position(self):
        """
        以元组形式获取当前位置
        """
        return self.xcor(), self.ycor()
    pos = position

    @turtle_method
    def distance(self, other):
        """
        获取当前位置与另一位置或海龟之间的距离。
        """
        if isinstance(other, Turtle):
            return self.distance(other.position())
        x, y = other
        return ((x - self.xcor()) ** 2 + (y - self.ycor()) ** 2) ** 0.5

    @turtle_method
    def radians(self):
        """
        将角度单位设置为弧度
        """
        return self.degrees(2 * pi)

    @turtle_method
    def color(self, *color):
        """
        同时设置画笔颜色和填充颜色
        """
        self.pencolor(*color)
        self.fillcolor(*color)

    @turtle_method
    def reset(self):
        self.home()
        self.clear()
