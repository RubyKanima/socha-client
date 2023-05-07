from socha import Field

from dataclasses import dataclass, field

@dataclass(order=True)
class Shape:
    root: Field
    orient: int = field(default=1)

    def __hash__(self):
        return str(self.root.coordinate.x) + str(self.root.coordinate.y)

@dataclass(order=True, eq=False)
class Triangle(Shape):
    left: Field
    right: Field

    @property
    def fish(self):
        return sum(self.root.fish, self.left.fish, self.right.fish)
     
@dataclass(order=True, eq=False)
class Line(Shape):
    buddy: Field

@dataclass(order=True)
class Group:
    childs: dict
