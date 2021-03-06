from server.game.piece import Piece
from server.game.board import Board
from server.game.move import Move, Square
from .helper import get_empty_board


def test_validate_pawn_forward_three():
    forward_three_move = Move(Square(0, 6), Square(0, 3))
    assert not Board().validate_move(forward_three_move)


def test_validate_pawn_side():
    board = get_empty_board()
    pawn = Square(3, 3)
    board.state[pawn.y][pawn.x] = Piece.PAWN

    side_move = Move(pawn, Square(2, 3))
    assert not board.validate_move(side_move)


def test_validate_diagonal_no_capture():
    diagonal_no_capture_move = Move(Square(0, 6), Square(1, 5))
    assert not Board().validate_move(diagonal_no_capture_move)


def test_pawn_forward():
    board = Board()

    forward_move = Move(Square(0, 6), Square(0, 5))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN] * 8
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

    assert Board().validate_move(forward_move)

    assert board.register_move(forward_move)
    assert board.state == expected_state


def test_pawn_advance():
    board = Board()

    advance_move = Move(Square(0, 6), Square(0, 4))

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

    assert Board().validate_move(advance_move)

    assert board.register_move(advance_move)
    assert board.state == expected_state


def test_pawn_capture():
    board = Board()
    move_white_left_1 = Move(Square(0, 6), Square(0, 4))
    move_black_left_1 = Move(Square(1, 1), Square(1, 3))
    move_white_left_2 = Move(Square(0, 4), Square(1, 3))

    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    expected_state = [
        [piece * -1 for piece in back_row],
        [Piece.PAWN * -1, Piece.NONE, *[Piece.PAWN * -1] * 6],
        [Piece.NONE] * 8,
        [Piece.NONE, Piece.PAWN, *[Piece.NONE] * 6],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE, *[Piece.PAWN] * 7],
        [piece for piece in back_row],
    ]

    assert board.register_move(move_white_left_1)
    assert board.register_move(move_black_left_1)
    assert board.validate_move(move_white_left_2)
    assert board.register_move(move_white_left_2)
    assert board.state == expected_state


def test_pawn_capture_backwards():
    board = Board()
    board.state = [
        [*[piece * -1 for piece in [Piece.NONE] * 7], Piece.KING * -1],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.PAWN, *[Piece.NONE] * 7],
        [Piece.NONE, -Piece.PAWN, *[Piece.NONE] * 6],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [*[[Piece.NONE] * 7], Piece.KING],
    ]

    pawn_capture_backwards = Move(Square(0, 3), Square(1, 4))

    assert not board.validate_move(pawn_capture_backwards)


def test_pawn_capture_forward():
    board = Board()

    move1 = Move(Square(4, 6), Square(4, 4))
    move2 = Move(Square(4, 1), Square(4, 3))
    move3 = Move(Square(4, 4), Square(4, 3))

    assert board.register_move(move1)
    assert board.register_move(move2)
    assert not board.register_move(move3)


def test_pawn_en_passant():
    board = Board()

    move1 = Move(Square(5, 6), Square(5, 4))
    move2 = Move(Square(4, 1), Square(4, 3))
    move3 = Move(Square(5, 4), Square(5, 3))
    move4 = Move(Square(6, 1), Square(6, 3))
    move5 = Move(Square(5, 3), Square(6, 2))

    assert board.register_move(move1)
    assert board.register_move(move2)
    assert board.register_move(move3)
    assert board.register_move(move4)
    assert board.register_move(move5)
    assert board.state[3][6] == Piece.NONE


def test_pawn_not_en_passant():
    board = Board()

    move1 = Move(Square(5, 6), Square(5, 4))
    move2 = Move(Square(4, 1), Square(4, 3))
    move3 = Move(Square(5, 4), Square(5, 3))
    move4 = Move(Square(6, 1), Square(6, 3))
    move5 = Move(Square(5, 3), Square(4, 2))

    assert board.register_move(move1)
    assert board.register_move(move2)
    assert board.register_move(move3)
    assert board.register_move(move4)
    assert not board.register_move(move5)


def test_pawn_invalid_en_passant():
    board = Board()

    move1 = Move(Square(4, 6), Square(4, 4))
    move2 = Move(Square(5, 1), Square(4, 2))

    assert board.register_move(move1)
    assert not board.register_move(move2)


def test_pawn_invalid_capture():
    board = Board()

    move1 = Move(Square(3, 6), Square(3, 4))
    move2 = Move(Square(7, 1), Square(3, 5))

    assert board.register_move(move1)
    assert not board.register_move(move2)


def test_pawn_promotion1():
    board = get_empty_board()

    pawn = Square(4, 1)
    board.state[pawn.y][pawn.x] = Piece.PAWN

    move = Move(pawn, Square(4, 0), Piece.QUEEN)

    assert board.register_move(move)
    assert board.state[0][4] == Piece.QUEEN


def test_pawn_promotion2():
    board = get_empty_board()

    pawn = Square(4, 6)
    board.state[pawn.y][pawn.x] = -Piece.PAWN
    board.is_white_turn = False

    move = Move(pawn, Square(4, 7), Piece.QUEEN)

    assert board.register_move(move)
    assert board.state[7][4] == -Piece.QUEEN


def test_pawn_promotion_diag():
    board = get_empty_board()

    pawn = Square(4, 6)
    queen = Square(5, 7)
    board.state[pawn.y][pawn.x] = -Piece.PAWN
    board.state[queen.y][queen.x] = Piece.QUEEN
    board.is_white_turn = False

    move = Move(pawn, Square(5, 7), Piece.QUEEN)

    assert board.register_move(move)
    assert board.state[7][5] == -Piece.QUEEN


def test_illegal_pawn_move():
    board = get_empty_board()

    pawn = Square(4, 1)
    board.state[pawn.y][pawn.x] = Piece.PAWN

    move = Move(pawn, Square(4, 0))

    assert not board.register_move(move)
