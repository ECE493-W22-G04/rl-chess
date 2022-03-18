from game.board import Board, Piece
from server.game.board import Move, Square


def test_knight():
    board = Board()

    knight_forward = Move(Square(1, 7), Square(0, 5))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    first_expected_state = [
        [piece * -1 for piece in back_row],
        [Piece.NONE, *[piece * -1 for piece in [Piece.PAWN] * 7]],
        [-Piece.PAWN, *[Piece.NONE] * 7],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.KNIGHT, *[Piece.NONE] * 7],
        [Piece.PAWN] * 8,
        [Piece.ROOK, Piece.NONE, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    assert board.validate_move(knight_forward)
    board.register_move(knight_forward)

    black_pawn_forward = Move(Square(0, 1), Square(0, 2))
    board.register_move(black_pawn_forward)

    assert board.state == first_expected_state
