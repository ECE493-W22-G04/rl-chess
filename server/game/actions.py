import itertools

from server.game.piece import Piece
from server.game.move import Move, Square

ACTIONS = []
for (from_x, from_y) in itertools.product(range(8), repeat=2):
    # Horizontal moves
    for x in range(8):
        if x == from_x:
            continue
        ACTIONS.append(Move(Square(from_x, from_y), Square(x, from_y)))
    # Vertical moves
    for y in range(8):
        if y == from_y:
            continue
        ACTIONS.append(Move(Square(from_x, from_y), Square(from_x, y)))
    # Diagonal moves
    for increment in range(1, 8):
        for (x_increment, y_increment) in itertools.product([increment, -increment], repeat=2):
            to_x = from_x + x_increment
            to_y = from_y + y_increment
            if to_x < 0 or to_x > 7 or to_y < 0 or to_y > 7:
                continue
            ACTIONS.append(Move(Square(from_x, from_y), Square(to_x, to_y)))
    # Knight moves
    for x_incr in range(-2, 3):
        for y_incr in range(-2, 3):
            if abs(x_incr) == abs(y_incr):
                continue
            to_x = from_x + x_incr
            to_y = from_y + y_incr
            if to_x < 0 or to_x > 7 or to_y < 0 or to_y > 7:
                continue
            ACTIONS.append(Move(Square(from_x, from_y), Square(to_x, to_y)))

# Promotions
for promoted_to in [Piece.QUEEN, Piece.BISHOP, Piece.ROOK, Piece.KNIGHT]:
    for column in range(8):
        for row in [1, 6]:
            ACTIONS.append(Move(Square(column, row), Square(column, row - 1 if row == 1 else row + 1), promotion=promoted_to))

ACTIONS = list(set(ACTIONS))
