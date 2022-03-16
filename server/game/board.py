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
            [piece * -1 for piece in back_row],
            [piece * -1 for piece in front_row],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [piece for piece in front_row],
            [piece for piece in back_row],
        ]

        self.__actions = list(itertools.product(range(8), repeat=4))
    
    def get_actions(self):
        return self.__actions

    def get_legal_actions(self):
        pass

    def register(self, from_to: Move):
        pass

    def validate_move(self, move: Move):
        initial = (move[0], move[1])
        final = (move[2], move[3])

        piece = self.state[initial[0], initial[1]]

        if abs(piece) == Piece.PAWN:
            if piece > 0:
                if final[0] == initial[0] and final[1] - initial[1] == 1 and self.state[final[0], final[1]] == 0:
                    return True # Move forward by 1
                if abs(final[0] - initial[0]) == 1 and final[1] - initial[1] == 1 and self.state[final[0], final[1]] != 0:
                    return True # Capture
                if final[0] == initial[0] and initial[1] == 6 and final[1] == 4 and self.state[final[0], final[1]] == 0:
                    return True # First move
                return False                
            pass
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
