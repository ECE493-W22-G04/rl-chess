from game.board import Board, Piece
from server.game.board import Move, Square


def test_bishop_diagonal():
    board = Board()

    pawn = Square(1, 6)
    board.state[pawn.y][pawn.x] = Piece.NONE

    bishop_diagonal = Move(Square(2, 7), Square(0, 5))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN for _ in range(8)]
    expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.BISHOP, *[Piece.NONE] * 7],
        [Piece.PAWN, Piece.NONE, Piece.PAWN, *[Piece.PAWN] * 5],
        [Piece.ROOK, Piece.KNIGHT, Piece.NONE, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    assert board.validate_move(bishop_diagonal)

    board.register_move(bishop_diagonal)
    assert board.state == expected_state
