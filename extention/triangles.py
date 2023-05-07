from socha import Field

from dataclasses import dataclass, field

@dataclass(order=True)
class Shape:
    root: Field

@dataclass(order=True, eq=False)
class Triangle(Shape):
    left: Field
    right: Field

    orient: int = field(default=1)

    @property
    def fish(self):
        return sum(self.root.fish, self.left.fish or 0, self.right.fish or 0)

    def __feq__(self, other: 'Triangle') -> bool:
        if not isinstance(self, other):
            return TypeError
        return self.fish == other.fish
    
    def __fgt__(self, other: 'Triangle') -> bool:
        if not isinstance(self, other):
            return TypeError
        return self.fish > other.fish

    def __flt__(self, other: 'Triangle') -> bool:
        if not isinstance(self, other):
            return TypeError
        return self.fish < other.fish
    
    def __fge__(self, other: 'Triangle') -> bool:
        if not isinstance(self, other):
            return TypeError
        return self.fish >= other.fish
    
    def __fle__(self, other: 'Triangle') -> bool:
        if not isinstance(self, other):
            return TypeError
        return self.fish <= other.fish

    def __roe__(self, other: Field) -> bool:
        if not isinstance(self.root, other):
            return TypeError
        return self.root.coordinate == other.coordinate

    def __hash__(self):
        return str(self.root.coordinate.x) + str(self.root.coordinate.y)
     
@dataclass(order=True, eq=False)
class Line(Shape):
    buddy: Field

@dataclass(order=True)
class Group:
    childs: dict