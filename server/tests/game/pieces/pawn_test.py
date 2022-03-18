from game.board import Board, Piece
from server.game.board import Move, Square


def test_validate_pawn():
    board = Board()

    forward_move = Move(Square(0, 6), Square(0, 5))
    advance_forward_move = Move(Square(0, 6), Square(0, 4))
    assert board.validate_move(forward_move)
    assert board.validate_move(advance_forward_move)

    forward_three_move = Move(Square(0, 6), Square(0, 3))
    side_move = Move(Square(0, 6), Square(1, 6))
    diagonal_no_capture_move = Move(Square(0, 6), Square(1, 5))
    assert not board.validate_move(forward_three_move)
    assert not board.validate_move(side_move)
    assert not board.validate_move(diagonal_no_capture_move)


def test_pawn_forward():
    board = Board()

    forward_move = Move(Square(0, 6), Square(0, 5))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN for _ in range(8)]
    expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        *([[Piece.NONE] * 8] * 3),
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
