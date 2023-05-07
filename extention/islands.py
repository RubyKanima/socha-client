from socha import Board, Field
from dataclasses import dataclass

from .triangles import Triangle


@dataclass
class Island:
    board: Board
    fields: list[Field]
    triangles: Triangle
