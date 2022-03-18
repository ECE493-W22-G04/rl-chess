from game.board import Board, Piece
from server.game.board import Move, Square


def test_validate_queen_diagonal():
    board = Board()

    pawn = Square(2, 6)
    board.state[pawn.y][pawn.x] = Piece.NONE

    queen_diagonal = Move(Square(3, 7), Square(0, 4))
    assert board.validate_move(queen_diagonal)


def test_move_queen_diagonal():
    board = Board()

    pawn = Square(2, 6)
    board.state[pawn.y][pawn.x] = Piece.NONE

    queen_diagonal = Move(Square(3, 7), Square(0, 4))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN for _ in range(8)]
    expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.QUEEN, *[Piece.NONE] * 7],
        [Piece.NONE] * 8,
        [Piece.PAWN, Piece.PAWN, Piece.NONE, *[Piece.PAWN] * 5],
        [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.NONE, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    board.register_move(queen_diagonal)
    assert board.state == expected_state
