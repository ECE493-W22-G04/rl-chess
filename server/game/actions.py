import itertools

from .piece import Piece
from .move import Move, Square

ACTIONS = []
for from_coordinate in itertools.product(range(8), repeat=2):
    # Horizontal moves
    for x in range(8):
        if x == from_coordinate[0]:
            continue
        ACTIONS.append(Move(Square(from_coordinate[0], from_coordinate[1]), Square(x, from_coordinate[1])))
    # Vertical moves
    for y in range(8):
        if y == from_coordinate[1]:
            continue
        ACTIONS.append(Move(Square(from_coordinate[0], from_coordinate[1]), Square(from_coordinate[0], y)))
    # Diagonal moves
    for increment in range(-7, 8):
        to_x = from_coordinate[0] + increment
        to_y = from_coordinate[1] + increment
        if to_x < 0 or to_x > 7 or to_y < 0 or to_y > 7:
            continue
        ACTIONS.append(Move(Square(from_coordinate[0], from_coordinate[1]), Square(to_x, to_y)))
    for increment in range(-7, 8):
        to_x = from_coordinate[0] - increment
        to_y = from_coordinate[1] + increment
        if to_x < 0 or to_x > 7 or to_y < 0 or to_y > 7:
            continue
        ACTIONS.append(Move(Square(from_coordinate[0], from_coordinate[1]), Square(to_x, to_y)))
    # Knight moves
    for x_incr in range(-2, 3):
        for y_incr in range(-2, 3):
            if abs(x_incr) == abs(y_incr):
                continue
            to_x = from_coordinate[0] + x_incr
            to_y = from_coordinate[1] + y_incr
            if to_x < 0 or to_x > 7 or to_y < 0 or to_y > 7:
                continue
            ACTIONS.append(Move(Square(from_coordinate[0], from_coordinate[1]), Square(to_x, to_y)))

# Promotions
for promoted_to in [Piece.QUEEN, Piece.BISHOP, Piece.ROOK, Piece.KNIGHT]:
    for column in range(8):
        for row in [1, 6]:
            ACTIONS.append(Move(Square(column, row), Square(column, row - 1 if row == 1 else row + 1), promotion=promoted_to))
