from game.board import Board, Piece
from server.game.board import Move, Square


def test_board_init():
    board = Board()
    back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
    front_row = [Piece.PAWN for _ in range(8)]

    expected = [
        [piece * -1 for piece in back_row],
        [piece * -1 for piece in front_row],
        [0 for _ in range(8)],
        [0 for _ in range(8)],
        [0 for _ in range(8)],
        [0 for _ in range(8)],
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


def test_pawn():
    board = Board()

    forward_move = Move(Square(0, 6), Square(0, 5))
    advance_forward_move = Move(Square(0, 6), Square(0, 4))
    assert board.validate_move(forward_move)
    assert board.validate_move(advance_forward_move)

    forward_three_move = Move(Square(0, 6), Square(0, 3))
    side_move = Move(Square(0, 6), Square(1, 6))
    diagonal_no_capture_move = Move(Square(0, 6), Square(1, 5))
    assert not board.validate_move(forward_three_move)
    assert not board.validate_move(side_move)
    assert not board.validate_move(diagonal_no_capture_move)
