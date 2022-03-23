from game.board import Board, Piece
from server.game.move import Move, Square


def test_king_forward():
    board = Board()

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    expected_state = [
        [piece * -1 for piece in back_row],
        [Piece.NONE, *[piece * -1 for piece in [Piece.PAWN] * 7]],
        [-Piece.PAWN, *[Piece.NONE] * 7],
        [Piece.NONE] * 8,
        [*[Piece.NONE] * 4, Piece.PAWN, *[Piece.NONE] * 3],
        [Piece.NONE] * 8,
        [*[Piece.PAWN] * 4, Piece.KING, *[Piece.PAWN] * 3],
        [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.NONE, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    pawn_forward = Move(Square(4, 6), Square(4, 4))
    assert board.register_move(pawn_forward)

    black_pawn_forward = Move(Square(0, 1), Square(0, 2))
    assert board.register_move(black_pawn_forward)

    king_forward = Move(Square(4, 7), Square(4, 6))
    assert board.validate_move(king_forward)

    assert board.register_move(king_forward)
    assert board.state == expected_state
