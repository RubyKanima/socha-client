from socha import *
from logic import Logic

class Shape:

    def __init__(self, root: Field, children: list[Field] = [], orient: int = 1, shape: str = 'Triangle'):
        self.root = root
        self.children = children
        self.orient = orient
        self.shape = shape

    def fish(self):
        f = self.root.fish
        for c in self.children:
            f += c.fish
        return f

    def hash(self) -> str:
        return str(self.root.coordinate.x) + str(self.root.coordinate.y)

class Tile:

    def __init__(self, root: HexCoordinate, penguin: Penguin, fish: int = 0, shapes: dict[str, Shape] = [], inters: int = 0, spot: str = None, group: int = None):
        self.root = root
        self.penguin = penguin
        self.fish = fish
        self.shapes = shapes
        self.inters = inters
        self.spot = spot
        self.group = group

class Group:

    def __init__(self, index: int, group: dict[str, Tile], fish: int = 0, penguins: list[Penguin] = []):
        self.index = index
        self.group = group
        self.fish = fish
        self.penguins = penguins

    def is_contesting(self):
        if not self.penguins:
            return False
        team = self.penguins[0].team_enum.name
        for each in self.penguins:
            if each.team_enum.name != team:
                return True
        return False
    
    def contains_team(self, team_str: str):
        for penguin in self.penguins:
            if team_str == penguin.team_enum.name:
                return True
        return False

class Subgroup(Group):

    def __init__(self, index: int, group: dict[str, Tile], fish: int = 0, penguins: list[Penguin] = [], neighbors: list['Subgroup'] = []):
        super().__init__(index, group, fish, penguins)
        self.neighbors = neighbors

    def sub_group_testing(self, memo = []):
        this_neighbors = []
        for neighbor in self.neighbors:
            if neighbor not in memo:
                this_neighbors.append(neighbor)
        if not this_neighbors:
            return self.fish
        for this_neighbor in this_neighbors:
            return 
        
class FullGroup(Group):

    def __init__(self, index: int, group: dict[str, Tile], fish: int = 0, penguins: list[Penguin] = [], _subgroups: list[Subgroup] = [], _check_list: list[str] = []):
        super().__init__(index, group, fish, penguins)
        self._subgroups = _subgroups
        self._check_list = _check_list

    def subgroups(self) -> list[Subgroup]:
        if not self._subgroups:
            self._subgroups = self._make_subgroups()
        return self._subgroups
    
    def _get_subgroup_by_coord(self, _subgroups: list[Subgroup], coord: HexCoordinate) -> Subgroup:
        this_hash = own_hash(coord)
        for subgroup in _subgroups:
            if this_hash in subgroup.group:
                return subgroup
            
    def get_subgroup_by_coord(self, coord: HexCoordinate) -> Subgroup:
        this_hash = own_hash(coord)
        for subgroup in self.subgroups():
            if this_hash in subgroup.group:
                return subgroup

    def _make_subgroups(self, spot:str = "black"):
        index_count = 0
        subgroups: list[Subgroup] = []
        self._check_list = [key for key in self.group]
        black_spots = [self.group[tile] for tile in self.group if self.group[tile].spot == spot]

        for tile in black_spots:
            self._check_list.remove(own_hash(tile.root))
            this_dict: dict[str, Tile] = {}
            this_dict[own_hash(tile.root)] = tile
            subgroups.append(Subgroup(index_count, this_dict, tile.fish, [], [],))
            index_count+=1

        for tile in black_spots:
            for neighbor in tile.root.get_neighbors():
                if own_hash(neighbor) in self._check_list and self.group[own_hash(neighbor)].spot != "black":
                    this_subgroup, new_fish = self._make_subgroup(neighbor) #initial recursive call
                    new_subgroup = Subgroup(index_count, this_subgroup, new_fish, [], [])
                    subgroups.append(new_subgroup)
                    index_count+=1

        for tile in black_spots:
            tile_group = self._get_subgroup_by_coord(_subgroups = subgroups, coord = tile.root)
            if tile_group:
                for neighbor in tile.root.get_neighbors():
                    for subgroup in subgroups:
                        if own_hash(neighbor) in subgroup.group and not subgroup in tile_group.neighbors:
                            tile_group.neighbors.append(subgroup)
                            subgroup.neighbors.append(tile_group)

        for penguin in self.penguins:
            for neighbor in penguin.coordinate.get_neighbors():
                for subgroup in subgroups:
                        if own_hash(neighbor) in subgroup.group and not penguin in subgroup.penguins:
                            subgroup.penguins.append(penguin)

        return subgroups

    def _make_subgroup(self, coord: HexCoordinate):
        this_hash = own_hash(coord)
        this_fish = self.group[this_hash].fish
        self._check_list.remove(this_hash)
        neighbors = [n for n in coord.get_neighbors() if own_hash(n) in self._check_list] #check for penguin in penguins
        for each in neighbors:
            if self.group[own_hash(each)].spot == "black": 
                neighbors.remove(each)
        this_dict: dict[str, Tile] = {}
        this_dict[this_hash] = self.group[this_hash]
        if neighbors == []:
            return this_dict, this_fish
        return_dict: dict[str, Tile] = {}
        for neighbor in neighbors:
            if own_hash(neighbor) in self._check_list:
                group, fish = self._make_subgroup(neighbor)
                return_dict = {**group, **return_dict}
                this_fish: int = this_fish + fish
        return {**return_dict, **this_dict}, this_fish


class TriBoard:

    def __init__(self, board: Board, current_team: Team, _check_list: list = [], _groups: list[Group] = [], _tri_board: list[list[Tile]] = []):
        self.board = board
        self.current_team = current_team
        self._check_list = _check_list
        self._groups = _groups
        self._tri_board = _tri_board
    
    def tri_board(self):
        if self._tri_board: return self._tri_board
        else:
            self._tri_board = self._make_tri_board()
            return self._tri_board

    def groups(self):
        if self._groups: return self._groups
        else: 
            self._groups = self._make_groups()
            return self._groups
        
    def is_any_contest(self):
        for each in self.groups():
            if each.is_contesting():
                return True
        return False
    
    def get_contesting_penguins(self) -> list[Penguin]:
        this_penguins = []
        for group in self.groups():
            if group.is_contesting():
                for penguin in group.penguins:
                    if penguin not in this_penguins:
                        this_penguins.append(penguin)
        return this_penguins

    def get_least_shapes_move(self, logic: Logic):
        max_move = logic.game_state.possible_moves[0]
        check_groups = self.get_best_tiles(logic.game_state.current_team.penguins)
        better_moves = [move for move in logic.game_state.possible_moves if own_hash(move.to_value) in check_groups]
        min_val = 6
        valid_list = []

        for move in better_moves:
            if self.get_tile(move.to_value).spot == "yellow":
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
    
    def get_best_tiles(self, penguins: list[Penguin]):
        best_tiles = []
        for penguin in penguins:
            this_groups: list[Group] = []
            for group in self.groups():
                if penguin in group.penguins:
                    this_groups.append(group)
            if not this_groups:
                break
            this_best_group = this_groups[0]
            for each in this_groups:
                if each.fish > this_best_group.fish:
                    this_best_group = each
            best_tiles.extend(this_best_group.group)
        return best_tiles
        
    def _make_tri_board(self) -> list[list[Tile]]:
        tri_board = []
        for row in self.board.board:
            y = []
            for field in row:

                y.append(self.make_tile(field.coordinate))
            tri_board.append(y)
        return tri_board
    
    def get_tile(self, coord: HexCoordinate) -> Tile:
        coord = coord.to_cartesian()
        tri = self.tri_board()
        return tri[coord.y][coord.x]
    
    def get_group(self, hash_str: str):
        for group in self.groups():
            if hash_str in group.group:
                return group

    def _make_groups(self):
        groups: list[FullGroup] = []
        index_count: int = 0
        self._check_list = [field.coordinate for row in self.board.board for field in row if field.fish > 0]

        while self._check_list:
            this_coord = self._check_list[0]
            if own_is_destination_valid(self.board, this_coord):
                group, fish = self._make_group(this_coord, index_count)   #initial call of the recursive function
                groups.append(FullGroup(index_count, group, fish, [], [], []))
                index_count+=1

        penguins: list[Penguin] = []
        penguins.extend(self.current_team.penguins)
        penguins.extend(self.current_team.opponent.penguins)
        for penguin in penguins: #could of course be in recursion but for that I'd need a global var that resets in every initial recursion call
            for neighbor in penguin.coordinate.get_neighbors():
                for group in groups:
                        if own_hash(neighbor) in group.group and not penguin in group.penguins:
                            group.penguins.append(penguin)
        return groups


    def _make_group(self, root: HexCoordinate, group_count:int = 0):
        self._check_list.remove(root)
        root_cart = root.to_cartesian()
        this_fish = self.board.get_field(root).fish
        neighbors = [n for n in root.get_neighbors() if n in self._check_list]
        this_dict: dict[str, Tile] = {}
        this_dict[own_hash(root)] = self.get_tile(root)
        self._tri_board[root_cart.y][root_cart.x].group = group_count
        if neighbors == []:                                                                         #wenn filtered neighbors == []
            return this_dict, this_fish
        return_group = {}
        for neighbor in neighbors:
            if neighbor in self._check_list:
                group, fish = self._make_group(neighbor)
                return_group = {**group, **return_group}
                this_fish = this_fish + fish
        return {**return_group,**this_dict}, this_fish
    
    def make_groups_from(self) -> list[FullGroup]:
        groups: list[FullGroup] = []
        self._check_list = get_all_coords(self.board)

        for penguin in self.current_team.penguins:
            for neighbor in penguin.coordinate.get_neighbors():
                if not self.in_groups(neighbor, groups) and own_is_destination_valid(self.board, neighbor):
                    
                    group, fish = self.make_group(neighbor)   #initial call of the recursive function

                    groups.append(FullGroup(group, fish, [penguin])) #penguin isn't necessary here but whatever
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
            spot = "yellow"
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
        return None      
    
    def hash(self, coordinate: HexCoordinate):
        return (str(coordinate.x) + str(coordinate.y))

    def in_groups(self, coord: HexCoordinate, groups: list[FullGroup]) -> bool:
        for group in groups:
            if own_hash(coord) in group.group:
                return True
        return False
    
    def perform_move(self, move: Move):
        
        updated_board = self.board.move(move)

        next_team = self.current_team
        for penguin in updated_board.get_teams_penguins(self.current_team.opponent.name):
            if not updated_board.possible_moves_from(penguin.coordinate) == []:
                next_team = self.current_team.opponent
                break
            break

        return TriBoard(updated_board, next_team, [] , [], [])
    
from .board_extentions import own_hash, own_is_destination_valid, get_all_coords, own_get_neighbors, own_is_valid