from socha import *
from typing import Optional, List
import math
    
def get_possible_movements(state: GameState, team: TeamEnum = None):
    ''' 
    gets the possible moves from a team if the penguins could be move
    
    this is only worth using before turn 9
    '''
    if team == None:
        team = state.current_team
    possible_movements = []
    penguins: list[Penguin] = state.board.get_teams_penguins(team.name)
    for penguin in penguins:
        possible_movements.extend(state.board.possible_moves_from(penguin.coordinate, penguin.team_enum))
    return possible_movements

def get_fields_in_direction(board: Board, origin: HexCoordinate, direction: Vector, team_enum: Optional[TeamEnum] = None) -> List[Field]:
    """
    Gets all moves in the given direction from the given origin.

    Args:
        origin: The origin of the move.
        direction: The direction of the move.
        team_enum: Team to make moves for.

    Returns:
            `List[Field]`: List of moves that can be made in the given direction from the given index,
                        for the given team_enum
    """
    if team_enum is None:
        team_enum = board.get_field(origin).penguin.team_enum
    if not board.get_field(origin).penguin or board.get_field(origin).penguin.team_enum != team_enum:
        return []

    fields = []
    for i in range(1, 8):
        destination = origin.add_vector(direction.scalar_product(i))
        if board._is_destination_valid(destination):
            fields.append(board.get_field(destination))
        else:
            break
    return fields

def get_possible_fields_from(state: GameState, position: HexCoordinate, team_enum: TeamEnum = None)-> List[Field]:
    if team_enum == None:
        team_enum = state.current_team.name
    if not state.board.is_valid(position):
        raise IndexError(f"Index out of range: [x={position.x}, y={position.y}]")
    if not state.board.get_field(position).penguin or (
            team_enum and state.board.get_field(position).penguin.team_enum != team_enum):
        return []
    return [field for direction in Vector().directions for field in get_fields_in_direction(state.board, position, direction, team_enum)]

def get_possible_fields(state: GameState, team: TeamEnum = None)-> List[Field]:
    if team == None:
        team = state.current_team
    possible_fields = []
    penguins: list[Penguin] = state.board.get_teams_penguins(team.name)
    for penguin in penguins:
        possible_fields.extend(get_possible_fields_from(state, penguin.coordinate, penguin.team_enum))
    return possible_fields

def get_penguin_neighbor_moves(board: Board,penguins: List[Penguin]):
    neighbor_moves = []
    for penguin in penguins:
        neighbors = [each for each in get_neighbor_fields_coordinate(board, penguin.coordinate) if each.fish >= 1]
        for each in neighbors:
            neighbor_moves.append(Move(penguin.team_enum, each.coordinate, penguin.coordinate))
    return neighbor_moves    

def get_neighbor_fields_coordinate(board: Board, coordinate: HexCoordinate):
    return [board.get_field(each) for each in coordinate.get_neighbors() if board.is_valid(each)]

def get_neighbor_fields(board: Board, field: Field) -> List[Field]:
    return [board.get_field(each) for each in field.coordinate.get_neighbors() if board.is_valid(each)]
        
def get_dir(r: Vector):
  '''
  `get_dir_()` is faster
  '''
  direction_x = r.d_x / math.sqrt(r.d_x ** 2) if not r.d_x == 0 else 0
  direction_y = r.d_y / math.sqrt(r.d_y ** 2) if not r.d_y == 0 else 0
  return Vector(math.floor(direction_x), math.floor(direction_y))

def get_dir_(r: Vector):
    '''
    `get_dir_()` is a specified version of the directional vector for socha
    '''
    n_y = -1 if r.d_y < 0 else 0 if r.d_y == 0 else 1    
    n_x = -1 if r.d_x < 0 else 1
    n_x = n_x*2 if n_y == 0 else n_x
    return Vector(n_x, n_y)

def remove_solo_fields(state: GameState, move_list: list[Move]):
    for move in move_list:
        count = 0
        for each in move.to_value.get_neighbors(): 
            count += 1 if state.board._is_destination_valid(each) else 0
        if count == 0:
            move_list.remove(move)
    return move_list    
                    

