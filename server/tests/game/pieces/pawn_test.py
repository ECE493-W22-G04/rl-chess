from server.game.board import Board
from server.game.piece import Piece
from server.game.move import Move, Square


def test_validate_pawn_forward():
    forward_move = Move(Square(0, 6), Square(0, 5))
    assert Board().validate_move(forward_move)


def test_validate_pawn_advance():
    advance_forward_move = Move(Square(0, 6), Square(0, 4))
    assert Board().validate_move(advance_forward_move)


def test_validate_pawn_forward_three():
    forward_three_move = Move(Square(0, 6), Square(0, 3))
    assert not Board().validate_move(forward_three_move)


def test_validate_pawn_side():
    side_move = Move(Square(0, 6), Square(1, 6))
    assert not Board().validate_move(side_move)


def test_validate_diagonal_no_capture():
    diagonal_no_capture_move = Move(Square(0, 6), Square(1, 5))
    assert not Board().validate_move(diagonal_no_capture_move)


def test_pawn_forward():
    board = Board()

    forward_move = Move(Square(0, 6), Square(0, 5))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN for _ in range(8)]
    expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.PAWN, *[Piece.NONE] * 7],
        [Piece.NONE, *[Piece.PAWN] * 7],
        [piece for piece in back_row],
    ]

    board.register_move(forward_move)
    assert board.state == expected_state


def test_pawn_advance():
    board = Board()

    forward_move = Move(Square(0, 6), Square(0, 4))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN for _ in range(8)]
    expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.PAWN, *[Piece.NONE] * 7],
        [Piece.NONE] * 8,
        [Piece.NONE, *[Piece.PAWN] * 7],
        [piece for piece in back_row],
    ]

    board.register_move(forward_move)
    assert board.state == expected_state
