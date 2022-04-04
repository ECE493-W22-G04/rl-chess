from typing import NamedTuple, Optional
from .piece import Piece


class Square(NamedTuple):
    x: int
    y: int


class Move(NamedTuple):
    from_square: Square
    to_square: Square
    promotion: Optional[Piece] = None
