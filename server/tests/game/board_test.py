from game.board import Board
from game.piece import Piece
from game.move import Move, Square


def test_board_init():
    board = Board()
    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN] * 8

    expected = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [piece for piece in front_row],
        [piece for piece in back_row],
    ]
    assert board.state == expected


def test_actions():
    board = Board()
    pieces_to_choose_from = 8 * 8
    pieces_to_target_to = 8 * 8
    pieces_to_promote = 8 * 2
    pieces_to_promote_to = 4
    assert len(board.get_actions()) < pieces_to_choose_from * pieces_to_target_to + pieces_to_promote * pieces_to_promote_to


def test_turn():
    board = Board()
    assert board.is_white_turn
    assert board.register_move(Move(Square(0, 6), Square(0, 5)))
    assert not board.is_white_turn
    assert board.register_move(Move(Square(0, 1), Square(0, 2)))
    assert board.is_white_turn


def test_bounds():
    board = Board()
    move = Move(Square(-1, 0), Square(0, 0))
    assert not board.validate_move(move)

def test_checkmate():
    board = get_empty_board()

    king = Square(3, 0)
    queen = Square(3, 1)
    bishop = Square(4, 2)

    board.state[king.y][king.x] = -Piece.KING
    board.state[queen.y][queen.x] = Piece.QUEEN
    board.state[bishop.y][bishop.x] = Piece.BISHOP

    assert board.is_checkmate()
