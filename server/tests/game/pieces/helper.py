from server.game.board import Board
from server.game.piece import Piece


def get_empty_board() -> Board:
    board = Board()
    board.state = [
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
        [Piece.NONE] * 8,
    ]
    board.board_states = []
    return board
