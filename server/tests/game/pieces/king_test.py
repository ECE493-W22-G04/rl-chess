from game.board import Board, Piece
from server.game.board import Move, Square


def test_king_forward():
    board = Board()

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN] * 8
    expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [*[Piece.NONE] * 4, Piece.PAWN, *[Piece.NONE] * 3],
        [Piece.NONE] * 8,
        [*[Piece.PAWN] * 4, Piece.KING, *[Piece.PAWN] * 3],
        [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.NONE, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    pawn_forward = Move(Square(4, 6), Square(4, 4))
    board.register_move(pawn_forward)

    king_forward = Move(Square(4, 7), Square(4, 6))
    assert board.validate_move(king_forward)

    board.register_move(king_forward)
    assert board.state == expected_state
