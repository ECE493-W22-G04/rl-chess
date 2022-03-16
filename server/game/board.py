from enum import IntEnum
import itertools

class Piece(IntEnum):
    PAWN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

Move = tuple[int, int, int, int]

class Board:
    def __init__(self) -> None:
        back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
        front_row = [Piece.PAWN for _ in range(8)]

        self.state = [
            [piece * -1 for piece in back_row], # Black
            [piece * -1 for piece in front_row],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [piece for piece in front_row],
            [piece for piece in back_row], # White
        ]

        self.__actions = list(itertools.product(range(8), repeat=4))
    
    def get_actions(self):
        return self.__actions

    def get_legal_actions(self):
        pass

    def register(self, from_to: Move):
        pass

    def validate_move(self, move: Move):
        from_x = move[0]
        from_y = move[1]
        to_x = move[2]
        to_y = move[3]

        piece = self.state[from_y][from_x]
        target = self.state[to_y][to_x]

        if abs(piece) == Piece.PAWN:
            if piece > 0: # White piece
                if to_x == from_x and to_y - from_y == -1 and target == 0:
                    return True # Move forward by 1
                if abs(to_x - from_x) == 1 and to_y - from_y == -1 and target != 0:
                    return True # Capture
                if to_x == from_x and from_y == 6 and to_y == 4 and target == 0:
                    return True # First move
            else: # Black piece
                if to_x == from_x and to_y - from_y == 1 and target == 0:
                    return True # Move forward by 1
                if abs(to_x - from_x) == 1 and to_y - from_y == 1 and target != 0:
                    return True # Capture
                if to_x == from_x and from_y == 1 and to_y == 3 and target == 0:
                    return True # First move
            return False                
        if abs(piece) == Piece.BISHOP:
            pass
        if abs(piece) == Piece.KNIGHT:
            pass
        if abs(piece) == Piece.ROOK:
            pass
        if abs(piece) == Piece.QUEEN:
            pass
        if abs(piece) == Piece.KING:
            pass

        return False
