import itertools

from .piece import Piece
from .move import Move, Square
from .validators import is_diagonal_forward, is_same_side, is_diagonal_move, is_forward_move, is_pawns_first_move, is_diagonal_path_clear, is_knight_move, is_rook_move, is_rook_path_clear


class Board:

    def __init__(self) -> None:
        back_row = [Piece.ROOK, Piece.KNIGHT, Piece.BISHOP, Piece.QUEEN, Piece.KING, Piece.BISHOP, Piece.KNIGHT, Piece.ROOK]
        front_row = [Piece.PAWN] * 8

        self.state = [
            [piece * -1 for piece in back_row],  # Black
            [piece * -1 for piece in front_row],
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [piece for piece in front_row],
            [piece for piece in back_row],  # White
        ]

        self.is_white_turn = True

        self.actions: list[Move] = []
        for from_coordinate in itertools.product(range(8), repeat=2):
            for to_coordinate in itertools.product(range(8), repeat=2):
                self.actions.append(Move(Square(from_coordinate[1], from_coordinate[0]), Square(to_coordinate[1], to_coordinate[0])))

        for promoted_to in [Piece.QUEEN, Piece.BISHOP, Piece.ROOK, Piece.KNIGHT]:
            for column in range(8):
                for row in [1, 6]:
                    self.actions.append(Move(Square(column, row), Square(column, row - 1 if row == 1 else row + 1), promotion=promoted_to))

    def __str__(self) -> str:

        def piece_to_str(piece: int):
            pieces = {
                Piece.NONE: ' ',
                Piece.ROOK: '♜',
                Piece.KNIGHT: '♞',
                Piece.BISHOP: '♝',
                Piece.QUEEN: '♛',
                Piece.KING: '♚',
                Piece.PAWN: '♟',
            }
            black_to_white_offset = ord('♖') - ord('♜')
            offset = 0 if piece < 0 else black_to_white_offset
            return chr(ord(pieces[abs(piece)]) + offset)

        return '\n\n'.join(['\t'.join([piece_to_str(piece) for piece in row]) for row in self.state])

    def get_actions(self):
        return self.actions

    def get_legal_actions(self):
        legal_actions: list[Move] = []
        for move in self.actions:
            if not self.validate_move(move):
                continue
            legal_actions.append(move)
        return legal_actions

    def register_move(self, move: Move) -> bool:
        if not self.validate_move(move):
            return False

        piece_to_move = self.state[move.from_square.y][move.from_square.x]
        self.state[move.to_square.y][move.to_square.x] = piece_to_move
        self.state[move.from_square.y][move.from_square.x] = Piece.NONE

        self.is_white_turn = not self.is_white_turn
        return True

    def validate_move(self, move: Move):
        from_x = move.from_square.x
        from_y = move.from_square.y
        to_x = move.to_square.x
        to_y = move.to_square.y

        for coordinate in [from_x, from_y, to_x, to_y]:
            if coordinate < 0 or coordinate > 7:
                return False

        piece_to_move = self.state[from_y][from_x]
        piece_at_target = self.state[to_y][to_x]

        if self.is_white_turn and piece_to_move < 0:
            return False

        if not self.is_white_turn and piece_to_move > 0:
            return False

        if to_x == from_x and to_y == from_y:
            return False

        if is_same_side(piece_to_move, piece_at_target):
            return False

        if abs(piece_to_move) == Piece.PAWN:
            if is_diagonal_forward(move, piece_to_move > 0):
                return abs(to_x - from_x) == 1 and abs(to_y - from_y) == 1 and piece_at_target != Piece.NONE
            if is_pawns_first_move(move, piece_to_move > 0):
                return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) <= 2
            return is_forward_move(move, piece_to_move > 0) and abs(to_y - from_y) == 1
        if abs(piece_to_move) == Piece.BISHOP:
            return is_diagonal_move(move) and is_diagonal_path_clear(self.state, move)
        if abs(piece_to_move) == Piece.KNIGHT:
            return is_knight_move(move)
        if abs(piece_to_move) == Piece.ROOK:
            return is_rook_move(move) and is_rook_path_clear(self.state, move)
        if abs(piece_to_move) == Piece.QUEEN:
            return (is_diagonal_move(move) and is_diagonal_path_clear(self.state, move)) or (is_rook_move(move) and is_rook_path_clear(self.state, move))
        if abs(piece_to_move) == Piece.KING:
            # TODO: Check if move results in a 'check' -> invalid
            return abs(to_x - from_x) <= 1 and abs(to_y - from_y) <= 1

        return False
