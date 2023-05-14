from socha import *

from dataclasses import dataclass, field

@dataclass(order=True)
class Shape:
    root: Field
    children: list[Field] = field(default_factory=[])
    orient: int = 1
    shape: str = 'Triangle'

    @property
    def fish(self):
        f = self.root.fish
        for c in self.children:
            f += c.fish
        return f

    @property
    def hash(self) -> str:
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

    def __init__(self, board: Board, current_team: Team):   
        self.board = board
        self.current_team = current_team

    @property
    def groups(self): 
        return self.groups or self.build_groups(self.current_team)

    def build_groups(self):
        groups = []
        for penguin in self.current_team.penguins:
            if not self.hash(penguin.coordinate) in groups:
                groups.append(self.extend_shape(penguin.coordinate))
        return groups


    def extend_shape(self, root: HexCoordinate, memory= []):
        new_neighbors = [each for each in root.get_neighbors if self.board._is_destination_valid(each) and self.hash(each) not in memory]
        new_list: dict = self.hash_dict_shape(root)
        if new_neighbors == []:
            return new_list
        for neighbor in new_neighbors:
            add_list = self.extend_shape(self, neighbor)
            new_list.update(add_list)
        return new_list

    def hash_dict_shape(self, root: HexCoordinate):
        

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

test_shape_1 = Shape(
    root=Field(HexCoordinate(3, 7), None, 3),
    children=[Field(HexCoordinate(2, 6), None, 1), Field(HexCoordinate(4, 8), None, 4)],
    orient=-1,
    shape='Triangle'
)

print(test_shape_1.fish)

# __repr__ idea
string = ""
string += "  3   O  \n"
string += "   \ /   \n"
string += "    4---3\n"
string += "         \n"
string += "         \n"
#print(string)


'''print(test_tri.__class__.__name__) # important!!'''