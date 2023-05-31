from .n_coordinates import *
from socha import Move, TeamEnum

from enum import Enum
from typing import Optional, List
import random
import math

class NTeamEnum(Enum):
    ONE = -1
    TWO = -2

    def to_team_enum(self):
        if self.name == -1:
            return TeamEnum("ONE")
        else:
            return TeamEnum("TWO")

class NBoard():

    def __init__(self, board: list[list[int]], _penguin_coords, ):
        self.board = board
        self._penguin_coords = _penguin_coords

    @property
    def penguin_coords(self) -> list[list[NHexCoordinate],list[NHexCoordinate]]:
        if not self._penguin_coords:
            self._penguin_coords = self.__get_all_penguins()
        return self._penguin_coords

    def __get_all_penguins(self) -> list[list[NHexCoordinate],list[NHexCoordinate]]:
        penguins = [[],[]]
        for y in range(8):
            for x in range(8):
                if self.board[y][x] == -1:
                    penguins[0].append(NCartesianCoordinate(x,y).to_hex())
                elif self.board[y][x] == -2:
                    penguins[1].append(NCartesianCoordinate(x,y).to_hex())
        return penguins

    def _get_field(self, x:int, y:int) -> int:
        return self.board[y][x]

    def get_field(self, position: NHexCoordinate) -> int:
        cartesian = position.to_cartesian()
        if cartesian.is_inbounce():
            return self._get_field(cartesian.x, cartesian.y)

        raise IndexError(f"Index out of range: [x={cartesian.x}, y={cartesian.y}]")
    
    def _is_occupied(self, x:int, y:int) -> bool:
        return self._get_field(x, y) < 0
    
    def is_occupied(self, position: NHexCoordinate) ->bool:
        return self.get_field(position) < 0
    
    def _is_valid(self, x:int, y:int) ->bool:
        return self._get_field(x, y) > 0
    
    def is_valid(self, position: NHexCoordinate) ->bool:
        return self.get_field(position) > 0
    
    def get_field_by_index(self, index: int) -> int:
        return self._get_field(NCartesianCoordinate.from_index(index, 8, 8))
    
    def get_all_fields(self) -> list[int]:
        """
        Gets all Fields of the board.

        :return: All Fields of the board.
        """
        return_list = []
        for each in self.board:
            return_list.extend(each)
        return return_list
    
    def contains(self, x:int, y:int, value:int):
        return self.board[y][x] == value
    
    def get_moves_in_direction(self, origin: NHexCoordinate, dir: NVector, team_enum: Optional[NTeamEnum] = None):

        if team_enum is None:
            team_enum = NTeamEnum(-1)
            
        if not self.is_occupied(origin) or self.get_field(origin) != team_enum.name:
            return []
        
        moves = []
        for i in range(1, 8):
            destination = origin.add_vector(dir.scalar_product(i))
            if self.is_valid(destination):
                moves.append(Move(team_enum=team_enum, from_value=origin, to_value=destination))
            else:
                break
        return moves
    
    def possible_moves_from(self, origin: NHexCoordinate, team_enum: Optional[NTeamEnum] = None) -> List[Move]:
        if not origin.is_inbounce():
            raise IndexError(f"Index out of range: [x={origin.x}, y={origin.y}]")
        if not self.is_occupied(origin) or (team_enum and self.get_field(origin) != team_enum):
            return []
        return [move for direction in NVector().directions for move in
                self.get_moves_in_direction(origin, direction, team_enum)]
    
    def perform_move(self, move: Move):
        to_val = move.to_value.to_cartesian()
        from_val = move.from_value.to_cartesian()
        new_board = self.board.copy()
        new_board[to_val.y][to_val.x] = new_board[from_val.y][from_val.x]
        new_board[from_val.y][from_val.x] = 0
        return NBoard(new_board)
    
    

    def get_possible_fish(self, team: NTeamEnum) -> int:
        if not team:
            raise ValueError("team is not given")
        if team != -2 and team != -1:
            raise ValueError(f"False Value in team: {team}")
        
        penguins = self.penguin_coords[0] if team == -1 else self.penguin_coords[1]

        fish = 0
        for penguin in penguins:
            for direction in NVector().directions:
                for i in range(1, 8):
                    destination = penguin.add_vector(direction.scalar_product(i))
                    if self.is_valid(destination):
                        fish += self.get_field(destination)
                    else:
                        break
        return fish
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.board == other.board
        return False
    

    
        
    

    
    
