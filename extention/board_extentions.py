from socha import *

own_directions = [
    Vector(1,-1),
    Vector(2, 0),
    Vector(1, 1),
    Vector(-1,1),
    Vector(-2,0),
    Vector(-1,-1)
]
        
def own_is_valid(coordinates: HexCoordinate) -> bool:
    array_coordinates = coordinates.to_cartesian()
    return 0 <= array_coordinates.x < 8 and 0 <= array_coordinates.y < 8

def get_all_coords(board: Board) -> list[Field]:
        
    return [field.coordinate for row in board.board for field in row]

def own_is_destination_valid(board: Board, destination: HexCoordinate) -> bool:
    if not own_is_valid(destination):
        return False
    field = board.get_field(destination)
    if field.fish > 0:
        return True
    return False

def own_get_neighbors(coord: HexCoordinate):
    return [coord.add_vector(vector) for vector in own_directions]

def own_hash(coordinate: HexCoordinate):
    return (str(coordinate.x) + str(coordinate.y))

def get_possible_fish(state: GameState, team: TeamEnum = None) -> int:
    if team == None:
        team = state.current_team.name
    penguins: list[Penguin] = state.board.get_teams_penguins(team)
    fish = 0
    for penguin in penguins:
        for direction in Vector().directions:
            for i in range(1, 8):
                destination = penguin.coordinate.add_vector(direction.scalar_product(i))
                if state.board._is_destination_valid(destination):
                    fish += state.board.get_field(destination).fish
                else:
                    break
    return fish

def get_possible_moves_from_team(board: Board, teamenum: TeamEnum) -> list[Move]:
    penguins = board.get_teams_penguins(teamenum)
    
    poss_moves = []

    for each in penguins:
        poss_moves.extend(board.possible_moves_from(each.coordinate, teamenum))

    return poss_moves

def copycat(move: Move, team: TeamEnum):
    from_hex = HexCoordinate(15 - move.from_value.x, 7 - move.from_value.y) if move.from_value != None else None
    to_hex = HexCoordinate(15 - move.to_value.x, 7 - move.to_value.y)
    return Move(team_enum= team, to_value= to_hex, from_value= from_hex)

from .triangles import *

def copycat_validity(move: Move, tri_board: 'TriBoard'):
    this_groups = tri_board.get_group(own_hash(move.to_value))
    if not this_groups:
        return False
    if not this_groups.is_contesting():
        return False
    return True