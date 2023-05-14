from socha import *
from board_extentions import *
import random

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
class Tile:

    root: Field
    penguin: Penguin
    children: dict[Shape] = field(default_factory={})
    fish: int = 0

@dataclass(order=True)
class Group:

    children: dict[Tile] = field(default_factory={})
    fields: dict[list[str]] = field(default_factory={})
    penguins: list[Penguin] = field(default_factory=[])
    fish: int = 0

        
@dataclass(order=True)
class TriBoard:

    board: Board
    current_team: Team
    groups: list[Group]

    def construct(self):
        '''stuff'''

    def build_groups(self):
        groups = []
        for penguin in self.current_team.penguins:
            new_group = self.extend_shape(penguin.coordinate)
            if new_group:
                groups.append(new_group)
        return groups

    def extend_shape(self, root: HexCoordinate, group = {} , memory= []):
        new_neighbors = [each for each in root.get_neighbors if self.board._is_destination_valid(each) and self.hash(each) not in memory]
        new_list: dict = self.hash_dict_shape(root)
        if new_neighbors == []:
            return new_list
        for neighbor in new_neighbors:
            add_list = self.extend_shape(self, neighbor)
            new_list.update(add_list)
        return new_list
    
    def calc_tile_ente(self, field: Field):
        '''
        calcs tiles for that given Field
        '''

        neighbors = field.coordinate.get_neighbors()
        neighbors_bool = []
        for i in range(len(neighbors)):
            if own_is_valid(neighbors[i]):
                n_field = self.board.get_field(neighbors[i])

                if n_field.fish > 0:
                    neighbors_bool.append(True)
                elif n_field.penguin != None:
                    if n_field.penguin.team_enum.name == self.current_team.name.name:
                        neighbors_bool.append(True)
            
            if not neighbors_bool[i]:
                neighbors_bool.append(False)

        [print(each) for each in neighbors_bool]

    def make_tile(self, root: HexCoordinate):
        shapes = {"test"} # @Ente
        return Tile(root, shapes)

    def hash(self, coordinate: HexCoordinate):
        return str(coordinate.x) + str(coordinate.y)

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

test_board_1 = generate_board()
#test_board_1.pretty_print()
test_triboard_1 = TriBoard(
    board=test_board_1,
    current_team=Team(TeamEnum('ONE'), 0, [], []),
    groups=[]
)

rng_field = test_board_1.board[random.randint(0, 7)][random.randint(0, 7)]
test_board_1.pretty_print()
print(rng_field)
test_triboard_1.calc_tile(rng_field)


'''print(test_tri.__class__.__name__) # important!!'''
'''
left_up = True
right_up = True
right = False
right_down = True
left_down = False

tri_up = False
tri_down = False
line_up = False
line_side = False
line_down = False

if right_up and left_up: tri_up = True
if right_down and left_down: tri_down = True
if not right:
    if not tri_up and right_up: line_up = True
    if not tri_down and right_down: line_down = True
elif not right_up and not right_down: line_side = True

print("tri_up:", tri_up)
print("tri_down:", tri_down)
print("line_up:", line_up)
print("line_side:", line_side)
print("line_down:", line_down)'''