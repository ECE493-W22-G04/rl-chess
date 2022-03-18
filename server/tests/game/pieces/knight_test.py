from game.board import Board, Piece
from server.game.board import Move, Square


def test_knight_moves():
    board = Board()

    first_move = Move(Square(1, 7), Square(0, 5))
    second_move = Move(Square(0, 5), Square(2, 4))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN] * 8
    first_expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.KNIGHT, *[Piece.NONE] * 7],
        [Piece.PAWN] * 8,
        [Piece.ROOK, Piece.NONE, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]
    second_expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [*[Piece.NONE] * 2, Piece.KNIGHT, *[Piece.NONE] * 5],
        [Piece.NONE] * 8,
        [Piece.PAWN] * 8,
        [Piece.ROOK, Piece.NONE, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    assert board.validate_move(first_move)

    board.register_move(first_move)
    assert board.state == first_expected_state

    assert board.validate_move(second_move)

    board.register_move(second_move)
    assert board.state == second_expected_state
