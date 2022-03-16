from enum import Enum

class Piece(Enum):
    PAWN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Board:
    def __init__(self) -> None:
        back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.KNIGHT]
        front_row = [Piece.PAWN for _ in range(8)]

        self.state = [
            [piece * -1 for piece in back_row],
            [piece * -1 for piece in front_row],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [piece for piece in front_row],
            [piece for piece in back_row],
        ]
    
    def get_actions():
        pass

    def get_legal_actions():
        pass
