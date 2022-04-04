from .piece import Piece
from .move import Move


def exclusive_range(i: int, j: int):
    """Helper function to return the range exclusive of the ends and determines the step size automatically"""
    if j > i:
        return range(i + 1, j, 1)
    return range(i - 1, j, -1)


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


def is_diagonal_forward(move: Move, is_white: bool):
    if is_white:
        return is_diagonal_move(move) and move.to_square.y < move.from_square.y
    return is_diagonal_move(move) and move.to_square.y > move.from_square.y


def is_diagonal_move(move: Move):
    return abs(move.to_square.x - move.from_square.x) == abs(move.to_square.y - move.from_square.y)


def is_diagonal_path_clear(board: list[list[Piece]], move: Move):
    xs = exclusive_range(move.from_square.x, move.to_square.x)
    ys = exclusive_range(move.from_square.y, move.to_square.y)
    coordinates = zip(xs, ys)
    for coordinate in coordinates:
        if board[coordinate[1]][coordinate[0]] != Piece.NONE:
            return False
    return True


def is_rook_move(move: Move):
    if abs(move.to_square.x - move.from_square.x) > 0:
        return abs(move.to_square.y - move.from_square.y) == 0
    return abs(move.to_square.y - move.from_square.y) > 0


def is_rook_path_clear(board: list[list[Piece]], move: Move):
    if abs(move.to_square.x - move.from_square.x) > 0:
        for i in exclusive_range(move.from_square.x, move.to_square.x):
            if board[move.from_square.y][i] != Piece.NONE:
                return False

    for i in exclusive_range(move.from_square.y, move.to_square.y):
        if board[i][move.from_square.x] != Piece.NONE:
            return False

    return True


def is_pawn_path_clear(board: list[list[Piece]], move: Move, is_white: bool):
    offset = -1 if is_white else 1

    for i in exclusive_range(move.from_square.y, move.to_square.y + offset):
        if board[i][move.from_square.x] != Piece.NONE:
            return False

    return True


# check that end row forces a promotion
def is_pawn_end_row_valid(move: Move, is_white):
    test_y = 0 if is_white else 7
    if move.to_square.y == test_y:
        return move.promotion != None
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
