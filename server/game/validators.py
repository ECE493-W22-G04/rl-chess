from .piece import Piece
from .move import Move


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
