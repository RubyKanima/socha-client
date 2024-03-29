from socha import *
from typing import List

from dataclasses import dataclass

class Tile(Field):

    def __init__(self):
        self.neighbors = self.coordinate.get_neighbors()

    def _expand(_tile) -> list:
        list = []
        for each in _tile.neighbors:
            if each not in list:
                list.append(Tile._expand(_tile, list))
        return list.append(_tile)


    def is_valuable(_tile) -> bool:
        return _tile.fish in [2,3,4]

@dataclass
class CustomBoard(Board):

    board: Board


    def del_fields(board: Board, _del: List[int]) -> Board:
        new_board: List[List[Field]] = []
        for row in board.board:
            row_list = []
            for field in row:
                if field.fish in _del or field.penguin:
                    row_list.append(Field(HexCoordinate(field.coordinate.x, field.coordinate.y), None, 0))
                else:
                    row_list.append(field)
            new_board.append(row_list)
        return Board(new_board)
    
    def del_fields(board: Board, _del: int):
        new_board: List[List[Field]] = []
        for row in board.board:
            row_list = []
            for field in row:
                if field.fish == _del or field.penguin:
                    row_list.append(Field(HexCoordinate(field.coordinate.x, field.coordinate.y), None, 0))
                else:
                    row_list.append(field)
            new_board.append(row_list)
        return Board(new_board)
    
    def filter_moves(board: Board, move_list: List[Move]):
        move_list_to = [each.to_value for each in move_list]
        new_board = []
        for row in board.board:
            row_list = []
            for field in row:
                if field.coordinate in move_list_to or field.penguin:
                    row_list.append(field)
                else:
                    row_list.append(Field(field.coordinate, None, 0))
            new_board.append(row_list)
        return Board(new_board)

    def filter_fields(board: Board, filter: int):
        filter_list = [0,1,2,3,4].remove(filter)
        return CustomBoard.del_fields(board, filter_list)
    
    def filter_fields(board: Board, filter: list = [0,1]):
        filter_list = [[0,1,2,3,4].remove(each) for each in filter]
        return CustomBoard.del_fields(board, filter_list)


class Blob():
    
    def __init__(self, blob: List[Field]):
        self.blob = blob
        self.fish = self._get_fish_val()
        self.quantity = len(blob)
    
    def _get_fish_val(self) -> int:
        fish = 0
        for each in self.blob:
            fish += each.fish
        return fish
    
    def _create_blob(self, _board: Board):
        new_board = CustomBoard.del_fields(_board, 1)