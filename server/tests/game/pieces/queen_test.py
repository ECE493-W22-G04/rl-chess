from game.board import Board, Piece
from server.game.board import Move, Square


def test_queen_diagonal():
    board = Board()

    pawn = Square(2, 6)
    board.state[pawn.y][pawn.x] = Piece.NONE

    queen_diagonal = Move(Square(3, 7), Square(0, 4))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN] * 8
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

    assert board.validate_move(queen_diagonal)

    assert board.register_move(queen_diagonal)
    assert board.state == expected_state


def test_queen_vertical():
    board = Board()

    pawn = Square(3, 6)
    board.state[pawn.y][pawn.x] = Piece.NONE

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    expected_state = [
        [piece * -1 for piece in back_row],
        [*[piece * -1 for piece in [Piece.PAWN] * 3], Piece.QUEEN, *[piece * -1 for piece in [Piece.PAWN] * 4]],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [*[Piece.PAWN] * 3, Piece.NONE, *[Piece.PAWN] * 4],
        [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.NONE, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    queen_vertical = Move(Square(3, 7), Square(3, 1))
    assert board.validate_move(queen_vertical)

    assert board.register_move(queen_vertical)
    assert board.state == expected_state


def test_queen_horizontal():
    board = Board()

    bishop = Square(2, 7)
    board.state[bishop.y][bishop.x] = Piece.NONE

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN for _ in range(8)]
    expected_state = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.PAWN] * 8,
        [Piece.ROOK, Piece.KNIGHT, Piece.QUEEN, Piece.NONE, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK],
    ]

    queen_horizontal = Move(Square(3, 7), Square(2, 7))
    assert board.validate_move(queen_horizontal)

    assert board.register_move(queen_horizontal)
    assert board.state == expected_state
