from socha import *
from dataclasses import dataclass, field
from copy import copy
from .board_extentions import *
from logic import Logic
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

    root: HexCoordinate
    penguin: Penguin
    fish: int = 0
    shapes: dict[str, Shape] = field(default_factory={})
    inters: int = 0
    spot: str = None
    

@dataclass(order=True)
class Group:

    group: dict[str, Tile]
    fish: int = 0
    penguins: list[Penguin] = field(default_factory=[])
    
@dataclass(order=True, repr=True)
class TriBoard:

    board: Board
    current_team: Team
    _check_list: list[str] = field(default_factory=[])
    _groups: list[Group] = field(default_factory=[])
    _tri_board: list[list[Tile]] = field(default_factory=[])
    
    @property
    def tri_board(self):
        if self._tri_board: return self._tri_board
        else:
            self._tri_board = self._make_tri_board()
            return self._tri_board

    @property 
    def groups(self):
        if self._groups: return self._groups
        else: 
            self._groups = self._make_groups()
            return self._groups
        
    def get_least_shapes_move(self, logic: Logic):
        max_move = logic.game_state.possible_moves[0]
        min_val = 6
        valid_list = []

        for move in logic.game_state.possible_moves:
            if self.get_tile(move.to_value).spot == "end":
                valid_list.append(move)

        if not valid_list:        
            for move in logic.game_state.possible_moves:
                if self.get_tile(move.to_value).spot == "white":
                    valid_list.append(move)
        
        if not valid_list:
            valid_list = logic.game_state.possible_moves

        for move in valid_list:
            tile = self.get_tile(move.to_value)
            val = tile.inters
            if val <= min_val and not val == 0:
                min_val = val
                max_move = move
        return max_move
        
    def _make_tri_board(self) -> list[list[Tile]]:
        tri_board = []
        for row in self.board.board:
            y = []
            for field in row:

                y.append(self.make_tile(field.coordinate))
            tri_board.append(y)
        return tri_board
    
    def get_tile(self, coord: HexCoordinate):
        coord = coord.to_cartesian()
        return self.tri_board[coord.y][coord.x]

    def _make_groups(self):
        groups: list[Group] = []
        self._check_list = [field.coordinate for row in self.board.board for field in row if field.fish > 0]

        while self._check_list:
            this_coord = self._check_list[0]
            print(this_coord)
            if own_is_destination_valid(self.board, this_coord):
                group, fish = self._make_group(this_coord)   #initial call of the recursive function
                groups.append(Group(group, fish, []))

        penguins: list[Penguin] = []
        penguins.extend(self.current_team.penguins)
        penguins.extend(self.current_team.opponent.penguins)
        for penguin in penguins: #could of course be in recursion but for that I'd need a global var that resets in every initial recursion call
            for neighbor in penguin.coordinate.get_neighbors():
                for group in groups:
                        if own_hash(neighbor) in group.group and not penguin in group.penguins:
                            group.penguins.append(penguin)
        return groups


    def _make_group(self, root: HexCoordinate):
        self._check_list.remove(root)
        this_fish = self.board.get_field(root).fish
        neighbors = [n for n in root.get_neighbors() if n in self._check_list]
        this_dict: dict[str, Tile] = {}
        this_dict[own_hash(root)] = self.get_tile(root)
        if neighbors == []:                                                                         #wenn filtered neighbors == []
            return this_dict, this_fish
        return_group = {}
        for neighbor in neighbors:
            if neighbor in self._check_list:
                group, fish = self._make_group(neighbor)
                return_group = {**group, **return_group}
                this_fish = this_fish + fish
        return {**return_group,**this_dict}, this_fish
    
    def make_groups_from(self) -> list[Group]:
        groups: list[Group] = []
        self._check_list = get_all_coords(self.board)

        for penguin in self.current_team.penguins:
            for neighbor in penguin.coordinate.get_neighbors():
                if not self.in_groups(neighbor, groups) and own_is_destination_valid(self.board, neighbor):
                    
                    group, fish = self.make_group(neighbor)   #initial call of the recursive function

                    groups.append(Group(group, fish, [penguin])) #penguin isn't necessary here but whatever
                else:
                    for group in groups:
                        if own_hash(neighbor) in group.group and not penguin in group.penguins:
                            group.penguins.append(penguin)
        for other_penguin in self.current_team.opponent.penguins: #could of course be in recursion but for that I'd need a global var that resets in every initial recursion call
            for neighbor in other_penguin.coordinate.get_neighbors():
                for group in groups:
                        if own_hash(neighbor) in group.group and not other_penguin in group.penguins:
                            group.penguins.append(other_penguin)
        return groups

    def make_group(self, root: HexCoordinate) -> dict[str, Tile]:
        self._check_list.remove(root)
        this_fish = self.board.get_field(root).fish
        neighbors = [n for n in root.get_neighbors() if n in self._check_list and own_is_destination_valid(self.board, n)]    #filter: alle nachbarn, wenn sie in new_list sind und valid
        return_hash: dict[str, Tile] = {}
        return_hash[own_hash(root)] = self.make_tile(root)
        if neighbors == []:                                                                         #wenn filtered neighbors == []
            return return_hash, this_fish
        return_dict = {}
        for neighbor in neighbors:
            if neighbor in self._check_list:
                hash_dict, fish = self.make_group(neighbor)
                return_dict = {**hash_dict, **return_dict}
                this_fish = this_fish + fish
        return {**return_dict,**return_hash}, this_fish

    def get_subgroups(self):
        ''''''

    def make_tile(self, root: HexCoordinate):
        field = self.board.get_field(root)
        shape_list = self.make_shape(root)
        intersection_num, spot = self.count_intersections(root)
        return Tile(root, field.penguin, field.fish, shape_list, intersection_num, spot)

    def make_shape(self, root: HexCoordinate):
        fields = []
        shape_list = []
        tri_up = False
        tri_down = False

        for vector in Vector().directions:
            n = root.add_vector(vector)
            fields.append(self.board._is_destination_valid(n))
        
        if fields[5] and fields[0]: 
            shape_list.append(Shape(root, [fields[0], fields[5]], -1, "Triangle"))  # up right & up left
            tri_up = True 
        if fields[3] and fields[2]:
            shape_list.append(Shape(root, [fields[3], fields[2]], 1, "Triangle"))   # down right & down left
            tri_down = True
        if not fields[4]:                                                           # not right
            if not tri_up and fields[0]: 
                shape_list.append(Shape(root, [fields[0]], -1, "line"))             # not up tri & up right
            if not tri_down and fields[2]: 
                shape_list.append(Shape(root, [fields[2]], 1, "line"))              # not down tri & down right
        elif not (fields[0] or fields[2]):
            shape_list.append(Shape(root, [fields[4]], 0, "line"))                  # not (up right | down right)
        
        return shape_list
    
    def count_intersections(self, root: HexCoordinate):
        count = 0
        redspot = False
        blackspot = True
        empty_mirror = False
        mirror = True
        neighbors = []
        for n in own_get_neighbors(root):   #Nachbarliste machen
            if own_is_valid(n):
                neighbors.append(self.board.get_field(n).get_fish() > 0)
            else:
                neighbors.append(False)
        for i in range(0,6):
            if neighbors[i]:
                if neighbors[(i+1) % 6]:
                    count += 1
                    blackspot = False
                elif not neighbors[i-1]:
                    count += 1
                    redspot = True
            elif not neighbors[i-3]:
                empty_mirror = True
            elif neighbors[i-3]:
                mirror = False
        if empty_mirror and count == 2:
            redspot = True

        spot = "white"

        if count == 1 and redspot:
            spot = "end"
        elif blackspot and not mirror:
            spot = "black"
        elif redspot:
            spot = "red"

        return count, spot

    def tile_valid(self, destination: HexCoordinate) -> Field | None:
        if not own_is_valid(destination):                               # Not Valid
            return None
        field = self.board.get_field(destination)                       # valid
        if field.fish > 0:                                              # If not occupied
            return field                            
        return None                                                     # If anything else
    """
    def is_tile_valid(self, destination: HexCoordinate) -> bool:
        '''
        ! unused !
        '''
        if not own_is_valid(destination):                               # Not Valid
            return False
        field = self.board.get_field(destination)                       # Valid
        if field.fish > 0:                                              # If not occupied
            return True                            
        if field.penguin:                                               # If occupied
            if field.penguin.team_enum.name == self.current_team.name.name:  # If own team
                return True
        return False                                                     # If anything else
    """
    def hash(self, coordinate: HexCoordinate):
        return (str(coordinate.x) + str(coordinate.y))

    def in_groups(self, coord: HexCoordinate, groups: list[Group]) -> bool:
        for group in groups:
            if own_hash(coord) in group.group:
                return True
        return False

    def __own_repr__(self):
        from .print_extentions import print_group_board_color
        for group in self.groups:
            print_group_board_color(self.board, group, self.current_team.name.name)
            print(group.fish,"  ", group.penguins)
            print()

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