from socha import *
from dataclasses import dataclass, field

from .board_extentions import *

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
    fish: int = 0
    children: dict[Shape] = field(default_factory={})
    

@dataclass(order=True)
class Group:

    children: dict[Tile] = field(default_factory={})
    fields: dict[list[str]] = field(default_factory={})
    penguins: list[Penguin] = field(default_factory=[])
    fish: int = 0

    def remove_field(self, coordinate: HexCoordinate):
        '''
        removes given field by key and mods the shapes

        pseudo:
        if field in fields
        remove tile at field (if exists)
        remove field from fields
        recalc tiles of neighbors
        '''
        rm_hash = self.hash(coordinate)
        if not rm_hash in self.fields: return
        if rm_hash in self.children:
            del self.children[rm_hash]
        del self.fields[rm_hash]
        self.fish


        #### WORK IN PROGRESS

    def tri_to_line(self):
        '''
        converts triangle to line by given key and removed field
        '''

    def hash(self, coordinate: HexCoordinate):
        return (str(coordinate.x) + str(coordinate.y))
        
@dataclass(order=True,repr=True)
class TriBoard:

    board: Board
    current_team: Team
    hash_list: list[str] = field(default_factory=[])
    _groups: list[Group] = None
    
    @property 
    def groups(self):
        if self._groups: return self._groups
        else: 
            self._groups = self.build_groups()
            return self._groups

    def build_groups(self) -> list[Group]:
        groups: list[Group] = []

        for penguin in self.current_team.penguins:
            if not self.hash(penguin.coordinate) in self.hash_list:
                groups.append(Group(self.extend_shape(penguin.coordinate, True)))
        return groups

    def extend_shape(self, root: HexCoordinate, first = False, group = {}) -> dict[Tile]:
        hash = self.hash(root)
        if not own_is_valid(root):return
        if hash in self.hash_list: return
        this_field = self.board.get_field(root)
        if self.tile_valid(this_field.coordinate):
            group[hash] = self.make_tile(root)
            self.hash_list.append(hash)
        new_neighbor = [neighbor for neighbor in root.get_neighbors() if not self.hash(neighbor) in self.hash_list and own_is_valid(neighbor)]
        for neighbor in new_neighbor:
            self.extend_shape(neighbor)
        if first:
            return group

    def make_tile(self, root: HexCoordinate):
        '''
        ! TEST NEEDED !
        '''
        field = self.board.get_field(root)
        fields = []
        shape_list = []
        tri_up = False
        tri_down = False
        for vector in Vector().directions:
            n = root.add_vector(vector)
            fields.append(self.tile_valid(n))
        
        if fields[5] and fields[0]: 
            shape_list.append(Shape(root, [fields[0], fields[5]], -1, "Triangle"))# up right & up left
            tri_up = True 
        if fields[3] and fields[2]:
            shape_list.append(Shape(root, [fields[3], fields[2]], 1, "Triangle"))# down right & down left
            tri_down = True
        if not fields[4]:                                                   # not right
            if not tri_up and fields[0]: 
                shape_list.append(Shape(root, [fields[0]], -1, "line"))     # not up tri & up right
            if not tri_down and fields[2]: 
                shape_list.append(Shape(root, [fields[2]], 1, "line"))      # not down tri & down right
        elif not (fields[0] or fields[2]): 
            shape_list.append(Shape(root, [fields[4]], 0, "line"))          # not (up right | down right)
        
        return Tile(root, field.penguin, field.fish, shape_list)

    def tile_valid(self, destination: HexCoordinate):
        if not own_is_valid(destination):                               # Not Valid
            return None
        field = self.board.get_field(destination)                       # Valid
        if field.fish > 0:                                              # If not occupied
            return field                            
        if field.penguin:                                               # If occupied
            if field.penguin.team_enum.name == self.current_team.name.name:  # If own team
                return field
        return None                                                     # If anything else

    def hash(self, coordinate: HexCoordinate):
        return (str(coordinate.x) + str(coordinate.y))

    def get_subgroup(self):
        '''
        get subgroup from key and its missing neighbors
        '''

    def search_group(self):
        '''
        search the group for something (dont know yet)
        '''


#### TESTING ####"""
"""
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
)

rng_field = test_board_1.board[random.randint(0, 7)][random.randint(0, 7)]
test_board_1.pretty_print()
print(rng_field)
test_triboard_1.calc_tile_ente(rng_field)

"""
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