from socha import *

from dataclasses import dataclass, field

@dataclass(order=True)
class Shape:
    root: Field
    children: list[Field] = field(default_factory=[])
    orient: int = 1
    shape: str = "Triangle"

    @property
    def fish(self):
        f = self.root.fish
        for c in self.children:
            f += c.fish
        return f

    @property
    def hash(self):
        return str(self.root.coordinate.x) + str(self.root.coordinate.y)

    '''
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

@dataclass(order=True)
class Group:
    children: dict[dict] = field(default_factory={})
    fields: dict[list] = field(default_factory={})
    fish: int = 0

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


#### TESTING ####


'''print(test_tri.__class__.__name__) # important!!'''