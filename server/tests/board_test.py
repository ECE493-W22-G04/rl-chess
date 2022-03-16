from game.board import Board, Piece

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
    assert len(board.get_actions()) == 64 * 64
