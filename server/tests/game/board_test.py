from server.game.board import Board
from server.game.piece import Piece


def test_board_init():
    board = Board()
    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN for _ in range(8)]

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
    assert len(board.get_actions()) == pieces_to_choose_from * pieces_to_target_to + pieces_to_promote * pieces_to_promote_to
