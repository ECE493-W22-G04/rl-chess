from game.board import Board, Piece
from server.game.board import Move, Square


def test_validate_queen_diagonal():
    board = Board()

    pawn = Square(2, 6)
    board.state[pawn.y][pawn.x] = Piece.NONE

    print(board)

    queen_diagonal = Move(Square(3, 7), Square(0, 4))
    print(board.state[7][3])
    assert board.validate_move(queen_diagonal)
