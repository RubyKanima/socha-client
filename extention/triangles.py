from socha import *

from dataclasses import dataclass, field

'''@dataclass(order=True)
class Shape:
    root: Field
    children: dict
    orient: int = -1 | 0 | 1
    _fish: int

    @property
    def hash(self):
        return str(self.root.coordinate.x) + str(self.root.coordinate.y) + str(self.orient)

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
        return self.root.coordinate == other.coordinate'''


        



    




#### TESTING ####

test_tri = Triangle(Field(HexCoordinate(3, 7), None, 3), {'left': Field(HexCoordinate(2, 6), Penguin(HexCoordinate(2, 6), TeamEnum('ONE')), 0), 'right': Field(HexCoordinate(2, 6), Penguin(HexCoordinate(2, 6), TeamEnum('ONE')), 0)}, -1)
test_line = Line(Field(HexCoordinate(3, 7), None, 3), Field(HexCoordinate(4, 8), None, 1), 1)
print(test_tri.hash)
print(test_line.hash)

test = {test_tri.hash: 123}

@dataclass(order=True)
class Triangle:
    root: Field
    left: Field
    right: Field
    
    @property
    def fish(self):
        return sum(self.root.fish, self.left.fish or 0, self.right.fish or 0)


@dataclass(order=True)
class Line:
    root: Field
    right: Field
    
    @property
    def fish(self):
        return sum(self.root.fish, self.right.fish or 0)
    
print(test)
@dataclass(order=True)
class Group:
    shapes: dict[str, Triangle | Line]
    fields: dict[str, list[str]]

'''print(test_tri.__class__.__name__) # important!!'''@dataclass
class TriBoard:

    board: Board
    
    @property
    def groups(self):
        return 

    def construct(self):
        '''stuff'''

    def build_group(self):
        '''
        build a group from given list of fields (board)
        '''

    def remove_field(self):
        '''
        removes given field by key and mods the shapes
        '''

    def tri_to_line(self):
        '''
        converts triangle to line by given key and removed field
        '''

    def get_subgroup(self):
        '''
        get subgroup from key and its missing neighbors
        '''

    def search_group(self):
        '''
        search the group for something (dont know yet)
        '''