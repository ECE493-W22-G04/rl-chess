from typing import NamedTuple, Optional
from enum import IntEnum
import itertools


class Piece(IntEnum):
    NONE = 0
    PAWN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Square(NamedTuple):
    x: int
    y: int


class Move(NamedTuple):
    from_square: Square
    to_square: Square
    promotion: Optional[Piece] = None


def is_pawns_first_move(move: Move, is_white: bool):
    if is_white:
        return move.from_square.y == 6
    return move.from_square.y == 1


def is_forward_move(move: Move, is_white: bool):
    if move.from_square.x != move.to_square.x:
        return False
    if is_white:
        return move.to_square.y < move.from_square.y
    return move.to_square.y > move.from_square.y


def is_diagonal_move(move: Move):
    return abs(move.to_square.x - move.from_square.x) == abs(move.to_square.y - move.from_square.y)


def is_diagonal_path_clear(board: list[list[Piece]], move: Move):
    for i in range(move.from_square.x, move.to_square.x, 1 if move.from_square.x < move.to_square.x else -1):
        if board[i][i] != 0:
            return False
    return True


def is_rook_move(move: Move):
    if abs(move.to_square.x - move.from_square.x) > 0:
        return abs(move.to_square.y - move.from_square.y) == 0
    return abs(move.to_square.y - move.from_square.y) > 0


def is_rook_path_clear(board: list[list[Piece]], move: Move):
    if abs(move.to_square.x - move.from_square.x) > 0:
        for i in range(move.from_square.x, move.to_square.x, 1 if move.from_square.x < move.to_square.x else -1):
            if board[move.from_square.y][i] != 0:
                return False

    for i in range(move.from_square.y, move.to_square.y, 1 if move.from_square.y < move.to_square.y else -1):
        if board[i][move.from_square.x] != 0:
            return False

    return True


def is_knight_move(move: Move):
    if abs(move.to_square.x - move.from_square.x) == 1:
        return abs(move.to_square.y - move.from_square.y) == 2
    if abs(move.to_square.x - move.from_square.x) == 2:
        return abs(move.to_square.y - move.from_square.y) == 1
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
            [Piece.NONE for _ in range(8)],
            [Piece.NONE for _ in range(8)],
            [Piece.NONE for _ in range(8)],
            [Piece.NONE for _ in range(8)],
            [piece for piece in front_row],
            [piece for piece in back_row],  # White
        ]

        self.actions: list[Move] = []
        for from_coordinate in itertools.product(range(8), repeat=2):
            for to_coordinate in itertools.product(range(8), repeat=2):
                self.actions.append(Move(Square(from_coordinate[1], to_coordinate[0]), Square(to_coordinate[1], to_coordinate[1])))

        for promoted_to in [Piece.QUEEN, Piece.BISHOP, Piece.ROOK, Piece.KNIGHT]:
            for column in range(8):
                for row in [1, 6]:
                    self.actions.append(Move(Square(column, row), Square(column, row - 1 if row == 1 else row + 1), promotion=promoted_to))

    def get_actions(self):
        return self.actions

    def get_legal_actions(self):
        pass

    def register(self, from_to: Move):
        pass

    def validate_move(self, move: Move):
        from_x = move.from_square.x
        from_y = move.from_square.y
        to_x = move.to_square.x
        to_y = move.to_square.y

        piece_to_move = self.state[from_y][from_x]
        piece_at_target = self.state[to_y][to_x]

        if to_x == from_x and to_y == from_y:
            return False

        if is_same_side(piece_to_move, piece_at_target):
            return False

        if abs(piece_to_move) == Piece.PAWN:
            if is_diagonal_move(move):
                return abs(to_x - from_x) == 1 and is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) == 1 and piece_at_target != Piece.NONE
            if is_pawns_first_move(move, piece_to_move > 0):
                return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) <= 2
            return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) == 1
        if abs(piece_to_move) == Piece.BISHOP:
            return is_diagonal_move(move) and is_diagonal_path_clear(self.state, move)
        if abs(piece_to_move) == Piece.KNIGHT:
            return is_knight_move(move)
        if abs(piece_to_move) == Piece.ROOK:
            return is_rook_move(move) and is_rook_path_clear(self.state, move)
        if abs(piece_to_move) == Piece.QUEEN:
            return is_diagonal_move(move) and is_diagonal_path_clear(self.state, move) or is_rook_move(move) and is_rook_path_clear(self.state, move)
        if abs(piece_to_move) == Piece.KING:
            return abs(to_x - from_x) == 1 and abs(to_y - from_y) == 1

        return False
