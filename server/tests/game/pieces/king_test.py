from game.board import Board, Piece
from server.game.move import Move, Square
from server.tests.game.pieces.helper import get_empty_board
from copy import deepcopy


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


def test_forbid_king_move_to_check():
    board = get_empty_board()

    king = Square(2, 3)
    queen = Square(4, 4)

    board.state[king.y][king.x] = Piece.KING
    board.state[queen.y][queen.x] = -Piece.QUEEN

    king_to_check = Move(king, Square(3, 3))

    old_board_state = deepcopy(board.state)
    assert not board.validate_move(king_to_check)
    assert not board.register_move(king_to_check)
    assert old_board_state == board.state


def test_forbid_king_move_to_check2():
    board = get_empty_board()

    king = Square(3, 0)
    queen = Square(3, 1)

    board.state[king.y][king.x] = Piece.KING
    board.state[queen.y][queen.x] = -Piece.QUEEN

    king_escape_attempt = Move(king, Square(4, 0))

    assert not board.validate_move(king_escape_attempt)
    assert len(board.get_legal_actions()) == 1

    capture_queen_move = board.get_legal_actions()[0]
    assert board.state[capture_queen_move.to_square.y][capture_queen_move.to_square.x] == -Piece.QUEEN
