from game.board import Board, Piece
from server.game.move import Move, Square


def test_rook_vertical():
    board = Board()

    pawn = Square(0, 6)
    board.state[pawn.y][pawn.x] = Piece.NONE

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    expected_state = [
        [piece * -1 for piece in back_row],
        [Piece.ROOK, *[piece * -1 for piece in [Piece.PAWN] * 7]],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE, *[Piece.PAWN] * 7],
        [Piece.NONE, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    rook_vertical = Move(Square(0, 7), Square(0, 1))
    assert board.validate_move(rook_vertical)

    assert board.register_move(rook_vertical)
    assert board.state == expected_state


def test_rook_horizontal():
    board = Board()

    knight = Square(1, 7)
    board.state[knight.y][knight.x] = Piece.NONE

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN] * 8
    expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.PAWN] * 8,
        [Piece.NONE, Piece.ROOK, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    rook_horizontal = Move(Square(0, 7), Square(1, 7))
    assert board.validate_move(rook_horizontal)

    assert board.register_move(rook_horizontal)
    assert board.state == expected_state
