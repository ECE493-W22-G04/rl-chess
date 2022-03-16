from enum import IntEnum
import itertools


class Piece(IntEnum):
    PAWN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


Move = tuple[int, int, int, int]  # (from_x, from_y, to_x, to_y)


def is_pawns_first_move(move: Move, is_white: bool):
    if is_white:
        return move[1] == 6
    return move[1] == 1


def is_forward_move(move: Move, is_white: bool):
    if move[0] != move[2]:
        return False
    if is_white:
        return move[3] < move[1]
    return move[3] > move[1]


def is_diagonal_move(move: Move):
    return abs(move[2] - move[0]) == abs(move[3] - move[1])


def is_rook_move(move: Move):
    if abs(move[2] - move[0]) > 0:
        return abs(move[3] - move[1]) == 0
    return abs(move[3] - move[1]) > 0


def is_knight_move(move: Move):
    if abs(move[2] - move[0]) == 1:
        return abs(move[3] - move[1]) == 2
    if abs(move[2] - move[0]) == 2:
        return abs(move[3] - move[1]) == 1
    return False


def is_same_side(piece1: int, piece2: int):
    if piece1 > 0:
        return piece2 > 0
    return piece2 < 0


class Board:

    def __init__(self) -> None:
        back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
        front_row = [Piece.PAWN for _ in range(8)]

        self.state = [
            [piece * -1 for piece in back_row],  # Black
            [piece * -1 for piece in front_row],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [0 for _ in range(8)],
            [piece for piece in front_row],
            [piece for piece in back_row],  # White
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

        piece_to_move = self.state[from_y][from_x]
        piece_at_target = self.state[to_y][to_x]

        if to_x == from_x and to_y == from_y:
            return False

        if is_same_side(piece_to_move, piece_at_target):
            return False

        if abs(piece_to_move) == Piece.PAWN:
            if is_diagonal_move(move):
                return abs(to_x - from_x) == 1 and is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) == 1 and piece_at_target != 0
            if is_pawns_first_move(move, piece_to_move > 0):
                return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) <= 2
            return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) == 1
        if abs(piece_to_move) == Piece.BISHOP:
            return is_diagonal_move(move)
        if abs(piece_to_move) == Piece.KNIGHT:
            return is_knight_move(move)
        if abs(piece_to_move) == Piece.ROOK:
            return is_rook_move(move)
        if abs(piece_to_move) == Piece.QUEEN:
            return is_diagonal_move(move) or self.is_knight_move(move)
        if abs(piece_to_move) == Piece.KING:
            return abs(to_x - from_x) == 1 and abs(to_y - from_y) == 1

        return False
