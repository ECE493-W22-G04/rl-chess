from copy import deepcopy
from webbrowser import get

from server.game.board import Board
from server.game.piece import Piece
from server.game.move import Move, Square
from .pieces.helper import get_empty_board


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


def test_no_duplicate_actions():
    board = Board()
    assert len(set(board.get_actions())) == len(board.get_actions())


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


def test_check():
    board = get_empty_board()

    king = Square(3, 3)
    knight = Square(5, 4)

    board.state[king.y][king.x] = Piece.KING
    board.state[knight.y][knight.x] = -Piece.KNIGHT

    assert board.is_check()


def test_check2():
    board = get_empty_board()

    king = Square(4, 0)
    queen = Square(3, 1)

    board.state[king.y][king.x] = Piece.KING
    board.state[queen.y][queen.x] = -Piece.QUEEN

    assert board.is_check()


def test_non_check():
    board = get_empty_board()

    king = Square(4, 6)
    pawn = Square(5, 5)
    queen = Square(3, 4)

    board.state[king.y][king.x] = Piece.KING
    board.state[pawn.y][pawn.x] = Piece.PAWN
    board.state[queen.y][queen.x] = -Piece.QUEEN

    pawn_forward = Move(pawn, Square(5, 4))

    assert board.validate_move(pawn_forward)


def test_check_unblock():
    board = get_empty_board()

    king = Square(4, 0)
    pawn = Square(3, 1)
    queen = Square(2, 2)

    board.state[king.y][king.x] = Piece.KING
    board.state[pawn.y][pawn.x] = Piece.PAWN
    board.state[queen.y][queen.x] = -Piece.QUEEN

    pawn_unblock_queen = Move(pawn, Square(3, 2))

    assert not board.validate_move(pawn_unblock_queen)


def test_move_to_check():
    board = get_empty_board()

    king = Square(4, 4)
    queen = Square(3, 6)

    board.state[king.y][king.x] = -Piece.KING
    board.state[queen.y][queen.x] = Piece.QUEEN

    move = Move(queen, Square(3, 3))

    assert board.register_move(move)
    assert board.is_check()
    assert not board.is_checkmate()


def test_checkmate():
    board = get_empty_board()

    king = Square(3, 0)
    queen = Square(3, 1)
    bishop = Square(4, 2)

    board.state[king.y][king.x] = Piece.KING
    board.state[queen.y][queen.x] = -Piece.QUEEN
    board.state[bishop.y][bishop.x] = -Piece.BISHOP

    assert board.is_check()
    assert board.is_checkmate()


def test_checkmate2():
    board = Board()
    assert not board.is_checkmate()


def test_checkmate3():
    board = get_empty_board()

    king = Square(2, 0)
    queen = Square(0, 1)
    bishop = Square(4, 2)

    board.state[king.y][king.x] = Piece.KING
    board.state[queen.y][queen.x] = -Piece.QUEEN
    board.state[bishop.y][bishop.x] = -Piece.BISHOP

    move1 = Move(king, Square(3, 0))
    move2 = Move(queen, Square(3, 1))

    assert board.is_check()
    assert not board.is_checkmate()
    assert len(board.get_legal_actions()) == 1

    assert board.register_move(move1)
    assert not board.is_check()
    assert not board.is_checkmate()
    assert board.register_move(move2)

    assert board.is_check()
    assert board.is_checkmate()


def test_draw_stalemate():
    board = get_empty_board()
    king = Square(3, 7)
    queen = Square(7, 5)
    bishop = Square(3, 4)

    board.state[king.y][king.x] = Piece.KING
    board.state[queen.y][queen.x] = -Piece.QUEEN
    board.state[bishop.y][bishop.x] = -Piece.BISHOP

    move1 = Move(king, Square(4, 7))
    move2 = Move(queen, Square(3, 5))

    assert board.register_move(move1)
    assert board.register_move(move2)
    assert board.is_stalemate()
    assert board.is_draw()


def test_draw_repetition():
    board = get_empty_board()
    king1 = Square(3, 7)
    king2 = Square(4, 7)
    queen1 = Square(3, 5)
    queen2 = Square(4, 5)

    board.state[king1.y][king1.x] = Piece.KING
    board.state[queen1.y][queen1.x] = -Piece.QUEEN

    board.board_states = [deepcopy(board.state)]

    move1 = Move(king1, king2)
    move2 = Move(queen1, queen2)
    move3 = Move(king2, king1)
    move4 = Move(queen2, queen1)

    assert board.register_move(move1)
    assert not board.is_draw()

    assert board.register_move(move2)
    assert not board.is_draw()

    assert board.register_move(move3)
    assert not board.is_draw()

    assert board.register_move(move4)
    assert not board.is_draw()

    assert board.register_move(move1)
    assert not board.is_draw()

    assert board.register_move(move2)
    assert not board.is_draw()

    assert board.register_move(move3)
    assert not board.is_draw()

    assert board.register_move(move4)
    assert board.is_draw()


def test_fifty_move_rep():
    board = get_empty_board()
    king1 = Square(7, 7)
    king2 = Square(0, 0)

    board.state[king1.y][king1.x] = Piece.KING
    board.state[king2.y][king2.x] = -Piece.KING

    for _ in range(0, 7):
        prev_king1 = deepcopy(king1)
        king1 = Square(prev_king1.x - 1, prev_king1.y)
        move1 = Move(prev_king1, king1)

        prev_king2 = deepcopy(king2)
        king2 = Square(prev_king2.x + 1, prev_king2.y)
        move2 = Move(prev_king2, king2)

        assert board.register_move(move1)
        assert board.register_move(move2)
        assert not board.is_draw()

    for _ in range(0, 7):
        prev_king1 = deepcopy(king1)
        king1 = Square(prev_king1.x, prev_king1.y - 1)
        move1 = Move(prev_king1, king1)

        prev_king2 = deepcopy(king2)
        king2 = Square(prev_king2.x, prev_king2.y + 1)
        move2 = Move(prev_king2, king2)

        assert board.register_move(move1)
        assert board.register_move(move2)
        assert not board.is_draw()

    for _ in range(0, 7):
        prev_king1 = deepcopy(king1)
        king1 = Square(prev_king1.x + 1, prev_king1.y)
        move1 = Move(prev_king1, king1)

        prev_king2 = deepcopy(king2)
        king2 = Square(prev_king2.x - 1, prev_king2.y)
        move2 = Move(prev_king2, king2)

        assert board.register_move(move1)
        assert board.register_move(move2)
        assert not board.is_draw()

    for _ in range(0, 7):
        prev_king1 = deepcopy(king1)
        king1 = Square(prev_king1.x, prev_king1.y + 1)
        move1 = Move(prev_king1, king1)

        prev_king2 = deepcopy(king2)
        king2 = Square(prev_king2.x, prev_king2.y - 1)
        move2 = Move(prev_king2, king2)

        assert board.register_move(move1)
        assert board.register_move(move2)
        assert not board.is_draw()

    for _ in range(0, 7):
        prev_king1 = deepcopy(king1)
        king1 = Square(prev_king1.x - 1, prev_king1.y)
        move1 = Move(prev_king1, king1)

        prev_king2 = deepcopy(king2)
        king2 = Square(prev_king2.x + 1, prev_king2.y)
        move2 = Move(prev_king2, king2)

        assert board.register_move(move1)
        assert board.register_move(move2)
        assert not board.is_draw()

    for _ in range(0, 7):
        prev_king1 = deepcopy(king1)
        king1 = Square(prev_king1.x, prev_king1.y - 1)
        move1 = Move(prev_king1, king1)

        prev_king2 = deepcopy(king2)
        king2 = Square(prev_king2.x, prev_king2.y + 1)
        move2 = Move(prev_king2, king2)

        assert board.register_move(move1)
        assert board.register_move(move2)
        assert not board.is_draw()

    for _ in range(0, 7):
        prev_king1 = deepcopy(king1)
        king1 = Square(prev_king1.x + 1, prev_king1.y)
        move1 = Move(prev_king1, king1)

        prev_king2 = deepcopy(king2)
        king2 = Square(prev_king2.x - 1, prev_king2.y)
        move2 = Move(prev_king2, king2)

        assert board.register_move(move1)
        assert board.register_move(move2)
        assert not board.is_draw()

    prev_king1 = deepcopy(king1)
    king1 = Square(prev_king1.x, prev_king1.y + 1)
    move1 = Move(prev_king1, king1)

    prev_king2 = deepcopy(king2)
    king2 = Square(prev_king2.x, prev_king2.y - 1)
    move2 = Move(prev_king2, king2)

    assert board.register_move(move1)
    assert not board.is_draw()
    assert board.register_move(move2)
    assert board.is_draw()


def test_stores_moves():
    board = Board()

    assert len(board.moves) == 0

    first_move = Move(Square(0, 6), Square(0, 4))

    assert board.register_move(first_move)
    assert len(board.moves) == 1
    assert board.moves[0] == first_move

def test_promotion_non_pawn():
    board = get_empty_board()

    king = Square(0, 6)

    board.state[king.y][king.x] = Piece.KING

    move = Move(king, Square(0, 7), promotion=Piece.QUEEN)

    assert not board.register_move(move)
