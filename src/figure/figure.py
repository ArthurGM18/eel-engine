from .figure import _BaseFigure
from .figure import *
from dataclasses import dataclass, InitVar, field
from math import pi, cos, sin

@dataclass
class BaseFigure(_BaseFigure):

    x: int
    y: int

    def __post_init__(self, fill=False):
        if (fill): self.setMode(9)


    def __init_subclass__(cls):
        
        def func():
            
            inst = None
            annotations = []
            for _cls in cls.__mro__[-1::-1]:
                try: annotations.extend(_cls.__annotations__.keys())
                except: pass


            def inner(*args, target, **kwargs):
                nonlocal inst, annotations

                if inst is None: inst = cls(*args, **kwargs)

                else:
                    for arg, val in zip(annotations, args):
                        inst.__setattr__(arg, val)

                    for name, val in kwargs.items():
                        inst.__setattr__(name, val)

                inst.setColor(getColor())
                inst.setMode(2 + 7 * kwargs.get('fill'))
                inst.drawTo(target)

                return inst


            return inner

        globals()[f'draw{cls.__name__}'] =\
        globals()[f'draw{cls.__name__[:4]}'] = func()

    # ----------------------------------

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, v):
        self.x, self.y = v

    # ----------------------------------

    @property
    def fill(self):
        pass

    @fill.setter
    def fill(self, val: bool):
        self.setMode(2 + 7 * val)

    # ----------------------------------

    @property
    def color(self):
        return self.getColor()

    @color.setter
    def color(self, val: int):
        self.setColor(val)
        

@dataclass
class Rectangle(BaseFigure):
    
    width: int
    height: int

    fill: InitVar[bool]=False

    def layout(self):

        return [
            (0, 0), (self.width, 0),
            (self.width, self.height), (0, self.height)
        ]


    def isInside(self, x, y):
        return (
            x >= self.x and x < self.x+self.width and\
            y >= self.y and y < self.y+self.height
        )


    def collisionDistance(self):
        return max(self.width, self.height) * 1.2

    
    def collisionCenter(self):
        return (self.x+self.width/2, self.y+self.height/2)


@dataclass
class Triangle(BaseFigure, NoPhysics):

    radius: int
    angle: float=0

    fill: InitVar[bool]=False

    @property
    def angle(self) -> float:
        return self.__angle

    @angle.setter
    def angle(self, value: float):
        
        if type(value) is property: value = 0

        self.__angle = value

        a = value + pi * 2/3
        b = value + pi * 4/3
        c = value + pi * 2

        self.__sina = sin(a)
        self.__cosa = cos(a)

        self.__sinb = sin(b)
        self.__cosb = cos(b)

        self.__sinc = sin(c)
        self.__cosc = cos(c)


    def layout(self):
        
        return [
            (self.__cosa * self.radius, self.__sina * self.radius),
            (self.__cosb * self.radius, self.__sinb * self.radius),
            (self.__cosc * self.radius, self.__sinc * self.radius),
        ]


@dataclass
class Circle(BaseFigure):

    radius: int
    precision: int=1
    fill: InitVar[bool]=False

    def layout(self):

        used = round(self.radius * 20 * self.precision)
        tmp = pi * 2 / used

        return [
            (cos(a:=(tmp * i)) * self.radius, sin(a) * self.radius)
            for i in range(used)
        ]


    def isInside(self, x, y):
        return (
            ((self.x - x) ** 2 + (self.y - y) ** 2 <= self.radius ** 2)
        )


    def collisionDistance(self):
        return self.radius


    def collisionCenter(self):
        return (self.x, self.y)


@dataclass
class Sprite(Rectangle):

    img: InitVar[str] = None

    def __post_init__(self, fill, img):

        if img is None: raise ValueError("The `img` parameter cannot be null")

        self.setMode(7)
        self.setTexture(bytes(img, "utf-8"))


    def layout(self):

        w = self.width  / 2
        h = self.height / 2

        return [(w, -h), (w, h), (-w, h), (-w, -h)]


@dataclass
class Line(BaseFigure, NoPhysics):

    xp: int
    yp: int

    def layout(self):
        return [(0, 0), (self.xp - self.x, self.yp - self.y)]